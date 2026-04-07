"""Фасад для получения списка правил и запуска валидации документа."""

from __future__ import annotations

from pathlib import Path

from .config.validation_constants import DEFAULT_TEST_DOCX_PATH
from .config.rules_catalog import RULES_CATALOG_BY_VALIDATOR
from .models.rule_result import RuleResult
from .services.document_parser import DocumentParser
from .services.rich_parser import RichParser
from .services.validation_service import ValidationService
from .validators.abbreviations_validator import AbbreviationsValidator
from .validators.abstract_validator import AbstractValidator
from .validators.appendices_validator import AppendicesValidator
from .validators.contents_validator import ContentsValidator
from .validators.executor_list_validator import ExecutorListValidator
from .validators.general_validators import (
    FigureValidator,
    FootnotesValidator,
    FormulaValidator,
    GeneralRequirementsValidator,
    LinksValidator,
    NotesValidator,
    TableValidator,
)
from .validators.references_validator import ReferencesValidator
from .validators.terms_validator import TermsValidator
from .validators.title_page_validators import TitlePageValidator


class ReportAndListHandler:
    """Упрощенный API для получения каталога правил и проверки DOCX."""

    def __init__(self, *, encoding: bool = True, strict_docx_extension: bool = True) -> None:
        self.encoding = encoding
        self.strict_docx_extension = strict_docx_extension

    def getList(self) -> list[RuleResult]:
        """Возвращает сплошной список правил из rule_catalog без группировки."""
        flat_rules: list[RuleResult] = []
        for rules in RULES_CATALOG_BY_VALIDATOR.values():
            for rule in rules:
                flat_rules.append(
                    RuleResult(
                        rule_id=rule.rule_id,
                        section=rule.section,
                        description=rule.description,
                        severity=rule.severity,
                        status=rule.status,
                        message=rule.message,
                        gost_ref=rule.gost_ref,
                        implemented=rule.implemented,
                    )
                )
        if self.encoding:
            print(f"getList: получено правил={len(flat_rules)}")
        return flat_rules

    def converter_result(self, rules: list[RuleResult]) -> dict[str, list[dict[str, object]]]:
        """Конвертирует list[RuleResult] в JSON-совместимый payload для фронта."""
        return {
            "list": [
                {
                    "rule_id": rule.rule_id,
                    "section": rule.section,
                    "description": rule.description,
                    "severity": rule.severity,
                    "status": rule.status,
                    "message": rule.message,
                    "gost_ref": rule.gost_ref,
                    "implemented": rule.implemented,
                }
                for rule in rules
            ]
        }

    def validate(self, file_path: str) -> list[RuleResult]:
        """Проверяет документ и возвращает общий список правил со статусами и сообщениями."""
        if not file_path.strip():
            if self.encoding:
                print("Путь к файлу пуст")
            return []

        path = Path(file_path)

        if not path.exists():
            if self.encoding:
                print(f"Файл не найден: {path}")
            return []

        if not path.is_file():
            if self.encoding:
                print(f"Это не файл: {path}")
            return []

        if self.strict_docx_extension and path.suffix.lower() != ".docx":
            if self.encoding:
                print(f"Ожидается .docx, получено: {path.suffix or '<без расширения>'}")
            return []

        parser = DocumentParser()
        doc = parser.parse(str(path))
        rich_doc = RichParser().parse(str(path))
        doc.rich_document = rich_doc

        service = self._build_validation_service()
        flat_results = service.validate_rules(doc)

        if self.encoding:
            failed_count = sum(1 for rule in flat_results if rule.status == "FAIL")
            print(f"validate: файл={path.name}, правил={len(flat_results)}, fail={failed_count}")

        return flat_results

    def _build_validation_service(self) -> ValidationService:
        """Собирает ValidationService с тем же составом валидаторов, что и в main."""
        service = ValidationService()
        service.register(TitlePageValidator())
        service.register(ExecutorListValidator())
        service.register(AbstractValidator())
        service.register(ContentsValidator())
        service.register(TermsValidator())
        service.register(AbbreviationsValidator())
        service.register(ReferencesValidator())
        service.register(AppendicesValidator())
        service.register(GeneralRequirementsValidator())
        service.register(FigureValidator())
        service.register(TableValidator())
        service.register(FormulaValidator())
        service.register(LinksValidator())
        service.register(NotesValidator())
        service.register(FootnotesValidator())
        return service


if __name__ == "__main__":
    handler = ReportAndListHandler(encoding=True)

    rules = handler.getList()
    print(handler.converter_result(rules))

    result = handler.validate(DEFAULT_TEST_DOCX_PATH)
    print(handler.converter_result(result))
