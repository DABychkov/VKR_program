"""Валидатор раздела 1.7 "ПЕРЕЧЕНЬ СОКРАЩЕНИЙ И ОБОЗНАЧЕНИЙ"."""

from ..models.document_structure import DocumentStructure
from ..models.validation_result import Severity, ValidationResult
from ..utils.definitions_utils import (
    extract_definition_items,
    find_intro_line,
    has_left_indentation,
    intro_phrase_matches,
    is_alphabetical,
)
from .base_validator import BaseValidator


class AbbreviationsValidator(BaseValidator):
    """Проверка структурного элемента 1.7 по ТЗ."""

    SECTION_NAME = "ПЕРЕЧЕНЬ СОКРАЩЕНИЙ И ОБОЗНАЧЕНИЙ"
    COMBINED_SECTION_NAME = "ОПРЕДЕЛЕНИЯ, ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ"
    EXPECTED_INTRO = "В настоящем отчете о НИР применяют следующие сокращения и обозначения"

    def validate(self, document: DocumentStructure) -> ValidationResult:
        result = ValidationResult(validator_name="AbbreviationsValidator")

        section_text = self._find_abbreviations_section(document.sections)
        has_combined = self._has_combined_section(document.sections)

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

        lines = [line for line in section_text.split("\n") if line.strip()]
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

    def _find_abbreviations_section(self, sections: dict[str, str]) -> str | None:
        for name, text in sections.items():
            if self.SECTION_NAME in name.upper():
                return text
        return None

    def _has_combined_section(self, sections: dict[str, str]) -> bool:
        return any(self.COMBINED_SECTION_NAME in name.upper() for name in sections)
