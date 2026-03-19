"""Содержательные проверки для валидатора раздела "СПИСОК ИСПОЛНИТЕЛЕЙ"."""

from re import Pattern

from ..models.validation_result import Severity, ValidationResult
from .common.regex_utils import count_pattern_matches
from .common.section_utils import any_item_contains, any_item_contains_all, text_contains_any


def check_title_page_executor(
    title_page: str,
    result: ValidationResult,
    executor_on_title_pattern: Pattern[str],
) -> None:
    """Проверяет наличие исполнителя на титульнике (если список отсутствует)."""
    if not text_contains_any(title_page, ["исполнитель"]):
        result.add_error(
            Severity.RECOMMENDATION,
            'Не найдена секция "СПИСОК ИСПОЛНИТЕЛЕЙ" и нет фразы "Исполнитель:" на титульнике. '
            'Если исполнителей >2, добавьте структурный элемент "СПИСОК ИСПОЛНИТЕЛЕЙ"'
        )
        return

    if not executor_on_title_pattern.search(title_page):
        result.add_error(
            Severity.RECOMMENDATION,
            'Исполнитель на титульнике найден, но инициалы не распознаны (формат: А.В.)'
        )


def check_executor_section(
    lines: list[str],
    result: ValidationResult,
    initials_pattern: Pattern[str],
) -> None:
    """Проверяет структуру и содержание секции СПИСОК ИСПОЛНИТЕЛЕЙ."""
    if not any_item_contains(lines, "исполнител"):
        result.add_error(
            Severity.CRITICAL,
            'В списке исполнителей отсутствует роль "Исполнители:"'
        )

    initials_count = count_pattern_matches(lines, initials_pattern)

    if initials_count == 0:
        result.add_error(
            Severity.CRITICAL,
            'В списке исполнителей не найдены инициалы (формат: А.В.)'
        )
    elif initials_count < 2:
        result.add_error(
            Severity.RECOMMENDATION,
            f'В списке исполнителей найден только {initials_count} человек. '
            'Если исполнителей <=2, список можно разместить на титульнике'
        )

    has_responsible = any_item_contains_all(lines, ["отв", "исполнител"])
    if not has_responsible:
        result.add_error(
            Severity.RECOMMENDATION,
            'Рекомендуется указать ответственного исполнителя ("Отв. Исполнитель")'
        )
