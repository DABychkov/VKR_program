"""Валидаторы общих форматно-стилевых требований."""

from .figure_validator import FigureValidator
from .formula_validator import FormulaValidator
from .general_requirements_validator import GeneralRequirementsValidator
from .links_validator import LinksValidator
from .table_validator import TableValidator

__all__ = [
    "GeneralRequirementsValidator",
    "FigureValidator",
    "TableValidator",
    "FormulaValidator",
    "LinksValidator",
]
