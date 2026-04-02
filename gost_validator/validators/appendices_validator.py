"""Валидатор раздела 1.10 "ПРИЛОЖЕНИЯ"."""

from ..models.document_structure import DocumentStructure
from ..models.validation_result import ValidationResult
from ..config.validation_constants import (
    APPENDIX_SECTION_KEYWORDS,
    CONTENTS_SECTION_KEYWORDS,
    SECTION_APPENDIX,
)
from ..config.regex_patterns import RE_APPENDIX_HEADER
from ..utils.appendices_validation_utils import (
    check_contents_mentions,
    check_designation_sequence,
    extract_label,
    extract_title,
    is_valid_label,
)
from ..utils.common.section_utils import (
    find_section_entries_by_keywords,
    find_section_text_by_keywords,
    get_non_empty_lines,
)
from .base_validator import BaseValidator


class AppendicesValidator(BaseValidator):
    """Проверка структурного элемента 1.10 по ТЗ."""

    APPENDIX_KEYWORD = SECTION_APPENDIX
    INVALID_CYRILLIC_LABELS = {"Ё", "З", "Й", "О", "Ч", "Ъ", "Ы", "Ь"}
    INVALID_LATIN_LABELS = {"I", "O"}
    APPENDIX_HEADER_RE = RE_APPENDIX_HEADER

    def validate(self, document: DocumentStructure) -> ValidationResult:
        result = ValidationResult(validator_name="AppendicesValidator")

        appendix_sections = find_section_entries_by_keywords(
            document.sections,
            APPENDIX_SECTION_KEYWORDS,
            match_mode="startswith",
        )
        if not appendix_sections:
            result.add_rule(
                "APPX-001",
                "FAIL",
                'Разделы приложений не найдены. Ожидаются заголовки формата '
                '"ПРИЛОЖЕНИЕ А" или "ПРИЛОЖЕНИЕ 1". '
                'Если в отчете есть дополнительные материалы, рекомендуется оформить их как приложения.',
            )
            return result

        result.add_rule("APPX-001", "OK")

        contents_text = find_section_text_by_keywords(document.sections, CONTENTS_SECTION_KEYWORDS)
        appendix_entries: list[tuple[str, str | None, str]] = []
        sequence_labels: list[str] = []

        for header, section_text in appendix_sections:
            label = extract_label(header, self.APPENDIX_HEADER_RE)
            title = extract_title(header)
            if not label:
                result.add_rule(
                    "APPX-003",
                    "FAIL",
                    f'В заголовке приложения "{header}" не удалось определить обозначение '
                    '(букву или цифру после слова "ПРИЛОЖЕНИЕ").',
                )
                continue

            if not is_valid_label(label, self.INVALID_CYRILLIC_LABELS, self.INVALID_LATIN_LABELS):
                result.add_rule(
                    "APPX-003",
                    "FAIL",
                    f'Обозначение приложения "{label}" не соответствует допустимому формату ГОСТ.',
                )
                appendix_entries.append((label, title, header))
            else:
                result.add_rule("APPX-003", "OK")
                sequence_labels.append(label)
                appendix_entries.append((label, title, header))
                
            lines = get_non_empty_lines(section_text, strip=True)
            if not lines:
                result.add_rule(
                    "APPX-004",
                    "FAIL",
                    f'Приложение "{label}" найдено, но не содержит текста и заголовка.',
                )
                continue
            else:
                result.add_rule("APPX-004", "OK")

            if not title:
                result.add_rule(
                    "APPX-005",
                    "FAIL",
                    f'В заголовке приложения "{header}" не удалось определить название. '
                    'Ожидается формат: ПРИЛОЖЕНИЕ X, строка в скобках, затем название.',
                )
                continue
            else:
                result.add_rule("APPX-005", "OK")

            if title.endswith("."):
                result.add_rule(
                    "APPX-006",
                    "FAIL",
                    f'Заголовок приложения "{label}" заканчивается точкой. '
                    'По ГОСТ оформляют его без точки в конце.',
                )
            else:
                result.add_rule("APPX-006", "OK")

        digits_non_sequential, cyrillic_non_sequential, latin_non_sequential = check_designation_sequence(
            sequence_labels,
            self.INVALID_CYRILLIC_LABELS,
            self.INVALID_LATIN_LABELS,
        )
        if digits_non_sequential:
            result.add_rule(
                "APPX-007",
                "FAIL",
                'Обозначения приложений в виде цифр идут не последовательно. '
            )
        elif cyrillic_non_sequential:
            result.add_rule(
                "APPX-007",
                "FAIL",
                'Кириллические обозначения приложений идут не по порядку. '
                'Рекомендуется проверить последовательность приложений.'
            )
        elif latin_non_sequential:
            result.add_rule(
                "APPX-007",
                "FAIL",
                'Латинские обозначения приложений идут не по порядку. '
                'Рекомендуется проверить последовательность приложений.'
            )
        elif sequence_labels:
            result.add_rule("APPX-007", "OK")

        contents_facts = check_contents_mentions(
            contents_text,
            appendix_entries,
            self.APPENDIX_KEYWORD,
        )
        for label, has_appendix_marker, has_title in contents_facts:
            if not has_appendix_marker:
                result.add_rule(
                    "APPX-008",
                    "FAIL",
                    f'Приложение "{label}" не найдено в содержании. '
                    'Если содержание оформлено, рекомендуется перечислить в нем все приложения.'
                )
                continue

            if has_title is False:
                result.add_rule(
                    "APPX-008",
                    "FAIL",
                    f'В содержании найдено обозначение приложения "{label}", но не найдено его название. '
                    'Указать в содержании корректно обозначение и наименование приложения.'
                )
            else:
                result.add_rule("APPX-008", "OK")

        if contents_text and appendix_entries:
            result.add_rule("APPX-008", "OK")

        return result