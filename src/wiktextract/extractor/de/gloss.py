import re
from collections import defaultdict
from typing import Dict, List

from wikitextprocessor import NodeKind, WikiNode
from wikitextprocessor.parser import LevelNode
from wiktextract.extractor.de.utils import find_and_remove_child, match_senseid
from wiktextract.page import clean_node
from wiktextract.wxr_context import WiktextractContext


def extract_glosses(
    wxr: WiktextractContext,
    page_data: List[Dict],
    level_node: LevelNode,
) -> None:
    for list_node in level_node.find_child(NodeKind.LIST):
        process_gloss_list_item(wxr, page_data, list_node)

    for non_list_node in level_node.invert_find_child(NodeKind.LIST):
        wxr.wtp.debug(
            f"Found unexpected non-list node in pronunciation section: {non_list_node}",
            sortid="extractor/de/pronunciation/extract_pronunciation/64",
        )


def process_gloss_list_item(
    wxr: WiktextractContext,
    page_data: List[Dict],
    list_node: WikiNode,
    parent_senseid: str = "",
    parent_gloss_data: defaultdict(list) = None,
) -> None:
    for list_item_node in list_node.find_child(NodeKind.LIST_ITEM):
        item_type = list_item_node.sarg
        if item_type == "*":
            handle_sense_modifier(wxr, list_item_node)

        elif item_type in [":", "::"]:
            if any(
                [
                    template_node.template_name
                    in ["QS Herkunft", "QS Bedeutungen"]
                    for template_node in list_item_node.find_child_recursively(
                        NodeKind.TEMPLATE
                    )
                ]
            ):
                continue

            gloss_data = (
                defaultdict(list)
                if parent_gloss_data is None
                else parent_gloss_data.copy()
            )

            # Extract sub-glosses for later processing
            sub_glosses_list_nodes = list(
                find_and_remove_child(list_item_node, NodeKind.LIST)
            )

            raw_gloss = clean_node(wxr, {}, list_item_node.children)
            gloss_data["raw_glosses"] = [raw_gloss]

            process_K_template(wxr, gloss_data, list_item_node)

            gloss_text = clean_node(wxr, gloss_data, list_item_node.children)

            senseid, gloss_text = match_senseid(gloss_text)

            if senseid:
                senseid = (
                    senseid
                    if senseid[0].isnumeric()
                    else parent_senseid + senseid
                )
                gloss_data["senseid"] = senseid
            else:
                wxr.wtp.debug(
                    f"Failed to extract sense number from gloss node: {list_item_node}",
                    sortid="extractor/de/glosses/extract_glosses/28",
                )

            # XXX: Extract tags from nodes instead using Italic and Template
            gloss_text = extract_tags_from_gloss_text(gloss_data, gloss_text)

            if gloss_text or not sub_glosses_list_nodes:
                gloss_data["glosses"] = [gloss_text]
                page_data[-1]["senses"].append(gloss_data)

            for sub_list_node in sub_glosses_list_nodes:
                process_gloss_list_item(
                    wxr,
                    page_data,
                    sub_list_node,
                    senseid,
                    gloss_data if not gloss_text else None,
                )

        else:
            wxr.wtp.debug(
                f"Unexpected list item in glosses: {list_item_node}",
                sortid="extractor/de/glosses/extract_glosses/29",
            )
            continue


def handle_sense_modifier(wxr, list_item_node):
    wxr.wtp.debug(
        f"Skipped a sense modifier in gloss list: {list_item_node}",
        sortid="extractor/de/glosses/extract_glosses/19",
    )
    # XXX: We should extract the modifier. However, it seems to affect
    # multiple glosses. Needs investigation.
    pass


def process_K_template(
    wxr: WiktextractContext,
    gloss_data: defaultdict(list),
    list_item_node: NodeKind.LIST_ITEM,
) -> None:
    for template_node in list_item_node.find_child(NodeKind.TEMPLATE):
        if template_node.template_name == "K":
            text = clean_node(wxr, gloss_data, template_node).removesuffix(":")
            tags = re.split(r";|,", text)
            gloss_data["tags"] = [t.strip() for t in tags]

            # Prepositional and case information is sometimes only expanded to
            # category links and not present in cleaned node. We still want it
            # as a tag.
            prep = template_node.template_parameters.get("Prä")
            case = template_node.template_parameters.get("Kas")
            category = (prep if prep else "") + (" + " + case if case else "")
            if category:
                gloss_data["tags"].append(category)

            # XXX: Investigate better ways to handle free text in K template
            ft = template_node.template_parameters.get("ft")
            if ft:
                wxr.wtp.debug(
                    f"Found ft '{ft}' in K template which could be considered part of the gloss. Moved to tags for now.",
                    sortid="extractor/de/glosses/extract_glosses/63",
                )

            # Remove the template_node from the children of list_item_node
            list_item_node.children = [
                c for c in list_item_node.children if c != template_node
            ]


def extract_tags_from_gloss_text(
    gloss_data: defaultdict(list), gloss_text: str
) -> None:
    parts = gloss_text.split(":", 1)
    if len(parts) > 1:
        tags_part = parts[0].strip()

        categories = [c.strip() for c in re.split(",", tags_part)]
        if all(c.isalnum() for c in categories):
            gloss_data["tags"].extend(categories)
            return parts[1].strip()

    return gloss_text
