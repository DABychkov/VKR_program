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


def check_figure_caption_centered(figure_caption_features: Iterable[Any]) -> list[int]:
    """Возвращает paragraph_index подписей, которые не выровнены по центру."""
    invalid_indexes: list[int] = []
    for caption in figure_caption_features:
        paragraph_index = int(getattr(caption, "paragraph_index", -1))
        alignment = getattr(caption, "alignment", "unknown")

        if alignment == "center":
            continue

        invalid_indexes.append(paragraph_index)

    return invalid_indexes


def check_figure_caption_without_period(figure_caption_features: Iterable[Any]) -> list[int]:
    """Возвращает paragraph_index подписей, которые заканчиваются точкой."""
    invalid_indexes: list[int] = []
    for caption in figure_caption_features:
        paragraph_index = int(getattr(caption, "paragraph_index", -1))
        ends_with_period = bool(getattr(caption, "ends_with_period", False))

        if not ends_with_period:
            continue

        invalid_indexes.append(paragraph_index)

    return invalid_indexes


def check_figure_caption_pattern(figure_caption_features: Iterable[Any]) -> list[int]:
    """Возвращает paragraph_index подписей с некорректным типом паттерна подписи."""
    invalid_indexes: list[int] = []
    allowed_pattern_types = {
        "figure_caption_global",
        "figure_caption_sectional",
        "figure_caption_appendix",
    }

    for caption in figure_caption_features:
        paragraph_index = int(getattr(caption, "paragraph_index", -1))
        caption_number = getattr(caption, "caption_number", None)
        pattern_type = getattr(caption, "pattern_type", None)
        in_appendix = bool(getattr(caption, "in_appendix", False))

        has_number = bool(caption_number and str(caption_number).strip())
        is_known_pattern = pattern_type in allowed_pattern_types
        is_appendix_pattern_outside_appendix = (not in_appendix) and pattern_type == "figure_caption_appendix"

        if has_number and is_known_pattern and not is_appendix_pattern_outside_appendix:
            continue

        invalid_indexes.append(paragraph_index)

    return invalid_indexes


def check_figure_caption_explanation_dash(figure_caption_features: Iterable[Any]) -> list[int]:
    """Возвращает paragraph_index подписей, где пояснение есть, но разделитель не тире."""
    invalid_indexes: list[int] = []
    for caption in figure_caption_features:
        paragraph_index = int(getattr(caption, "paragraph_index", -1))
        caption_number = getattr(caption, "caption_number", None)
        caption_text = str(getattr(caption, "caption_text", "") or "")
        has_dash_separator = bool(getattr(caption, "has_dash_separator", False))

        if not caption_number:
            continue

        # Если после номера есть непустой текст, считаем, что у подписи есть пояснение.
        number_token = str(caption_number).strip()
        tail = caption_text.split(number_token, 1)[-1].strip() if number_token and number_token in caption_text else ""
        tail_without_separator = tail.lstrip("-–—: ").strip()
        has_explanation = bool(tail_without_separator)

        if not has_explanation:
            continue

        if has_dash_separator:
            continue

        invalid_indexes.append(paragraph_index)

    return invalid_indexes


def check_figure_caption_format(figure_caption_features: Iterable[Any]) -> list[int]:
    """Совместимость: агрегированная проверка (центр/без точки/с номером)."""
    invalid_by_center = set(check_figure_caption_centered(figure_caption_features))
    invalid_by_period = set(check_figure_caption_without_period(figure_caption_features))

    invalid_by_number: set[int] = set()
    for caption in figure_caption_features:
        paragraph_index = int(getattr(caption, "paragraph_index", -1))
        caption_number = getattr(caption, "caption_number", None)
        has_number = bool(caption_number and str(caption_number).strip())
        if has_number:
            continue
        invalid_by_number.add(paragraph_index)

    return sorted(invalid_by_center | invalid_by_period | invalid_by_number)
