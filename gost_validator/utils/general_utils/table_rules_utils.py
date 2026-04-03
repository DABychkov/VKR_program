"""Проверки для правил TABLE-* (таблицы)."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def check_table_title_position_left(table_features: Iterable[Any]) -> list[int]:
    """Возвращает table_index таблиц без корректного заголовка сверху/слева."""
    invalid_indexes: list[int] = []
    for table in table_features:
        table_index = int(getattr(table, "table_index", -1))
        title = getattr(table, "title_above_text", None)
        title_paragraph_index = getattr(table, "title_paragraph_index", None)
        title_alignment = getattr(table, "title_alignment", "unknown")

        has_title = bool(title and str(title).strip())
        has_title_above = title_paragraph_index is not None
        is_left = title_alignment == "left"

        if has_title and has_title_above and is_left:
            continue

        invalid_indexes.append(table_index)

    return invalid_indexes
