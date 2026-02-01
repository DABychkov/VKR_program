"""Модель структуры документа."""

from dataclasses import dataclass, field


@dataclass
class DocumentStructure:
    filename: str
    title_page_text: str  # Первые ~30 абзацев (титульник)
    sections: dict[str, str] = field(default_factory=dict)  # {"РЕФЕРАТ": "текст...", "ВВЕДЕНИЕ": "текст..."}
    all_paragraphs: list[str] = field(default_factory=list)  # Все абзацы документа
