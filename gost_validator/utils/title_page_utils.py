"""Вспомогательные функции для работы с титульным листом."""

from datetime import datetime

from ..config.regex_patterns import RE_INITIALS, RE_YEAR_1900_2099
from ..models.validation_result import Severity, ValidationResult
from .common.regex_utils import extract_int_by_pattern
from .common.section_utils import find_first_index_contains, text_contains_any
from .common.text_utils import is_uppercase_text


def find_organization_block(paragraphs: list[str], start_idx: int = 0, end_idx: int = 15) -> list[str]:
    """
    Ищет блок с наименованием организации (верхняя часть титульника).
    
    Блок должен быть в верхних строках (0-15) и состоять из текста капсом.
    Пропускаем начальные не-капс строки (министерство может быть не капсом).
    """
    org_block = []
    found_caps = False
    
    for para in paragraphs[start_idx:end_idx]:
        # Пропускаем пустые
        if not para.strip():
            continue
        
        # Если капсом
        if para.strip().isupper():
            org_block.append(para.strip())
            found_caps = True
        else:
            # Если уже нашли капс-блок, то не-капс означает конец блока
            if found_caps:
                break
            # Иначе продолжаем искать (может быть министерство не капсом вначале)
    
    return org_block


def find_metadata_block(paragraphs: list[str]) -> dict[str, str]:
    """
    Ищет блок с УДК, регистрационными номерами (левая сторона титульника).
    
    Возвращает словарь: {"УДК": "...", "Рег. N НИОКТР": "...", ...}
    """
    metadata = {}
    for para in paragraphs[:30]:  # Первые 30 строк титульника
        if "УДК" in para.upper():
            metadata["УДК"] = para.strip()
        elif "РЕГ" in para.upper() and "НИОКТР" in para.upper():
            metadata["Рег. N НИОКТР"] = para.strip()
        elif "РЕГ" in para.upper() and "ИКРБС" in para.upper():
            metadata["Рег. N ИКРБС"] = para.strip()
    return metadata


def find_approval_stamp(paragraphs: list[str]) -> tuple[str | None, str | None]:
    """
    Ищет грифы СОГЛАСОВАНО и УТВЕРЖДАЮ.
    
    Возвращает кортеж: (согласовано_текст, утверждаю_текст)
    """
    sogl = None
    utv = None
    
    for para in paragraphs[:30]:
        if "СОГЛАСОВАНО" in para.upper():
            sogl = para.strip()
        if "УТВЕРЖДАЮ" in para.upper():
            utv = para.strip()
    
    return sogl, utv


def find_document_type(paragraphs: list[str]) -> str | None:
    """
    Ищет тип документа (ОТЧЕТ О НАУЧНО-ИССЛЕДОВАТЕЛЬСКОЙ РАБОТЕ).
    
    Должно быть капсом, две строки: "ОТЧЕТ" и "О НАУЧНО-ИССЛЕДОВАТЕЛЬСКОЙ РАБОТЕ".
    """
    for i, para in enumerate(paragraphs[:30]):
        if "ОТЧЕТ" in para.upper() and i + 1 < len(paragraphs):
            next_para = paragraphs[i + 1]
            if "НАУЧНО-ИССЛЕДОВАТЕЛЬСКОЙ" in next_para.upper():
                return f"{para.strip()}\n{next_para.strip()}"
    return None


def extract_initials(text: str) -> list[str]:
    """
    Извлекает инициалы из текста (например, 'А.В. Иванов' → ['А.В.']).
    
    Паттерн: заглавная буква + точка + заглавная буква + точка
    """
    return RE_INITIALS.findall(text)


def find_place_and_year(paragraphs: list[str]) -> tuple[str | None, int | None]:
    """
    Ищет место и год на титульнике.
    
    Формат: "Москва 2026" или "Москва, 2026" или просто "2026"
    Ищет снизу вверх по всем строкам титульника.
    Возвращает: (место, год)
    """
    # Ищем год во всех абзацах снизу вверх
    for para in reversed(paragraphs):
        if not para.strip():
            continue
        
        # Ищем год (4 цифры, начинается с 19 или 20)
        year = extract_int_by_pattern(para, RE_YEAR_1900_2099, group=1)
        if year is not None:
            # Место = все что до года
            place = RE_YEAR_1900_2099.sub('', para).strip(' ,')
            return place if place else None, year
    
    return None, None


