"""Утилиты для типовых операций на регулярных выражениях."""

import re
from re import Pattern

from ..config.regex_patterns import RE_NUMBERED_ITEM_PREFIX


def extract_int_by_pattern(text: str, pattern: Pattern[str], group: int | str = 1) -> int | None:
    """Ищет pattern в text и возвращает целое из указанной группы."""
    match = pattern.search(text)
    if not match:
        return None

    try:
        return int(match.group(group))
    except (IndexError, TypeError, ValueError):
        return None


def split_words_by_non_word(text: str) -> list[str]:
    """Делит строку по не-словесным символам и убирает пустые токены."""
    return [token for token in re.split(r"\W+", text) if token]


def extract_numbered_item_number(line: str) -> int | None:
    """Извлекает номер из строки формата '1. ...' или '1 ...'."""
    return extract_int_by_pattern(line, RE_NUMBERED_ITEM_PREFIX, group=1)


def count_pattern_matches(items: list[str], pattern: Pattern[str]) -> int:
    """
    Посчитать сколько элементов совпадают с паттерном.
    
    Пример:
        items = ["А.В. Иванов", "Петров", "И.М. Сидоров"]
        pattern = RE_INITIALS
        count_pattern_matches(items, pattern)  # → 2
    """
    return sum(1 for item in items if pattern.search(item))


def filter_pattern_matches(items: list[str], pattern: Pattern[str]) -> list[str]:
    """
    Получить только элементы совпадающие с паттерном.
    
    Пример:
        items = ["А.В. Иванов", "Петров", "И.М. Сидоров"]
        pattern = RE_INITIALS
        filter_pattern_matches(items, pattern)  # → ["А.В. Иванов", "И.М. Сидоров"]
    """
    return [item for item in items if pattern.search(item)]


def find_first_by_pattern(items: list[str], pattern: Pattern[str]) -> str | None:
    """
    Найти первый элемент совпадающий с паттерном.
    
    Пример:
        items = ["something", "А.В. Иванов", "Петров"]
        pattern = RE_INITIALS
        find_first_by_pattern(items, pattern)  # → "А.В. Иванов"
    """
    for item in items:
        if pattern.search(item):
            return item
    return None
