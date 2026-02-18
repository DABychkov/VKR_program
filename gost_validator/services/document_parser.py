"""Парсер DOCX: извлекает титульник и находит секции документа."""

import os
import re
from docx import Document

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
        
        # Собираем все абзацы
        all_paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        
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
    
    def _find_sections(self, paragraphs: list[str]) -> dict[str, str]:
        """Находит секции документа (РЕФЕРАТ, ВВЕДЕНИЕ и т.д.)"""
        sections = {}
        current_section = None
        current_text = []
        
        for para in paragraphs:
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
                if self._is_main_section_start(para):
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
