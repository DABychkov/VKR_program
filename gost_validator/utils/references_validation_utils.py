"""Содержательные проверки для валидатора раздела "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ"."""

from re import Pattern

from ..models.validation_result import Severity, ValidationResult
from .common.regex_utils import extract_numbered_item_number, filter_pattern_matches


def check_numbering_sequence(list_items: list[str], result: ValidationResult) -> None:
    """Проверяет, что нумерация строго последовательная (1, 2, 3, ...)."""
    expected = 1
    for item in list_items:
        actual = extract_numbered_item_number(item)
        if actual is None:
            continue
        if actual != expected:
            result.add_error(
                Severity.RECOMMENDATION,
                f"Нарушена нумерация в списке использованных источников: "
                f"ожидался номер {expected}, найден {actual}.",
            )
            break
        expected += 1


def check_initials_presence(
    list_items: list[str], result: ValidationResult, initials_pattern: Pattern[str]
) -> None:
    """Рекомендация: хотя бы часть записей должна содержать инициалы авторов."""
    items_with_initials = filter_pattern_matches(list_items, initials_pattern)
    if list_items and not items_with_initials:
        result.add_error(
            Severity.RECOMMENDATION,
            'В записях "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ" не обнаружены инициалы авторов '
            '(ожидается формат "Фамилия И.О." или "И.О. Фамилия"). '
            'Рекомендуется проверить оформление источников.',
        )
