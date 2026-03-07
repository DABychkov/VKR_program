"""Вспомогательные функции для валидации реферата."""

import re


def extract_volume_metrics(text: str) -> dict[str, int | None]:
    """
    Извлекает метрики объема (страницы, книги, иллюстрации и т.д.) из текста.
    
    Возвращает словарь вида:
    {"pages": 150, "books": 2, "illustrations": 5, "tables": 3, "sources": 10, "appendices": 2}
    """
    metrics = {
        "pages": None,
        "books": None,
        "illustrations": None,
        "tables": None,
        "sources": None,
        "appendices": None
    }
    
    # Паттерны ищем числа перед ключевыми словами
    patterns = {
        "pages": r"(\d+)\s*(?:страниц|страница|сстр|с\.)",
        "books": r"(\d+)\s*(?:книг|книги|кн\.|от книг)",
        "illustrations": r"(\d+)\s*(?:иллюстрац|рисунк|рис\.|фиг|фиг\.)",
        "tables": r"(\d+)\s*(?:табли|таблиц|табл|табл\.)",
        "sources": r"(\d+)\s*(?:источник|использ\s+источник|ист\.|исчисл)",
        "appendices": r"(\d+)\s*(?:прилож|приложен|прил\.|приложён)"
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metrics[key] = int(match.group(1))
    
    return metrics


def find_keywords_section(paragraphs: list[str]) -> str | None:
    """
    Ищет секцию ключевых слов в реферате.
    
    Ключевые слова обычно идут отдельным абзацем после информации об объеме.
    Они написаны капсом, через запятые, без точки в конце.
    """
    for i, para in enumerate(paragraphs):
        # Ищем строку почти целиком капсом, содержащую запятые
        stripped = para.strip()
        if not stripped:
            continue
        
        # Ключевые слова: почти все капсом, много запятых
        uppercase_count = sum(1 for c in stripped if c.isupper())
        letter_count = sum(1 for c in stripped if c.isalpha())
        comma_count = stripped.count(',')
        
        # Если >70% текста капсом, есть запятые и текст разумной длины
        if letter_count > 0 and (uppercase_count / letter_count) > 0.7 and comma_count >= 2:
            # Проверяем что это не название или нумерация
            if not re.match(r'^\d+\.?\s+', stripped):
                return stripped
    
    return None


def check_keywords_format(keywords_text: str) -> dict[str, bool]:
    """
    Проверяет формат ключевых слов по требованиям ГОСТ.
    
    Возвращает словарь с результатами проверок.
    """
    results = {
        "is_uppercase": True,
        "has_commas": True,
        "no_trailing_period": True,
        "no_line_breaks": True
    }
    
    if not keywords_text:
        return {k: False for k in results.keys()}
    
    # 1. Проверка что капсом
    # Исключаем цифры и спецсимволы, смотрим только буквы
    letters = [c for c in keywords_text if c.isalpha()]
    if letters:
        uppercase_letters = [c for c in letters if c.isupper()]
        results["is_uppercase"] = len(uppercase_letters) / len(letters) > 0.8
    
    # 2. Проверка запятых (разделение)
    results["has_commas"] = ',' in keywords_text
    
    # 3. Проверка отсутствия точки в конце
    results["no_trailing_period"] = not keywords_text.strip().endswith('.')
    
    # 4. Проверка отсутствия переносов строк
    results["no_line_breaks"] = '\n' not in keywords_text
    
    return results


def find_text_keywords_in_abstract(text: str) -> dict[str, bool]:
    """
    Ищет ключевые фразы в тексте реферата.
    
    Возвращает словарь с наличием ключевых фраз.
    """
    keywords = {
        "goal": False,      # "цель"
        "object": False,    # "объект"
        "recommendations": False  # "рекомендац"
    }
    
    text_lower = text.lower()
    
    if re.search(r'\bцель', text_lower):
        keywords["goal"] = True
    
    if re.search(r'\bобъект', text_lower):
        keywords["object"] = True
    
    if re.search(r'\bрекомендац', text_lower):
        keywords["recommendations"] = True
    
    return keywords


def count_abstract_characters(abstract_text: str) -> int:
    """
    Считает печатные знаки в реферате (буквы, цифры, пунктуация).
    
    Исключает только пробелы и переносы строк.
    """
    # Убираем только пробелы и переносы строк
    clean_text = abstract_text.replace(' ', '').replace('\n', '').replace('\t', '')
    return len(clean_text)
