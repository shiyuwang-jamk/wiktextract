# Code for parsing inflection tables.
#
# Copyright (c) 2021 Tatu Ylonen.  See file LICENSE and https://ylonen.org.

import re
import copy
import enum
import html
import functools
import collections
import unicodedata
from wikitextprocessor import Wtp, WikiNode, NodeKind, ALL_LANGUAGES
from wiktextract.config import WiktionaryConfig
from wiktextract.tags import valid_tags
from wiktextract.inflectiondata import infl_map, infl_start_map, infl_start_re
from wiktextract.datautils import (data_append, data_extend, freeze,
                                   split_at_comma_semi)
from wiktextract.form_descriptions import (classify_desc, decode_tags,
                                           parse_head_final_tags)
from wiktextract.parts_of_speech import PARTS_OF_SPEECH


# Set this to a word form to debug how that is analyzed, or None to disable
debug_word = None  # None to disable


# Column texts that are interpreted as an empty column.
IGNORED_COLVALUES = set([
    "-", "־", "᠆", "‐", "‑", "‒", "–", "—", "―", "−",
    "⸺", "⸻", "﹘", "﹣", "－", "/", "?"])

# These tags are never inherited from above
noinherit_tags = set([
    "infinitive-i",
    "infinitive-i-long",
    "infinitive-ii",
    "infinitive-iii",
    "infinitive-iv",
    "infinitive-v",
])

# Words in title that cause addition of tags in all entries
title_contains_global_map = {
    "possessive": "possessive",
    "negative": "negative",
    "comparative": "comparative",
    "superlative": "superlative",
    "combined forms": "combined-form",
    "mutation": "mutation",
    "definite article": "definite",
    "indefinite article": "indefinite",
    "indefinite declension": "indefinite",
    "definite declension": "definite",
    "pre-reform": "dated",
    "personal pronouns": "personal pronoun",
    "composed forms of": "multiword-construction",
    "subordinate-clause forms of": "subordinate-clause",
    "western lombard": "Western-Lombard",
    "eastern lombard": "Eastern-Lombard",
    "participles of": "participle",
}
for k, v in title_contains_global_map.items():
    if any(t not in valid_tags for t in v.split()):
        print("TITLE_CONTAINS_GLOBAL_MAP UNRECOGNIZED TAG: {}: {}"
              .format(k, v))
title_contains_global_re = re.compile(
    r"(?i)(^|\b)({})($|\b)"
    .format("|".join(re.escape(x)
                     for x in title_contains_global_map.keys())))

# Words in title that cause addition of tags to word-tags "form"
title_contains_wordtags_map = {
    "pf": "perfective",
    "impf": "imperfective",
    "strong": "strong",
    "weak": "weak",
    "countable": "countable",
    "uncountable": "uncountable",
    "inanimate": "inanimate",
    "animate": "animate",
    "transitive": "transitive",
    "intransitive": "intransitive",
    "ditransitive": "ditransitive",
    "ambitransitive": "ambitransitive",
    "proper noun": "proper-noun",
    "no plural": "no-plural",
    "imperfective": "imperfective",
    "perfective": "perfective",
    "no supine stem": "no-supine",
    "no perfect stem": "no-perfect",
    "deponent": "deponent",
    "irregular": "irregular",
    "no short forms": "no-short-form",
    "iō-variant": "iō-variant",
    "1st declension": "declension-1",
    "2nd declension": "declension-2",
    "3rd declension": "declension-3",
    "4th declension": "declension-4",
    "5th declension": "declension-5",
    "6th declension": "declension-6",
    "first declension": "declension-1",
    "second declension": "declension-2",
    "third declension": "declension-3",
    "fourth declension": "declension-4",
    "fifth declension": "declension-5",
    "sixth declension": "declension-6",
    "1st conjugation": "conjugation-1",
    "2nd conjugation": "conjugation-2",
    "3rd conjugation": "conjugation-3",
    "4th conjugation": "conjugation-4",
    "5th conjugation": "conjugation-5",
    "6th conjugation": "conjugation-6",
    "7th conjugation": "conjugation-7",
    "first conjugation": "conjugation-1",
    "second conjugation": "conjugation-2",
    "third conjugation": "conjugation-3",
    "fourth conjugation": "conjugation-4",
    "fifth conjugation": "conjugation-5",
    "sixth conjugation": "conjugation-6",
    "seventh conjugation": "conjugation-7",
}
for k, v in title_contains_wordtags_map.items():
    if any(t not in valid_tags for t in v.split()):
        print("TITLE_CONTAINS_WORDTAGS_MAP UNRECOGNIZED TAG: {}: {}"
              .format(k, v))
title_contains_wordtags_re = re.compile(
    r"(?i)(^|\b)({})($|\b)"
    .format("|".join(re.escape(x)
                     for x in title_contains_wordtags_map.keys())))

# Parenthesized elements in title that are converted to tags in "word-tags" form
title_elements_map = {
    "weak": "weak",
    "strong": "strong",
    "masculine": "masculine",
    "feminine": "feminine",
    "neuter": "neuter",
    "singular": "singular",
    "plural": "plural",
}
for k, v in title_elements_map.items():
    if any(t not in valid_tags for t in v.split()):
        print("TITLE_ELEMENTS_MAP UNRECOGNIZED TAG: {}: {}"
              .format(k, v))

# Parenthized element starts to map them to tags for form for the rest of
# the element
title_elemstart_map = {
    "auxiliary": "auxiliary",
    "Kotus type": "class",
    "ÕS type": "class",
    "class": "class",
    "short class": "class",
    "type": "class",
    "strong class": "class",
    "weak class": "class",
    "accent paradigm": "accent-paradigm",
}
for k, v in title_elemstart_map.items():
    if any(t not in valid_tags for t in v.split()):
        print("TITLE_ELEMSTART_MAP UNRECOGNIZED TAG: {}: {}"
              .format(k, v))
title_elemstart_re = re.compile(
    r"^({}) "
    .format("|".join(re.escape(x) for x in title_elemstart_map.keys())))


# Languages with three genders masculine, feminine, neuter (and impersonal
# not used)
MFN_LANGUAGES = set([
    "Czech",
    "French",
    "German Low German",
    "German",
    "Polish",
    "Russian",
    "Spanish",
])

# Languages with just two genders masculine and feminine (neuter and
# impersonal not used)
MF_LANGUAGES = set([
    "Portuguese",
    "Irish",
])

# Languages with virile-nonvirile distinction in the plural
# (generally Slavic)
PL_VIRILE_LANGS = set([
    "Polish",
    "Russian",
])

# Languages with animate/inanimate distinction in the masculine singular
# (generally Slavic)
MASC_ANIMATE_LANGS = set([
    "Polish",
    "Russian",
    "Czech",
])

# Languages with only singular and plural for number (i.e., no dual, paucal etc)
# (listing the language here only matters if simplications are needed in
# inflection table parsing).
SINGULAR_PLURAL_LANGS = set([
    "Dutch",
    "English",
    "Finnish",
    "French",
    "Irish",
    "Portuguese",
    "Spanish",
    "Swedish",
])

# Languages that have other voice forms in inflection tables besides
# just active and passive
NON_ACTIVE_PASSIVE_LANGS = set([
])

# Languages that have "strong" and "weak" tags and where they should be
# eliminated if both are present.
STRONG_WEAK_LANGS = set([
    "Irish",
])

# For tables in these languages, an empty row resets hdrspans
EMPTY_ROW_RESETS_LANGS = set([
    "Latvian",
])

# Specification for language-specific processing.  Each entry starts
# with a list of languages that it applies to (a language can be
# specified in multiple entries) and then a list of parts-of-speech.
# It is then followed by any number of pattern-tags pairs, where
# pattern will be escaped, except ^ at the beginning is interpreted as
# restricting it to the beginning.  The matched parts will be removed
# from the word.
lang_specific_data = [
    [["German"], ["verb"],
     ["^ich ", "first-person singular"],
     ["^du ", "second-person singular"],
     ["^er ", "third-person singular"],
     ["^wir ", "first-person plural"],
     ["^ihr ", "second-person plural"],
     ["^sie ", "third-person plural"],
     ["^dass ich ", "first-person singular subordinate-clause"],
     ["^dass du ", "second-person singular subordinate-clause"],
     ["^dass er ", "third-person singular subordinate-clause"],
     ["^dass wir ", "first-person plural subordinate-clause"],
     ["^dass ihr ", "second-person plural subordinate-clause"],
     ["^dass sie ", "third-person plural subordinate-clause"],
     [" (du)", "second-person singular"],
     [" (ihr)", "second-person plural"],
     ],
]
specific_by_lang = collections.defaultdict(list)
for lst in lang_specific_data:
    assert isinstance(lst, list)
    assert len(lst) >= 3
    for rule_lang in lst[0]:
        assert isinstance(rule_lang, str)
        for rule_pos in lst[1]:
            assert isinstance(rule_pos, str)
            for rule in lst[2:]:
                assert isinstance(rule, list)
                rule_pattern, rule_tags = rule
                assert isinstance(rule_pattern, str)
                assert isinstance(rule_tags, str)
                for t in rule_tags.split():
                    assert t in valid_tags
                specific_by_lang[rule_lang, rule_pos].append(
                    [rule_pattern, rule_tags])
