"""Точка входа: валидация документов по ГОСТ 7.32-2017."""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from gost_validator.services.document_parser import DocumentParser
from gost_validator.services.rich_parser import RichParser
from gost_validator.services.validation_service import ValidationService
from gost_validator.validators.title_page_validators import TitlePageValidator
from gost_validator.validators.executor_list_validator import ExecutorListValidator
from gost_validator.validators.abstract_validator import AbstractValidator
from gost_validator.validators.contents_validator import ContentsValidator
from gost_validator.validators.terms_validator import TermsValidator
from gost_validator.validators.abbreviations_validator import AbbreviationsValidator
from gost_validator.validators.references_validator import ReferencesValidator
from gost_validator.validators.appendices_validator import AppendicesValidator
from gost_validator.models.validation_result import Severity


def debug_rich_document(file_path: str) -> None:
    """Печатает debug-отчет rich-признаков (этап 1-2)."""
    parser = RichParser()
    rich_doc = parser.parse(file_path)

    print("\n" + "=" * 60)
    print("RICH DEBUG REPORT (ЭТАП 1-2)")
    print("=" * 60)
    print(f"Файл: {rich_doc.source_file}")
    print(f"Секций: {len(rich_doc.pages_settings)}")
    print(f"Абзацев: {len(rich_doc.paragraph_features)}")
    print(f"Футеров: {len(rich_doc.footer_features)}")
    print(f"Таблиц: {len(rich_doc.table_features)}")
    print(f"Подписей рисунков: {len(rich_doc.figure_caption_features)}")
    print(f"Ссылок: {len(rich_doc.links_features)}")

    print("\nПараметры страниц по секциям:")
    for section in rich_doc.pages_settings:
        print(
            "  "
            f"section={section.section_index}, "
            f"start={section.start_type}, "
            f"A={section.page_width_mm}x{section.page_height_mm} мм, "
            f"margins(L/R/T/B)={section.margin_left_mm}/{section.margin_right_mm}/"
            f"{section.margin_top_mm}/{section.margin_bottom_mm} мм"
        )

    print("\nПризнаки пагинации в футерах:")
    for footer in rich_doc.footer_features:
        print(
            "  "
            f"section={footer.section_index}, "
            f"has_PAGE={footer.has_page_field}, "
            f"fmt={footer.page_field_format}, "
            f"align={footer.alignment}, "
            f"restart={footer.restart_numbering}, "
            f"start={footer.start_number}"
        )

    print("\nПервые 100 абзацев:")
    for para in rich_doc.paragraph_features[:100]:
        snippet = para.text.replace("\n", " ").strip()
        if len(snippet) > 70:
            snippet = f"{snippet[:67]}..."
        print(
            "  "
            f"#{para.block_index} align={para.alignment} "
            f"indent(first/left/right)={para.first_line_indent_mm}/{para.left_indent_mm}/{para.right_indent_mm} мм "
            f"line={para.line_spacing} "
            f"bold={para.bold_ratio} italic={para.italic_ratio} "
            f"runs={len(para.runs_features)} text='{snippet}'"
        )

    print("\nПервые 5 таблиц:")
    for table in rich_doc.table_features[:5]:
        title = (table.title_above_text or "")[:60]
        header_runs_count = sum(len(cell.runs_features) for cell in table.header_row_cells)
        first_col_runs_count = sum(len(cell.runs_features) for cell in table.first_column_cells)
        header_text_preview = " | ".join(
            cell.text for cell in table.header_row_cells if cell.text
        )[:80]
        first_col_preview = " | ".join(
            cell.text for cell in table.first_column_cells if cell.text
        )[:80]
        print(
            "  "
            f"table={table.table_index} "
            f"size={table.rows_count}x{table.cols_count} "
            f"title_pattern={table.title_pattern_type} "
            f"inside(H/V)={table.has_inside_horizontal_borders}/{table.has_inside_vertical_borders} "
            f"outer(T/B/L/R)={table.has_outer_top_border}/{table.has_outer_bottom_border}/"
            f"{table.has_outer_left_border}/{table.has_outer_right_border} "
            f"diag={table.has_diagonal_borders} "
            f"header_cells={len(table.header_row_cells)} "
            f"header_runs={header_runs_count} "
            f"first_col_cells={len(table.first_column_cells)} "
            f"first_col_runs={first_col_runs_count} "
            f"title='{title}'"
        )
        if header_text_preview:
            print(f"    header_preview='{header_text_preview}'")
        if first_col_preview:
            print(f"    first_col_preview='{first_col_preview}'")

    print("\nПервые 5 подписей рисунков:")
    for caption in rich_doc.figure_caption_features[:5]:
        text = caption.caption_text[:80]
        print(
            "  "
            f"p={caption.paragraph_index} "
            f"align={caption.alignment} "
            f"dash={caption.has_dash_separator} "
            f"period={caption.ends_with_period} "
            f"text='{text}'"
        )

    print("\nПервые 10 ссылок:")
    for link in rich_doc.links_features[:10]:
        print(
            "  "
            f"type={link.link_type} "
            f"target={link.target_number} "
            f"range={link.is_range} "
            f"raw='{link.raw_text}'"
        )


