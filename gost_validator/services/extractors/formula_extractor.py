"""Извлечение признаков формул/уравнений.

Текущий файл — скелет. Реализацию добавляем поэтапно.
"""

from docx import Document

from ...models.rich_document_structure import FormulaFeature


def extract_formula_features(doc: Document) -> list[FormulaFeature]:
    """Возвращает признаки формул.

    Этап 2-3:
    - text/regex признаки (номер, где, пустые строки)
    - опционально OMML XML для точной диагностики
    """
    _ = doc
    return []
