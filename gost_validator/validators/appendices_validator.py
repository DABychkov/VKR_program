"""Валидатор раздела 1.10 "ПРИЛОЖЕНИЯ"."""

from ..models.document_structure import DocumentStructure
from ..models.validation_result import Severity, ValidationResult
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
            result.add_error(
                Severity.RECOMMENDATION,
                'Разделы "ПРИЛОЖЕНИЕ" не найдены. Если в отчете есть дополнительные материалы, '
                'рекомендуется оформить их как приложения.',
            )
            return result

        contents_text = find_section_text_by_keywords(document.sections, CONTENTS_SECTION_KEYWORDS)
        appendix_entries: list[tuple[str, str, str]] = []

        for header, section_text in appendix_sections:
            label = extract_label(header, self.APPENDIX_HEADER_RE)
            if not label:
                result.add_error(
                    Severity.CRITICAL,
                    f'Заголовок приложения "{header}" не содержит обозначение после слова '
                    '"ПРИЛОЖЕНИЕ".',
                )
                continue

            if not is_valid_label(label, self.INVALID_CYRILLIC_LABELS, self.INVALID_LATIN_LABELS):
                result.add_error(
                    Severity.CRITICAL,
                    f'Обозначение приложения "{label}" не соответствует допустимому формату ГОСТ.',
                )
                
            lines = get_non_empty_lines(section_text, strip=True)
            if not lines:
                result.add_error(
                    Severity.CRITICAL,
                    f'Приложение "{label}" найдено, но не содержит текста и заголовка.',
                )
                continue

            title_line = lines[0]
            appendix_entries.append((label, title_line, header))

            if title_line.upper().startswith(self.APPENDIX_KEYWORD):
                result.add_error(
                    Severity.CRITICAL,
                    f'После заголовка "{header}" не найдено отдельное название приложения.',
                )
            elif title_line.endswith("."):
                result.add_error(
                    Severity.CRITICAL,
                    f'Заголовок приложения "{label}" заканчивается точкой. '
                    'По ТЗ оформляют его без точки в конце.',
                )

        sequence_errors = check_designation_sequence(
            appendix_entries,
            self.INVALID_CYRILLIC_LABELS,
            self.INVALID_LATIN_LABELS,
        )
        for message in sequence_errors:
            result.add_error(Severity.CRITICAL, message)

        contents_errors = check_contents_mentions(
            contents_text,
            appendix_entries,
            self.APPENDIX_KEYWORD,
        )
        for message in contents_errors:
            result.add_error(Severity.CRITICAL, message)

        return result
