"""Валидатор списка исполнителей по ГОСТ 7.32-2017."""

from ..models.document_structure import DocumentStructure
from ..models.validation_result import ValidationResult, Severity
from ..config.regex_patterns import RE_EXECUTOR_ON_TITLE, RE_INITIALS
from ..config.validation_constants import EXECUTOR_SECTION_KEYWORDS
from ..utils.executor_validation_utils import check_executor_section, check_title_page_executor
from ..utils.section_utils import find_section_text_by_keywords, get_non_empty_lines
from .base_validator import BaseValidator


class ExecutorListValidator(BaseValidator):
    """
    Валидатор списка исполнителей (структурный элемент 1.3 по ТЗ).
    
    Правила:
    - Условный элемент (если исполнителей > 2)
    - Если 1 исполнитель -> должен быть на титульнике "Исполнитель:"
    - Формат: слева должности/степени, справа инициалы+фамилия
    - Обязательные роли: "Исполнители:"
    - Условные роли: "Отв. Исполнитель", "Соисполнители:"
    """
    
    def validate(self, document: DocumentStructure) -> ValidationResult:
        result = ValidationResult(validator_name="ExecutorListValidator")
        
        # Проверяем наличие секции "СПИСОК ИСПОЛНИТЕЛЕЙ"
        section_text = find_section_text_by_keywords(document.sections, EXECUTOR_SECTION_KEYWORDS)
        
        if not section_text:
            # Если секции нет, проверяем титульник
            check_title_page_executor(document.title_page_text, result, RE_EXECUTOR_ON_TITLE)
        else:
            # Если секция есть, валидируем её
            lines = get_non_empty_lines(section_text, strip=False)
            check_executor_section(lines, result, RE_INITIALS)
        
        return result
