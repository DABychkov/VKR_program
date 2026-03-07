"""Валидатор реферата по ГОСТ 7.32-2017."""

import re

from ..models.document_structure import DocumentStructure
from ..models.validation_result import ValidationResult, Severity
from ..utils.abstract_utils import (
    extract_volume_metrics,
    find_keywords_section,
    check_keywords_format,
    find_text_keywords_in_abstract,
    count_abstract_characters
)
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
        abstract_text = document.sections.get("РЕФЕРАТ")
        
        if not abstract_text:
            result.add_error(
                Severity.CRITICAL,
                'Структурный элемент "РЕФЕРАТ" не найден'
            )
            return result
        
        # Разбиваем реферат на строки
        lines = abstract_text.split('\n')
        
        # 1. Проверка сведений об объеме
        self._check_volume_info(lines, result)
        
        # 2. Проверка ключевых слов
        self._check_keywords(lines, result)
        
        # 3. Проверка текста реферата (рекомендации)
        self._check_abstract_text(abstract_text, result)
        
        # 4. Проверка объема реферата
        self._check_abstract_size(abstract_text, result)
        
        return result
    
    def _check_volume_info(self, lines: list[str], result: ValidationResult):
        """Проверка сведений об объеме отчета в первых строках реферата."""
        # Метрики должны быть в первых нескольких строках (обычно в одной)
        first_part = '\n'.join(lines[:5])
        metrics = extract_volume_metrics(first_part)
        
        # Проверяем что найдены основные метрики
        required_metrics = ["pages", "books", "illustrations", "tables", "sources"]
        found_metrics = [k for k, v in metrics.items() if v is not None and k in required_metrics]
        
        if len(found_metrics) < 3:
            result.add_error(
                Severity.CRITICAL,
                f'Неполна информация об объеме отчета. Найдено: {found_metrics}. '
                'Требуется указать: страницы, книги, иллюстрации, таблицы, источники'
            )
        
        # Проверяем формат: должны разделяться запятыми, в одну строку
        volume_line = first_part.strip()
        if found_metrics and ',' not in volume_line:
            result.add_error(
                Severity.CRITICAL,
                'Сведения об объеме должны разделяться запятыми и располагаться в одну строку'
            )
    
    def _check_keywords(self, lines: list[str], result: ValidationResult):
        """Проверка формата и наличия ключевых слов."""
        keywords_section = find_keywords_section(lines)
        
        if not keywords_section:
            result.add_error(
                Severity.RECOMMENDATION,
                'Ключевые слова не найдены или неправильно отформатированы'
            )
            return
        
        # Проверяем формат ключевых слов
        format_check = check_keywords_format(keywords_section)
        
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
    
    def _check_abstract_text(self, abstract_text: str, result: ValidationResult):
        """Проверка текста реферата на наличие ключевых фраз (рекомендация)."""
        keywords = find_text_keywords_in_abstract(abstract_text)
        
        missing_keywords = [k for k, v in keywords.items() if not v]
        
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
    
    def _check_abstract_size(self, abstract_text: str, result: ValidationResult):
        """Проверка того что объем реферата достаточный (>= 850 символов)."""
        char_count = count_abstract_characters(abstract_text)
        
        if char_count < self.MIN_ABSTRACT_SIZE:
            result.add_error(
                Severity.RECOMMENDATION,
                f'Рекомендуется расширить реферат. '
                f'Текущий объем: {char_count} символов, '
                f'рекомендуемый минимум: {self.MIN_ABSTRACT_SIZE} символов'
            )
