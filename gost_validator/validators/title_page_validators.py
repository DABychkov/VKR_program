"""Валидаторы для проверки титульного листа."""

from ..models.document_structure import DocumentStructure
from ..models.validation_result import Severity, ValidationResult
from ..config.regex_patterns import RE_HAS_DIGIT
from ..utils.title_page_utils import (
    check_approval_stamps,
    check_document_type,
    check_metadata,
    check_organization,
    check_place_and_year,
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
        org_block, has_org_keywords = check_organization(paragraphs)
        if not org_block:
            result.add_error(
                Severity.CRITICAL,
                "Не найдено наименование организации в верхней части титульника, либо оно не написан заглавными буквами"
            )
        elif not has_org_keywords:
            result.add_error(
                Severity.RECOMMENDATION,
                "Наименование организации возможно некорректно (нет ключевых слов: Министерство, Федеральное и т.д.)"
            )
        
        # 2. Проверка метаданных УДК (обязательно)
        has_udk, udk_has_digits, has_nioktr = check_metadata(paragraphs, RE_HAS_DIGIT)
        if not has_udk:
            result.add_error(
                Severity.CRITICAL,
                "Отсутствует индекс УДК на титульном листе"
            )
        elif not udk_has_digits:
            result.add_error(
                Severity.CRITICAL,
                "УДК должен содержать цифры"
            )

        if not has_nioktr:
            result.add_error(
                Severity.RECOMMENDATION,
                "Рекомендуется указать регистрационный номер НИОКТР"
            )
        
        # 3. Проверка грифов (УТВЕРЖДАЮ обязательно, СОГЛАСОВАНО условно)
        utv, initials_found = check_approval_stamps(paragraphs)
        if not utv:
            result.add_error(
                Severity.CRITICAL,
                "Отсутствует гриф УТВЕРЖДАЮ на титульном листе либо он написан не заглавными буквами"
            )
        elif not initials_found:
            result.add_error(
                Severity.CRITICAL,
                "После грифа УТВЕРЖДАЮ не найдены инициалы (формат: А.В.)"
            )
        
        # 4. Проверка вида документа (обязательно)
        doc_type, has_two_lines, is_uppercase = check_document_type(paragraphs)
        if not doc_type:
            result.add_error(
                Severity.CRITICAL,
                "Не найден тип документа (ОТЧЕТ О НАУЧНО-ИССЛЕДОВАТЕЛЬСКОЙ РАБОТЕ)"
            )
        else:
            if not has_two_lines:
                result.add_error(
                    Severity.CRITICAL,
                    "Тип документа должен быть на двух строках: 'ОТЧЕТ' и 'О НАУЧНО-ИССЛЕДОВАТЕЛЬСКОЙ РАБОТЕ'"
                )

            if not is_uppercase:
                result.add_error(
                    Severity.CRITICAL,
                    "Тип документа должен быть написан заглавными буквами"
                )
        
        # 5. Проверка места и года (обязательно)
        place, year, current_year, is_future_year = check_place_and_year(paragraphs)
        if not year:
            result.add_error(
                Severity.CRITICAL,
                "Не найден год на титульном листе"
            )
        else:
            if is_future_year:
                result.add_error(
                    Severity.CRITICAL,
                    f"Год на титульном листе ({year}) больше текущего ({current_year})"
                )

            if not place:
                result.add_error(
                    Severity.RECOMMENDATION,
                    "Рекомендуется указать место (город) на титульном листе"
                )
        
        return result
