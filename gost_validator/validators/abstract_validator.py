"""Валидатор реферата по ГОСТ 7.32-2017."""

from ..models.document_structure import DocumentStructure
from ..models.validation_result import ValidationResult
from ..config.validation_constants import ABSTRACT_SECTION_KEYWORDS
from ..utils.abstract_utils import (
    check_abstract_size,
    check_abstract_text,
    check_keywords,
    check_volume_info,
)
from ..utils.common.section_utils import find_section_text_by_keywords, get_non_empty_lines
from .base_validator import BaseValidator


class AbstractValidator(BaseValidator):
    """
    Валидатор реферата (структурный элемент 1.4 по ТЗ).
    
    Проверяет:
    1. Наличие сведений об объеме (страницы, книги, иллюстрации, таблицы, источники, приложения)
    2. Формат ключевых слов (капс, запятые, без точки)
    3. Ключевые фразы в тексте реферата (цель, объект - рекомендация)
    4. Объем реферата (>= 850 символов - рекомендация)
    """
    
    MIN_ABSTRACT_SIZE = 850  # Минимум символов в реферате
    
    def validate(self, document: DocumentStructure) -> ValidationResult:
        result = ValidationResult(validator_name="AbstractValidator")

        # Базовая проверка наличия раздела всегда выполняется.
        result.add_rule(rule_id="ABSTRACT-001", status="OK", implemented=True)
        
        # Ищем секцию РЕФЕРАТ
        abstract_text = find_section_text_by_keywords(document.sections, ABSTRACT_SECTION_KEYWORDS)
        
        if not abstract_text:
            result.add_rule(
                rule_id="ABSTRACT-001",
                status="FAIL",
                message='Структурный элемент "РЕФЕРАТ" не найден',
                implemented=True,
            )
            return result

        # Ниже - правила, которые можно проверить только если раздел найден.
        for rule_id in (
            "ABSTRACT-002",
            "ABSTRACT-003",
            "ABSTRACT-004",
            "ABSTRACT-005",
            "ABSTRACT-006",
            "ABSTRACT-007",
            "ABSTRACT-008",
            "ABSTRACT-009",
            "ABSTRACT-010",
        ):
            result.add_rule(rule_id=rule_id, status="OK", implemented=True)
        
        # Разбиваем реферат на строки
        lines = get_non_empty_lines(abstract_text, strip=False)
        
        # 1. Проверка сведений об объеме
        check_volume_info(lines, result)
        
        # 2. Проверка ключевых слов
        check_keywords(lines, result)
        
        # 3. Проверка текста реферата (рекомендации)
        check_abstract_text(abstract_text, result)
        
        # 4. Проверка объема реферата
        check_abstract_size(abstract_text, result, self.MIN_ABSTRACT_SIZE)
        
        return result
