"""Валидатор раздела 1.9 "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ"."""

from ..models.document_structure import DocumentStructure
from ..models.validation_result import Severity, ValidationResult
from ..config.regex_patterns import RE_NUMBERED_LIST_ITEM_LINE, RE_SURNAME_WITH_INITIALS
from ..config.validation_constants import (
    REFERENCES_SECTION_KEYWORDS,
)
from ..utils.references_validation_utils import check_initials_presence, check_numbering_sequence
from ..utils.common.section_utils import find_section_text_by_keywords, get_non_empty_lines
from .base_validator import BaseValidator


class ReferencesValidator(BaseValidator):
    """

    По ТЗ:
    - Раздел обязательный. Проверяем наличие фразы "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ".
    - После фразы текст не должен быть пустым.
    - Список должен начинаться с "1.".
    - Рекомендация: в каждом элементе должны быть инициалы (шаблон «Буква.Буква.»).
    """

    # Шаблон элемента списка: «1.», «2.» и т.д., а также «1 Автор» (без точки).
    _LIST_ITEM_RE = RE_NUMBERED_LIST_ITEM_LINE

    # Шаблон инициалов: Ф.И. или Фамилия И.О. - ищем хотя бы «Х.Х.» (буква, точка, буква, точка)
    _INITIALS_RE = RE_SURNAME_WITH_INITIALS

    def validate(self, document: DocumentStructure) -> ValidationResult:
        result = ValidationResult(validator_name="ReferencesValidator")

        section_text = find_section_text_by_keywords(document.sections, REFERENCES_SECTION_KEYWORDS)

        if section_text is None:
            result.add_error(
                Severity.CRITICAL,
                'Обязательный раздел "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ" не найден.',
            )
            return result

        lines = get_non_empty_lines(section_text, strip=True)

        if not lines:
            result.add_error(
                Severity.CRITICAL,
                'Раздел "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ" найден, но он пустой.',
            )
            return result

        # Проверяем, что список начинается с "1."
        if not self._LIST_ITEM_RE.match(lines[0]):
            result.add_error(
                Severity.CRITICAL,
                'Список использованных источников должен начинаться с нумерованного пункта "1. ...".',
            )

        # Собираем элементы списка (строки, начинающиеся с числа и точки)
        list_items = [line for line in lines if self._LIST_ITEM_RE.match(line)]

        if not list_items:
            result.add_error(
                Severity.CRITICAL,
                'В разделе "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ" не обнаружено нумерованных записей '
                '(ожидается формат "1. Автор И.О. Название...").',
            )
            return result

        numbering_ok, expected, actual = check_numbering_sequence(list_items)
        if not numbering_ok:
            result.add_error(
                Severity.RECOMMENDATION,
                f"Нарушена нумерация в списке использованных источников: "
                f"ожидался номер {expected}, найден {actual}.",
            )

        has_initials = check_initials_presence(list_items, self._INITIALS_RE)
        if list_items and not has_initials:
            result.add_error(
                Severity.RECOMMENDATION,
                'В записях "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ" не обнаружены инициалы авторов '
                '(ожидается формат "Фамилия И.О." или "И.О. Фамилия"). '
                'Рекомендуется проверить оформление источников.',
            )

        return result
