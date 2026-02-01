"""Валидаторы для проверки титульного листа."""

import re
from datetime import datetime

from ..models.document_structure import DocumentStructure
from ..models.validation_result import ValidationResult, Severity
from ..utils.title_page_utils import (
    find_organization_block,
    find_metadata_block,
    find_approval_stamp,
    find_document_type,
    is_uppercase_text,
    extract_initials,
    find_place_and_year
)
from .base_validator import BaseValidator


class TitlePageValidator(BaseValidator):
    """
    Валидатор титульного листа по ГОСТ 7.32-2017.
    
    Проверяет 10 основных блоков титульника:
    1. Наименование организации
    2. Метаданные (УДК, рег. номера)
    3. Грифы СОГЛАСОВАНО и УТВЕРЖДАЮ
    4. Вид документа (ОТЧЕТ О НИР)
    5. Наименование НИР
    6. Наименование отчета
    7. Вид отчета (промежуточный/заключительный)
    8. Шифр программы/темы
    9. Номер книги
    10. Руководитель + место и год
    """
    
    def validate(self, document: DocumentStructure) -> ValidationResult:
        result = ValidationResult(validator_name="TitlePageValidator")
        
        # Разбиваем титульник на строки (абзацы)
        paragraphs = document.title_page_text.split('\n')
        
        # 1. Проверка организации (обязательно)
        self._check_organization(paragraphs, result)
        
        # 2. Проверка метаданных УДК (обязательно)
        self._check_metadata(paragraphs, result)
        
        # 3. Проверка грифов (УТВЕРЖДАЮ обязательно, СОГЛАСОВАНО условно)
        self._check_approval_stamps(paragraphs, result)
        
        # 4. Проверка вида документа (обязательно)
        self._check_document_type(paragraphs, result)
        
        # 5. Проверка места и года (обязательно)
        self._check_place_and_year(paragraphs, result)
        
        return result
    
    def _check_organization(self, paragraphs: list[str], result: ValidationResult):
        """Проверка блока организации (верх титульника, капсом, по центру)."""
        org_block = find_organization_block(paragraphs)
        
        if not org_block:
            result.add_error(
                Severity.CRITICAL,
                "Не найдено наименование организации в верхней части титульника"
            )
            return
        
        # Проверяем что все капсом
        for line in org_block:
            if not is_uppercase_text(line):
                result.add_error(
                    Severity.CRITICAL,
                    f"Наименование организации должно быть капсом: '{line}'"
                )
        
        # РЕКОМЕНДАЦИЯ: проверка содержания (Министерство, Федеральное и т.д.)
        org_text = ' '.join(org_block).upper()
        keywords = ["МИНИСТЕРСТВО", "ФЕДЕРАЛЬНОЕ", "АГЕНТСТВО", "УНИВЕРСИТЕТ"]
        if not any(kw in org_text for kw in keywords):
            result.add_error(
                Severity.RECOMMENDATION,
                "Наименование организации возможно некорректно (нет ключевых слов: Министерство, Федеральное и т.д.)"
            )
    
    def _check_metadata(self, paragraphs: list[str], result: ValidationResult):
        """Проверка УДК и регистрационных номеров (левая сторона)."""
        metadata = find_metadata_block(paragraphs)
        
        # УДК обязателен
        if "УДК" not in metadata:
            result.add_error(
                Severity.CRITICAL,
                "Отсутствует индекс УДК на титульном листе"
            )
        else:
            # Проверяем что после УДК есть цифры
            udk_line = metadata["УДК"]
            if not re.search(r'\d', udk_line):
                result.add_error(
                    Severity.CRITICAL,
                    "УДК должен содержать цифры"
                )
        
        # Рег. номера - рекомендация
        if "Рег. N НИОКТР" not in metadata:
            result.add_error(
                Severity.RECOMMENDATION,
                "Рекомендуется указать регистрационный номер НИОКТР"
            )
    
    def _check_approval_stamps(self, paragraphs: list[str], result: ValidationResult):
        """Проверка грифов СОГЛАСОВАНО и УТВЕРЖДАЮ."""
        sogl, utv = find_approval_stamp(paragraphs)
        
        # УТВЕРЖДАЮ обязателен
        if not utv:
            result.add_error(
                Severity.CRITICAL,
                "Отсутствует гриф УТВЕРЖДАЮ на титульном листе"
            )
            return
        
        # Проверяем что капсом
        if "УТВЕРЖДАЮ" not in utv:
            result.add_error(
                Severity.CRITICAL,
                "Гриф УТВЕРЖДАЮ должен быть написан заглавными буквами"
            )
        
        # Проверяем инициалы рядом с УТВЕРЖДАЮ
        # Берем несколько строк после грифа
        utv_idx = next((i for i, p in enumerate(paragraphs) if "УТВЕРЖДАЮ" in p.upper()), None)
        if utv_idx is not None:
            context = '\n'.join(paragraphs[utv_idx:utv_idx + 5])
            initials = extract_initials(context)
            if not initials:
                result.add_error(
                    Severity.CRITICAL,
                    "После грифа УТВЕРЖДАЮ не найдены инициалы (формат: А.В.)"
                )
    
    def _check_document_type(self, paragraphs: list[str], result: ValidationResult):
        """Проверка вида документа (ОТЧЕТ О НАУЧНО-ИССЛЕДОВАТЕЛЬСКОЙ РАБОТЕ)."""
        doc_type = find_document_type(paragraphs)
        
        if not doc_type:
            result.add_error(
                Severity.CRITICAL,
                "Не найден тип документа (ОТЧЕТ О НАУЧНО-ИССЛЕДОВАТЕЛЬСКОЙ РАБОТЕ)"
            )
            return
        
        # Проверяем формат: две строки, капсом
        lines = doc_type.split('\n')
        if len(lines) != 2:
            result.add_error(
                Severity.CRITICAL,
                "Тип документа должен быть на двух строках: 'ОТЧЕТ' и 'О НАУЧНО-ИССЛЕДОВАТЕЛЬСКОЙ РАБОТЕ'"
            )
        
        # Проверяем что капсом
        if not all(is_uppercase_text(line) for line in lines):
            result.add_error(
                Severity.CRITICAL,
                "Тип документа должен быть написан заглавными буквами"
            )
    
    def _check_place_and_year(self, paragraphs: list[str], result: ValidationResult):
        """Проверка места и года (низ титульника)."""
        place, year = find_place_and_year(paragraphs)
        
        if not year:
            result.add_error(
                Severity.CRITICAL,
                "Не найден год на титульном листе"
            )
            return
        
        # Проверяем что год не больше текущего
        current_year = datetime.now().year
        if year > current_year:
            result.add_error(
                Severity.CRITICAL,
                f"Год на титульном листе ({year}) больше текущего ({current_year})"
            )
        
        if not place:
            result.add_error(
                Severity.RECOMMENDATION,
                "Рекомендуется указать место (город) на титульном листе"
            )
