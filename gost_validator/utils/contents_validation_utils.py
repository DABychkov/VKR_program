"""Содержательные проверки для валидатора раздела "СОДЕРЖАНИЕ"."""

from ..config.regex_patterns import RE_DOT_LEADER, RE_TOC_ITEM_WITH_PAGE, RE_WIDE_SPACE_PAGE_SUFFIX
from ..models.validation_result import Severity, ValidationResult
from .section_utils import find_first_by_key, validate_pairwise_order


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


def check_required_items(
    toc_items: list[dict[str, int | str]],
    result: ValidationResult,
    required_items: dict[str, str],
) -> None:
    """Проверяет обязательные позиции в содержании по ТЗ."""
    titles_upper = [str(item["title_upper"]) for item in toc_items]

    for required_text in required_items:
        if not any(required_text in title for title in titles_upper):
            result.add_error(
                Severity.CRITICAL,
                f'В содержании отсутствует обязательный пункт "{required_text}"',
            )


def check_required_item_order(toc_items: list[dict[str, int | str]], result: ValidationResult) -> None:
    """Проверяет логический порядок страниц обязательных разделов."""
    
    intro_item = find_first_by_key(toc_items, lambda x: x["title_upper"], "ВВЕДЕНИЕ")
    conclusion_item = find_first_by_key(toc_items, lambda x: x["title_upper"], "ЗАКЛЮЧЕНИЕ")
    sources_item = find_first_by_key(toc_items, lambda x: x["title_upper"], "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ")

    intro_page = int(intro_item["page"]) if intro_item else None
    conclusion_page = int(conclusion_item["page"]) if conclusion_item else None
    sources_page = int(sources_item["page"]) if sources_item else None

    validate_pairwise_order(
        intro_page, conclusion_page,
        "В содержании номер страницы раздела "
        '"ВВЕДЕНИЕ" должен быть меньше номера страницы "ЗАКЛЮЧЕНИЕ"',
        result, Severity.RECOMMENDATION
    )

    validate_pairwise_order(
        conclusion_page, sources_page,
        "В содержании номер страницы раздела "
        '"ЗАКЛЮЧЕНИЕ" должен быть меньше номера страницы "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ"',
        result, Severity.RECOMMENDATION
    )


def check_page_numbers_are_positive(
    toc_items: list[dict[str, int | str]], result: ValidationResult
) -> None:
    """Проверяет валидность номеров страниц."""
    invalid_items = [item for item in toc_items if int(item["page"]) <= 0]
    for item in invalid_items:
        result.add_error(
            Severity.CRITICAL,
            f'В содержании обнаружен некорректный номер страницы: "{item["title"]}" -> {item["page"]}',
        )


def check_dot_leaders_hint(lines: list[str], result: ValidationResult) -> None:
    """Добавляет рекомендацию по разделителю названия и страницы."""
    content_lines = [line for line in lines if line.strip() and line.strip().upper() != "СОДЕРЖАНИЕ"]

    has_dots = any(RE_DOT_LEADER.search(line) for line in content_lines)
    has_tab_separator = any("\t" in line for line in content_lines)
    has_wide_space_separator = any(RE_WIDE_SPACE_PAGE_SUFFIX.search(line) for line in content_lines)

    if content_lines and not (has_dots or has_tab_separator or has_wide_space_separator):
        result.add_error(
            Severity.RECOMMENDATION,
            "В содержании не обнаружен явный разделитель между названием раздела и номером страницы "
            "(отточия, табуляция или расширенный пробел). Проверьте визуальное оформление оглавления.",
        )
