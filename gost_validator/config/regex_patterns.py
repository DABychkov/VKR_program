"""Единый набор регулярных выражений проекта."""

import re


# Общие паттерны
RE_HAS_DIGIT = re.compile(r"\d")
RE_INITIALS = re.compile(r"[А-ЯA-Z]\.[А-ЯA-Z]\.")
RE_SURNAME_WITH_INITIALS = re.compile(
    r"[А-ЯA-Z][а-яa-z]*\s+[А-ЯA-Z]\.[А-ЯA-Z]\.",
    re.UNICODE,
)
RE_YEAR_1900_2099 = re.compile(r"\b(19\d{2}|20\d{2})\b")

# Нумерованные строки/списки
RE_NUMBERED_LIST_ITEM_LINE = re.compile(r"^\d{1,3}\.?\s+\S")
RE_NUMBERED_ITEM_PREFIX = re.compile(r"^(\d{1,3})\.?\s")
RE_NUMBERED_PREFIX_GENERIC = re.compile(r"^\d+\.?\s+")

# Оглавление/страницы
RE_TOC_ITEM_WITH_PAGE = re.compile(
    r"^(?P<title>.+?)\s*(?:\.{2,}\s*)?(?P<page>\d+)\s*$"
)
RE_DOT_LEADER = re.compile(r"\.{2,}")
RE_WIDE_SPACE_PAGE_SUFFIX = re.compile(r"\s{2,}\d+\s*$")
RE_LINE_ENDS_WITH_DIGITS = re.compile(r"\d+\s*$")
RE_NON_DIGIT_BEFORE_PAGE = re.compile(r"\D\s*\d+\s*$")

# Приложения
RE_APPENDIX_HEADER = re.compile(
    r"^ПРИЛОЖЕНИЕ\s+([А-ЯA-Z0-9]+)\s*$",
    re.IGNORECASE,
)

# Титульник/исполнители
RE_EXECUTOR_ON_TITLE = re.compile(r"[Ии]сполнитель[:\s]+.*?[А-ЯA-Z]\.[А-ЯA-Z]\.", re.DOTALL)

# Реферат
RE_ABSTRACT_METRICS = {
    "pages": re.compile(r"(\d+)\s*(?:страниц|страница|сстр|с\.)", re.IGNORECASE),
    "books": re.compile(r"(\d+)\s*(?:книг|книги|кн\.|от книг)", re.IGNORECASE),
    "illustrations": re.compile(r"(\d+)\s*(?:иллюстрац|рисунк|рис\.|фиг|фиг\.)", re.IGNORECASE),
    "tables": re.compile(r"(\d+)\s*(?:табли|таблиц|табл|табл\.)", re.IGNORECASE),
    "sources": re.compile(r"(\d+)\s*(?:источник|использ\s+источник|ист\.|исчисл)", re.IGNORECASE),
    "appendices": re.compile(r"(\d+)\s*(?:прилож|приложен|прил\.|приложён)", re.IGNORECASE),
}
RE_WORD_GOAL = re.compile(r"\bцель")
RE_WORD_OBJECT = re.compile(r"\bобъект")
RE_WORD_RECOMMEND = re.compile(r"\bрекомендац")

# Термины/сокращения
DEFINITION_DASHES = "-–—"
RE_DEFINITION_ITEM_DASH = re.compile(
    rf"^(?P<left>.+?)\s*[{DEFINITION_DASHES}]\s*(?P<right>.+)$"
)
RE_DEFINITION_ITEM_COLON = re.compile(r"^(?P<left>.+?)\s*:\s*(?P<right>.+)$")
RE_LEFT_INDENTATION = re.compile(r"^\s+")

# Основная часть (начало)
RE_MAIN_SECTION_START_PATTERNS = (
    re.compile(r"^\d+\s+[А-ЯA-Z]", re.IGNORECASE),
    re.compile(r"^\d+\.\s+[А-ЯA-Z]", re.IGNORECASE),
    re.compile(r"^Глава\s+\d+", re.IGNORECASE),
    re.compile(r"^ГЛАВА\s+\d+", re.IGNORECASE),
)
