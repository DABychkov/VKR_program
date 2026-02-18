"""Точка входа: валидация документов по ГОСТ 7.32-2017."""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from gost_validator.services.document_parser import DocumentParser
from gost_validator.services.validation_service import ValidationService
from gost_validator.validators.title_page_validators import TitlePageValidator
from gost_validator.validators.executor_list_validator import ExecutorListValidator
from gost_validator.models.validation_result import Severity


def validate_document(file_path: str) -> None:
    """Валидирует документ по ГОСТ 7.32-2017."""
    parser = DocumentParser()
    doc = parser.parse(file_path)

    # Показываем найденные секции
    print(f"\nФайл: {doc.filename}")
    print(f"Найдено секций: {len(doc.sections)}")
    if doc.sections:
        print("  Секции документа:", ", ".join(doc.sections.keys()))

    # Регистрируем валидаторы
    service = ValidationService()
    service.register(TitlePageValidator())
    service.register(ExecutorListValidator())

    # Запускаем проверку
    results = service.validate(doc)

    # Выводим результаты
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ ВАЛИДАЦИИ")
    print("="*60)
    
    for res in results:
        # Если ошибок нет - не выводим
        if not res.has_errors():
            print(f"\n{res.validator_name}: ВСЕ OK")
            continue
        
        # Иначе выводим ошибки по категориям
        print(f"\n{res.validator_name}:")
        
        # Критические ошибки
        critical = [err for err in res.errors if err[0] == Severity.CRITICAL]
        if critical:
            print("\n  КРИТИЧЕСКИЕ ОШИБКИ (обязательно по ГОСТ):")
            for _, msg in critical:
                print(f"     - {msg}")
        
        # Рекомендации
        recommendations = [err for err in res.errors if err[0] == Severity.RECOMMENDATION]
        if recommendations:
            print("\n  РЕКОМЕНДАЦИИ (желательно исправить):")
            for _, msg in recommendations:
                print(f"     - {msg}")


def main():
    """Интерактивный режим валидации."""
    print("=" * 60)
    print("ВАЛИДАТОР ГОСТ 7.32-2017")
    print("Проверка титульного листа и структуры документа")
    print("=" * 60)
    print("\nВведите путь к .docx файлу или 'exit' для выхода")
    
    while True:
        path = input("\n> ").strip()
        
        if path.lower() in {"exit", "quit", "выход"}:
            print("Завершение работы")
            break
        
        if not path:
            continue
        
        if not os.path.exists(path):
            print("Файл не найден")
            continue
        
        try:
            validate_document(path)
        except Exception as exc:
            print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()
