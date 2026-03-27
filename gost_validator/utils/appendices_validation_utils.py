"""Содержательные проверки для валидатора раздела "ПРИЛОЖЕНИЯ"."""

from re import Pattern

from .common.section_utils import check_is_sequential


def extract_label(header: str, appendix_header_re: Pattern[str]) -> str | None:
    """Извлекает обозначение приложения из заголовка."""
    match = appendix_header_re.match(header.strip())
    if not match:
        return None
    return match.group(1).upper()


def is_valid_label(
    label: str,
    invalid_cyrillic_labels: set[str],
    invalid_latin_labels: set[str],
) -> bool:
    """Проверяет соответствие обозначения приложения допустимому формату."""
    if label.isdigit():
        return True

    if len(label) != 1:
        return False

    if "А" <= label <= "Я":
        return label not in invalid_cyrillic_labels

    if "A" <= label <= "Z":
        return label not in invalid_latin_labels

    return False


def check_designation_sequence(
    appendix_entries: list[tuple[str, str, str]],
    invalid_cyrillic_labels: set[str],
    invalid_latin_labels: set[str],
) -> tuple[bool, bool, bool]:
    """Проверяет последовательность обозначений приложений."""
    labels = [label for label, _, _ in appendix_entries]
    if len(labels) < 2:
        return False, False, False

    digits_non_sequential = False
    cyrillic_non_sequential = False
    latin_non_sequential = False

    def _check_letter_sequence(
        alphabet: str,
        invalid_labels: set[str],
    ) -> bool:
        order = [char for char in alphabet if char not in invalid_labels]
        indexes = [order.index(label) for label in labels if label in order]
        return len(indexes) == len(labels) and not check_is_sequential(indexes)

    if all(label.isdigit() for label in labels):
        numbers = [int(label) for label in labels]
        digits_non_sequential = not check_is_sequential(numbers)
        return digits_non_sequential, cyrillic_non_sequential, latin_non_sequential

    if all(len(label) == 1 and "А" <= label <= "Я" for label in labels):
        cyrillic_non_sequential = _check_letter_sequence(
            alphabet="АБВГДЕЖИКЛМНПРСТУФХЦШЩЭЮЯ",
            invalid_labels=invalid_cyrillic_labels,
        )
        return digits_non_sequential, cyrillic_non_sequential, latin_non_sequential

    if all(len(label) == 1 and "A" <= label <= "Z" for label in labels):
        latin_non_sequential = _check_letter_sequence(
            alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            invalid_labels=invalid_latin_labels,
        )
    return digits_non_sequential, cyrillic_non_sequential, latin_non_sequential


def check_contents_mentions(
    contents_text: str | None,
    appendix_entries: list[tuple[str, str, str]],
    appendix_keyword: str,
) -> list[tuple[str, bool, bool]]:
    """Проверяет, что приложения и их названия указаны в содержании."""
    if not contents_text:
        return []

    facts: list[tuple[str, bool, bool]] = []

    contents_upper = contents_text.upper()
    for label, title, _ in appendix_entries:
        appendix_marker = f"{appendix_keyword} {label}".upper()
        has_appendix_marker = appendix_marker in contents_upper
        if not has_appendix_marker:
            facts.append((label, False, False))
            continue

        normalized_title = title.upper()
        has_title = not normalized_title or normalized_title in contents_upper
        facts.append((label, True, has_title))
    return facts
