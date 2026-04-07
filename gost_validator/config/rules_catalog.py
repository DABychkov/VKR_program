"""Каталог правил по умолчанию для заполнения rule_results."""

from __future__ import annotations

from ..models.rule_result import RuleResult
from ..models.validation_result import Severity


RULES_CATALOG_BY_VALIDATOR: dict[str, list[RuleResult]] = {
    "TitlePageValidator": [
        RuleResult("TITLE-001", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден блок организации с заглавными буквами", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.10.1"),
        RuleResult("TITLE-002", "ТИТУЛЬНЫЙ_ЛИСТ", "Наименование организации найдено по ключевым словам", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.1.2"),
        RuleResult("TITLE-003", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден УДК", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.10.1"),
        RuleResult("TITLE-004", "ТИТУЛЬНЫЙ_ЛИСТ", "В строке УДК есть цифры", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.10.1"),
        RuleResult("TITLE-005", "ТИТУЛЬНЫЙ_ЛИСТ", "Указан регистрационный номер НИОКТР", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.1.2"),
        RuleResult("TITLE-006", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден гриф УТВЕРЖДАЮ", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.10.1;"),
        RuleResult("TITLE-007", "ТИТУЛЬНЫЙ_ЛИСТ", "После грифа УТВЕРЖДАЮ найдены инициалы", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.10.1"),
        RuleResult("TITLE-008", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден вид документа ОТЧЕТ О НИР", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 5.1.2"),
        RuleResult("TITLE-009", "ТИТУЛЬНЫЙ_ЛИСТ", "ОТЧЕТ О НИР написан в двух строках", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.10.1"),
        RuleResult("TITLE-010", "ТИТУЛЬНЫЙ_ЛИСТ", "ОТЧЕТ О НИР написан заглавными буквами", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.10.1"),
        RuleResult("TITLE-011", "ТИТУЛЬНЫЙ_ЛИСТ", "Найден год", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.10.1"),
        RuleResult("TITLE-012", "ТИТУЛЬНЫЙ_ЛИСТ", "Год <= текущего", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.10.1"),
        RuleResult("TITLE-013", "ТИТУЛЬНЫЙ_ЛИСТ", "Найдено место составления", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 6.10.1"),
    ],
    "ExecutorListValidator": [
        RuleResult("EXEC-001", "СПИСОК_ИСПОЛНИТЕЛЕЙ", "Есть секция \"СПИСОК ИСПОЛНИТЕЛЕЙ\" или исполнитель на титуле", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, п. 5.2"),
        RuleResult("EXEC-002", "СПИСОК_ИСПОЛНИТЕЛЕЙ", "Испольнитель на титульнике с инициалами", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.2.2"),
        RuleResult("EXEC-003", "СПИСОК_ИСПОЛНИТЕЛЕЙ", "В секции есть роль \"Исполнители\"", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 5.2.1"),
        RuleResult("EXEC-004", "СПИСОК_ИСПОЛНИТЕЛЕЙ", "Найдены инициалы в формате А.В.", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, п. 6.11"),
        RuleResult("EXEC-005", "СПИСОК_ИСПОЛНИТЕЛЕЙ", "Список испольниетлей 1 можно разместить на титульнике", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.2.2"),
        RuleResult("EXEC-006", "СПИСОК_ИСПОЛНИТЕЛЕЙ", "Есть \"Отв. исполнитель\"", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.2.1"),
    ],
    "AbstractValidator": [
        RuleResult("ABSTRACT-001", "РЕФЕРАТ", "Раздел РЕФЕРАТ найден", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, п. 5.3"),
        RuleResult("ABSTRACT-002", "РЕФЕРАТ", "Найдены метрики объема (страницы/книги/рис/табл/источники), минимум 3", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп.5.3.2"),
        RuleResult("ABSTRACT-003", "РЕФЕРАТ", "Метрики разделены запятыми", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.12.1"),
        RuleResult("ABSTRACT-004", "РЕФЕРАТ", "Ключевые слова найдены", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.3.2.1"),
        RuleResult("ABSTRACT-005", "РЕФЕРАТ", "Ключевые слова капсом", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 6.12.2"),
        RuleResult("ABSTRACT-006", "РЕФЕРАТ", "Ключевые слова через запятые", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 6.12.2"),
        RuleResult("ABSTRACT-007", "РЕФЕРАТ", "Ключевые слова без точки в конце", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.12.2"),
        RuleResult("ABSTRACT-008", "РЕФЕРАТ", "Ключевые слова без переносов", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 6.12.2"),
        RuleResult("ABSTRACT-009", "РЕФЕРАТ", "В тексте есть цель/объект/рекомендации", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.3.2.2 "),
        RuleResult("ABSTRACT-010", "РЕФЕРАТ", "Объем реферата >= порога", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.3.2.2 "),
    ],
    "ContentsValidator": [
        RuleResult("CONTENTS-001", "СОДЕРЖАНИЕ", "Раздел СОДЕРЖАНИЕ найден", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.4.3"),
        RuleResult("CONTENTS-002", "СОДЕРЖАНИЕ", "Раздел СОДЕРЖАНИЕ не пустой", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 5.4.1"),
        RuleResult("CONTENTS-003", "СОДЕРЖАНИЕ", "Строки содержания распознаны с номерами страниц", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 5.4.1"),
        RuleResult("CONTENTS-004", "СОДЕРЖАНИЕ", "Есть обязательные пункты НИР", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 5.4.1"),
        RuleResult("CONTENTS-005", "СОДЕРЖАНИЕ", "Порядок страниц ВВЕДЕНИЕ < ЗАКЛЮЧЕНИЕ", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.4.1"),
        RuleResult("CONTENTS-006", "СОДЕРЖАНИЕ", "Порядок страниц ЗАКЛЮЧЕНИЕ < ИСТОЧНИКИ", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.4.1"),
        RuleResult("CONTENTS-007", "СОДЕРЖАНИЕ", "Номера страниц > 0", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 5.4.1"),
        RuleResult("CONTENTS-008", "СОДЕРЖАНИЕ", "Есть визуальный разделитель (точки/таб/широкий пробел)", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 6.13"),
    ],
    "TermsValidator": [
        RuleResult("TERMS-001", "ТЕРМИНЫ_И_ОПРЕДЕЛЕНИЯ", "Раздел ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ найден", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.6.2"),
        RuleResult("TERMS-002", "ТЕРМИНЫ_И_ОПРЕДЕЛЕНИЯ", "Вводная фраза близка к ГОСТ", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 5.5.2"),
        RuleResult("TERMS-003", "ТЕРМИНЫ_И_ОПРЕДЕЛЕНИЯ", "Есть элементы ТЕРМИН — ОПРЕДЕЛЕНИЕ", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.14"),
        RuleResult("TERMS-004", "ТЕРМИНЫ_И_ОПРЕДЕЛЕНИЯ", "Нет левого отступа у левой колонки", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.14"),
        RuleResult("TERMS-005", "ТЕРМИНЫ_И_ОПРЕДЕЛЕНИЯ", "Термин и определение без знаков в конце", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.14"),
        RuleResult("TERMS-006", "ТЕРМИНЫ_И_ОПРЕДЕЛЕНИЯ", "Алфавитный порядок", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.14"),
    ],
    "AbbreviationsValidator": [
        RuleResult("ABBR-001", "СОКРАЩЕНИЯ_И_ОБОЗНАЧЕНИЯ", "Раздел СОКРАЩЕНИЯ И ОБОЗНАЧЕНИЯ найден или есть объединенный раздел", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.6.2"),
        RuleResult("ABBR-002", "СОКРАЩЕНИЯ_И_ОБОЗНАЧЕНИЯ", "Вводная фраза близка к ГОСТ", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 5.6.1"),
        RuleResult("ABBR-003", "СОКРАЩЕНИЯ_И_ОБОЗНАЧЕНИЯ", "Есть элементы СОКРАЩЕНИЕ — РАСШИФРОВКА", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.15"),
        RuleResult("ABBR-004", "СОКРАЩЕНИЯ_И_ОБОЗНАЧЕНИЯ", "Нет отступа у левой колонки", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.15"),
        RuleResult("ABBR-005", "СОКРАЩЕНИЯ_И_ОБОЗНАЧЕНИЯ", "Алфавитный порядок", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.15"),
        RuleResult("ABBR-006", "СОКРАЩЕНИЯ_И_ОБОЗНАЧЕНИЯ", "Сокращения и расшифровки без знаков в конце", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.15"),
    ],
    "ReferencesValidator": [
        RuleResult("REFS-001", "СПИСОК_ИСТОЧНИКОВ", "Раздел СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ найден", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 5.10"),
        RuleResult("REFS-002", "СПИСОК_ИСТОЧНИКОВ", "Раздел не пустой", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 5.10.1"),
        RuleResult("REFS-003", "СПИСОК_ИСТОЧНИКОВ", "Первый элемент нумерованный", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.16"),
        RuleResult("REFS-004", "СПИСОК_ИСТОЧНИКОВ", "В разделе есть нумерованные записи", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.16"),
        RuleResult("REFS-005", "СПИСОК_ИСТОЧНИКОВ", "Последовательность нумерации", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 6.16"),
        RuleResult("REFS-006", "СПИСОК_ИСТОЧНИКОВ", "В записях есть инициалы", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.82-2001, подп. 5.3.1.3"),
    ],
    "AppendicesValidator": [
        RuleResult("APPX-001", "ПРИЛОЖЕНИЯ", "Приложения найдены", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 5.11"),
        RuleResult("APPX-003", "ПРИЛОЖЕНИЯ", "Обозначение приложения валидно", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.17.3"),
        RuleResult("APPX-009", "ПРИЛОЖЕНИЯ", "После обозначения есть отдельная строка статуса в скобках", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 6.17.7"),
        RuleResult("APPX-004", "ПРИЛОЖЕНИЯ", "Приложение не пустое", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.17.1"),
        RuleResult("APPX-005", "ПРИЛОЖЕНИЯ", "После заголовка есть отдельное название", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.17.3"),
        RuleResult("APPX-006", "ПРИЛОЖЕНИЯ", "Заголовок приложения без точки в конце", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.17.3"),
        RuleResult("APPX-007", "ПРИЛОЖЕНИЯ", "Последовательность обозначений приложений", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.17.4"),
        RuleResult("APPX-008", "ПРИЛОЖЕНИЯ", "Приложение перечислено в содержании", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.17.7"),
    ],
    "GeneralRequirementsValidator": [
        RuleResult("GENERAL-001", "ОБЩИЕ_ТРЕБОВАНИЯ", "Поля страницы 30/15/20/20 мм", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.1.1"),
        RuleResult("GENERAL-002", "ОБЩИЕ_ТРЕБОВАНИЯ", "Абзацный отступ около 1.25 см", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.1.1"),
        RuleResult("GENERAL-003", "ОБЩИЕ_ТРЕБОВАНИЯ", "Межстрочный интервал соответствует профилю", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.1.1"),
        RuleResult("GENERAL-004", "ОБЩИЕ_ТРЕБОВАНИЯ", "Размер шрифта не ниже минимального порога", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.1.1"),
        RuleResult("GENERAL-005", "ОБЩИЕ_ТРЕБОВАНИЯ", "Доля курсива не превышает порог", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 6.1.1"),
        RuleResult("GENERAL-006", "ОБЩИЕ_ТРЕБОВАНИЯ", "Цвет шрифта преимущественно черный", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.1.1"),
        RuleResult("GENERAL-007", "ОБЩИЕ_ТРЕБОВАНИЯ", "Большая часть текста в Times New Roman", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.1.1"),
        RuleResult("GENERAL-008", "ОБЩИЕ_ТРЕБОВАНИЯ", "Страницы документа пронумерованы", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.3.1"),
        RuleResult("GENERAL-009", "ОБЩИЕ_ТРЕБОВАНИЯ", "Нумерация страниц выполнена по центру", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.3.1"),
    ],
    "FigureValidator": [
        RuleResult("FIG-001", "РИСУНКИ", "Подпись рисунка расположена снизу", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.5.7"),
        RuleResult("FIG-002", "РИСУНКИ", "Подпись рисунка по центру", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.5.7"),
        RuleResult("FIG-003", "РИСУНКИ", "Пояснение (при наличии) в подписи оформлено через тире", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.5.7"),
        RuleResult("FIG-004", "РИСУНКИ", "Подпись рисунка с прописной буквы без точки в конце", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.5.7"),
        RuleResult("FIG-005", "РИСУНКИ", "Подпись рисунка соответствует паттерну: 1 / 1.1 / А.3(если в приложении)", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.5.5, 6.5.6"),
    ],
    "TableValidator": [
        RuleResult("TABLE-001", "ТАБЛИЦЫ", "Подпись таблицы расположена сверху и выровнен влево", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.6.3"),
        RuleResult("TABLE-002", "ТАБЛИЦЫ", "Подпись соответсвует патерну  1 / 1.1 / А.3(если в приложении)", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.6.4"),
        RuleResult("TABLE-003", "ТАБЛИЦЫ", "Наименование таблицы(при его наличии) приводиться через тире", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.6.3"),
        RuleResult("TABLE-004", "ТАБЛИЦЫ", "Наименование таблицы с прописной буквы без точки в конце", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.6.3"),
        RuleResult("TABLE-005", "ТАБЛИЦЫ", "В таблице отсутствуют диагональные линии", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.6.6"),
        RuleResult("TABLE-006", "ТАБЛИЦЫ", "Заголовки граф начинаются с прописной буквы", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.6.5"),
        RuleResult("TABLE-007", "ТАБЛИЦЫ", "Заголовки граф начинаются не заканчивается точкой", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.6.5"),
    ],
    "FormulaValidator": [
        RuleResult("FORMULA-001", "ФОРМУЛЫ", "Формула на отдельной строке и с корректными отбивками", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 6.8.1"),
        RuleResult("FORMULA-002", "ФОРМУЛЫ", "Пояснение с \"где\" оформлено корректно", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 6.8.2"),
        RuleResult("FORMULA-003", "ФОРМУЛЫ", "Справа от формулы есть ее номер", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.8.3"),
        RuleResult("FORMULA-004", "ФОРМУЛЫ", "Формула находиться в центре", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.8.3"),
        RuleResult("FORMULA-005", "ФОРМУЛЫ", "Номер формулы соответсвует шаблонам: (1), (1.2.3), etc.", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.8.3, 6.8.5"),
    ],
    "LinksValidator": [
        RuleResult("LINK-001", "ССЫЛКИ", "Ссылки на рисунки/таблицы/формулы и источники ссылаются на существующие объекты", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 6.5.1, 6.6.2"),
        RuleResult("LINK-002", "ССЫЛКИ", "Ссылка на таблицу идет до таблицы", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.6.2"),
        RuleResult("LINK-003", "ССЫЛКИ", "Ссылка на рисунок расположена до подписи рисунка", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.5.1"),
    ],
    "NotesValidator": [
        RuleResult("NOTE-001", "ПРИМЕЧАНИЯ", "Примечание найдено, но не соответствует шаблону", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.7.3"),
        RuleResult("NOTE-002", "ПРИМЕЧАНИЯ", "Примечание размещено сразу после связанного материала (рисунок/таблица)", Severity.RECOMMENDATION.value, gost_ref="ГОСТ 7.32-2017, подп. 6.7.3"),
        RuleResult("NOTE-003", "ПРИМЕЧАНИЯ", "Примечание оформлено с большой буквы", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.7.2"),
        RuleResult("NOTE-004", "ПРИМЕЧАНИЯ", "Текст примечания начинается с большой буквы", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.7.3"),
        RuleResult("NOTE-005", "ПРИМЕЧАНИЯ", "Если примечаний несколько, пишется \"Примечания\", а не \"Примечание\"", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.7.3"),
        RuleResult("NOTE-006", "ПРИМЕЧАНИЯ", "В примечаниях тире и нумерация используются согласованно", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.7.3"),
        RuleResult("NOTE-007", "ПРИМЕЧАНИЯ", "В нумерованных примечаниях нет точки после номера", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.7.3"),
    ],
    "FootnotesValidator": [
        RuleResult("FOOT-001", "СНОСКИ", "Маркер сноски резолвится", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.7.4"),
        RuleResult("FOOT-002", "СНОСКИ", "При наличии сносок обнаружена разделительная линия перед блоком сносок", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.7.4"),
        RuleResult("FOOT-003", "СНОСКИ", "Разделительная линия короткая", Severity.CRITICAL.value, gost_ref="ГОСТ 7.32-2017, подп. 6.7.4"),
    ],
    #93 правила и 15 валидаторов в сумме
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
            gost_ref=rule.gost_ref,
            implemented=rule.implemented,
        )
        for rule in defaults
    ]