specific_by_lang_re = {}
specific_by_lang_map = {}
for (rule_lang, rule_pos), lst in specific_by_lang.items():
    starts = list(x[0][1:] for x in lst if x[0].startswith("^"))
    others = list(x[0] for x in lst if not x[0].startswith("^"))
    rs = []
    if starts:
        rs.append(r"^(" + "|".join(re.escape(x) for x in starts) + ")")
    if others:
        rs.append(r"(" + "|".join(re.escape(x) for x in others) + ")")
    specific_by_lang_re[rule_lang, rule_pos] = re.compile("|".join(rs))
    ht = {}
    specific_by_lang_map[rule_lang, rule_pos] = ht
    for k, v in lst:
        if k.startswith("^"):
            k = k[1:]
        assert k not in ht
        ht[k] = v.split()


# Maps language to allowed categories for col0 expansion when there are
# other headers on the same row. First value is allowed col0 tag categories
# in such cases, and second value is allowed later header tag categories.
col0_expand_allowed = {
    "default": [set(["number", "mood", "referent", "aspect", "tense",
                     "voice", "non-finite", "case", "possession"]),
                set(["person", "gender", "number", "degree", "polarity",
                     "voice", "register"])],
    "German Low German": [set(["mood", "non-finite"]),
                          set(["tense"])],
    "Czech": [set(["tense", "mood", "non-finite"]),
              set(["tense", "mood", "voice"])],
    "Estonian": [set(["non-finite"]), set(["voice"])],
}


# Tag combination mappings for specific languages/part-of-speech.  These are
# used as a post-processing step for forms extracted from tables.  Each
# element has list of languages, list of part-of-speech, and one or more
# source set - replacement set pairs.
lang_tag_mappings = [
    [["Armenian"], ["noun"],
     [["possessive", "singular"], ["possessive", "possessive-single"]],
     [["possessive", "plural"], ["possessive", "possessive-many"]],
    ],
]
for lst in lang_tag_mappings:
    assert len(lst) >= 3
    assert all(isinstance(x, str) for x in lst[0])  # languages
    assert all(x in PARTS_OF_SPEECH for x in lst[1])  # parts of speech
    for src, dst in lst[2:]:
        assert all(t in valid_tags for t in src)
        assert all(t in valid_tags for t in dst)


class InflCell(object):
    """Cell in an inflection table."""
    __slots__ = (
        "text",
        "is_title",
        "start",
        "colspan",
        "rowspan",
    )
    def __init__(self, text, is_title, start, colspan, rowspan):
        assert isinstance(text, str)
        assert is_title in (True, False)
        assert isinstance(start, int)
        assert isinstance(colspan, int) and colspan >= 1
        assert isinstance(rowspan, int) and rowspan >= 1
        self.text = text.strip()
        self.is_title = text and is_title
        self.colspan = colspan
        self.rowspan = rowspan
    def __str__(self):
        return "{}/{}/{}/{}".format(
            self.text, self.is_title, self.colspan, self.rowspan)
    def __repr__(self):
        return str(self)


class HdrSpan(object):
    """Saved information about a header cell/span during the parsing
    of a table."""
    __slots__ = (
        "start",
        "colspan",
        "rowspan",
        "rownum",      # Row number where this occurred
        "tagsets",  # set of tuples
        "used",  # At least one text cell after this
        "text",  # For debugging
        "all_headers_row",
        "expanded",  # The header has been expanded to cover whole row/part
    )
    def __init__(self, start, colspan, rowspan, rownum, tagsets,
                 text, all_headers_row):
        assert isinstance(start, int) and start >= 0
        assert isinstance(colspan, int) and colspan >= 1
        assert isinstance(rownum, int)
        assert isinstance(tagsets, set)
        for x in tagsets:
            assert isinstance(x, tuple)
        assert all_headers_row in (True, False)
        self.start = start
        self.colspan = colspan
        self.rowspan = rowspan
        self.rownum = rownum
        self.tagsets = set(tuple(sorted(set(tags))) for tags in tagsets)
        self.used = False
        self.text = text
        self.all_headers_row = all_headers_row
        self.expanded = False


def is_superscript(ch):
    """Returns True if the argument is a superscript character."""
    assert isinstance(ch, str) and len(ch) == 1
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return False
    return re.match(r"SUPERSCRIPT |MODIFIER LETTER SMALL ", name) is not None


def remove_useless_tags(lang, pos, tags):
    """Remove certain tag combinations from ``tags`` when they serve no purpose
    together (cover all options)."""
    assert isinstance(lang, str)
    assert isinstance(pos, str)
    assert isinstance(tags, set)
    if lang in MASC_ANIMATE_LANGS:
        if "animate" in tags and "inanimate" in tags:
            tags.remove("animate")
            tags.remove("inanimate")
        if "virile" in tags and "nonvirile" in tags:
            tags.remove("virile")
            tags.remove("nonvirile")
    if lang in SINGULAR_PLURAL_LANGS:
        if "singular" in tags and "plural" in tags:
            tags.remove("singular")
            tags.remove("plural")
    if lang in MFN_LANGUAGES:
        if "masculine" in tags and "feminine" in tags and "neuter" in tags:
            tags.remove("masculine")
            tags.remove("feminine")
            tags.remove("neuter")
    if lang in MF_LANGUAGES:
        if "masculine" in tags and "feminine" in tags:
            tags.remove("masculine")
            tags.remove("feminine")
    if lang not in NON_ACTIVE_PASSIVE_LANGS:
        if "active" in tags and "passive" in tags:
            tags.remove("active")
            tags.remove("passive")
    if lang in STRONG_WEAK_LANGS and "strong" in tags and "weak" in tags:
        tags.remove("strong")
        tags.remove("weak")
    if ("first-person" in tags and "second-person" in tags and
        "third-person" in tags):
        tags.remove("first-person")
        tags.remove("second-person")
        tags.remove("third-person")


def tagset_cats(tagset):
    """Returns a set of tag categories for the tagset (merged from all
    alternatives)."""
    return set(valid_tags[t]
               for ts in tagset
               for t in ts)


def or_tagsets(lang, pos, tagsets1, tagsets2):
    """Merges two tagsets (the new tagset just merges the tags from both, in
    all combinations).  If they contain simple alternatives (differ in
    only one category), they are simply merged; otherwise they are split to
    more alternatives.  The tagsets are assumed be sets of sorted tuples."""
    assert isinstance(tagsets1, set) and len(tagsets1) >= 1
    assert all(isinstance(x, tuple) for x in tagsets1)
    assert isinstance(tagsets2, set) and len(tagsets2) >= 1
    assert all(isinstance(x, tuple) for x in tagsets1)
    tagsets = set()  # This will be the result

    def add_tags(tags1):
        if not tags1:
            return  # empty set would merge with anything, won't change result
        if not tagsets:
            tagsets.add(tags1)
            return
        for tags2 in tagsets:
            # Determine if tags1 can be merged with tags2
            num_differ = 0
            if tags1 and tags2:
                cats1 = set(valid_tags[t] for t in tags1)
                cats2 = set(valid_tags[t] for t in tags2)
                cats = cats1 | cats2
                for cat in cats:
                    tags1_in_cat = set(t for t in tags1 if valid_tags[t] == cat)
                    tags2_in_cat = set(t for t in tags2 if valid_tags[t] == cat)
                    if (tags1_in_cat != tags2_in_cat or
                        not tags1_in_cat or not tags2_in_cat):
                        num_differ += 1
                        if not tags1_in_cat or not tags2_in_cat:
                            # Prevent merging if one is empty
                            num_differ += 1
            # print("tags1={} tags2={} num_differ={}"
            #       .format(tags1, tags2, num_differ))
            if num_differ <= 1:
                # Yes, they can be merged
                tagsets.remove(tags2)
                tags = set(tags1) | set(tags2)
                remove_useless_tags(lang, pos, tags)
                tags = tuple(sorted(tags))
                add_tags(tags)  # Could result in further merging
                return
        # If we could not merge, add to tagsets
        tagsets.add(tags1)

    for tags in tagsets1:
        add_tags(tags)
    for tags in tagsets2:
        add_tags(tags)
    if not tagsets:
        tagsets.add(())

    # print("or_tagsets: {} + {} -> {}"
    #       .format(tagsets1, tagsets2, tagsets))
    return tagsets


