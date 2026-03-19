"""Валидатор раздела 1.7 "ПЕРЕЧЕНЬ СОКРАЩЕНИЙ И ОБОЗНАЧЕНИЙ"."""

from ..models.document_structure import DocumentStructure
from ..models.validation_result import Severity, ValidationResult
from ..config.validation_constants import (
    ABBREVIATIONS_SECTION_KEYWORDS,
    COMBINED_DEFINITIONS_SECTION_KEYWORDS,
)
from ..utils.definitions_utils import (
    extract_definition_items,
    find_intro_line,
    has_left_indentation,
    intro_phrase_matches,
    is_alphabetical,
)
from ..utils.common.section_utils import (
    find_section_text_by_keywords,
    get_non_empty_lines,
    has_section_by_keywords,
)
from .base_validator import BaseValidator


class AbbreviationsValidator(BaseValidator):
    """Проверка структурного элемента 1.7 по ТЗ."""

    EXPECTED_INTRO = "В настоящем отчете о НИР применяют следующие сокращения и обозначения"

    def validate(self, document: DocumentStructure) -> ValidationResult:
        result = ValidationResult(validator_name="AbbreviationsValidator")

        section_text = find_section_text_by_keywords(document.sections, ABBREVIATIONS_SECTION_KEYWORDS)
        has_combined = has_section_by_keywords(document.sections, COMBINED_DEFINITIONS_SECTION_KEYWORDS)

        # Условно-обязательный: если нет 1.7 и нет объединенного раздела -> рекомендация.
        if not section_text:
            if not has_combined:
                result.add_error(
                    Severity.RECOMMENDATION,
                    'Раздел "ПЕРЕЧЕНЬ СОКРАЩЕНИЙ И ОБОЗНАЧЕНИЙ" не найден. '
                    'Если в документе используются сокращения/обозначения, рекомендуется добавить раздел 1.7 '
                    'или объединенный раздел "ОПРЕДЕЛЕНИЯ, ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ".',
                )
            return result

        lines = get_non_empty_lines(section_text, strip=False)
        intro = find_intro_line(lines)
        if intro and not intro_phrase_matches(intro, self.EXPECTED_INTRO, min_common_words=8):
            result.add_error(
                Severity.CRITICAL,
                'В разделе "ПЕРЕЧЕНЬ СОКРАЩЕНИЙ И ОБОЗНАЧЕНИЙ" отсутствует '
                'требуемая вводная формулировка или она слишком сильно отличается от ГОСТ.',
            )

        items = extract_definition_items(section_text)
        if not items:
            result.add_error(
                Severity.CRITICAL,
                'В разделе "ПЕРЕЧЕНЬ СОКРАЩЕНИЙ И ОБОЗНАЧЕНИЙ" не найдены строки '
                'формата "СОКРАЩЕНИЕ — РАСШИФРОВКА".',
            )
            return result

        abbreviations = [left for left, _, _ in items]

        # По ТЗ: без отступа в левой колонке.
        indented = [raw for _, _, raw in items if has_left_indentation(raw)]
        if indented:
            result.add_error(
                Severity.RECOMMENDATION,
                'В части строк раздела 1.7 обнаружен абзацный отступ перед сокращением. '
                'Рекомендуется располагать сокращения без отступа.',
            )

        # По ТЗ: алфавитный порядок.
        if not is_alphabetical(abbreviations):
            result.add_error(
                Severity.RECOMMENDATION,
                'Сокращения в разделе 1.7 не в алфавитном порядке. '
                'Рекомендуется упорядочить список по алфавиту.',
            )

        return result

    
