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
from ..utils.common.section_utils import (
    find_section_text_by_keywords,
    get_non_empty_lines,
    validate_pairwise_order,
)
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

        missing_required = check_required_items(toc_items, self.REQUIRED_ITEMS)
        for required_text in missing_required:
            result.add_error(
                Severity.CRITICAL,
                f'В содержании отсутствует обязательный пункт "{required_text}"',
            )

        intro_page, conclusion_page, sources_page = check_required_item_order(toc_items)

        validate_pairwise_order(
            intro_page,
            conclusion_page,
            "В содержании номер страницы раздела "
            '"ВВЕДЕНИЕ" должен быть меньше номера страницы "ЗАКЛЮЧЕНИЕ"',
            result,
            Severity.RECOMMENDATION,
        )

        validate_pairwise_order(
            conclusion_page,
            sources_page,
            "В содержании номер страницы раздела "
            '"ЗАКЛЮЧЕНИЕ" должен быть меньше номера страницы "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ"',
            result,
            Severity.RECOMMENDATION,
        )

        invalid_pages = check_page_numbers_are_positive(toc_items)
        for item in invalid_pages:
            result.add_error(
                Severity.CRITICAL,
                f'В содержании обнаружен некорректный номер страницы: "{item["title"]}" -> {item["page"]}',
            )

        if check_dot_leaders_hint(lines):
            result.add_error(
                Severity.RECOMMENDATION,
                "В содержании не обнаружен явный разделитель между названием раздела и номером страницы "
                "(отточия, табуляция или расширенный пробел). Проверьте визуальное оформление оглавления.",
            )

        return result
