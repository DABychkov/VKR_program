"""Валидатор реферата по ГОСТ 7.32-2017."""

from ..models.document_structure import DocumentStructure
from ..models.validation_result import ValidationResult, Severity
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
        
        # Ищем секцию РЕФЕРАТ
        abstract_text = find_section_text_by_keywords(document.sections, ABSTRACT_SECTION_KEYWORDS)
        
        if not abstract_text:
            result.add_error(
                Severity.CRITICAL,
                'Структурный элемент "РЕФЕРАТ" не найден'
            )
            return result
        
        # Разбиваем реферат на строки
        lines = get_non_empty_lines(abstract_text, strip=False)
        
        # 1. Проверка сведений об объеме
        found_metrics, has_invalid_volume_separator = check_volume_info(lines)
        if len(found_metrics) < 3:
            result.add_error(
                Severity.CRITICAL,
                f'Неполна информация об объеме отчета. Найдено: {found_metrics}. '
                'Требуется указать: страницы, книги, иллюстрации, таблицы, источники'
            )
        if has_invalid_volume_separator:
            result.add_error(
                Severity.CRITICAL,
                'Сведения об объеме должны разделяться запятыми и располагаться в одну строку'
            )
        
        # 2. Проверка ключевых слов
        keywords_section, format_check = check_keywords(lines)
        if not keywords_section:
            result.add_error(
                Severity.RECOMMENDATION,
                'Ключевые слова не найдены или неправильно отформатированы'
            )
        else:
            if not format_check["is_uppercase"]:
                result.add_error(
                    Severity.CRITICAL,
                    'Ключевые слова должны быть написаны прописными буквами (капсом)'
                )

            if not format_check["has_commas"]:
                result.add_error(
                    Severity.CRITICAL,
                    'Ключевые слова должны разделяться запятыми'
                )

            if not format_check["no_trailing_period"]:
                result.add_error(
                    Severity.CRITICAL,
                    'Ключевые слова не должны заканчиваться точкой'
                )

            if not format_check["no_line_breaks"]:
                result.add_error(
                    Severity.CRITICAL,
                    'Ключевые слова должны располагаться в одну строку без переносов'
                )
        
        # 3. Проверка текста реферата (рекомендации)
        missing_keywords = check_abstract_text(abstract_text)
        if missing_keywords:
            missing_labels = {
                "goal": "цель",
                "object": "объект",
                "recommendations": "рекомендации"
            }
            missing_text = ", ".join(missing_labels.get(k, k) for k in missing_keywords)
            result.add_error(
                Severity.RECOMMENDATION,
                f'Рекомендуется уточнить в тексте реферата: {missing_text}'
            )
        
        # 4. Проверка объема реферата
        char_count = check_abstract_size(abstract_text)
        if char_count < self.MIN_ABSTRACT_SIZE:
            result.add_error(
                Severity.RECOMMENDATION,
                f'Рекомендуется расширить реферат. '
                f'Текущий объем: {char_count} символов, '
                f'рекомендуемый минимум: {self.MIN_ABSTRACT_SIZE} символов'
            )
        
        return result
