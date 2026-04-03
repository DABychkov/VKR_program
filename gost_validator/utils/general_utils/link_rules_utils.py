"""Проверки для правил LINK-* (ссылки)."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from ...config.regex_patterns import RE_TABLE_TITLE


def _extract_table_number(title_text: str | None) -> str | None:
    if not title_text:
        return None
    match = RE_TABLE_TITLE.match(title_text)
    if not match:
        return None
    number = match.group(2)
    return number.strip() if isinstance(number, str) and number.strip() else None


def _build_figure_caption_index_by_number(figure_caption_features: Iterable[Any]) -> dict[str, int]:
    caption_index_by_number: dict[str, int] = {}
    for caption in figure_caption_features:
        caption_number = getattr(caption, "caption_number", None)
        if not caption_number:
            continue

        paragraph_index = int(getattr(caption, "paragraph_index", -1))
        if paragraph_index < 0:
            continue

        # Берем первую встретившуюся подпись по номеру.
        caption_index_by_number.setdefault(caption_number, paragraph_index)

    return caption_index_by_number


def _build_valid_link_positions_by_number(links_features: Iterable[Any], link_type: str) -> dict[str, list[int]]:
    link_positions_by_number: dict[str, list[int]] = {}
    for link in links_features:
        if getattr(link, "link_type", None) != link_type:
            continue

        if getattr(link, "resolved_in_target_list", None) is False:
            continue
        if link_type == "figure" and getattr(link, "resolved_with_object", None) is False:
            continue

        target_number = getattr(link, "target_number", None)
        if not target_number:
            continue

        paragraph_index = getattr(link, "paragraph_index", None)
        if paragraph_index is None:
            continue

        link_positions_by_number.setdefault(target_number, []).append(int(paragraph_index))

    return link_positions_by_number


def check_figure_link_before_caption(
    links_features: Iterable[Any],
    figure_caption_features: Iterable[Any],
) -> list[int]:
    """Возвращает paragraph_index ссылок на рисунки, которые идут не до подписи."""
    caption_index_by_number = _build_figure_caption_index_by_number(figure_caption_features)
    valid_link_positions_by_number = _build_valid_link_positions_by_number(links_features, link_type="figure")
    first_valid_link_index_by_number: dict[str, int] = {
        target_number: min(positions)
        for target_number, positions in valid_link_positions_by_number.items()
        if positions
    }

    invalid_link_paragraph_indexes: list[int] = []
    for link in links_features:
        if getattr(link, "link_type", None) != "figure":
            continue

        link_paragraph_index = getattr(link, "paragraph_index", None)
        if link_paragraph_index is None:
            invalid_link_paragraph_indexes.append(-1)
            continue

        # Если резолвер уже сказал, что ссылка неразрешима, сразу считаем ее нарушением.
        if getattr(link, "resolved_in_target_list", None) is False:
            invalid_link_paragraph_indexes.append(int(link_paragraph_index))
            continue
        if getattr(link, "resolved_with_object", None) is False:
            invalid_link_paragraph_indexes.append(int(link_paragraph_index))
            continue

        target_number = getattr(link, "target_number", None)
        if not target_number:
            invalid_link_paragraph_indexes.append(int(link_paragraph_index))
            continue

        # По каждому target проверяем только первую валидную ссылку.
        first_link_index = first_valid_link_index_by_number.get(target_number)
        if first_link_index is not None and int(link_paragraph_index) != first_link_index:
            continue

        # Если ссылка не попала в валидный индекс (из-за неполных данных), считаем нарушением.
        if int(link_paragraph_index) not in valid_link_positions_by_number.get(target_number, []):
            invalid_link_paragraph_indexes.append(int(link_paragraph_index))
            continue

        caption_index = caption_index_by_number.get(target_number)
        if caption_index is None:
            invalid_link_paragraph_indexes.append(int(link_paragraph_index))
            continue

        # Ссылка должна идти до подписи целевого рисунка.
        if int(link_paragraph_index) < caption_index:
            continue

        invalid_link_paragraph_indexes.append(int(link_paragraph_index))

    return invalid_link_paragraph_indexes


def check_table_link_before_table(links_features: Iterable[Any], table_features: Iterable[Any]) -> list[int]:
    """Возвращает table_index таблиц, для которых нет ссылки до таблицы."""
    table_link_positions = _build_valid_link_positions_by_number(links_features, link_type="table")

    invalid_indexes: list[int] = []
    for table in table_features:
        table_index = int(getattr(table, "table_index", -1))
        table_anchor_index = getattr(table, "table_anchor_paragraph_index", None)
        table_number = _extract_table_number(getattr(table, "title_above_text", None))

        if table_anchor_index is None or not table_number:
            invalid_indexes.append(table_index)
            continue

        links_before = [idx for idx in table_link_positions.get(table_number, []) if idx < int(table_anchor_index)]
        if links_before:
            continue

        invalid_indexes.append(table_index)

    return invalid_indexes