def and_tagsets(lang, pos, tagsets1, tagsets2):
    """Merges tagsets by taking union of all cobinations, without trying
    to determine whether they are compatible."""
    assert isinstance(tagsets1, set) and len(tagsets1) >= 1
    assert all(isinstance(x, tuple) for x in tagsets1)
    assert isinstance(tagsets2, set) and len(tagsets2) >= 1
    assert all(isinstance(x, tuple) for x in tagsets1)
    new_tagsets = set()
    for tags1 in tagsets1:
        for tags2 in tagsets2:
            tags = set(tags1) | set(tags2)
            remove_useless_tags(lang, pos, tags)
            tags = tuple(sorted(tags))
            new_tagsets.add(tags)
    # print("and_tagsets: {} + {} -> {}"
    #       .format(tagsets1, tagsets2, new_tagsets))
    return new_tagsets


@functools.lru_cache(65536)
def clean_header(word, col, skip_paren):
    """Cleans a row/column header for later processing."""
    hdr_tags = []
    orig_col = col
    col = re.sub(r"(?s)\s*➤\s*$", "", col)
    col = re.sub(r"(?s)\s*,\s*$", "", col)
    col = re.sub(r"(?s)\s*•\s*$", "", col)
    if col not in infl_map and skip_paren:
        col = re.sub(r"[,/]?\s+\([^)]*\)\s*$", "", col)
    col = col.strip()
    if re.search(r"^(There are |"
                 r"\* |"
                 r"see |"
                 r"Use |"
                 r"use the |"
                 r"Only used |"
                 r"The forms in |"
                 r"these are also written |"
                 r"The genitive can be |"
                 r"Genitive forms are rare or non-existant|"
                 r"Accusative Note: |"
                 r"Classifier Note: |"
                 r"Noun: Assamese nouns are |"
                 r"the active conjugation|"
                 r"the instrumenal singular|"
                 r"Note:|"
                 r"\^* Note:|"
                 r"possible mutated form |"
                 r"The future tense: |"
                 r"Notes:)",
                col):
        return "", [], [], []
    refs = []
    ref_symbols = "*△†0123456789"
    while True:
        m = re.search(r"\^(.|\([^)]*\))$", col)
        if not m:
            break
        r = m.group(1)
        if r.startswith("(") and r.endswith(")"):
            r = r[1:-1]
        if r == "rare":
            hdr_tags.append("rare")
        elif r == "vos":
            hdr_tags.append("formal")
        elif r == "tú":
            hdr_tags.append("informal")
        else:
            # XXX handle refs from m.group(1)
            pass
        col = col[:m.start()]
    if col.endswith("ʳᵃʳᵉ"):
        hdr_tags.append("rare")
        col = col[:-4].strip()
    if col.endswith("ᵛᵒˢ"):
        hdr_tags.append("formal")
        col = col[:-3].strip()
    while col and is_superscript(col[0]):
        if len(col) > 1 and col[1] in ("⁾", " ", ":"):
            # Note definition
            return "", [], [[col[0], col[2:].strip()]], []
        refs.append(col[0])
        col = col[1:]
    while col and (is_superscript(col[-1]) or col[-1] in ("†",)):
        # Numbers and H/L/N are useful information
        refs.append(col[-1])
        col = col[:-1]
    if len(col) > 2 and col[1] in (")", " ", ":") and col[0].isdigit():
        # Another form of note definition
        return "", [], [[col[0], col[2:].strip()]], []
    col = col.strip()
    if col.endswith("*"):
        col = col[:-1].strip()
        refs.append("*")
    if col.endswith("(*)"):
        col = col[:-3].strip()
        refs.append("*")
    # print("CLEAN_HEADER: orig_col={!r} col={!r} refs={!r} hdr_tags={}"
    #       .format(orig_col, col, refs, hdr_tags))
    return col.strip(), refs, [], hdr_tags


@functools.lru_cache(10000)
def parse_title(title, source):
    """Parses inflection table title.  This returns (global_tags, word_tags,
    extra_forms), where ``global_tags`` is tags to be added to each inflection
    entry, ``word_tags`` are tags for the word but not to be added to every
    form, and ``extra_forms`` is dictionary describing additional forms to be
    included in the part-of-speech entry)."""
    assert isinstance(title, str)
    assert isinstance(source, str)
    title = html.unescape(title)
    title = re.sub(r"(?i)<[^>]*>", "", title).strip()
    title = re.sub(r"\s+", " ", title)
    # print("PARSE_TITLE:", title)
    global_tags = []
    word_tags = []
    extra_forms = []
    # Check for the case that the title is in infl_map
    if title in infl_map:
        return infl_map[title].split(), [], []
    if title.lower() in infl_map:
        return infl_map[title.lower()].split(), [], []
    # Add certain global tags based on contained words
    for m in re.finditer(title_contains_global_re, title):
        global_tags.extend(title_contains_global_map[
            m.group(0).lower()].split())
    # Add certain tags to word-tags "form" based on contained words
    for m in re.finditer(title_contains_wordtags_re, title):
        word_tags.extend(title_contains_wordtags_map[
            m.group(0).lower()].split())
    # Check for <x>-type at the beginning of title (e.g., Armenian)
    m = re.search(r"\b(\w+-type|accent-\w+|\w+-stem|[^ ]+ gradation|"
                  r"[^ ]+ alternation|(First|Second|Third|Fourth|Fifth|"
                  r"Sixth|Seventh) Conjugation|"
                  r"(1st|2nd|3rd|4th|5th|6th) declension)\b", title)
    if m:
        dt = {"form": m.group(1),
              "source": source + " title",
              "tags": ["class"]}
        extra_forms.append(dt)
    # Parse parenthesized part from title
    for m in re.finditer(r"\(([^)]*)\)", title):
        for elem in m.group(1).split(","):
            elem = elem.strip()
            if elem in title_elements_map:
                word_tags.extend(title_elements_map[elem].split())
            else:
                m = re.match(title_elemstart_re, elem)
                if m:
                    tags = title_elemstart_map[m.group(1)].split()
                    dt = {"form": elem[m.end():],
                          "source": source + " title",
                          "tags": tags}
                    extra_forms.append(dt)
    # For titles that contains no parenthesized parts, do some special
    # handling to still interpret parts from them
    if title.find("(") < 0:
        # No parenthesized parts
        m = re.search(r"\b(Portuguese) (-.* verb) ", title)
        if m is not None:
            dt = {"form": m.group(2),
                  "tags": ["class"],
                  "source": source + " title"}
            extra_forms.append(dt)
        for elem in title.split(","):
            elem = elem.strip()
            if elem in title_elements_map:
                word_tags.extend(title_elements_map[elem].split())
            elif elem.endswith("-stem"):
                dt = {"form": elem,
                      "tags": ["class"],
                      "source": source + " title"}
                extra_forms.append(dt)
    return global_tags, word_tags, extra_forms


def expand_header(ctx, word, lang, pos, text, tags0, silent=False):
    """Expands a cell header to tags, handling conditional expressions
    in infl_map.  This returns list of tuples of tags, each list element
    describing an alternative interpretation.  ``tags0`` is combined
    column and row tags for the cell in which the text is being interpreted
    (conditional expressions in inflection data may depend on it)."""
    assert isinstance(ctx, Wtp)
    assert isinstance(word, str)
    assert isinstance(lang, str)
    assert isinstance(pos, str)
    assert isinstance(text, str)
    assert isinstance(tags0, (list, tuple, set))
    assert silent in (True, False)
    # print("EXPAND_HDR:", text)
    # First map the text using the inflection map
    if text in infl_map:
        v = infl_map[text]
    else:
        m = re.match(infl_start_re, text)
        if m is None:
            return []  # Unrecognized header
        v = infl_start_map[m.group(1)]
        # print("INFL_START {} -> {}".format(text, v))

    # Then loop interpreting the value, until the value is a simple string.
    # This may evaluate nested conditional expressions.
    while True:
        # If it is a string, we are done.
        if isinstance(v, str):
            tags = set(v.split())
            remove_useless_tags(lang, pos, tags)
            return [tuple(sorted(tags))]
        # For a list, just interpret it as alternatives.  (Currently the
        # alternatives must directly be strings.)
        if isinstance(v, (list, tuple)):
            ret = set()
            for x in v:
                tags = set(x.split())
                remove_useless_tags(lang, pos, tags)
                ret.add(tuple(sorted(tags)))
            return list(sorted(ret))
        # Otherwise the value should be a dictionary describing a conditional
        # expression.
        if not isinstance(v, dict):
            ctx.debug("inflection table: internal: "
                      "UNIMPLEMENTED INFL_MAP VALUE: {}"
                      .format(infl_map[text]))
            return [()]
        # Evaluate the conditional expression.
        assert isinstance(v, dict)
        cond = "default-true"
        # Handle "lang" condition.  The value must be either a single language
        # or a list of languages, and the condition evaluates to True if
        # the table is in one of those languages.
        if cond and "lang" in v:
            c = v["lang"]
            if isinstance(c, str):
                cond = c == lang
            else:
                assert isinstance(c, (list, tuple, set))
                cond = lang in c
        # Handle "if" condition.  The value must be a string containing
        # a space-separated list of tags.  The condition evaluates to True
        # if ``tags0`` contains all of the listed tags.  If the condition
        # is of the form "any: ...tags...", then any of the tags will be
        # enough.
        if cond and "if" in v:
            c = v["if"]
            assert isinstance(c, str)
            # "if" condition is true if any of the listed tags is present
            if c.startswith("any: "):
                cond = any(t in tags0 for t in c[5:].split())
            else:
                cond = all(t in tags0 for t in c.split())
        # Warning message about missing conditions for debugging.
        if cond == "default-true" and not silent:
            print("IF MISSING COND: word={} lang={} text={} tags0={} "
                  "c={} cond={}"
                  .format(word, lang, text, tags0, c, cond))
        # Based on the result of evaluating the condition, select either
        # "then" part or "else" part.
        if cond:
            v = v.get("then", "")
        else:
            v = v.get("else")
            if v is None:
                if not silent:
                    print("IF WITHOUT ELSE EVALS False: {}/{} {!r} tags0={}"
                          .format(word, lang, text, tags0))
                v = ""


