"""Вспомогательные функции для работы с титульным листом."""

import re


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
    pattern = r'[А-ЯA-Z]\.[А-ЯA-Z]\.'
    return re.findall(pattern, text)


def is_uppercase_text(text: str) -> bool:
    """
    Проверяет, что текст написан заглавными буквами (капсом).
    
    Игнорирует цифры, пробелы и знаки препинания.
    """
    # Убираем не-буквы
    letters_only = ''.join(c for c in text if c.isalpha())
    if not letters_only:
        return False
    return letters_only.isupper()


def check_centered_alignment(para_obj) -> bool:
    """
    Проверяет, что абзац выровнен по центру.
    
    Работает с объектом Paragraph из python-docx.
    """
    # Если у абзаца есть alignment и он WD_ALIGN_PARAGRAPH.CENTER
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    return para_obj.alignment == WD_ALIGN_PARAGRAPH.CENTER


def find_place_and_year(paragraphs: list[str]) -> tuple[str | None, int | None]:
    """
    Ищет место и год в нижней части титульника (последние 5 строк).
    
    Формат: "Москва 2026" или "Москва, 2026"
    Возвращает: (место, год)
    """
    # Проверяем последние 5 абзацев
    for para in reversed(paragraphs[-5:]):
        # Ищем год (4 цифры)
        year_match = re.search(r'\b(20\d{2})\b', para)
        if year_match:
            year = int(year_match.group(1))
            # Место = все что до года
            place = re.sub(r'\b20\d{2}\b', '', para).strip(' ,')
            return place, year
    
    return None, None
