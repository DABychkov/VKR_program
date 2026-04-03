"""Специализированные утилиты для общих требований (GENERAL-*)."""

from .general_requirements_utils import (
    check_first_line_indent,
    check_italic_share,
    check_line_spacing,
    check_min_font_size_share,
    check_non_black_share,
    check_page_margins,
    check_target_font_share,
)

__all__ = [
    "check_page_margins",
    "check_first_line_indent",
    "check_line_spacing",
    "check_min_font_size_share",
    "check_italic_share",
    "check_non_black_share",
    "check_target_font_share",
]