def compute_coltags(lang, pos, hdrspans, start, colspan, mark_used, celltext):
    """Computes column tags for a column of the given width based on the
    current header spans."""
    assert isinstance(lang, str)
    assert isinstance(pos, str)
    assert isinstance(hdrspans, list)
    assert isinstance(start, int) and start >= 0
    assert isinstance(colspan, int) and colspan >= 1
    assert mark_used in (True, False)
    assert isinstance(celltext, str)  # For debugging only
    # print("COMPUTE_COLTAGS CALLED start={} colspan={} celltext={}"
    #       .format(start, colspan, celltext))
    # For debugging, set this to the form for whose cell you want debug prints
    if celltext == debug_word:
        print("COMPUTE_COLTAGS CALLED start={} colspan={} celltext={!r}"
              .format(start, colspan, celltext))
        for hdrspan in hdrspans:
            print("  row={} start={} colspans={} tagsets={}"
                  .format(hdrspan.rownum, hdrspan.start, hdrspan.colspan,
                          hdrspan.tagsets))
    used = set()
    coltags = set([()])
    last_header_row = 1000000
    # Iterate through the headers in reverse order, i.e., headers lower in the
    # table (closer to the cell) first.
    row_tagsets = set([()])
    row_tagsets_rownum = 1000000
    used_hdrspans = set()
    for hdrspan in reversed(hdrspans):
        if (hdrspan.start + hdrspan.colspan <= start or
            hdrspan.start >= start + colspan):
            # Does not horizontally overlap current cell. Ignore this hdrspan.
            if celltext == debug_word:
                print("Ignoring row={} start={} colspan={} tagsets={}"
                      .format(hdrspan.rownum, hdrspan.start,
                              hdrspan.colspan, hdrspan.tagsets))
            continue
        # If the cell partially overlaps the current cell, assume we have
        # reached something unrelated and abort.
        if (hdrspan.start < start and
            hdrspan.start + hdrspan.colspan > start and
            hdrspan.start + hdrspan.colspan < start + colspan):
            if celltext == debug_word:
                print("break on partial overlap at start {} {} {}"
                      .format(hdrspan.start, hdrspan.colspan, hdrspan.tagsets))
            break
        if (hdrspan.start < start + colspan and
            hdrspan.start > start and
            hdrspan.start + hdrspan.colspan > start + colspan and
            not hdrspan.expanded):
            if celltext == debug_word:
                print("break on partial overlap at end {} {} {}"
                      .format(hdrspan.start, hdrspan.colspan, hdrspan.tagsets))
            break
        # Check if we have already used this cell.
        if id(hdrspan) in used_hdrspans:
            continue
        # We are going to use this cell.
        used_hdrspans.add(id(hdrspan))
        tagsets = hdrspan.tagsets
        # If the hdrspan is fully inside the current cell and does not cover
        # it fully, check if we should merge information from multiple cells.
        if (not hdrspan.expanded and
            (hdrspan.start > start or
             hdrspan.start + hdrspan.colspan < start + colspan)):
            # Multiple columns apply to the current cell, only
            # gender/number/case tags present
            # If there are no tags outside the range in any of the
            # categories included in these cells, don't add anything
            # (assume all choices valid in the language are possible).
            in_cats = set(valid_tags[t]
                          for x in hdrspans
                          if x.rownum == hdrspan.rownum and
                          x.start >= start and
                          x.start + x.colspan <= start + colspan
                          for tt in x.tagsets
                          for t in tt)
            if celltext == debug_word:
                print("in_cats={}".format(in_cats))
            # Merge the tagsets into existing tagsets.  This merges
            # alternatives into the same tagset if there is only one
            # category different; otherwise this splits the tagset into
            # more alternatives.
            includes_all_on_row = True
            for x in hdrspans:
                if x.rownum != hdrspan.rownum:
                    continue
                if (x.start < start or
                    x.start + x.colspan > start + colspan):
                    if celltext == debug_word:
                        print("NOT IN RANGE: {} {} {}"
                              .format(x.start, x.colspan, x.tagsets))
                    includes_all_on_row = False
                    continue
                if id(x) in used_hdrspans:
                    if celltext == debug_word:
                        print("ALREADY USED: {} {} {}"
                              .format(x.start, x.colspan, x.tagsets))
                    continue
                used_hdrspans.add(id(x))
                if celltext == debug_word:
                    print("Merging into wide col: x.rownum={} "
                          "x.start={} x.colspan={} "
                          "start={} colspan={}"
                          .format(x.rownum, x.start, x.colspan, start, colspan))
                tagsets = or_tagsets(lang, pos, tagsets, x.tagsets)
            # If all headers on the row were included, ignore them.
            # See e.g. kunna/Swedish/Verb.
            if includes_all_on_row:
                tagsets = set([()])
            # For limited categories, if the category doesn't appear
            # outside, we won't include the category
            if not in_cats - set(("gender", "number", "person", "case",
                                  "category", "voice")):
                # Sometimes we have masc, fem, neut and plural, so treat
                # number and gender as the same here (if one given, look for
                # the other too)
                if "number" in in_cats or "gender" in in_cats:
                    in_cats.update(("number", "gender"))
                # Determine which categories occur outside on
                # the same row.  Ignore headers that have been expanded
                # to cover the whole row/part of it.
                out_cats = set(valid_tags[t]
                               for x in hdrspans
                               if x.rownum == hdrspan.rownum and
                               not x.expanded and
                               (x.start < start or
                                x.start + x.colspan > start + colspan)
                               for tt in x.tagsets
                               for t in tt)
                if celltext == debug_word:
                    print("in_cats={} out_cats={}"
                          .format(in_cats, out_cats))
                # Remove all inside categories that do not appear outside
                new_tagsets = set()
                for ts in tagsets:
                    tags = tuple(sorted(t for t in ts
                                        if valid_tags[t] in out_cats))
                    new_tagsets.add(tags)
                if celltext == debug_word and new_tagsets != tagsets:
                    print("Removed tags that do not appear outside {} -> {}"
                          .format(tagsets, new_tagsets))
                tagsets = new_tagsets
        key = (hdrspan.start, hdrspan.colspan)
        if key in used:
            if celltext == debug_word:
                print("Cellspan already used: start={} colspan={} rownum={} {}"
                      .format(hdrspan.start, hdrspan.colspan, hdrspan.rownum,
                              hdrspan.tagsets))
            continue
        tcats = tagset_cats(tagsets)
        # Most headers block using the same column position above.  However,
        # "register" tags don't do this (cf. essere/Italian/verb: "formal")
        if len(tcats) != 1 or "register" not in tcats:
            used.add(key)
        if mark_used:
            # XXX I don't think this case is used any more, check!
            hdrspan.used = True
        # If we have moved to a different row, merge into column tagsets
        # (we use different and_tagsets within the row)
        if row_tagsets_rownum != hdrspan.rownum:
            ret = and_tagsets(lang, pos, coltags, row_tagsets)
            if celltext == debug_word:
                print("merging rows: {} {} -> {}"
                      .format(coltags, row_tagsets, ret))
            coltags = ret
            row_tagsets = set([()])
            row_tagsets_rownum = hdrspan.rownum
        # Merge into coltags
        if hdrspan.all_headers_row and hdrspan.rownum + 1 == last_header_row:
            # If this row is all headers and immediately preceeds the last
            # header we accepted, take any header from there.
            row_tagsets = and_tagsets(lang, pos, row_tagsets, tagsets)
            if celltext == debug_word:
                print("merged (next header row): {}".format(row_tagsets))
        else:
            # new_cats is for the new tags (higher up in the table)
            new_cats = tagset_cats(tagsets)
            # cur_cats is for the tags already collected (lower in the table)
            cur_cats = tagset_cats(coltags)
            if celltext == debug_word:
                print("row={} start={} colspan={} tagsets={} coltags={} "
                      "new_cats={} cur_cats={}"
                      .format(hdrspan.rownum, hdrspan.start, hdrspan.colspan,
                              tagsets, coltags, new_cats, cur_cats))
            if "detail" in new_cats:
                if not any(coltags):  # Only if no tags so far
                    coltags = or_tagsets(lang, pos, coltags, tagsets)
                if celltext == debug_word:
                    print("stopping on detail after merge")
                break
            elif ("non-finite" in new_cats and
                  cur_cats & set(("mood", "non-finite", "person",
                                  "number"))):
                if celltext == debug_word:
                    print("stopping on non-finite new")
                break
            elif ("non-finite" in cur_cats and
                  "mood" in new_cats):
                if celltext == debug_word:
                    print("stopping on non-finite cur")
                break
            elif ("mood" in new_cats and
                  "mood" in cur_cats and
                  # Allow if all new tags are already in current set
                  any(t not in ts1
                      for ts1 in coltags  # current
                      for ts2 in tagsets  # new (from above)
                      for t in ts2)):
                if celltext == debug_word:
                    print("stopping on mood-mood")
                pass  # Skip this header
            elif "number" in cur_cats and "number" in new_cats:
                if celltext == debug_word:
                    print("stopping on number-number")
                    break
            elif "number" in cur_cats and "gender" in new_cats:
                if celltext == debug_word:
                    print("stopping on number-gender")
                break
            else:
                # Merge tags and continue to next header up/left in the table.
                row_tagsets = and_tagsets(lang, pos, row_tagsets, tagsets)
                if celltext == debug_word:
                    print("merged: {}".format(coltags))
        # Update the row number from which we have last taken headers
        last_header_row = hdrspan.rownum
    # Merge the final row tagset into coltags
    coltags = and_tagsets(lang, pos, coltags, row_tagsets)
    #print("HDRSPANS:", list((x.start, x.colspan, x.tagsets) for x in hdrspans))
    if celltext == debug_word:
        print("COMPUTE_COLTAGS {} {} {}: {}"
              .format(start, colspan, mark_used, coltags))
    assert isinstance(coltags, set)
    assert all(isinstance(x, tuple) for x in coltags)
    return coltags


