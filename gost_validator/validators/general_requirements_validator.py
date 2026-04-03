"""Валидатор общих требований оформления (GENERAL-001..GENERAL-007)."""

from ..models.document_structure import DocumentStructure
from ..models.validation_result import ValidationResult
from ..utils.general_utils import (
    check_first_line_indent,
    check_italic_share,
    check_line_spacing,
    check_min_font_size_share,
    check_non_black_share,
    check_page_margins,
    check_target_font_share,
)
from .base_validator import BaseValidator


class GeneralRequirementsValidator(BaseValidator):
    """Проверка общих требований оформления документа по rich-признакам."""

    def validate(self, document: DocumentStructure) -> ValidationResult:
        result = ValidationResult(validator_name="GeneralRequirementsValidator")
        rich_doc = document.rich_document

        if rich_doc is None:
            return result

        def format_int_list(values: list[int], preview_limit: int = 12) -> str:
            if not values:
                return ""
            preview = ", ".join(str(v) for v in values[:preview_limit])
            if len(values) > preview_limit:
                preview += f", ... (+{len(values) - preview_limit})"
            return preview

        def format_share(share: float | None) -> str:
            if share is None:
                return "N/A"
            return f"{share * 100:.1f}%"

        paragraph_features = [
            paragraph
            for paragraph in getattr(rich_doc, "paragraph_features", [])
            if (getattr(paragraph, "text", "") or "").strip()
        ]

        invalid_sections = check_page_margins(getattr(rich_doc, "pages_settings", []))
        if invalid_sections:
            result.add_rule(
                "GENERAL-001",
                "FAIL",
                "Профиль полей 30/15/20/20 мм нарушен в секциях: "
                f"{format_int_list(invalid_sections)}.",
            )
        else:
            result.add_rule("GENERAL-001", "OK")

        if paragraph_features:
            italic_threshold = 0.2
            min_tnr_share = 0.7

            invalid_indent = check_first_line_indent(paragraph_features)
            if invalid_indent:
                result.add_rule(
                    "GENERAL-002",
                    "FAIL",
                    "Абзацный отступ не соответствует целевому значению в абзацах: "
                    f"{format_int_list(invalid_indent)}.",
                )
            else:
                result.add_rule("GENERAL-002", "OK")

            invalid_spacing = check_line_spacing(paragraph_features)
            if invalid_spacing:
                result.add_rule(
                    "GENERAL-003",
                    "FAIL",
                    "Недопустимый межстрочный интервал в абзацах: "
                    f"{format_int_list(invalid_spacing)}.",
                )
            else:
                result.add_rule("GENERAL-003", "OK")

            font_ok, font_bad_share = check_min_font_size_share(paragraph_features)
            if not font_ok:
                result.add_rule(
                    "GENERAL-004",
                    "FAIL",
                    "Доля абзацев с размером шрифта ниже 12 pt превышает порог: "
                    f"{format_share(font_bad_share)}.",
                )
            else:
                result.add_rule("GENERAL-004", "OK")

            italic_ok, italic_share = check_italic_share(paragraph_features)
            if not italic_ok:
                result.add_rule(
                    "GENERAL-005",
                    "FAIL",
                    "Доля курсива превышает допустимый порог "
                    f"{format_share(italic_threshold)}: {format_share(italic_share)}.",
                )
            else:
                result.add_rule("GENERAL-005", "OK")

            non_black_ok, non_black_share = check_non_black_share(paragraph_features)
            if not non_black_ok:
                result.add_rule(
                    "GENERAL-006",
                    "FAIL",
                    "Обнаружена недопустимая доля не-черного цвета шрифта: "
                    f"{format_share(non_black_share)}.",
                )
            else:
                result.add_rule("GENERAL-006", "OK")

            font_family_ok, font_family_share = check_target_font_share(
                paragraph_features,
                min_target_share=min_tnr_share,
                treat_unknown_as_non_target=True,
            )
            if not font_family_ok:
                result.add_rule(
                    "GENERAL-007",
                    "FAIL",
                    "Доля текста в Times New Roman ниже порога "
                    f"{format_share(min_tnr_share)}: {format_share(font_family_share)}.",
                )
            else:
                result.add_rule("GENERAL-007", "OK")

        return result
