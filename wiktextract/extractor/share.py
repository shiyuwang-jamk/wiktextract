import re
from html import unescape
from typing import Iterable, List, Optional, Tuple, Union

from wikitextprocessor import NodeKind, WikiNode

WIKIMEDIA_COMMONS_URL = "https://commons.wikimedia.org/wiki/Special:FilePath/"


def contains_list(
    contents: Union[WikiNode, List[Union[WikiNode, str]]]
) -> bool:
    """Returns True if there is a list somewhere nested in contents."""
    if isinstance(contents, (list, tuple)):
        return any(contains_list(x) for x in contents)
    if not isinstance(contents, WikiNode):
        return False
    kind = contents.kind
    if kind == NodeKind.LIST:
        return True
    return contains_list(contents.children) or contains_list(contents.sarg if
                                            contents.sarg else contents.largs)


def strip_nodes(
    nodes: List[Union[WikiNode, str]]
) -> Iterable[Union[WikiNode, str]]:
    # filter nodes that only have newlines, white spaces and non-breaking spaces
    return filter(
        lambda node: isinstance(node, WikiNode)
        or (isinstance(node, str) and len(unescape(node).strip()) > 0),
        nodes,
    )


def filter_child_wikinodes(
    node: WikiNode, node_type: NodeKind
) -> List[Union[WikiNode, str]]:
    return [
        child
        for child in node.children
        if isinstance(child, WikiNode) and child.kind == node_type
    ]


def capture_text_in_parentheses(text: str) -> Tuple[List[str], str]:
    """
    Return a list of text inside parentheses, and the rest test.
    """
    rest_parts = []
    capture_text_list = []
    last_group_end = 0
    for m in re.finditer(r"\([^()]+\)", text):
        not_captured = text[last_group_end : m.start()].strip()
        if len(not_captured) > 0:
            rest_parts.append(not_captured)
        last_group_end = m.end()
        capture_text_list.append(m.group()[1:-1])

    rest_text = " ".join(rest_parts) if len(rest_parts) > 0 else text
    return capture_text_list, rest_text


def split_chinese_variants(text: str) -> Iterable[Tuple[Optional[str], str]]:
    """
    Return Chinese character variant and text
    """
    if "／" in text:
        splite_result = text.split("／")
        if len(splite_result) != 2:
            yield None, text
        else:
            for variant_index, variant in enumerate(splite_result):
                yield "zh-Hant" if variant_index == 0 else "zh-Hans", variant
    else:
        yield None, text
