# VKR_program - GOST Document Validator

Программа для автоматизированной проверки документов научно-исследовательских работ на соответствие требованиям **ГОСТ 7.32-2017** (межгосударственный стандарт).

## Описание

GOST Document Validator - Python приложение для валидации научных отчетов, ВКР и НИР в соответствии с российскими стандартами оформления документов. Программа проверяет:

- **Титульный лист** - структура, реквизиты, грифы согласования
- **Объем и структура** - наличие всех обязательных разделов
- **Реферат** - объем, ключевые слова, содержание
- **Содержание** - нумерация, номера страниц
- **Термины и определения** - оформление, алфавитный порядок
- **Сокращения и обозначения** - структура, формат
- **Общие требования** - форматирование, шрифты, интервалы

## Функциональность

 Парсинг DOCX документов  
 Валидация структуры по ГОСТ 7.32-2017  
 Проверка титульного листа  
 Анализ реферата и ключевых слов  
 Верификация содержания  
 Детальный отчет об ошибках и рекомендациях  

## Структура проекта

```
gost_validator/
├── config/
│   ├── __init__.py
│   └── settings.py              # Конфигурация и константы
├── models/
│   ├── __init__.py
│   ├── document_structure.py     # Модели структуры документа
│   └── validation_result.py      # Модель результатов валидации
├── services/
│   ├── __init__.py
│   ├── document_parser.py        # Парсинг DOCX файлов
│   └── validation_service.py     # Основная логика валидации
├── utils/
│   ├── __init__.py
│   ├── text_utils.py             # Утилиты для работы с текстом
│   └── title_page_utils.py       # Утилиты для титульного листа
├── validators/
│   ├── __init__.py
│   ├── base_validator.py         # Базовый класс валидатора
│   └── title_page_validators.py  # Валидаторы титульного листа
├── main.py                       # Точка входа приложения
└── requirements.txt
```

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/DABychkov/VKR_program.git
cd VKR_program
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

## Использование

```bash
python gost_validator/main.py <path_to_document.docx>
```

### Пример вывода:
```
Validation Report
================
Document: report.docx
Status:  WARNINGS FOUND

Title Page Validation:
   Organization name found
   Approval signatures present
   UDC index format issue
   Registration number missing

Abstract Validation:
   Keywords present
   Abstract length < 850 characters (recommended)

Content Validation:
   Table of contents present
   Introduction found
   Conclusion found
```

## Требования

- Python 3.8+
- python-docx>=0.8.11

## Автор

**DABychkov**  
МАИ

## Лицензия

MIT
