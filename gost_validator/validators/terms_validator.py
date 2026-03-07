"""Валидатор раздела 1.6 "ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ"."""

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


class TermsValidator(BaseValidator):
    """Проверка структурного элемента 1.6 по ТЗ."""

    SECTION_NAME = "ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ"
    COMBINED_SECTION_NAME = "ОПРЕДЕЛЕНИЯ, ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ"
    EXPECTED_INTRO = (
        "В настоящем отчете о НИР применяют следующие термины "
        "с соответствующими определениями"
    )

    def validate(self, document: DocumentStructure) -> ValidationResult:
        result = ValidationResult(validator_name="TermsValidator")

        section_name, section_text = self._find_terms_section(document.sections)
        has_combined = self._has_combined_section(document.sections)

        # Условно-обязательный: отсутствие = рекомендация, если нет комбинированного варианта.
        if not section_text:
            if not has_combined:
                result.add_error(
                    Severity.RECOMMENDATION,
                    'Раздел "ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ" не найден. '
                    'Если в документе используются термины, рекомендуется добавить раздел 1.6.',
                )
            return result

        lines = [line for line in section_text.split("\n") if line.strip()]
        intro = find_intro_line(lines)
        if intro and not intro_phrase_matches(intro, self.EXPECTED_INTRO, min_common_words=9):
            result.add_error(
                Severity.CRITICAL,
                'В разделе "ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ" отсутствует требуемая вводная формулировка '
                'или она слишком сильно отличается от ГОСТ.',
            )

        items = extract_definition_items(section_text)
        if not items:
            result.add_error(
                Severity.CRITICAL,
                'В разделе "ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ" не найдены статьи формата '
                '"ТЕРМИН — ОПРЕДЕЛЕНИЕ" (или табличный эквивалент).',
            )
            return result

        terms = [left for left, _, _ in items]

        # По ТЗ: слева без абзацного отступа.
        indented = [raw for _, _, raw in items if has_left_indentation(raw)]
        if indented:
            result.add_error(
                Severity.RECOMMENDATION,
                'В части строк раздела 1.6 обнаружен абзацный отступ перед термином. '
                'Рекомендуется располагать термины без отступа.',
            )

        # По ТЗ: без знаков препинания в конце термина.
        bad_trailing = [term for term in terms if term.rstrip().endswith((".", ";", ":", ","))]
        if bad_trailing:
            result.add_error(
                Severity.RECOMMENDATION,
                'Некоторые термины в разделе 1.6 заканчиваются знаком препинания. '
                'Рекомендуется убрать пунктуацию в конце левой части статьи.',
            )

        # По ТЗ: алфавитный порядок.
        if not is_alphabetical(terms):
            result.add_error(
                Severity.RECOMMENDATION,
                'Термины в разделе 1.6 не в алфавитном порядке. '
                'Рекомендуется упорядочить список по алфавиту.',
            )

        return result

    def _find_terms_section(self, sections: dict[str, str]) -> tuple[str | None, str | None]:
        for name, text in sections.items():
            if self.SECTION_NAME in name.upper():
                return name, text
        return None, None

    def _has_combined_section(self, sections: dict[str, str]) -> bool:
        return any(self.COMBINED_SECTION_NAME in name.upper() for name in sections)