def validate_document(file_path: str) -> None:
    """Валидирует документ по ГОСТ 7.32-2017."""
    parser = DocumentParser()
    doc = parser.parse(file_path)

    # Показываем найденные секции
    print(f"\nФайл: {doc.filename}")
    print(f"Найдено секций: {len(doc.sections)}")
    if doc.sections:
        print("  Секции документа:", ", ".join(doc.sections.keys()))

    # Регистрируем валидаторы
    service = ValidationService()
    service.register(TitlePageValidator())
    service.register(ExecutorListValidator())
    service.register(AbstractValidator())
    service.register(ContentsValidator())
    service.register(TermsValidator())
    service.register(AbbreviationsValidator())
    service.register(ReferencesValidator())
    service.register(AppendicesValidator())

    # Запускаем проверку
    results = service.validate(doc)

    # Выводим результаты
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ ВАЛИДАЦИИ")
    print("="*60)
    
    for res in results:
        # Если ошибок нет - не выводим
        if not res.has_errors():
            print(f"\n{res.validator_name}: ВСЕ OK")
            continue
        
        # Иначе выводим ошибки по категориям
        print(f"\n{res.validator_name}:")
        
        # Критические ошибки
        critical = [err for err in res.errors if err[0] == Severity.CRITICAL]
        if critical:
            print("\n  КРИТИЧЕСКИЕ ОШИБКИ (обязательно по ГОСТ):")
            for _, msg in critical:
                print(f"     - {msg}")
        
        # Рекомендации
        recommendations = [err for err in res.errors if err[0] == Severity.RECOMMENDATION]
        if recommendations:
            print("\n  РЕКОМЕНДАЦИИ (желательно исправить):")
            for _, msg in recommendations:
                print(f"     - {msg}")


def main():
    """Интерактивный режим валидации."""
    print("=" * 60)
    print("ВАЛИДАТОР ГОСТ 7.32-2017")
    print("Проверка титульного листа и структуры документа")
    print("=" * 60)
    print("\nКоманды:")
    print("  1) <path.docx>          - обычная валидация")
    print("  2) rich <path.docx>     - rich debug (этап 1-2)")
    print("  3) exit                 - выход")
    
    while True:
        path = input("\n> ").strip()
        
        if path.lower() in {"exit", "quit", "выход"}:
            print("Завершение работы")
            break
        
        if not path:
            continue

        is_rich_mode = False
        target_path = path
        if path.lower().startswith("rich "):
            is_rich_mode = True
            target_path = path[5:].strip()

        if not target_path:
            print("Укажите путь к файлу после команды")
            continue
        
        if not os.path.exists(target_path):
            print("Файл не найден")
            continue
        
        try:
            if is_rich_mode:
                debug_rich_document(target_path)
            else:
                validate_document(target_path)
        except Exception as exc:
            print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()
