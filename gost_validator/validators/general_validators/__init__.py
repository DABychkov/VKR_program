"""Валидаторы общих форматно-стилевых требований."""

from .figure_validator import FigureValidator
from .general_requirements_validator import GeneralRequirementsValidator

__all__ = [
    "GeneralRequirementsValidator",
    "FigureValidator",
]
