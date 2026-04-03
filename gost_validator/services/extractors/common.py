"""Общие helper-функции для extractor-модулей."""

from __future__ import annotations

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Length

from ...models.rich_document_structure import AlignmentValue, RunFeature


def clean_text(text: str | None) -> str:
    """Нормализует строку: убирает лишние пробелы и переносы."""
    return " ".join((text or "").split())


def alignment_to_value(alignment: WD_ALIGN_PARAGRAPH | int | None) -> AlignmentValue:
    """Нормализует выравнивание Word в наш enum-строковый формат."""
    if alignment is None:
        return "unknown"

    mapping: dict[int, AlignmentValue] = {
        int(WD_ALIGN_PARAGRAPH.LEFT): "left",
        int(WD_ALIGN_PARAGRAPH.CENTER): "center",
        int(WD_ALIGN_PARAGRAPH.RIGHT): "right",
        int(WD_ALIGN_PARAGRAPH.JUSTIFY): "justify",
        int(WD_ALIGN_PARAGRAPH.DISTRIBUTE): "distribute",
    }
    return mapping.get(int(alignment), "unknown")


def to_mm(value: Length | None) -> float | None:
    """Переводит длину из внутренних единиц Word в миллиметры."""
    if value is None:
        return None
    return float(value.mm)


def to_pt(value: Length | None) -> float | None:
    """Переводит длину из внутренних единиц Word в пункты (pt)."""
    if value is None:
        return None
    return float(value.pt)


def safe_style_name(run_or_paragraph: object) -> str | None:
    """Возвращает имя стиля, если оно задано на объекте."""
    style = getattr(run_or_paragraph, "style", None)
    if style is None:
        return None
    return getattr(style, "name", None)


def run_color_rgb(run: object) -> str | None:
    """Возвращает RGB-цвет run, если он задан явно."""
    font = getattr(run, "font", None)
    if font is None or font.color is None or font.color.rgb is None:
        return None
    return str(font.color.rgb)


def _resolve_run_font_name(run: object) -> str | None:
    """Определяет effective font name c учетом run/символьного стиля/стиля абзаца."""
    direct_font_name = getattr(getattr(run, "font", None), "name", None)
    if direct_font_name:
        return direct_font_name

    run_style = getattr(run, "style", None)
    if run_style is not None:
        run_style_font_name = getattr(getattr(run_style, "font", None), "name", None)
        if run_style_font_name:
            return run_style_font_name

    paragraph = getattr(run, "_parent", None)
    paragraph_style = getattr(paragraph, "style", None)
    checked_styles = 0
    while paragraph_style is not None and checked_styles < 10:
        paragraph_style_font_name = getattr(getattr(paragraph_style, "font", None), "name", None)
        if paragraph_style_font_name:
            return paragraph_style_font_name
        paragraph_style = getattr(paragraph_style, "base_style", None)
        checked_styles += 1

    return None


def _resolve_run_font_size_pt(run: object) -> float | None:
    """Определяет effective font size c учетом run/символьного стиля/стиля абзаца."""
    direct_size = getattr(getattr(run, "font", None), "size", None)
    if direct_size is not None:
        return float(direct_size.pt)

    run_style = getattr(run, "style", None)
    if run_style is not None:
        run_style_size = getattr(getattr(run_style, "font", None), "size", None)
        if run_style_size is not None:
            return float(run_style_size.pt)

    paragraph = getattr(run, "_parent", None)
    paragraph_style = getattr(paragraph, "style", None)
    checked_styles = 0
    while paragraph_style is not None and checked_styles < 10:
        paragraph_style_size = getattr(getattr(paragraph_style, "font", None), "size", None)
        if paragraph_style_size is not None:
            return float(paragraph_style_size.pt)
        paragraph_style = getattr(paragraph_style, "base_style", None)
        checked_styles += 1

    return None


def extract_run_feature(run: object) -> RunFeature:
    """Нормализует python-docx run в RunFeature."""
    return RunFeature(
        text=run.text,
        font_name=_resolve_run_font_name(run),
        font_size_pt=_resolve_run_font_size_pt(run),
        bold=run.bold,
        italic=run.italic,
        underline=bool(run.underline) if run.underline is not None else None,
        all_caps=run.font.all_caps,
        color_rgb=run_color_rgb(run),
        style_name=safe_style_name(run),
    )


def _alignment_from_xml(paragraph: object) -> AlignmentValue | None:
    """Читает w:pPr/w:jc напрямую из XML абзаца, если доступно."""
    p = getattr(paragraph, "_p", None)
    if p is None:
        return None

    ppr = p.find(qn("w:pPr"))
    if ppr is None:
        return None

    jc = ppr.find(qn("w:jc"))
    if jc is None:
        return None

    val = (jc.get(qn("w:val")) or "").lower()
    xml_map: dict[str, AlignmentValue] = {
        "left": "left",
        "center": "center",
        "right": "right",
        "both": "justify",
        "justify": "justify",
        "distribute": "distribute",
    }
    return xml_map.get(val)


def resolve_paragraph_alignment(paragraph: object, default_left: bool = True) -> AlignmentValue:
    """Определяет эффективное выравнивание абзаца с учетом наследования стиля."""
    direct_alignment = getattr(paragraph, "alignment", None)
    if direct_alignment is not None:
        return alignment_to_value(direct_alignment)

    paragraph_format = getattr(paragraph, "paragraph_format", None)
    if paragraph_format is not None:
        paragraph_format_alignment = getattr(paragraph_format, "alignment", None)
        if paragraph_format_alignment is not None:
            return alignment_to_value(paragraph_format_alignment)

    style = getattr(paragraph, "style", None)
    checked_styles = 0
    while style is not None and checked_styles < 10:
        style_p_format = getattr(style, "paragraph_format", None)
        if style_p_format is not None:
            style_alignment = getattr(style_p_format, "alignment", None)
            if style_alignment is not None:
                return alignment_to_value(style_alignment)
        style = getattr(style, "base_style", None)
        checked_styles += 1

    xml_alignment = _alignment_from_xml(paragraph)
    if xml_alignment is not None:
        return xml_alignment

    return "left" if default_left else "unknown"
