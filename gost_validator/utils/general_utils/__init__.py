"""Специализированные утилиты для общих требований (GENERAL-*)."""

from .general_requirements_utils import (
    check_first_line_indent,
    check_italic_share,
    check_line_spacing,
    check_min_font_size_share,
    check_non_black_share,
    check_page_numbering_centered,
    check_page_numbering_present,
    check_page_margins,
    check_target_font_share,
)
from .figure_rules_utils import (
    check_figure_caption_below,
    check_figure_caption_centered,
    check_figure_caption_explanation_dash,
    check_figure_caption_format,
    check_figure_caption_pattern,
    check_figure_caption_without_period,
)
from .table_rules_utils import (
    check_table_title_position_left,
)
from .formula_rules_utils import (
    check_formula_line_and_spacing,
    check_formula_where_format,
)
from .link_rules_utils import (
    check_figure_link_before_caption,
    check_table_link_before_table,
)

__all__ = [
    "check_page_margins",
    "check_first_line_indent",
    "check_line_spacing",
    "check_min_font_size_share",
    "check_italic_share",
    "check_non_black_share",
    "check_target_font_share",
    "check_page_numbering_present",
    "check_page_numbering_centered",
    "check_figure_caption_below",
    "check_figure_caption_centered",
    "check_figure_caption_without_period",
    "check_figure_caption_pattern",
    "check_figure_caption_explanation_dash",
    "check_figure_caption_format",
    "check_table_title_position_left",
    "check_table_link_before_table",
    "check_formula_line_and_spacing",
    "check_formula_where_format",
    "check_figure_link_before_caption",
]
