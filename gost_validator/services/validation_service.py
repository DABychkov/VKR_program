"""Сервис, который запускает валидаторы."""

from typing import List

from ..models.document_structure import DocumentStructure
from ..models.validation_result import ValidationResult
from ..validators.base_validator import BaseValidator


class ValidationService:
    def __init__(self) -> None:
        self.validators: list[BaseValidator] = []

    def register(self, validator: BaseValidator) -> None:
        self.validators.append(validator)

    def validate(self, document: DocumentStructure) -> List[ValidationResult]:
        results: list[ValidationResult] = []
        for validator in self.validators:
            results.append(validator.validate(document))
        return results
