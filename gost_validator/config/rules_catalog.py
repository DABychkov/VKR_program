"""Каталог правил по умолчанию для заполнения rule_results."""

from __future__ import annotations

from ..models.rule_result import RuleResult
from ..models.validation_result import Severity


RULES_CATALOG_BY_VALIDATOR: dict[str, list[RuleResult]] = {
    "TitlePageValidator": [
        RuleResult("TITLE-001", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден блок организации с заглавными буквами", Severity.CRITICAL.value),
        RuleResult("TITLE-002", "ТИТУЛЬНЫЙ_ЛИСТ", "Наименование организации найдено по ключевым словам", Severity.RECOMMENDATION.value),
        RuleResult("TITLE-003", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден УДК", Severity.CRITICAL.value),
        RuleResult("TITLE-004", "ТИТУЛЬНЫЙ_ЛИСТ", "В строке УДК есть цифры", Severity.CRITICAL.value),
        RuleResult("TITLE-005", "ТИТУЛЬНЫЙ_ЛИСТ", "Указан регистрационный номер НИОКТР", Severity.RECOMMENDATION.value),
        RuleResult("TITLE-006", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден гриф УТВЕРЖДАЮ", Severity.CRITICAL.value),
        RuleResult("TITLE-007", "ТИТУЛЬНЫЙ_ЛИСТ", "После грифа УТВЕРЖДАЮ найдены инициалы", Severity.CRITICAL.value),
        RuleResult("TITLE-008", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден вид документа ОТЧЕТ О НИР", Severity.CRITICAL.value),
        RuleResult("TITLE-009", "ТИТУЛЬНЫЙ_ЛИСТ", "ОТЧЕТ О НИР написан в двух строках", Severity.CRITICAL.value),
        RuleResult("TITLE-010", "ТИТУЛЬНЫЙ_ЛИСТ", "ОТЧЕТ О НИР написан заглавными буквами", Severity.CRITICAL.value),
        RuleResult("TITLE-011", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден год", Severity.CRITICAL.value),
        RuleResult("TITLE-012", "ТИТУЛЬНЫЙ_ЛИСТ", "Год <= текущего", Severity.CRITICAL.value),
        RuleResult("TITLE-013", "ТИТУЛЬНЫЙ_ЛИСТ", "Найдено место составления", Severity.RECOMMENDATION.value),
    ],
    "ExecutorListValidator": [
        RuleResult("EXEC-001", "СПИСОК_ИСПОЛНИТЕЛЕЙ", "Есть секция \"СПИСОК ИСПОЛНИТЕЛЕЙ\" или исполнитель на титуле", Severity.CRITICAL.value),
        RuleResult("EXEC-002", "СПИСОК_ИСПОЛНИТЕЛЕЙ", "Испольнитель на титульнике с инициалами", Severity.RECOMMENDATION.value),
        RuleResult("EXEC-003", "СПИСОК_ИСПОЛНИТЕЛЕЙ", "В секции есть роль \"Исполнители\"", Severity.CRITICAL.value),
        RuleResult("EXEC-004", "СПИСОК_ИСПОЛНИТЕЛЕЙ", "Найдены инициалы в формате А.В.", Severity.CRITICAL.value),
        RuleResult("EXEC-005", "СПИСОК_ИСПОЛНИТЕЛЕЙ", "Список испольниетлей 1 можно разместить на титульнике", Severity.RECOMMENDATION.value),
        RuleResult("EXEC-006", "СПИСОК_ИСПОЛНИТЕЛЕЙ", "Есть \"Отв. исполнитель\"", Severity.RECOMMENDATION.value),
    ],
    "AbstractValidator": [
        RuleResult("ABSTRACT-001", "РЕФЕРАТ", "Раздел РЕФЕРАТ найден", Severity.CRITICAL.value),
        RuleResult("ABSTRACT-002", "РЕФЕРАТ", "Найдены метрики объема (страницы/книги/рис/табл/источники), минимум 3", Severity.CRITICAL.value),
        RuleResult("ABSTRACT-003", "РЕФЕРАТ", "Метрики разделены запятыми", Severity.CRITICAL.value),
        RuleResult("ABSTRACT-004", "РЕФЕРАТ", "Ключевые слова найдены", Severity.RECOMMENDATION.value),
        RuleResult("ABSTRACT-005", "РЕФЕРАТ", "Ключевые слова капсом", Severity.RECOMMENDATION.value),
        RuleResult("ABSTRACT-006", "РЕФЕРАТ", "Ключевые слова через запятые", Severity.RECOMMENDATION.value),
        RuleResult("ABSTRACT-007", "РЕФЕРАТ", "Ключевые слова без точки в конце", Severity.CRITICAL.value),
        RuleResult("ABSTRACT-008", "РЕФЕРАТ", "Ключевые слова без переносов", Severity.RECOMMENDATION.value),
        RuleResult("ABSTRACT-009", "РЕФЕРАТ", "В тексте есть цель/объект/рекомендации", Severity.RECOMMENDATION.value),
        RuleResult("ABSTRACT-010", "РЕФЕРАТ", "Объем реферата >= порога", Severity.RECOMMENDATION.value),
    ],
    "ContentsValidator": [
        RuleResult("CONTENTS-001", "СОДЕРЖАНИЕ", "Раздел СОДЕРЖАНИЕ найден", Severity.RECOMMENDATION.value),
        RuleResult("CONTENTS-002", "СОДЕРЖАНИЕ", "Раздел СОДЕРЖАНИЕ не пустой", Severity.CRITICAL.value),
        RuleResult("CONTENTS-003", "СОДЕРЖАНИЕ", "Строки содержания распознаны с номерами страниц", Severity.CRITICAL.value),
        RuleResult("CONTENTS-004", "СОДЕРЖАНИЕ", "Есть обязательные пункты НИР", Severity.CRITICAL.value),
        RuleResult("CONTENTS-005", "СОДЕРЖАНИЕ", "Порядок страниц ВВЕДЕНИЕ < ЗАКЛЮЧЕНИЕ", Severity.RECOMMENDATION.value),
        RuleResult("CONTENTS-006", "СОДЕРЖАНИЕ", "Порядок страниц ЗАКЛЮЧЕНИЕ < ИСТОЧНИКИ", Severity.RECOMMENDATION.value),
        RuleResult("CONTENTS-007", "СОДЕРЖАНИЕ", "Номера страниц > 0", Severity.CRITICAL.value),
        RuleResult("CONTENTS-008", "СОДЕРЖАНИЕ", "Есть визуальный разделитель (точки/таб/широкий пробел)", Severity.RECOMMENDATION.value),
    ],
    "TermsValidator": [
        RuleResult("TERMS-001", "ТЕРМИНЫ_И_ОПРЕДЕЛЕНИЯ", "Раздел ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ найден", Severity.RECOMMENDATION.value),
        RuleResult("TERMS-002", "ТЕРМИНЫ_И_ОПРЕДЕЛЕНИЯ", "Вводная фраза близка к ГОСТ", Severity.CRITICAL.value),
        RuleResult("TERMS-003", "ТЕРМИНЫ_И_ОПРЕДЕЛЕНИЯ", "Есть элементы ТЕРМИН — ОПРЕДЕЛЕНИЕ", Severity.CRITICAL.value),
        RuleResult("TERMS-004", "ТЕРМИНЫ_И_ОПРЕДЕЛЕНИЯ", "Нет левого отступа у левой колонки", Severity.CRITICAL.value),
        RuleResult("TERMS-005", "ТЕРМИНЫ_И_ОПРЕДЕЛЕНИЯ", "Термин и определение без знаков в конце", Severity.CRITICAL.value),
        RuleResult("TERMS-006", "ТЕРМИНЫ_И_ОПРЕДЕЛЕНИЯ", "Алфавитный порядок", Severity.CRITICAL.value),
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
            status="SKIP",
            message=None,
            gost_ref="0",
            implemented=rule.implemented,
        )
        for rule in defaults
    ]