def lang_specific_tags(lang, pos, form):
    """Extracts tags from the word form itself in a language-specific way.
    This may also adjust the word form.
    For example, German inflected verb forms don't have person and number
    specified in the table, but include a pronoun.  This returns adjusted
    form and a list of tags."""
    assert isinstance(lang, str)
    assert isinstance(pos, str)
    assert isinstance(form, str)
    key = (lang, pos)
    r = specific_by_lang_re.get(key)
    if r is None:
        return form, []
    m = re.search(r, form)
    if m is None:
        return form, []
    v = specific_by_lang_map[key][m.group(0)]
    form = form[:m.start()] + form[m.end():]
    return form, v


def parse_simple_table(ctx, word, lang, pos, rows, titles, source):
    """This is the default table parser.  Despite its name, it can parse
    complex tables.  This returns a list of forms to be added to the
    part-of-speech, or None if the table could not be parsed."""
    assert isinstance(ctx, Wtp)
    assert isinstance(word, str)
    assert isinstance(lang, str)
    assert isinstance(pos, str)
    assert isinstance(rows, list)
    assert isinstance(source, str)
    for row in rows:
        for col in row:
            assert isinstance(col, InflCell)
    assert isinstance(titles, list)
    for x in titles:
        assert isinstance(x, str)
    # print("PARSE_SIMPLE_TABLE: TITLES:", titles)
    # print("ROWS:")
    # for row in rows:
    #     print("  ", row)
    ret = []
    hdrspans = []
    col_has_text = []
    rownum = 0
    title = None
    global_tags = []
    word_tags = []
    for title in titles:
        more_global_tags, more_word_tags, extra_forms = \
            parse_title(title, source)
        global_tags.extend(more_global_tags)
        word_tags.extend(more_word_tags)
        ret.extend(extra_forms)
    cell_rowcnt = collections.defaultdict(int)
    seen_cells = set()
    for row in rows:
        # print("ROW:", row)
        if not row:
            continue  # Skip empty rows without incrementing i
        all_headers = all(x.is_title or not x.text.strip()
                          for x in row)
        if (row[0].is_title and
            row[0].text and
            not is_superscript(row[0].text[0]) and
            row[0].text not in infl_map and
            re.sub(r"\s+", " ",
                   re.sub(r"\s*\([^)]*\)", "",
                          row[0].text)).strip() not in infl_map and
            not re.match(infl_start_re, row[0].text) and
            all(x.is_title == row[0].is_title and
                x.text == row[0].text
                for x in row)):
            if row[0].text and title is None:
                title = row[0].text
                if re.match(r"(Note:|Notes:)", title):
                    continue
                more_global_tags, more_word_tags, extra_forms = \
                    parse_title(title, source)
                global_tags.extend(more_global_tags)
                word_tags.extend(more_word_tags)
                ret.extend(extra_forms)
            continue  # Skip title rows without incrementing i
        rowtags = set([()])
        have_hdr = False
        have_text = False
        samecell_cnt = 0
        col0_hdrspan = None  # col0 or later header (despite its name)
        col0_followed_by_nonempty = False
        row_empty = True
        for j, cell in enumerate(row):
            colspan = cell.colspan
            rowspan = cell.rowspan
            previously_seen = id(cell) in seen_cells
            seen_cells.add(id(cell))
            if samecell_cnt == 0:
                # First column of a (possible multi-column) cell
                samecell_cnt = colspan - 1
            else:
                assert samecell_cnt > 0
                cell_initial = False
                samecell_cnt -= 1
                continue
            first_row_of_cell = cell_rowcnt[id(cell)] == 0
            cell_rowcnt[id(cell)] += 1
            # print("  COL:", col)
            col = cell.text
            if not col:
                continue
            row_empty = False

            # print(rownum, j, col)
            if cell.is_title:
                # It is a header cell
                col = re.sub(r"\s+", " ", col)
                text, refs, defs, hdr_tags = clean_header(word, col, True)
                if not text:
                    continue
                if text not in infl_map:
                    text1 = re.sub(r"\s*\([^)]*\)", "", text)
                    if text1 in infl_map:
                        text = text1
                    else:
                        text1 = re.sub(r"\s*,+\s+", " ", text)
                        text1 = re.sub(r"\s+", " ", text1)
                        if text1 in infl_map:
                            text = text1
                        elif not re.match(infl_start_re, text):
                            if text not in IGNORED_COLVALUES:
                                ctx.debug("inflection table: "
                                          "unhandled header: {!r}"
                                          .format(col))
                                text = "error-unrecognized-form"
                            continue
                # Mark that the column has text (we are not at top)
                while len(col_has_text) <= j:
                    col_has_text.append(False)
                col_has_text[j] = True
                # Check if the header expands to reset hdrspans
                v = expand_header(ctx, word, lang, pos, text, [], silent=True)
                if any("!" in tt for tt in v):
                    # Reset column headers (only on first row of cell)
                    if first_row_of_cell:
                        # print("RESET HDRSPANS on: {}".format(text))
                        hdrspans = []
                    continue
                # Text between headers on a row causes earlier headers to
                # be reset
                if have_text:
                    #print("  HAVE_TEXT BEFORE HDR:", col)
                    # Reset rowtags if new title column after previous
                    # text cells
                    # XXX beware of header "—": "" - must not clear on that if
                    # it expands to no tags
                    rowtags = set([()])
                have_hdr = True
                # print("HAVE_HDR:", col)
                # Update rowtags and coltags
                new_rowtags = set()
                new_coltags = set()
                all_hdr_tags = set()
                for rt0 in rowtags:
                    for ct0 in compute_coltags(lang, pos, hdrspans, j,
                                               colspan, False, col):
                        tags0 = set(rt0) | set(ct0) | set(global_tags)
                        alt_tags = expand_header(ctx, word, lang, pos,
                                                 text, tags0)
                        all_hdr_tags.update(alt_tags)
                        for tt in alt_tags:
                            new_coltags.add(tt)
                            # Kludge (saprast/Latvian/Verb): reset row tags
                            # if trying to add a non-finite after mood.
                            if (any(valid_tags[t] == "mood" for t in rt0) and
                                any(valid_tags[t] == "non-finite" for t in tt)):
                                tags = tuple(sorted(set(tt) | set(hdr_tags)))
                            else:
                                tags = tuple(sorted(set(tt) | set(rt0) |
                                                    set(hdr_tags)))
                            new_rowtags.add(tags)
                rowtags = new_rowtags
                new_coltags = set(x for x in new_coltags
                                  if not any(t in noinherit_tags for t in x))
                # print("new_coltags={} previously_seen={} all_hdr_tags={}"
                #       .format(new_coltags, previously_seen, all_hdr_tags))
                if any(new_coltags):
                    hdrspan = HdrSpan(j, colspan, rowspan, rownum,
                                      new_coltags, col, all_headers)
                    hdrspans.append(hdrspan)
                    # Handle headers that are above left-side header
                    # columns and are followed by personal pronouns in
                    # remaining columns (basically headers that
                    # evaluate to no tags).  In such cases widen the
                    # left-side header to the full row.
                    if previously_seen:
                        col0_followed_by_nonempty = True
                        continue
                    elif col0_hdrspan is None:
                        assert col0_hdrspan is None
                        col0_hdrspan = hdrspan
                    elif any(all_hdr_tags):
                        col0_cats = tagset_cats(col0_hdrspan.tagsets)
                        later_cats = tagset_cats(all_hdr_tags)
                        if lang in col0_expand_allowed:
                            col0_allowed, later_allowed = \
                                col0_expand_allowed[lang]
                        else:
                            col0_allowed, later_allowed = \
                                col0_expand_allowed["default"]
                        # print("col0_cats={} later_cats={} "
                        #       "fol_by_nonempty={} j={} end={} "
                        #       "tagsets={}"
                        #       .format(col0_cats, later_cats,
                        #               col0_followed_by_nonempty, j,
                        #               col0_hdrspan.start +
                        #               col0_hdrspan.colspan,
                        #               col0_hdrspan.tagsets))
                        # print("col0.rowspan={} rowspan={}"
                        #       .format(col0_hdrspan.rowspan, rowspan))
                        # Only expand if col0_cats and later_cats are allowed
                        # and don't overlap and col0 has tags, and there have
                        # been no disallowed cells in between.
                        #
                        # There are three cases here:
                        #   - col0_hdrspan set, continue with allowed current
                        #   - col0_hdrspan set, expand, start new
                        #   - col0_hdrspan set, no expand, start new
                        if (not col0_followed_by_nonempty and
                            # Only one cat of tags: kunna/Swedish
                            len(col0_cats) == 1 and
                            col0_hdrspan.rowspan >= rowspan and
                            not (col0_cats - col0_allowed) and
                            not (later_cats - later_allowed) and
                            not (col0_cats & later_cats)):
                            # First case: col0 set, continue
                            print("CONT")
                            continue
                        # We are going to start new col0_hdrspan.  Check if
                        # we should expand.
                        if (not col0_followed_by_nonempty and
                            len(col0_cats) == 1 and
                            j > col0_hdrspan.start + col0_hdrspan.colspan):
                            # Expand current col0_hdrspan
                            print("EXPANDING COL0 MID: {} from {} to {} "
                                  "cols {}"
                                  .format(col0_hdrspan.text,
                                          col0_hdrspan.colspan,
                                          j - col0_hdrspan.start,
                                          col0_hdrspan.tagsets))
                            col0_hdrspan.colspan = j - col0_hdrspan.start
                            col0_hdrspan.expanded = True
                        # Clear old col0_hdrspan
                        if col == debug_word:
                            print("START NEW {}".format(hdrspan.tagsets))
                        col0_hdrspan = None
                        # Now start new, unless it comes from previous row
                        if not previously_seen:
                            col0_hdrspan = hdrspan
                            col0_followed_by_nonempty = False
                continue

            # It is a normal text cell
            if col in IGNORED_COLVALUES:
                continue

            # These values are ignored, at least form now
            if re.match(r"^(# |\(see )", col):
                continue

            if j == 0 and (not col_has_text or not col_has_text[0]):
                continue  # Skip text at top left, as in Icelandic, Faroese
            # if col0_hdrspan is not None:
            #     print("COL0 FOLLOWED NONHDR: {!r} by {!r}"
            #           .format(col0_hdrspan.text, col))
            col0_followed_by_nonempty = True
            have_text = True
            while len(col_has_text) <= j:
                col_has_text.append(False)
            col_has_text[j] = True
            # Determine column tags for the multi-column cell
            combined_coltags = compute_coltags(lang, pos, hdrspans, j,
                                               colspan, True, col)
            # print("HAVE_TEXT:", repr(col))
            # Split the text into separate forms.  First simplify spaces except
            # newline.
            col = re.sub(r"[ \t\r]+", " ", col)
            # Split the cell text into alternatives
            if col and is_superscript(col[0]):
                alts = [col]
            else:
                separators = [";", "•", r"\n", " or "]
                if col.find(" + ") < 0:
                    separators.append(",")
                    if not col.endswith("/"):
                        separators.append("/")
                alts = split_at_comma_semi(col, separators=separators)
            # Remove "*" from beginning of forms, as in non-attested
            # or reconstructed forms.  Otherwise it might confuse romanization
            # detection.
            alts = list(x[1:] if re.match(r"\*[^ ]", x) else x
                        for x in alts)
            alts = list(x for x in alts
                        if not re.match(r"pronounced with |\(with ", x))
            # Handle the special case where romanization is given under
            # normal form, e.g. in Russian.  There can be multiple
            # comma-separated forms in each case.  We also handle the case
            # where instead of romanization we have IPA pronunciation
            # (e.g., avoir/French/verb).
            len2 = len(alts) // 2
            if (len(alts) % 2 == 0 and
                all(re.match(r"^\s*/.*/\s*$", x)
                    for x in alts[len2:])):
                alts = list((alts[i], "", alts[i + len2])
                            for i in range(len2))
            elif (len(alts) % 2 == 0 and
                  not any(x.find("(") >= 0 for x in alts) and
                  all(classify_desc(re.sub(r"\^.*$", "",
                                           "".join(xx for xx in x
                                                   if not is_superscript(xx))))
                      == "other"
                      for x in alts[:len2]) and
                  all(classify_desc(re.sub(r"\^.*$", "",
                                           "".join(xx for xx in x
                                                   if not is_superscript(xx))))
                      in ("romanization", "english")
                      for x in alts[len2:])):
                alts = list((alts[i], alts[i + len2], "")
                            for i in range(len2))
            else:
                new_alts = []
                for alt in alts:
                    if alt.find(" ") >= 0:
                        new_alts.append(alt)
                    else:
                        lst = [""]
                        idx = 0
                        for m in re.finditer(r"(^|\w)\((\w(\w\w?)?)\)",
                                             alt):
                            new_lst = []
                            for x in lst:
                                x += alt[idx: m.start()] + m.group(1)
                                idx = m.end()
                                new_lst.append(x)
                                new_lst.append(x + m.group(2))
                            lst = new_lst
                        for x in lst:
                            new_alts.append(x + alt[idx:])
                alts = list((x, "", "") for x in new_alts)
            # Generate forms from the alternatives
            for form, base_roman, ipa in alts:
                form = form.strip()
                extra_tags = []
                form, refs, defs, hdr_tags = clean_header(word, form, False)
                extra_tags.extend(hdr_tags)
                if base_roman:
                    base_roman, _, _, hdr_tags = clean_header(word, base_roman,
                                                              False)
                    extra_tags.extend(hdr_tags)
                # Do some additional clenanup on the cell.
                form = re.sub(r"^\s*,\s*", "", form)
                form = re.sub(r"\s*,\s*$", "", form)
                form = re.sub(r"\s*(,\s*)+", ", ", form)
                form = re.sub(r"(?i)^Main:", "", form)
                form = re.sub(r"\s+", " ", form)
                form = form.strip()
                # Handle parentheses in the table element.  We parse
                # tags anywhere and romanizations anywhere but beginning.
                roman = base_roman
                m = re.search(r"\s*\(([^)]*)\)", form)
                if m is not None:
                    paren = m.group(1)
                    if classify_desc(paren) == "tags":
                        tagsets1, topics1 = decode_tags(paren)
                        if not topics1:
                            for ts in tagsets1:
                                ts = list(x for x in ts
                                          if x.find(" ") < 0)
                                extra_tags.extend(ts)
                            form = (form[:m.start()] + " " +
                                    form[m.end():]).strip()
                    elif (m.start() > 0 and not roman and
                          classify_desc(form[:m.start()]) == "other" and
                          classify_desc(paren) in ("romanization", "english")
                          and not re.search(r"^with |-form$", paren)):
                        roman = paren
                        form = (form[:m.start()] + " " + form[m.end():]).strip()
                    elif re.search(r"^with |-form", paren):
                        form = (form[:m.start()] + " " + form[m.end():]).strip()
                # Ignore certain forms that are not really forms
                if form in ("", "not used", "not applicable", "unchanged",
                            "after an",  # in sona/Irish/Adj/Mutation
                ):
                    continue
                # print("ROWTAGS:", rowtags)
                # print("COLTAGS:", combined_coltags)
                # print("FORM:", repr(form))
                # Merge column tags and row tags.  We give preference
                # to moods etc coming from rowtags (cf. austteigen/German/Verb
                # imperative forms).
                for rt in sorted(rowtags):
                    for ct in sorted(combined_coltags):
                        tags = set(global_tags)
                        tags.update(extra_tags)
                        tags.update(rt)
                        # Merge tags from column.  For certain kinds of tags,
                        # those coming from row take precedence.
                        old_tags = set(tags)
                        for t in ct:
                            c = valid_tags[t]
                            if (c in ("mood",) and
                                any(valid_tags[tt] == c
                                    for tt in old_tags)):
                                continue
                            tags.add(t)

                        # Extract language-specific tags from the
                        # form.  This may also adjust the form.
                        form, lang_tags = lang_specific_tags(lang, pos, form)
                        tags.update(lang_tags)
                        # For non-finite verb forms, see if they would have
                        # a gender/class suffix
                        if pos == "verb" and any(valid_tags[t] == "non-finite"
                               for t in tags):
                            form, tt = parse_head_final_tags(ctx, lang, form)
                            tags.update(tt)

                        # Remove "personal" tag if have nth person; these
                        # come up with e.g. reconhecer/Portuguese/Verb.  But
                        # not if we also have "pronoun"
                        if ("personal" in tags and
                            "pronoun" not in tags and
                            any(x in tags for x in
                               ["first-person", "second-person",
                                "third-person"])):
                            tags.remove("personal")

                        # If we have impersonal, remove person and number.
                        # This happens with e.g. viajar/Portuguese/Verb
                        if "impersonal" in tags:
                            tags = tags - set(["first-person", "second-person",
                                               "third-person",
                                               "singular", "plural"])

                        # Remove unnecessary "positive" tag from verb forms
                        if pos == "verb" and "positive" in tags:
                            if "negative" in tags:
                                tags.remove("negative")
                            tags.remove("positive")

                        # Many Russian (and other Slavic?) inflection tables
                        # have animate/inanimate distinction that generates
                        # separate entries for neuter/feminine, but the
                        # distinction only applies to masculine.  Remove them
                        # form neuter/feminine and eliminate duplicates.
                        if lang in MASC_ANIMATE_LANGS:
                            for t1 in ("animate", "inanimate"):
                                for t2 in ("neuter", "feminine"):
                                    if (t1 in tags and t2 in tags and
                                        "masculine" not in tags and
                                        "plural" not in tags):
                                        tags.remove(t1)

                        # Remove the dummy mood tag that we sometimes
                        # use to block adding other mood and related
                        # tags
                        tags = tags - set(["dummy-mood"])

                        # Perform language-specific tag replacements according
                        # to rules in a table.
                        changed = True
                        while changed:
                            changed = False
                            for lst in lang_tag_mappings:
                                assert isinstance(lst, (list, tuple))
                                assert len(lst) >= 3
                                if lang not in lst[0] or pos not in lst[1]:
                                    continue
                                for src, dst in lst[2:]:
                                    assert isinstance(src, (list, tuple))
                                    assert isinstance(dst, (list, tuple))
                                    if all(t in tags for t in src):
                                        tags = (tags - set(src)) | set(dst)
                                        changed = True

                        # Add the form
                        tags = list(sorted(tags))
                        dt = {"form": form, "tags": tags, "source": source}
                        if roman:
                            dt["roman"] = roman
                        if ipa:
                            dt["ipa"] = ipa
                        ret.append(dt)
        # End of row.
        rownum += 1
        # For certain listed languages, if the row was empty, reset
        # hdrspans (saprast/Latvian/Verb, but not aussteigen/German/Verb).
        if row_empty and lang in EMPTY_ROW_RESETS_LANGS:
            hdrspans = []
        # Check if we should expand col0_hdrspan.
        if col0_hdrspan is not None:
            if lang in col0_expand_allowed:
                col0_allowed, later_allowed = \
                    col0_expand_allowed[lang]
            else:
                col0_allowed, later_allowed = \
                    col0_expand_allowed["default"]
            col0_cats = tagset_cats(col0_hdrspan.tagsets)
            # Only expand if col0_cats and later_cats are allowed
            # and don't overlap and col0 has tags, and there have
            # been no disallowed cells in between.
            if (not col0_followed_by_nonempty and
                not (col0_cats - col0_allowed) and
                j > col0_hdrspan.start + col0_hdrspan.colspan and
                len(col0_cats) == 1):
                # If an earlier header is only followed by headers that yield
                # no tags, expand it to entire row
                # print("EXPANDING COL0: {} from {} to {} cols {}"
                #       .format(col0_hdrspan.text, col0_hdrspan.colspan,
                #               len(row) - col0_hdrspan.start,
                #               col0_hdrspan.tagsets))
                col0_hdrspan.colspan = len(row) - col0_hdrspan.start
                col0_hdrspan.expanded = True
    # XXX handle refs and defs
    # for x in hdrspans:
    #     print("  HDRSPAN {} {} {} {!r}"
    #           .format(x.start, x.colspan, x.tagsets, x.text))

    # Post-process German nouns with articles
    if any("noun" in x["tags"] for x in ret):
        if lang in ("Alemannic German", "Cimbrian", "German",
                    "German Low German", "Hunsrik", "Luxembourish",
                    "Pennsylvania German"):
            new_ret = []
            for dt in ret:
                tags = dt["tags"]
                if "noun" in tags:
                    tags = list(t for t in tags if t != "noun")
                elif "indefinite" in tags or "definite" in tags:
                    continue  # Skip the articles
                # XXX remove: alternative code that adds "article" tag
                #     tags = list(sorted(set(tags) | set(["article"])))
                dt = dt.copy()
                dt["tags"] = tags
                new_ret.append(dt)
            ret = new_ret

    if word_tags:
        word_tags = list(sorted(set(word_tags)))
        dt = {"form": " ".join(word_tags),
              "source": source + " title",
              "tags": ["word-tags"]}
        ret.append(dt)

    return ret


