"""Проверки для правил FORMULA-* (формулы)."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def check_formula_line_and_spacing(formula_features: Iterable[Any]) -> list[int]:
    """Возвращает paragraph_index формул с нарушением расположения/отбивок."""
    invalid_indexes: list[int] = []
    for formula in formula_features:
        paragraph_index = int(getattr(formula, "paragraph_index", -1))
        has_blank_line_before = bool(getattr(formula, "has_blank_line_before", False))
        has_blank_line_after = bool(getattr(formula, "has_blank_line_after", False))

        if has_blank_line_before and has_blank_line_after:
            continue

        invalid_indexes.append(paragraph_index)

    return invalid_indexes


def check_formula_where_format(formula_features: Iterable[Any]) -> list[int]:
    """Возвращает paragraph_index формул без корректного пояснения с "где"."""
    invalid_indexes: list[int] = []
    for formula in formula_features:
        paragraph_index = int(getattr(formula, "paragraph_index", -1))
        has_explanation_where = bool(getattr(formula, "has_explanation_where", False))

        if has_explanation_where:
            continue

        invalid_indexes.append(paragraph_index)

    return invalid_indexes