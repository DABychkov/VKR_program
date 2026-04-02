"""Общие утилиты для работы с rich-признаками документа."""

from typing import Any, Iterable

from .text_utils import normalize_text_compact_upper


def is_centered(paragraph_feature: Any) -> bool:
    """Проверяет, что абзац выровнен по центру."""
    return getattr(paragraph_feature, "alignment", "unknown") == "center"


def is_bold(
    paragraph_feature: Any,
    min_bold_ratio: float = 0.5,
    allow_unknown_bold: bool = False,
) -> bool:
    """Проверяет, что абзац набран преимущественно полужирным."""
    bold_ratio = getattr(paragraph_feature, "bold_ratio", None)
    if bold_ratio is None:
        return allow_unknown_bold

    return bold_ratio >= min_bold_ratio


def is_center_bold(
    paragraph_feature: Any,
    min_bold_ratio: float = 0.5,
    allow_unknown_bold: bool = False,
) -> bool:
    """Проверяет, что абзац отцентрирован и набран преимущественно полужирным."""
    if not is_centered(paragraph_feature):
        return False

    return is_bold(
        paragraph_feature,
        min_bold_ratio=min_bold_ratio,
        allow_unknown_bold=allow_unknown_bold,
    )


def find_paragraph_index_by_text(paragraph_features: Iterable[Any], target_text: str) -> int | None:
    """Ищет индекс блока абзаца по нормализованному тексту."""
    target = normalize_text_compact_upper(target_text)
    if not target:
        return None

    for paragraph in paragraph_features:
        paragraph_text = normalize_text_compact_upper(getattr(paragraph, "text", ""))
        if paragraph_text == target:
            return int(getattr(paragraph, "block_index", -1))
    return None
