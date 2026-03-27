"""Вспомогательные функции для валидации реферата."""

from ..config.regex_patterns import (
    RE_ABSTRACT_METRICS,
    RE_NUMBERED_PREFIX_GENERIC,
    RE_WORD_GOAL,
    RE_WORD_OBJECT,
    RE_WORD_RECOMMEND,
)
from ..models.validation_result import Severity, ValidationResult
from .common.regex_utils import extract_int_by_pattern
from .common.text_utils import count_non_whitespace_characters


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
    
    for key, pattern in RE_ABSTRACT_METRICS.items():
        metrics[key] = extract_int_by_pattern(text, pattern, group=1)
    
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
            if not RE_NUMBERED_PREFIX_GENERIC.match(stripped):
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
    
    if RE_WORD_GOAL.search(text_lower):
        keywords["goal"] = True
    
    if RE_WORD_OBJECT.search(text_lower):
        keywords["object"] = True
    
    if RE_WORD_RECOMMEND.search(text_lower):
        keywords["recommendations"] = True
    
    return keywords


def check_volume_info(lines: list[str], result: ValidationResult) -> None:
    """Проверка сведений об объеме отчета в первых строках реферата."""
    first_part = '\n'.join(lines[:5])
    metrics = extract_volume_metrics(first_part)

    required_metrics = ["pages", "books", "illustrations", "tables", "sources"]
    found_metrics = [k for k, v in metrics.items() if v is not None and k in required_metrics]

    if len(found_metrics) < 3:
        result.add_error(
            Severity.CRITICAL,
            f'Неполна информация об объеме отчета. Найдено: {found_metrics}. '
            'Требуется указать: страницы, книги, иллюстрации, таблицы, источники'
        )

    volume_line = first_part.strip()
    if found_metrics and ',' not in volume_line:
        result.add_error(
            Severity.CRITICAL,
            'Сведения об объеме должны разделяться запятыми и располагаться в одну строку'
        )


def check_keywords(lines: list[str], result: ValidationResult) -> None:
    """Проверка формата и наличия ключевых слов."""
    keywords_section = find_keywords_section(lines)

    if not keywords_section:
        result.add_error(
            Severity.RECOMMENDATION,
            'Ключевые слова не найдены или неправильно отформатированы'
        )
        return

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


def check_abstract_text(abstract_text: str, result: ValidationResult) -> None:
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


def check_abstract_size(abstract_text: str, result: ValidationResult, min_abstract_size: int) -> None:
    """Проверка того, что объем реферата достаточный."""
    char_count = count_non_whitespace_characters(abstract_text)

    if char_count < min_abstract_size:
        result.add_error(
            Severity.RECOMMENDATION,
            f'Рекомендуется расширить реферат. '
            f'Текущий объем: {char_count} символов, '
            f'рекомендуемый минимум: {min_abstract_size} символов'
        )
