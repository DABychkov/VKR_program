"""Валидаторы для проверки титульного листа."""

from ..models.document_structure import DocumentStructure
from ..models.validation_result import ValidationResult
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
        check_organization(paragraphs, result)
        
        # 2. Проверка метаданных УДК (обязательно)
        check_metadata(paragraphs, result, RE_HAS_DIGIT)
        
        # 3. Проверка грифов (УТВЕРЖДАЮ обязательно, СОГЛАСОВАНО условно)
        check_approval_stamps(paragraphs, result)
        
        # 4. Проверка вида документа (обязательно)
        check_document_type(paragraphs, result)
        
        # 5. Проверка места и года (обязательно)
        check_place_and_year(paragraphs, result)
        
        return result
