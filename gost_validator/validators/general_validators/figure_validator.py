"""Валидатор правил оформления рисунков (FIG-001..FIG-005)."""

from ...models.document_structure import DocumentStructure
from ...models.validation_result import ValidationResult
from ...utils.general_utils import (
    check_figure_caption_below,
    check_figure_caption_centered,
    check_figure_caption_explanation_dash,
    check_figure_caption_pattern,
    check_figure_caption_without_period,
)
from ..base_validator import BaseValidator


class FigureValidator(BaseValidator):
    """Проверка оформления подписей рисунков по rich-признакам."""

    def validate(self, document: DocumentStructure) -> ValidationResult:
        result = ValidationResult(validator_name="FigureValidator")
        rich_doc = document.rich_document

        if rich_doc is None:
            return result

        figure_caption_features = list(getattr(rich_doc, "figure_caption_features", []) or [])
        if not figure_caption_features:
            return result

        caption_text_by_index: dict[int, str] = {}
        for caption in figure_caption_features:
            paragraph_index = int(getattr(caption, "paragraph_index", -1))
            caption_text = str(getattr(caption, "caption_text", "") or "").strip()
            if paragraph_index < 0 or not caption_text:
                continue
            caption_text_by_index.setdefault(paragraph_index, caption_text)

        def format_caption_examples(paragraph_indexes: list[int], preview_limit: int = 3) -> str:
            unique_indexes = list(dict.fromkeys(paragraph_indexes))
            snippets: list[str] = []
            for paragraph_index in unique_indexes:
                caption_text = caption_text_by_index.get(paragraph_index)
                if not caption_text:
                    continue
                if len(caption_text) > 80:
                    caption_text = f"{caption_text[:77]}..."
                snippets.append(f'"{caption_text}"')
                if len(snippets) >= preview_limit:
                    break

            if not snippets:
                return ""
            return " Примеры ошибки: " + "; ".join(snippets) + "."

        invalid_below = check_figure_caption_below(figure_caption_features)
        if invalid_below:
            result.add_rule(
                "FIG-001",
                "FAIL",
                "Подпись должна быть расположена под рисунком."
                + format_caption_examples(invalid_below),
            )
        else:
            result.add_rule("FIG-001", "OK")

        invalid_centered = check_figure_caption_centered(figure_caption_features)
        if invalid_centered:
            result.add_rule(
                "FIG-002",
                "FAIL",
                "Подпись рисунка должна быть выровнена по центру."
                + format_caption_examples(invalid_centered),
            )
        else:
            result.add_rule("FIG-002", "OK")

        invalid_explanation_dash = check_figure_caption_explanation_dash(figure_caption_features)
        if invalid_explanation_dash:
            result.add_rule(
                "FIG-003",
                "FAIL",
                "Пояснение в подписи (при наличии) должно быть оформлено через тире."
                + format_caption_examples(invalid_explanation_dash),
            )
        else:
            result.add_rule("FIG-003", "OK")

        invalid_without_period = check_figure_caption_without_period(figure_caption_features)
        if invalid_without_period:
            result.add_rule(
                "FIG-004",
                "FAIL",
                "Подпись рисунка не должна заканчиваться точкой."
                + format_caption_examples(invalid_without_period),
            )
        else:
            result.add_rule("FIG-004", "OK")

        invalid_pattern = check_figure_caption_pattern(figure_caption_features)
        if invalid_pattern:
            result.add_rule(
                "FIG-005",
                "FAIL",
                "Подпись рисунка должна соответствовать допустимому паттерну нумерации."
                + format_caption_examples(invalid_pattern),
            )
        else:
            result.add_rule("FIG-005", "OK")

        return result