def handle_generic_table(ctx, data, word, lang, pos, rows, titles, source):
    assert isinstance(ctx, Wtp)
    assert isinstance(data, dict)
    assert isinstance(word, str)
    assert isinstance(lang, str)
    assert isinstance(pos, str)
    assert isinstance(rows, list)
    assert isinstance(source, str)
    for row in rows:
        assert isinstance(row, list)
        for x in row:
            assert isinstance(x, InflCell)
    assert isinstance(titles, list)
    for x in titles:
        assert isinstance(x, str)

    # Try to parse the table as a simple table
    ret = parse_simple_table(ctx, word, lang, pos, rows, titles, source)
    if ret is None:
        # XXX handle other table formats
        # We were not able to handle the table
        return

    # Add the returned forms but eliminate duplicates.
    have_forms = set()
    for dt in data.get("forms", ()):
        have_forms.add(freeze(dt))
    for dt in ret:
        fdt = freeze(dt)
        if fdt in have_forms:
            continue  # Don't add duplicates Some Russian words have
        # Declension and Pre-reform declension partially duplicating
        # same data.  Don't add "dated" tags variant if already have
        # the same without "dated" from the modern declension table
        tags = dt.get("tags", [])
        for dated_tag in ("dated",):
            if dated_tag in tags:
                dt2 = dt.copy()
                tags2 = list(x for x in tags if x != dated_tag)
                dt2["tags"] = tags2
                if tags2 and freeze(dt2) in have_forms:
                    break  # Already have without archaic
        else:
            have_forms.add(fdt)
            data_append(ctx, data, "forms", dt)