def check_organization(paragraphs: list[str], result: ValidationResult) -> None:
    """Проверка блока организации (верх титульника, капсом, по центру)."""
    org_block = find_organization_block(paragraphs)

    if not org_block:
        result.add_error(
            Severity.CRITICAL,
            "Не найдено наименование организации в верхней части титульника"
        )
        return

    for line in org_block:
        if not is_uppercase_text(line):
            result.add_error(
                Severity.CRITICAL,
                f"Наименование организации должно быть капсом: '{line}'"
            )

    org_text = ' '.join(org_block).upper()
    keywords = ["МИНИСТЕРСТВО", "ФЕДЕРАЛЬНОЕ", "АГЕНТСТВО", "УНИВЕРСИТЕТ"]
    if not text_contains_any(org_text, keywords, case_sensitive=True):
        result.add_error(
            Severity.RECOMMENDATION,
            "Наименование организации возможно некорректно (нет ключевых слов: Министерство, Федеральное и т.д.)"
        )


def check_metadata(paragraphs: list[str], result: ValidationResult, has_digit_pattern) -> None:
    """Проверка УДК и регистрационных номеров (левая сторона)."""
    metadata = find_metadata_block(paragraphs)

    if "УДК" not in metadata:
        result.add_error(
            Severity.CRITICAL,
            "Отсутствует индекс УДК на титульном листе"
        )
    else:
        udk_line = metadata["УДК"]
        if not has_digit_pattern.search(udk_line):
            result.add_error(
                Severity.CRITICAL,
                "УДК должен содержать цифры"
            )

    if "Рег. N НИОКТР" not in metadata:
        result.add_error(
            Severity.RECOMMENDATION,
            "Рекомендуется указать регистрационный номер НИОКТР"
        )


def check_approval_stamps(paragraphs: list[str], result: ValidationResult) -> None:
    """Проверка грифов СОГЛАСОВАНО и УТВЕРЖДАЮ."""
    _, utv = find_approval_stamp(paragraphs)

    if not utv:
        result.add_error(
            Severity.CRITICAL,
            "Отсутствует гриф УТВЕРЖДАЮ на титульном листе"
        )
        return

    if "УТВЕРЖДАЮ" not in utv:
        result.add_error(
            Severity.CRITICAL,
            "Гриф УТВЕРЖДАЮ должен быть написан заглавными буквами"
        )

    utv_idx = find_first_index_contains(paragraphs, "УТВЕРЖДАЮ")
    if utv_idx is not None:
        context = '\n'.join(paragraphs[utv_idx:utv_idx + 5])
        initials = extract_initials(context)
        if not initials:
            result.add_error(
                Severity.CRITICAL,
                "После грифа УТВЕРЖДАЮ не найдены инициалы (формат: А.В.)"
            )


def check_document_type(paragraphs: list[str], result: ValidationResult) -> None:
    """Проверка вида документа (ОТЧЕТ О НАУЧНО-ИССЛЕДОВАТЕЛЬСКОЙ РАБОТЕ)."""
    doc_type = find_document_type(paragraphs)

    if not doc_type:
        result.add_error(
            Severity.CRITICAL,
            "Не найден тип документа (ОТЧЕТ О НАУЧНО-ИССЛЕДОВАТЕЛЬСКОЙ РАБОТЕ)"
        )
        return

    lines = doc_type.split('\n')
    if len(lines) != 2:
        result.add_error(
            Severity.CRITICAL,
            "Тип документа должен быть на двух строках: 'ОТЧЕТ' и 'О НАУЧНО-ИССЛЕДОВАТЕЛЬСКОЙ РАБОТЕ'"
        )

    if not all(is_uppercase_text(line) for line in lines):
        result.add_error(
            Severity.CRITICAL,
            "Тип документа должен быть написан заглавными буквами"
        )


def check_place_and_year(paragraphs: list[str], result: ValidationResult) -> None:
    """Проверка места и года (низ титульника)."""
    place, year = find_place_and_year(paragraphs)

    if not year:
        result.add_error(
            Severity.CRITICAL,
            "Не найден год на титульном листе"
        )
        return

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
