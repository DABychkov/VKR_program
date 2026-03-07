"""Парсер DOCX: извлекает титульник и находит секции документа."""

import os
import re
from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

from ..models.document_structure import DocumentStructure


class DocumentParser:
    # Ключевые секции по ГОСТ 7.32
    SECTION_KEYWORDS = [
        "СПИСОК ИСПОЛНИТЕЛЕЙ",
        "РЕФЕРАТ",
        "СОДЕРЖАНИЕ",
        "ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ",
        "ПЕРЕЧЕНЬ СОКРАЩЕНИЙ И ОБОЗНАЧЕНИЙ",
        "ВВЕДЕНИЕ",
        "ЗАКЛЮЧЕНИЕ",
        "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ",
        "ПРИЛОЖЕНИЕ",
        "ОПРЕДЕЛЕНИЯ, ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ"  # Альтернативный вариант
    ]
    
    def parse(self, file_path: str) -> DocumentStructure:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        if not file_path.lower().endswith(".docx"):
            raise ValueError("Ожидается файл .docx")

        doc = Document(file_path)

        # Собираем весь текст документа в порядке следования блоков (абзацы + строки таблиц).
        all_paragraphs = self._extract_text_blocks(doc)
        
        # Титульник = первые ~30 абзацев
        title_page_text = "\n".join(all_paragraphs[:30])
        
        # Ищем секции документа
        sections = self._find_sections(all_paragraphs)
        
        return DocumentStructure(
            filename=os.path.basename(file_path),
            title_page_text=title_page_text,
            sections=sections,
            all_paragraphs=all_paragraphs
        )

    def _extract_text_blocks(self, doc: Document) -> list[str]:
        """Извлекает текстовые блоки документа (абзацы и таблицы) в исходном порядке."""
        blocks: list[str] = []

        for child in doc.element.body.iterchildren():
            if isinstance(child, CT_P):
                paragraph = Paragraph(child, doc)
                text = paragraph.text.strip()
                if text:
                    blocks.append(text)
                continue

            if isinstance(child, CT_Tbl):
                table = Table(child, doc)
                for row in table.rows:
                    cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if not cells:
                        continue
                    # Храним строку таблицы как TSV-подобную запись для последующего парсинга.
                    blocks.append("\t".join(cells))

        return blocks
    
    def _find_sections(self, paragraphs: list[str]) -> dict[str, str]:
        """Находит секции документа (РЕФЕРАТ, ВВЕДЕНИЕ и т.д.)"""
        sections = {}
        current_section = None
        current_text = []

        def _is_contents_section(section_name: str | None) -> bool:
            if not section_name:
                return False
            return "СОДЕРЖАНИЕ" in section_name.upper()
        
        for para in paragraphs:
            # Внутри "СОДЕРЖАНИЕ" строки вида "ВВЕДЕНИЕ ... 9" или
            # "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ 67" являются элементами оглавления,
            # а не началом новой секции.
            if _is_contents_section(current_section) and self._is_contents_item_line(para):
                current_text.append(para)
                continue

            # Проверяем, это заголовок секции?
            if self._is_section_header(para):
                # Сохраняем предыдущую секцию
                if current_section:
                    sections[current_section] = "\n".join(current_text)
                # Начинаем новую секцию
                current_section = para.strip()
                current_text = []
            elif current_section:
                # Проверяем, не началась ли основная часть (номер раздела)
                # Паттерны: "1 НАЗВАНИЕ", "1. НАЗВАНИЕ", "Глава 1"
                # ВАЖНО: внутри секции "СОДЕРЖАНИЕ" такие строки нормальны,
                # поэтому преждевременно секцию не обрываем.
                if self._is_main_section_start(para) and not _is_contents_section(current_section):
                    # Основная часть началась - сохраняем текущую секцию и прекращаем
                    sections[current_section] = "\n".join(current_text)
                    current_section = None
                    current_text = []
                    continue
                # Добавляем текст к текущей секции
                current_text.append(para)
        
        # Сохраняем последнюю секцию
        if current_section:
            sections[current_section] = "\n".join(current_text)
        
        return sections

    def _is_contents_item_line(self, text: str) -> bool:
        """Проверяет, является ли строка элементом оглавления с номером страницы."""
        text_strip = text.strip()
        if not text_strip:
            return False

        # Примеры:
        # "ВВЕДЕНИЕ 9"
        # "Глава 1. Теория........5"
        # "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ\t38"
        if not re.search(r"\d+\s*$", text_strip):
            return False

        # Должен быть некоторый текст до номера страницы.
        return bool(re.search(r"\D\s*\d+\s*$", text_strip))
    
    def _is_section_header(self, text: str) -> bool:
        """Проверяет, является ли текст заголовком секции."""
        text_strip = text.strip()
        text_upper = text_strip.upper()
        
        # Заголовок должен:
        # 1. Содержать ключевое слово
        # 2. Быть капсом
        # 3. Быть коротким (не более 60 символов - чтобы отсечь длинные строки)
        # 4. Не содержать точек/отточий (чтобы отличить от содержания)
        
        if len(text_strip) > 60:
            return False

        if not text_strip.isupper():
            return False
        
        # Проверяем что это чистое ключевое слово (или почти)
        for keyword in self.SECTION_KEYWORDS:
            if keyword in text_upper:
                # Убираем пробелы и сравниваем длину - должно быть близко к ключевому слову
                clean_text = text_upper.replace(' ', '').replace('\t', '')
                clean_keyword = keyword.replace(' ', '')
                # Допускаем небольшое отличие (например, добавочные пробелы)
                if abs(len(clean_text) - len(clean_keyword)) <= 5:
                    return True

        return False
        
        return False
    
    def _is_main_section_start(self, text: str) -> bool:
        """Проверяет, началась ли основная часть (номер раздела)."""
        text = text.strip()
        # Паттерны: "1 НАЗВАНИЕ", "1. НАЗВАНИЕ", "Глава 1", "ГЛАВА 1"
        import re
        patterns = [
            r'^\d+\s+[А-ЯA-Z]',  # "1 ТЕОРЕТИЧЕСКАЯ"
            r'^\d+\.\s+[А-ЯA-Z]',  # "1. Теория"
            r'^Глава\s+\d+',  # "Глава 1"
            r'^ГЛАВА\s+\d+',  # "ГЛАВА 1"
        ]
        return any(re.match(pattern, text, re.IGNORECASE) for pattern in patterns)

