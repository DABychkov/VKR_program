"""Содержательные проверки для валидатора раздела "СПИСОК ИСПОЛНИТЕЛЕЙ"."""

from re import Pattern

from .common.regex_utils import count_pattern_matches
from .common.section_utils import any_item_contains, any_item_contains_all, text_contains_any


def check_title_page_executor(
    title_page: str,
    executor_on_title_pattern: Pattern[str],
) -> str | None:
    """Возвращает сообщение ошибки для титульника, если проверка не пройдена."""
    if not text_contains_any(title_page, ["исполнитель"]):
        return (
            'Не найдена секция "СПИСОК ИСПОЛНИТЕЛЕЙ" и нет фразы "Исполнитель:" на титульнике. '
            'Если исполнителей >2, добавьте структурный элемент "СПИСОК ИСПОЛНИТЕЛЕЙ"'
        )

    if not executor_on_title_pattern.search(title_page):
        return 'Исполнитель на титульнике найден, но инициалы не распознаны (формат: А.В.)'

    return None


def check_executor_section(
    lines: list[str],
    initials_pattern: Pattern[str],
) -> tuple[bool, int, bool]:
    """Возвращает признаки для проверки секции: роль, количество инициалов, ответственный."""
    has_role = any_item_contains(lines, "исполнител")

    initials_count = count_pattern_matches(lines, initials_pattern)
    has_responsible = any_item_contains_all(lines, ["отв", "исполнител"])

    return has_role, initials_count, has_responsible
