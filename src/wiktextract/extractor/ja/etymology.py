from wikitextprocessor.parser import LevelNode, NodeKind

from ...page import clean_node
from ...wxr_context import WiktextractContext
from .models import WordEntry


def extract_etymology_section(
    wxr: WiktextractContext,
    page_data: list[WordEntry],
    base_data: WordEntry,
    level_node: LevelNode,
) -> None:
    etymology_texts = []
    cats = {}
    for list_item in level_node.find_child_recursively(NodeKind.LIST_ITEM):
        text = clean_node(wxr, cats, list_item.children)
        if len(text) > 0:
            etymology_texts.append(text)
    if len(etymology_texts) == 0:
        text = clean_node(wxr, cats, level_node.children)
        if len(text) > 0:
            etymology_texts.append(text)
    base_data.etymology_texts = etymology_texts
    base_data.categories.extend(cats.get("categories", []))
    if level_node.kind != NodeKind.LEVEL3:  # under POS section
        for data in page_data:
            if (
                data.lang_code == base_data.lang_code
                and len(data.etymology_texts) == 0
            ):
                data.etymology_texts = etymology_texts
                data.categories.extend(cats.get("categories", []))
