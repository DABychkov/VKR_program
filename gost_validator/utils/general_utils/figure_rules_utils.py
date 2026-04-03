"""Проверки для правил FIG-* (рисунки)."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def check_figure_caption_below(figure_caption_features: Iterable[Any]) -> list[int]:
    """Возвращает paragraph_index подписей, которые не расположены под рисунком."""
    invalid_indexes: list[int] = []
    for caption in figure_caption_features:
        paragraph_index = int(getattr(caption, "paragraph_index", -1))
        drawing_relative_position = getattr(caption, "drawing_relative_position", "unknown")

        # Используем прямой флаг парсера: подпись корректна только при положении below.
        if drawing_relative_position == "below":
            continue

        invalid_indexes.append(paragraph_index)

    return invalid_indexes


def check_figure_caption_format(figure_caption_features: Iterable[Any]) -> list[int]:
    """Возвращает paragraph_index подписей с нарушением формата (центр/без точки/с номером)."""
    invalid_indexes: list[int] = []
    for caption in figure_caption_features:
        paragraph_index = int(getattr(caption, "paragraph_index", -1))
        alignment = getattr(caption, "alignment", "unknown")
        ends_with_period = bool(getattr(caption, "ends_with_period", False))
        caption_number = getattr(caption, "caption_number", None)

        has_number = bool(caption_number and str(caption_number).strip())
        if alignment == "center" and not ends_with_period and has_number:
            continue

        invalid_indexes.append(paragraph_index)

    return invalid_indexes