def handle_wikitext_table(config, ctx, word, lang, pos,
                          data, tree, titles, source):
    """Parses a table from parsed Wikitext format into rows and columns of
    InflCell objects and then calls handle_generic_table() to parse it into
    forms.  This adds the forms into ``data``."""
    assert isinstance(config, WiktionaryConfig)
    assert isinstance(ctx, Wtp)
    assert isinstance(word, str)
    assert isinstance(lang, str)
    assert isinstance(pos, str)
    assert isinstance(data, dict)
    assert isinstance(tree, WikiNode)
    assert tree.kind == NodeKind.TABLE
    assert isinstance(titles, list)
    assert isinstance(source, str)
    for x in titles:
        assert isinstance(x, str)
    # Imported here to avoid a circular import
    from wiktextract.page import clean_node, recursively_extract
    # print("HANDLE_WIKITEXT_TABLE", titles)

    cols_fill = []    # Filling for columns with rowspan > 1
    cols_filled = []  # Number of remaining rows for which to fill the column
    cols_headered = []  # True when column contains headers even if normal fmt
    rows = []
    assert tree.kind == NodeKind.TABLE
    for node in tree.children:
        if not isinstance(node, WikiNode):
            continue
        kind = node.kind
        # print("  {}".format(node))
        if kind == NodeKind.TABLE_CAPTION:
            # print("  CAPTION:", node)
            pass
        elif kind == NodeKind.TABLE_ROW:
            if "vsShow" in node.attrs.get("class", "").split():
                # vsShow rows are those that are intially shown in tables that
                # have more data.  The hidden data duplicates these rows, so
                # we skip it and just process the hidden data.
                continue

            # Parse a table row.
            row = []
            style = None
            for col in node.children:
                if not isinstance(col, WikiNode):
                    continue
                kind = col.kind
                if kind not in (NodeKind.TABLE_HEADER_CELL,
                                NodeKind.TABLE_CELL):
                    print("    UNEXPECTED ROW CONTENT: {}".format(col))
                    continue
                while len(row) < len(cols_filled) and cols_filled[len(row)] > 0:
                    cols_filled[len(row)] -= 1
                    row.append(cols_fill[len(row)])
                try:
                    rowspan = int(col.attrs.get("rowspan", "1"))
                    colspan = int(col.attrs.get("colspan", "1"))
                except ValueError:
                    rowspan = 1
                    colspan = 1
                # print("COL:", col)

                # Process any nested tables recursively.  XXX this
                # should also take prior text before nested tables as
                # headers, e.g., see anglais/Irish/Declension ("Forms
                # with the definite article" before the table)
                tables, rest = recursively_extract(col, lambda x:
                                                   isinstance(x, WikiNode) and
                                                   x.kind == NodeKind.TABLE)

                # Clean the rest of the cell.
                celltext = clean_node(config, ctx, None, rest)
                # print("CLEANED:", celltext)

                # Handle nested tables.
                for tbl in tables:
                    # Some nested tables (e.g., croí/Irish) have subtitles
                    # as normal paragraphs in the same cell under a descriptive
                    # test that should be treated as a title (e.g.,
                    # "Forms with the definite article", with "definite" not
                    # mentioned elsewhere).
                    new_titles = list(titles)
                    if celltext:
                        new_titles.append(celltext)
                    handle_wikitext_table(config, ctx, word, lang, pos, data,
                                          tbl, new_titles, source)

                # This magic value is used as part of header detection
                cellstyle = (col.attrs.get("style", "") + "//" +
                             col.attrs.get("class", "") + "//" +
                             str(kind))
                if not row:
                    style = cellstyle
                target = None
                idx = celltext.find(": ")
                is_title = False
                if idx >= 0 and celltext[:idx] in infl_map:
                    target = celltext[idx + 2:].strip()
                    # XXX add tags from target
                    celltext = celltext[:idx]
                    is_title = True
                elif ((kind == NodeKind.TABLE_HEADER_CELL and
                       celltext.find(" + ") < 0) or
                      (re.sub(r"\s+", " ",
                              re.sub(r"\s*\([^)]*\)", "",
                                     celltext)).strip() in infl_map and
                       celltext != word and
                       celltext not in ("I", "es")) or
                      (style == cellstyle and
                       celltext != word and
                       not style.startswith("////") and
                       celltext.find(" + ") < 0)):
                    is_title = True
                if (not is_title and len(row) < len(cols_headered) and
                    cols_headered[len(row)]):
                    # Whole column has title suggesting they are headers
                    # (e.g. "Case")
                    is_title = True
                if re.match(r"Conjugation of |Declension of |Inflection of|"
                            r"Mutation of",
                            celltext):
                    is_title = True
                if is_title:
                    while len(cols_headered) <= len(row):
                        cols_headered.append(False)
                    v = expand_header(ctx, word, lang, pos, celltext, [],
                                      silent=True)
                    if any("*" in tt for tt in v):
                        cols_headered[len(row)] = True
                        celltext = ""
                # XXX extra tags, see "target" above
                cell = InflCell(celltext, is_title, len(row), colspan, rowspan)
                for i in range(0, colspan):
                    if rowspan > 1:
                        while len(cols_fill) <= len(row):
                            cols_fill.append(None)
                            cols_filled.append(0)
                        cols_fill[len(row)] = cell
                        cols_filled[len(row)] = rowspan - 1
                    row.append(cell)
            if not row:
                continue
            while len(row) < len(cols_fill) and cols_filled[len(row)] > 0:
                cols_filled[len(row)] -= 1
                row.append(cols_fill[len(row)])
            # print("  ROW {!r}".format(row))
            rows.append(row)
        elif kind in (NodeKind.TABLE_HEADER_CELL, NodeKind.TABLE_CELL):
            # print("  TOP-LEVEL CELL", node)
            pass

    # Now we have a table that has been parsed into rows and columns of
    # InflCell objects.  Parse the inflection table from that format.
    handle_generic_table(ctx, data, word, lang, pos, rows, titles, source)


