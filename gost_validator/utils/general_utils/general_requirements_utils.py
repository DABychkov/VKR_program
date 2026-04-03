"""Параметризованные проверки для правил GENERAL-001..GENERAL-007."""

from typing import Any, Iterable

from ..common.rich_utils import (
    calc_font_family_share,
    calc_italic_share,
    calc_non_black_color_share,
    is_first_line_indent_match,
    is_line_spacing_allowed,
    is_page_margin_profile_match,
    is_paragraph_font_size_at_least,
)


def check_page_margins(
    pages_settings: Iterable[Any],
    *,
    left_mm: float = 30.0,
    right_mm: float = 15.0,
    top_mm: float = 20.0,
    bottom_mm: float = 20.0,
    tolerance_mm: float = 1.0,
) -> list[int]:
    """Возвращает индексы секций, где профиль полей не соответствует ГОСТ."""
    invalid_sections: list[int] = []
    for section in pages_settings:
        if not is_page_margin_profile_match(
            section,
            left_mm=left_mm,
            right_mm=right_mm,
            top_mm=top_mm,
            bottom_mm=bottom_mm,
            tolerance_mm=tolerance_mm,
        ):
            invalid_sections.append(int(getattr(section, "section_index", -1)))
    return invalid_sections


def check_first_line_indent(
    paragraph_features: Iterable[Any],
    *,
    expected_mm: float = 12.5,
    tolerance_mm: float = 1.0,
) -> list[int]:
    """Возвращает block_index абзацев с недопустимым абзацным отступом."""
    invalid_indexes: list[int] = []
    for paragraph in paragraph_features:
        if not is_first_line_indent_match(
            paragraph,
            expected_mm=expected_mm,
            tolerance_mm=tolerance_mm,
        ):
            invalid_indexes.append(int(getattr(paragraph, "block_index", -1)))
    return invalid_indexes


def check_line_spacing(
    paragraph_features: Iterable[Any],
    *,
    allowed_values: tuple[float, ...] = (1.0, 1.5),
    tolerance: float = 0.1,
) -> list[int]:
    """Возвращает block_index абзацев с недопустимым межстрочным интервалом."""
    invalid_indexes: list[int] = []
    for paragraph in paragraph_features:
        if not is_line_spacing_allowed(
            paragraph,
            allowed_values=allowed_values,
            tolerance=tolerance,
        ):
            invalid_indexes.append(int(getattr(paragraph, "block_index", -1)))
    return invalid_indexes


def check_min_font_size_share(
    paragraph_features: Iterable[Any],
    *,
    min_size_pt: float = 12.0,
    max_below_threshold_share: float = 0.05,
    allow_unknown_size: bool = True,
) -> tuple[bool, float]:
    """Проверяет, что доля абзацев с малым шрифтом не превышает порог."""
    total = 0
    invalid = 0
    for paragraph in paragraph_features:
        total += 1
        if not is_paragraph_font_size_at_least(
            paragraph,
            min_size_pt=min_size_pt,
            allow_unknown_size=allow_unknown_size,
        ):
            invalid += 1

    if total == 0:
        return True, 0.0

    share = invalid / total
    return share <= max_below_threshold_share, share


def check_italic_share(
    paragraph_features: Iterable[Any],
    *,
    max_italic_share: float = 0.2,
    by_characters: bool = True,
    treat_unknown_as_non_italic: bool = True,
) -> tuple[bool, float | None]:
    """Проверяет, что доля курсива не превышает порог."""
    share = calc_italic_share(
        paragraph_features,
        by_characters=by_characters,
        skip_unknown=not treat_unknown_as_non_italic,
    )
    if share is None:
        return True, None
    return share <= max_italic_share, share


def check_non_black_share(
    paragraph_features: Iterable[Any],
    *,
    max_non_black_share: float = 0.0,
    by_characters: bool = True,
    treat_unknown_as_black: bool = True,
) -> tuple[bool, float | None]:
    """Проверяет, что доля не-черного текста не превышает порог."""
    share = calc_non_black_color_share(
        paragraph_features,
        by_characters=by_characters,
        treat_unknown_as_black=treat_unknown_as_black,
    )
    if share is None:
        return True, None
    return share <= max_non_black_share, share


def check_target_font_share(
    paragraph_features: Iterable[Any],
    *,
    target_font_names: set[str] | tuple[str, ...] = ("Times New Roman",),
    min_target_share: float = 0.7,
    by_characters: bool = True,
    treat_unknown_as_non_target: bool = True,
) -> tuple[bool, float | None]:
    """Проверяет, что доля целевого шрифта не ниже порога."""
    share = calc_font_family_share(
        paragraph_features,
        target_font_names=target_font_names,
        by_characters=by_characters,
        case_sensitive=False,
        skip_unknown=not treat_unknown_as_non_target,
    )
    if share is None:
        return True, None
    return share >= min_target_share, share
