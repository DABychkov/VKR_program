"""Содержательные проверки для валидатора раздела "СОДЕРЖАНИЕ"."""

from ..config.regex_patterns import RE_DOT_LEADER, RE_TOC_ITEM_WITH_PAGE, RE_WIDE_SPACE_PAGE_SUFFIX
from .common.regex_utils import has_pattern_match
from .common.section_utils import (
    find_missing_needles,
    find_first_by_key,
)


def extract_toc_items(lines: list[str]) -> list[dict[str, int | str]]:
    """Извлекает элементы содержания в формате title + page."""
    items: list[dict[str, int | str]] = []

    for line in lines:
        line_upper = line.upper()
        if line_upper == "СОДЕРЖАНИЕ":
            continue

        match = RE_TOC_ITEM_WITH_PAGE.match(line)
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


def check_required_item_order(toc_items: list[dict[str, int | str]]) -> tuple[int | None, int | None, int | None]:
    """Возвращает страницы обязательных разделов для проверки порядка в валидаторе."""

    intro_item = find_first_by_key(toc_items, lambda x: x["title_upper"], "ВВЕДЕНИЕ")
    conclusion_item = find_first_by_key(toc_items, lambda x: x["title_upper"], "ЗАКЛЮЧЕНИЕ")
    sources_item = find_first_by_key(toc_items, lambda x: x["title_upper"], "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ")

    intro_page = int(intro_item["page"]) if intro_item else None
    conclusion_page = int(conclusion_item["page"]) if conclusion_item else None
    sources_page = int(sources_item["page"]) if sources_item else None

    return intro_page, conclusion_page, sources_page

def check_required_items(
    toc_items: list[dict[str, int | str]],
    required_items: dict[str, str],
) -> list[str]:
    """Возвращает обязательные позиции, которые не найдены в содержании."""
    titles_upper = [str(item["title_upper"]) for item in toc_items]
    return find_missing_needles(
        titles_upper,
        list(required_items.keys()),
        case_sensitive=True,
    )


def check_page_numbers_are_positive(
    toc_items: list[dict[str, int | str]],
) -> list[dict[str, int | str]]:
    """Возвращает элементы с невалидными номерами страниц."""
    return [item for item in toc_items if int(item["page"]) <= 0]


def check_dot_leaders_hint(lines: list[str]) -> bool:
    """Возвращает True, если в содержании не обнаружен визуальный разделитель."""
    content_lines = [line for line in lines if line.strip() and line.strip().upper() != "СОДЕРЖАНИЕ"]

    has_dots = has_pattern_match(content_lines, RE_DOT_LEADER)
    has_tab_separator = any("\t" in line for line in content_lines)
    has_wide_space_separator = has_pattern_match(content_lines, RE_WIDE_SPACE_PAGE_SUFFIX)

    return bool(content_lines and not (has_dots or has_tab_separator or has_wide_space_separator))