def handle_html_table(config, ctx, word, lang, pos, data, tree, titles, source):
    """Parses a table from parsed HTML format into rows and columns of
    InflCell objects and then calls handle_generic_table() to parse it into
    forms.  This adds the forms into ``data``."""
    assert isinstance(config, WiktionaryConfig)
    assert isinstance(ctx, Wtp)
    assert isinstance(word, str)
    assert isinstance(lang, str)
    assert isinstance(pos, str)
    assert isinstance(data, dict)
    assert isinstance(tree, WikiNode)
    assert tree.kind == NodeKind.HTML and tree.args == "table"
    assert isinstance(titles, list)
    for x in titles:
        assert isinstance(x, str)
    assert isinstance(source, str)

    ctx.debug("HTML TABLES NOT YET IMPLEMENTED at {}/{}"
              .format(word, lang))


def parse_inflection_section(config, ctx, data, word, lang, pos, section, tree):
    """Parses an inflection section on a page.  ``data`` should be the
    data for a part-of-speech, and inflections will be added to it."""

    # print("PARSE_INFLECTION_SECTION {}/{}/{}/{}"
    #       .format(word, lang, pos, section))
    assert isinstance(config, WiktionaryConfig)
    assert isinstance(ctx, Wtp)
    assert isinstance(data, dict)
    assert isinstance(word, str)
    assert isinstance(lang, str)
    assert pos in PARTS_OF_SPEECH
    assert isinstance(section, str)
    assert isinstance(tree, WikiNode)
    source = section

    def recurse_navframe(node, titles):
        titleparts = []

        def recurse1(node, in_navhead):
            if isinstance(node, (list, tuple)):
                for x in node:
                    recurse1(x, in_navhead)
                return
            if isinstance(node, str):
                titleparts.append(node)
                return
            if not isinstance(node, WikiNode):
                ctx.debug("inflection table: unhandled in NavFrame: {}"
                          .format(node))
                return
            kind = node.kind
            if kind == NodeKind.HTML:
                classes = node.attrs.get("class", "").split()
                if "NavToggle" in classes:
                    return
                if "NavHead" in classes:
                    # print("NAVHEAD:", node)
                    for x in node.children:
                        recurse1(x, True)
                    return
                if "NavContent" in classes:
                    title = "".join(titleparts).strip()
                    title = html.unescape(title)
                    title = title.strip()
                    new_titles = list(titles)
                    if not re.match(r"(Note:|Notes:)", title):
                        new_titles.append(title)
                    recurse(node, new_titles)
                    return
            elif kind == NodeKind.LINK:
                if len(node.args) > 1:
                    for x in node.args[1:]:
                        recurse1(x, in_navhead)
                else:
                    recurse1(node.args[0], in_navhead)
            for x in node.children:
                recurse1(x, in_navhead)
        recurse1(node, False)

    def recurse(node, titles):
        if not isinstance(node, WikiNode):
            return
        kind = node.kind
        if kind == NodeKind.TABLE:
            handle_wikitext_table(config, ctx, word, lang, pos,
                                  data, node, titles, source)
            return
        elif kind == NodeKind.HTML and node.args == "table":
            handle_html_table(config, ctx, word, lang, pos, data, node, titles,
                              source)
            return
        elif kind in (NodeKind.LEVEL2, NodeKind.LEVEL3, NodeKind.LEVEL4,
                      NodeKind.LEVEL5, NodeKind.LEVEL6):
            return  # Skip subsections
        if (kind == NodeKind.HTML and node.args == "div" and
            "NavFrame" in node.attrs.get("class", "").split()):
            recurse_navframe(node, titles)
            return
        for x in node.children:
            recurse(x, titles)

    assert tree.kind == NodeKind.ROOT
    for x in tree.children:
        recurse(x, [])

    # XXX this code is used for extracting tables for inflection tests
    if section != "Mutation":
        with open("temp.XXX", "w") as f:
            f.write(word + "\n")
            f.write(lang + "\n")
            f.write(pos + "\n")
            f.write(section + "\n")
            text = ctx.node_to_wikitext(tree)
            f.write(text + "\n")

# XXX check interdecir/Spanish - singular/plural issues

# XXX viajar/Portuguese: gerund has singular+plural - check if all columns
# containing same tag category are included, and then don't include anything
