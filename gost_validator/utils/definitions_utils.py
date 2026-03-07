"""Утилиты для разбора разделов терминов и сокращений."""

import re
from typing import Optional


_DASHES = "-–—"


def normalize_text(text: str) -> str:
    """Нормализует пробелы/регистр для сравнений."""
    return " ".join(text.replace("\t", " ").split()).strip().lower()


def find_intro_line(lines: list[str], search_depth: int = 5) -> str:
    """Берет первую непустую строку из начала секции (после заголовка)."""
    for line in lines[:search_depth]:
        clean = line.strip()
        if clean:
            return clean
    return ""


def intro_phrase_matches(actual_line: str, expected_phrase: str, min_common_words: int = 9) -> bool:
    """
    Проверяет, что вводная фраза близка к ожидаемой.

    Используем совпадение по количеству ключевых слов, а не точное равенство,
    чтобы переживать мелкие вариации формулировки.
    """
    actual_words = [w for w in re.split(r"\W+", normalize_text(actual_line)) if w]
    expected_words = [w for w in re.split(r"\W+", normalize_text(expected_phrase)) if w]

    if not actual_words or not expected_words:
        return False

    common = sum(1 for word in expected_words if word in actual_words)
    return common >= min_common_words


def split_definition_item(line: str) -> Optional[tuple[str, str]]:
    """
    Пытается извлечь пару (левый термин, правое определение) из строки.

    Поддерживаем варианты:
    - "TERM — definition"
    - "TERM – definition"
    - "TERM - definition"
    - "TERM\tdefinition" (Word-табуляция)
    - "TERM: definition" (мягкий fallback)
    """
    raw = line.strip()
    if not raw:
        return None

    # Приоритет 1: табуляция (часто используется в DOCX как псевдотаблица)
    if "\t" in raw:
        parts = [p.strip() for p in raw.split("\t") if p.strip()]
        if len(parts) >= 2:
            left = parts[0]
            right = " ".join(parts[1:]).strip()
            if left and right:
                return left, right

    # Приоритет 2: тире/дефис
    dash_match = re.match(rf"^(?P<left>.+?)\s*[{_DASHES}]\s*(?P<right>.+)$", raw)
    if dash_match:
        left = dash_match.group("left").strip()
        right = dash_match.group("right").strip()
        if left and right:
            return left, right

    # Приоритет 3: двоеточие (на случай локальных шаблонов)
    colon_match = re.match(r"^(?P<left>.+?)\s*:\s*(?P<right>.+)$", raw)
    if colon_match:
        left = colon_match.group("left").strip()
        right = colon_match.group("right").strip()
        if left and right:
            return left, right

    return None


def extract_definition_items(section_text: str) -> list[tuple[str, str, str]]:
    """
    Извлекает элементы списка определений.

    Возвращает список тройек:
    - left: термин/сокращение
    - right: определение
    - raw_line: исходная строка (для диагностики)
    """
    items: list[tuple[str, str, str]] = []
    for line in section_text.split("\n"):
        parsed = split_definition_item(line)
        if parsed:
            items.append((parsed[0], parsed[1], line))
    return items


def is_alphabetical(values: list[str]) -> bool:
    """Проверяет алфавитный порядок без учета регистра."""
    normalized = [normalize_text(v) for v in values if v.strip()]
    if len(normalized) < 2:
        return True
    return normalized == sorted(normalized)


def has_left_indentation(raw_line: str) -> bool:
    """Проверяет наличие отступа перед термином/сокращением."""
    return bool(re.match(r"^\s+", raw_line))
