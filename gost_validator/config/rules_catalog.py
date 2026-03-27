"""Каталог правил по умолчанию для заполнения rule_results."""

from __future__ import annotations

from ..models.rule_result import RuleResult
from ..models.validation_result import Severity


RULES_CATALOG_BY_VALIDATOR: dict[str, list[RuleResult]] = {
    "TitlePageValidator": [
        RuleResult("TITLE-001", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден блок организации", Severity.CRITICAL.value),
        RuleResult("TITLE-002", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден УДК", Severity.CRITICAL.value),
        RuleResult("TITLE-003", "ТИТУЛЬНЫЙ_ЛИСТ", "В строке УДК есть цифры", Severity.CRITICAL.value),
        RuleResult("TITLE-004", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден гриф УТВЕРЖДАЮ", Severity.CRITICAL.value),
        RuleResult("TITLE-005", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден вид документа ОТЧЕТ О НИР", Severity.CRITICAL.value),
        RuleResult("TITLE-006", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден год", Severity.CRITICAL.value),
        RuleResult("TITLE-007", "ТИТУЛЬНЫЙ_ЛИСТ", "Год не больше текущего", Severity.CRITICAL.value),
        RuleResult("TITLE-008", "ТИТУЛЬНЫЙ_ЛИСТ", "Найдено место составления", Severity.RECOMMENDATION.value),
    ],
    "AbstractValidator": [
        RuleResult("ABSTRACT-001", "РЕФЕРАТ", "Раздел РЕФЕРАТ найден", Severity.CRITICAL.value),
        RuleResult(
            "ABSTRACT-002",
            "РЕФЕРАТ",
            "Найдены метрики объема (страницы, книги, рисунки, таблицы, источники)",
            Severity.CRITICAL.value,
        ),
        RuleResult("ABSTRACT-003", "РЕФЕРАТ", "Метрики объема разделены запятыми", Severity.CRITICAL.value),
        RuleResult("ABSTRACT-004", "РЕФЕРАТ", "Ключевые слова найдены", Severity.RECOMMENDATION.value),
        RuleResult("ABSTRACT-005", "РЕФЕРАТ", "Ключевые слова набраны капсом", Severity.CRITICAL.value),
        RuleResult("ABSTRACT-006", "РЕФЕРАТ", "Ключевые слова разделены запятыми", Severity.CRITICAL.value),
        RuleResult("ABSTRACT-007", "РЕФЕРАТ", "Ключевые слова без точки в конце", Severity.CRITICAL.value),
        RuleResult("ABSTRACT-008", "РЕФЕРАТ", "Ключевые слова без переносов", Severity.CRITICAL.value),
        RuleResult("ABSTRACT-009", "РЕФЕРАТ", "В тексте есть цель/объект/рекомендации", Severity.RECOMMENDATION.value),
        RuleResult("ABSTRACT-010", "РЕФЕРАТ", "Объем реферата не ниже минимального порога", Severity.RECOMMENDATION.value),
    ],
    "ContentsValidator": [
        RuleResult("CONTENTS-001", "СОДЕРЖАНИЕ", "Раздел СОДЕРЖАНИЕ найден", Severity.RECOMMENDATION.value),
        RuleResult("CONTENTS-002", "СОДЕРЖАНИЕ", "Раздел СОДЕРЖАНИЕ не пустой", Severity.CRITICAL.value),
        RuleResult("CONTENTS-003", "СОДЕРЖАНИЕ", "Строки содержания распознаны с номерами страниц", Severity.CRITICAL.value),
        RuleResult(
            "CONTENTS-004",
            "СОДЕРЖАНИЕ",
            "Есть обязательные пункты: введение, заключение, список источников, приложения",
            Severity.CRITICAL.value,
        ),
        RuleResult("CONTENTS-005", "СОДЕРЖАНИЕ", "Логический порядок страниц обязательных пунктов", Severity.RECOMMENDATION.value),
        RuleResult("CONTENTS-006", "СОДЕРЖАНИЕ", "Номера страниц положительные", Severity.CRITICAL.value),
        RuleResult("CONTENTS-007", "СОДЕРЖАНИЕ", "Есть визуальный разделитель названия и номера страницы", Severity.RECOMMENDATION.value),
    ],
}


def build_default_rule_results(validator_name: str) -> list[RuleResult]:
    """Возвращает копию rule_results по каталогу для указанного валидатора."""
    defaults = RULES_CATALOG_BY_VALIDATOR.get(validator_name, [])
    return [
        RuleResult(
            rule_id=rule.rule_id,
            section=rule.section,
            description=rule.description,
            severity=rule.severity,
            status="OK",
            message=None,
            gost_ref="0",
            implemented=rule.implemented,
        )
        for rule in defaults
    ]
