"""Валидатор структурного элемента "СОДЕРЖАНИЕ" по ГОСТ 7.32-2017."""

from ..models.document_structure import DocumentStructure
from ..models.validation_result import Severity, ValidationResult
from ..config.validation_constants import CONTENTS_SECTION_KEYWORDS
from ..utils.contents_validation_utils import (
    check_dot_leaders_hint,
    check_page_numbers_are_positive,
    check_required_item_order,
    check_required_items,
    extract_toc_items,
)
from ..utils.common.section_utils import find_section_text_by_keywords, get_non_empty_lines
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

        contents_text = find_section_text_by_keywords(document.sections, CONTENTS_SECTION_KEYWORDS)

        if not contents_text:
            result.add_error(
                Severity.RECOMMENDATION,
                'Структурный элемент "СОДЕРЖАНИЕ" не найден. '
                'Если документ больше 10 страниц, рекомендуется добавить содержание.',
            )
            return result

        lines = get_non_empty_lines(contents_text, strip=True)

        if not lines:
            result.add_error(Severity.CRITICAL, 'Раздел "СОДЕРЖАНИЕ" найден, но он пустой')
            return result

        toc_items = extract_toc_items(lines)
        if not toc_items:
            result.add_error(
                Severity.CRITICAL,
                'Не удалось распознать строки содержания с номерами страниц. '
                'Ожидается формат: "Название раздела ... 12" или "Название раздела 12".',
            )
            return result

        check_required_items(toc_items, result, self.REQUIRED_ITEMS)
        check_required_item_order(toc_items, result)
        check_page_numbers_are_positive(toc_items, result)
        check_dot_leaders_hint(lines, result)

        return result
