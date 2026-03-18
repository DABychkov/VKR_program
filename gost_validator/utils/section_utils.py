"""Общие функции поиска и проверки секций документа."""

from typing import Literal

from ..models.validation_result import Severity, ValidationResult


MatchMode = Literal["contains", "startswith", "equals"]


def find_section_text_by_keywords(
    sections: dict[str, str],
    keywords: tuple[str, ...] | list[str],
    match_mode: MatchMode = "contains",
) -> str | None:
    """Возвращает текст первой секции, имя которой совпадает с ключевыми словами."""
    for section_name, section_text in sections.items():
        name_upper = section_name.upper().strip()
        for keyword in keywords:
            keyword_upper = keyword.upper().strip()
            if _matches(name_upper, keyword_upper, match_mode):
                return section_text
    return None


def get_non_empty_lines(section_text: str, strip: bool = True) -> list[str]:
    """Возвращает непустые строки секции с опциональным strip()."""
    if strip:
        return [line.strip() for line in section_text.split("\n") if line.strip()]
    return [line for line in section_text.split("\n") if line.strip()]


def has_section_by_keywords(
    sections: dict[str, str],
    keywords: tuple[str, ...] | list[str],
    match_mode: MatchMode = "contains",
) -> bool:
    """Проверяет наличие секции по ключевым словам."""
    return find_section_text_by_keywords(sections, keywords, match_mode) is not None


def find_section_entries_by_keywords(
    sections: dict[str, str],
    keywords: tuple[str, ...] | list[str],
    match_mode: MatchMode = "contains",
) -> list[tuple[str, str]]:
    """Возвращает все секции (имя, текст), совпавшие по ключевым словам."""
    found: list[tuple[str, str]] = []
    for section_name, section_text in sections.items():
        name_upper = section_name.upper().strip()
        for keyword in keywords:
            keyword_upper = keyword.upper().strip()
            if _matches(name_upper, keyword_upper, match_mode):
                found.append((section_name, section_text))
                break
    return found


def _matches(name_upper: str, keyword_upper: str, match_mode: MatchMode) -> bool:
    if match_mode == "contains":
        return keyword_upper in name_upper
    if match_mode == "startswith":
        return name_upper.startswith(keyword_upper)
    return name_upper == keyword_upper


def find_first_by_key(
    items: list,
    key_fn: callable,
    search_value: str,
) -> any | None:
    """
    Найти первый элемент где key_fn(item) содержит search_value.
    
    Пример:
        items = [{"title": "ВВЕДЕНИЕ", "page": 5}, {"title": "ЗАКЛЮЧЕНИЕ", "page": 20}]
        find_first_by_key(items, lambda x: x["title"], "ВВЕДЕНИЕ")  # → словарь
    """
    for item in items:
        key_value = str(key_fn(item)).upper()
        if search_value.upper() in key_value:
            return item
    return None


def check_is_sequential(values: list[int]) -> bool:
    """
    Проверяет что числовые значения идут подряд (1,2,3 или 5,6,7).
    
    Возвращает True если последовательны, False если нарушена.
    Пустой или одноэлементный список считается последовательным.
    
    Пример:
        check_is_sequential([1, 2, 3])  # → True
        check_is_sequential([1, 3, 5])  # → False
        check_is_sequential([5, 6, 7])  # → True
    """
    if len(values) < 2:
        return True
    
    expected = list(range(values[0], values[0] + len(values)))
    return values == expected


def validate_pairwise_order(
    val1: int | None,
    val2: int | None,
    error_msg: str,
    result: ValidationResult,
    severity: Severity = Severity.RECOMMENDATION,
) -> bool:
    """
    Проверяет что val1 < val2. Если нет — добавляет ошибку.
    
    Возвращает True если порядок корректен, False если нарушен.
    Если один из값ений None, проверка считается успешной.
    
    Пример:
        intro_page = 5
        conclusion_page = 3
        validate_pairwise_order(
            intro_page, 
            conclusion_page,
            "Введение должна быть перед заключением",
            result
        )  # → Добавляет error, возвращает False
    """
    if val1 and val2 and val1 >= val2:
        result.add_error(severity, error_msg)
        return False
    return True
