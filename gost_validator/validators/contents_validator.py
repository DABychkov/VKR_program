"""Валидатор структурного элемента "СОДЕРЖАНИЕ" по ГОСТ 7.32-2017."""

import re

from ..models.document_structure import DocumentStructure
from ..models.validation_result import Severity, ValidationResult
from .base_validator import BaseValidator


class ContentsValidator(BaseValidator):
    """
    Валидатор содержания (структурный элемент 1.5 по ТЗ).

    Логика по ТЗ:
    - "СОДЕРЖАНИЕ" может отсутствовать для коротких работ (< 10 страниц),
      поэтому отсутствие секции помечается как рекомендация.
    - Если секция есть, в ней должны быть ключевые элементы:
      "ВВЕДЕНИЕ", "ЗАКЛЮЧЕНИЕ", "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ".
    - Для строк оглавления ожидается номер страницы в конце строки.
    - Проверяется базовая консистентность номеров страниц обязательных пунктов.
    """

    REQUIRED_ITEMS = {
        "ВВЕДЕНИЕ": "ВВЕДЕНИЕ",
        "ЗАКЛЮЧЕНИЕ": "ЗАКЛЮЧЕНИЕ",
        "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ": "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ",
    }

    def validate(self, document: DocumentStructure) -> ValidationResult:
        result = ValidationResult(validator_name="ContentsValidator")

        contents_text = self._find_contents_section(document.sections)

        if not contents_text:
            result.add_error(
                Severity.RECOMMENDATION,
                'Структурный элемент "СОДЕРЖАНИЕ" не найден. '
                'Если документ больше 10 страниц, рекомендуется добавить содержание.',
            )
            return result

        lines = [line.strip() for line in contents_text.split("\n") if line.strip()]

        if not lines:
            result.add_error(Severity.CRITICAL, 'Раздел "СОДЕРЖАНИЕ" найден, но он пустой')
            return result

        toc_items = self._extract_toc_items(lines)
        if not toc_items:
            result.add_error(
                Severity.CRITICAL,
                'Не удалось распознать строки содержания с номерами страниц. '
                'Ожидается формат: "Название раздела ... 12" или "Название раздела 12".',
            )
            return result

        self._check_required_items(toc_items, result)
        self._check_required_item_order(toc_items, result)
        self._check_page_numbers_are_positive(toc_items, result)
        self._check_dot_leaders_hint(lines, result)

        return result

    def _find_contents_section(self, sections: dict[str, str]) -> str | None:
        """Ищет секцию содержания с учетом возможных вариаций написания."""
        for section_name, section_text in sections.items():
            name_upper = section_name.upper().strip()
            if "СОДЕРЖАНИЕ" in name_upper:
                return section_text
        return None

    def _extract_toc_items(self, lines: list[str]) -> list[dict[str, int | str]]:
        """Извлекает элементы содержания в формате title + page."""
        items: list[dict[str, int | str]] = []

        # Примеры поддерживаемых строк:
        # "ВВЕДЕНИЕ 9"
        # "1 Теоретическая часть...........12"
        # "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ\t67"
        line_pattern = re.compile(r"^(?P<title>.+?)\s*(?:\.{2,}\s*)?(?P<page>\d+)\s*$")

        for line in lines:
            line_upper = line.upper()
            if line_upper == "СОДЕРЖАНИЕ":
                continue

            match = line_pattern.match(line)
            if not match:
                continue

            title = match.group("title").strip()
            page_text = match.group("page").strip()

            if not title:
                continue

            try:
                page = int(page_text)
            except ValueError:
                continue

            items.append({"title": title, "title_upper": title.upper(), "page": page})

        return items

    def _check_required_items(self, toc_items: list[dict[str, int | str]], result: ValidationResult) -> None:
        """Проверяет обязательные позиции в содержании по ТЗ."""
        titles_upper = [str(item["title_upper"]) for item in toc_items]

        for required_text in self.REQUIRED_ITEMS:
            if not any(required_text in title for title in titles_upper):
                result.add_error(
                    Severity.CRITICAL,
                    f'В содержании отсутствует обязательный пункт "{required_text}"',
                )

    def _check_required_item_order(self, toc_items: list[dict[str, int | str]], result: ValidationResult) -> None:
        """Проверяет логический порядок страниц обязательных разделов."""

        def find_page(required_text: str) -> int | None:
            for item in toc_items:
                if required_text in str(item["title_upper"]):
                    return int(item["page"])
            return None

        intro_page = find_page("ВВЕДЕНИЕ")
        conclusion_page = find_page("ЗАКЛЮЧЕНИЕ")
        sources_page = find_page("СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ")

        # Строгий критичный порядок по ТЗ не указан, поэтому это рекомендация.
        if intro_page and conclusion_page and intro_page >= conclusion_page:
            result.add_error(
                Severity.RECOMMENDATION,
                "В содержании номер страницы раздела "
                '"ВВЕДЕНИЕ" должен быть меньше номера страницы "ЗАКЛЮЧЕНИЕ"',
            )

        if conclusion_page and sources_page and conclusion_page >= sources_page:
            result.add_error(
                Severity.RECOMMENDATION,
                "В содержании номер страницы раздела "
                '"ЗАКЛЮЧЕНИЕ" должен быть меньше номера страницы "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ"',
            )

    def _check_page_numbers_are_positive(self, toc_items: list[dict[str, int | str]], result: ValidationResult) -> None:
        """Проверяет валидность номеров страниц."""
        invalid_items = [item for item in toc_items if int(item["page"]) <= 0]
        for item in invalid_items:
            result.add_error(
                Severity.CRITICAL,
                f'В содержании обнаружен некорректный номер страницы: "{item["title"]}" -> {item["page"]}',
            )

    def _check_dot_leaders_hint(self, lines: list[str], result: ValidationResult) -> None:
        """Рекомендация по читаемому разделителю между названием и номером страницы."""
        content_lines = [line for line in lines if line.strip() and line.strip().upper() != "СОДЕРЖАНИЕ"]

        # По ТЗ обычно используют отточия, но в Word они нередко представлены
        # табуляцией или широким пробельным разделителем. Считаем все эти варианты допустимыми.
        has_dots = any(re.search(r"\.{2,}", line) for line in content_lines)
        has_tab_separator = any("\t" in line for line in content_lines)
        has_wide_space_separator = any(re.search(r"\s{2,}\d+\s*$", line) for line in content_lines)

        if content_lines and not (has_dots or has_tab_separator or has_wide_space_separator):
            result.add_error(
                Severity.RECOMMENDATION,
                "В содержании не обнаружен явный разделитель между названием раздела и номером страницы "
                "(отточия, табуляция или расширенный пробел). Проверьте визуальное оформление оглавления.",
            )
