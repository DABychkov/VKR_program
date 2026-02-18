"""Валидатор списка исполнителей по ГОСТ 7.32-2017."""

import re

from ..models.document_structure import DocumentStructure
from ..models.validation_result import ValidationResult, Severity
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
        section_text = self._find_executor_section(document.sections)
        
        if not section_text:
            # Если секции нет, проверяем титульник
            self._check_title_page_executor(document.title_page_text, result)
        else:
            # Если секция есть, валидируем её
            self._check_executor_section(section_text, result)
        
        return result
    
    def _find_executor_section(self, sections: dict[str, str]) -> str | None:
        """Ищет секцию списка исполнителей (с вариациями названия)."""
        keywords = [
            "СПИСОК ИСПОЛНИТЕЛЕЙ",
            "СПИСОК ИСПОЛЬНИТЕЛЕЙ",  # Частая опечатка
            "ИСПОЛНИТЕЛИ"
        ]
        
        for key in sections.keys():
            key_upper = key.upper()
            if any(kw in key_upper for kw in keywords):
                return sections[key]
        
        return None
    
    def _check_title_page_executor(self, title_page: str, result: ValidationResult):
        """Проверяет наличие исполнителя на титульнике (если список отсутствует)."""
        # Если секции "СПИСОК ИСПОЛНИТЕЛЕЙ" нет, значит исполнителей <=2
        # По ТЗ: должна быть фраза "Исполнитель:" на титульнике
        
        if "исполнитель" not in title_page.lower():
            result.add_error(
                Severity.RECOMMENDATION,
                'Не найдена секция "СПИСОК ИСПОЛНИТЕЛЕЙ" и нет фразы "Исполнитель:" на титульнике. '
                'Если исполнителей >2, добавьте структурный элемент "СПИСОК ИСПОЛНИТЕЛЕЙ"'
            )
            return
        
        # Проверяем формат: должны быть инициалы после "Исполнитель"
        executor_pattern = r'[Ии]сполнитель[:\s]+.*?[А-ЯA-Z]\.[А-ЯA-Z]\.'
        if not re.search(executor_pattern, title_page, re.DOTALL):
            result.add_error(
                Severity.RECOMMENDATION,
                'Исполнитель на титульнике найден, но инициалы не распознаны (формат: А.В.)'
            )
    
    def _check_executor_section(self, section_text: str, result: ValidationResult):
        """Проверяет структуру и содержание секции СПИСОК ИСПОЛНИТЕЛЕЙ."""
        lines = section_text.split('\n')
        
        # 1. Проверяем наличие обязательной роли "Исполнители:"
        if not any('исполнител' in line.lower() for line in lines):
            result.add_error(
                Severity.CRITICAL,
                'В списке исполнителей отсутствует роль "Исполнители:"'
            )
        
        # 2. Проверяем формат: слева текст (должность), справа инициалы
        # Считаем сколько строк содержат инициалы
        initials_count = 0
        for line in lines:
            if re.search(r'[А-ЯA-Z]\.[А-ЯA-Z]\.', line):
                initials_count += 1
        
        if initials_count == 0:
            result.add_error(
                Severity.CRITICAL,
                'В списке исполнителей не найдены инициалы (формат: А.В.)'
            )
        elif initials_count < 2:
            result.add_error(
                Severity.RECOMMENDATION,
                f'В списке исполнителей найден только {initials_count} человек. '
                'Если исполнителей <=2, список можно разместить на титульнике'
            )
        
        # 3. Проверяем наличие условных ролей (не критично, но рекомендуется)
        roles = {
            "Отв. Исполнитель": any('отв' in line.lower() and 'исполнител' in line.lower() for line in lines),
            "Соисполнители": any('соисполнител' in line.lower() for line in lines)
        }
        
        if not roles["Отв. Исполнитель"]:
            result.add_error(
                Severity.RECOMMENDATION,
                'Рекомендуется указать ответственного исполнителя ("Отв. Исполнитель")'
            )
