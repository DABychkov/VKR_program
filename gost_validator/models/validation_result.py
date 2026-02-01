"""Результат валидации с уровнем серьезности."""

from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    """Уровень серьезности ошибки."""
    CRITICAL = "CRITICAL"  # Обязательное по ГОСТ
    RECOMMENDATION = "RECOMMENDATION"  # Рекомендация


@dataclass
class ValidationResult:
    """Результат валидации документа."""
    validator_name: str
    is_valid: bool = True
    errors: list[tuple[Severity, str]] = field(default_factory=list)
    
    def add_error(self, severity: Severity, message: str):
        """Добавить ошибку."""
        self.errors.append((severity, message))
        if severity == Severity.CRITICAL:
            self.is_valid = False
    
    def has_errors(self) -> bool:
        """Есть ли ошибки."""
        return len(self.errors) > 0
