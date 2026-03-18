"""Содержательные проверки для валидатора раздела "ПРИЛОЖЕНИЯ"."""

from re import Pattern

from ..models.validation_result import Severity, ValidationResult
from .section_utils import check_is_sequential


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
    result: ValidationResult,
    invalid_cyrillic_labels: set[str],
    invalid_latin_labels: set[str],
) -> None:
    """Проверяет последовательность обозначений приложений."""
    labels = [label for label, _, _ in appendix_entries]
    if len(labels) < 2:
        return

    if all(label.isdigit() for label in labels):
        numbers = [int(label) for label in labels]
        if not check_is_sequential(numbers):
            result.add_error(
                Severity.RECOMMENDATION,
                'Обозначения приложений в виде цифр идут не последовательно. '
                'Рекомендуется проверить порядок приложений.',
            )
        return

    if all(len(label) == 1 and "А" <= label <= "Я" for label in labels):
        order = [char for char in "АБВГДЕЖИКЛМНПРСТУФХЦШЩЭЮЯ" if char not in invalid_cyrillic_labels]
        indexes = [order.index(label) for label in labels if label in order]
        if len(indexes) == len(labels) and not check_is_sequential(indexes):
            result.add_error(
                Severity.RECOMMENDATION,
                'Кириллические обозначения приложений идут не по порядку. '
                'Рекомендуется проверить последовательность приложений.',
            )
        return

    if all(len(label) == 1 and "A" <= label <= "Z" for label in labels):
        order = [char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if char not in invalid_latin_labels]
        indexes = [order.index(label) for label in labels if label in order]
        if len(indexes) == len(labels) and not check_is_sequential(indexes):
            result.add_error(
                Severity.RECOMMENDATION,
                'Латинские обозначения приложений идут не по порядку. '
                'Рекомендуется проверить последовательность приложений.',
            )


def check_contents_mentions(
    contents_text: str | None,
    appendix_entries: list[tuple[str, str, str]],
    result: ValidationResult,
    appendix_keyword: str,
) -> None:
    """Проверяет, что приложения и их названия указаны в содержании."""
    if not contents_text:
        return

    contents_upper = contents_text.upper()
    for label, title, _ in appendix_entries:
        appendix_marker = f"{appendix_keyword} {label}".upper()
        if appendix_marker not in contents_upper:
            result.add_error(
                Severity.RECOMMENDATION,
                f'Приложение "{label}" не найдено в содержании. '
                'Если содержание оформлено, рекомендуется перечислить в нем все приложения.',
            )
            continue

        normalized_title = title.upper()
        if normalized_title and normalized_title not in contents_upper:
            result.add_error(
                Severity.RECOMMENDATION,
                f'В содержании найдено обозначение приложения "{label}", но не найдено его название. '
                'Рекомендуется указать в содержании обозначение и наименование приложения.',
            )
