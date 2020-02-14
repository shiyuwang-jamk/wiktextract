# Template processing definitions for Wiktionary parser for extracting
# lexicon and various other information from Wiktionary.
#
# Copyright (c) 2018-2020 Tatu Ylonen.  See file LICENSE and https://ylonen.org

# These Wiktionary templates are silently ignored (though some of them may be
# used when cleaning up titles and values).
ignored_templates = set([
    "+obj",
    "+OBJ",
    "+preo",
    "-",
    "=",
    "*",
    "!",
    ",",
    "0",
    "Book-B",
    "C",
    "Clade",  # XXX Might want to dig information from this for hypernyms
    "CURRENTYEAR",
    "enPRchar",
    "EtymOnLine",
    "EtymOnline",
    "George Monbiot",
    "IPAchar",
    "J2G",
    "JSTOR",
    "LCC",
    "LR",
    "NNBS",
    "OCLC",
    "PAGENAME",
    "Platyrrhini Hypernyms",
    "Q",
    "SIC",
    "Spanish possessive adjectives",
    "Spanish possessive pronouns",
    "Template:letter-shaped",
    "Template:object-shaped",
    "The Last Man",
    "Webster 1913",
    "\\",
    "abbreviation-old",
    "af",
    "affix",
    "affixes",
    "altcaps",
    "alter",
    "anchor",
    "ant",
    "ante",
    "antonyms",
    "attention",
    "attn",
    "audio",
    "back-form",
    "bor",
    "borrowed",
    "bottom",
    "bottom2",
    "bottom3",
    "bottom4",
    "bottom5",
    "bullet",
    "bullet list",
    "c",
    "catlangcode",
    "catlangname",
    "checksense",
    "circa",
    "circa2",
    "circumfixsee",
    "cite",
    "cite book",
    "Cite book",
    "Cite news",
    "cite news",
    "cite newsgroup",
    "cite-av",
    "cite-book",
    "cite-journal",
    "cite-magazine",
    "cite-news",
    "cite-newgroup",
    "cite-song",
    "cite-text",
    "cite-video",
    "cite-web",
    "cite web",
    "clear",
    "cln",
    "cog",
    "col-top",
    "col-bottom",
    "col",
    "col-u",
    "col1",
    "col1-u",
    "col2",
    "col2-u",
    "col3",
    "col3-u",
    "col4",
    "col4-u",
    "col5",
    "col5-u",
    "colorbox",
    "color panel",
    "colour panel",
    "common names of Valerianella locusta",
    "compass",
    "compass-fi",
    "construed with",
    "coordinate terms",
    "cot",
    "datedef",
    "def-date",
    "defdate",
    "defdt",
    "defn",
    "demonstrative-accent-usage",
    "der",
    "der1",
    "der2",
    "der3",
    "Template:User:Donnanz/der3-u",
    "der4",
    "der5",
    "der bottom",
    "der-bottom",
    "der-bottom2",
    "der-bottom3",
    "der-bottom4",
    "der-mid2",
    "der-mid3",
    "der-mid4",
    "der-mid",
    "der top",
    "der-top",
    "der-top2",
    "der-top3",
    "der-top4",
    "derived",
    "derived terms",
    "dot",
    "doublet",
    "eggcorn of",
    "ellipsis",
    "em dash",
    "en dash",
    "es-demonstrative-accent-usage",
    "etyl",
    "example needed",
    "examples",
    "examples-right",
    "frac",
    "g",  # gender - too rare to be useful  XXX chk with other langs
    "gbooks",
    "gloss-stub",
    "holonyms",
    "hot sense",
    "hyp2",
    "hyp-top",
    "hyp-top2",
    "hyp-top3",
    "hyp-top4",
    "hyp-top5",
    "hyp-mid",
    "hyp-mid2",
    "hyp-mid3",
    "hyp-mid4",
    "hyp-mid5",
    "hyp-bottom",
    "hyp-bottom3",
    "hyp-bottom4",
    "hypo",
    "hyponyms",
    "hyper",
    "hypernyms",
    "indtr",
    "inh",
    "inherited",
    "interfixsee",
    "interwiktionary",
    "ISO 639",
    "ja-kanjitab",
    "jump",
    "katharevousa",
    "ko-inline",
    "lang",
    "list",
    "ll",
    "lookfrom",
    "Lookfrom",
    "maintenance line",
    "mediagenic terms",
    "mer",
    "meronyms",
    "mid",
    "mid2",
    "mid3",
    "mid4",
    "mid4",
    "mid5",
    "middot",
    "mul-kangxi radical-def",
    "mul-shuowen radical-def",
    "multiple images",
    "nbsp",
    "ndash",
    "no entry",
    "noncog",
    "noncognate",
    "nowrap",
    "nuclide",
    "object-shaped",
    "overline",
    "phrasebook",
    "pedia",
    "pedialite",
    "picdic",
    "picdiclabel",
    "picdiclabel/new",
    "polyominoes",
    "pos_v",
    "post",
    "prefixlanglemma",
    "prefixsee",
    "presidential nomics",
    "projectlink",
    "punctuation",
    "quote web",
    "quote-av",
    "quote-book",
    "quote-booken",
    "quote-hansard",
    "quote-journal",
    "quote-journalen",
    "quote-magazine",
    "quote-news",
    "quote-newsgroup",
    "quote-song",
    "quote-text",
    "quote-us-patent",
    "quote-video",
    "quote-video game",
    "quote-web",
    "quote-webpage",
    "quote-wikipedia",
    "quotebook",
    "redirect",
    "refn",
    "rel1",
    "rel2",
    "rel3",
    "rel4",
    "rel5",
    "rel-bottom",
    "rel-mid",
    "rel-mid2",
    "rel-mid3",
    "rel-mid4",
    "rel-mid5",
    "rel-top",
    "rel-top2",
    "rel-top3",
    "rel-top4",
    "rel-top5",
    "rootsee",
    "rfap",
    "rfc",
    "rfc-auto",
    "rfc-citation",
    "rfc-def",
    "rfc-header",
    "rfc-level",
    "rfc-subst",
    "rfc-tsort",
    "rfc-sense",
    "rfcite-sense",
    "rfclarify",
    "rfd-redundant",
    "rfd-sense",
    "rfdate",
    "rfdatek",
    "rfdatke",
    "rfdatekCornhill Magazine",
    "rfdatekShakespeare",
    "rfdef",
    "rfe",
    "rfex",
    "rfexample",
    "rfm-sense",
    "rfgloss",
    "rfquote",
    "rfquote-sense",
    "rfquotek",
    "rft-sense",
    "rftranslator",
    "rftranslit",
    "rfv-quote",
    "rfv-sense",
    "rhymes",
    "rhymes",
    "roa-opt-cite-cantigas",
    "see",
    "see also",
    "seeCites",
    "seemoreCites",
    "seemorecites",
    "seeMoreCites",
    "seeSynonyms",
    "senseid",
    "smallcaps",
    "soplink",
    "source",
    "spndash",
    "stroke order",
    "stub-gloss",
    "sub",
    "suffixsee",
    "suffixusex",
    "sup",
    "syn",
    "syndiff",
    "synonym",
    "synonyms",
    "t-check",
    "t+check",
    "tea room sense",
    "top",
    "top2",
    "top3",
    "top4",
    "top5",
    "topic",
    "topics",
    "translation only",
    "translation hub",
    "trans-mid",
    "trans-bottom",
    "uncertain",
    "unk",
    "unsupported",
    "used in phrasal verbs",
    "usex",
    "ux",
    "uxi",
    "vi-der",
    "video frames",
    "w:William Logan (poet)",
    "was wotd",
    "wikisaurus:movement",
    "wikisource1911Enc",
    "wikivoyage",
    "ws",
    "ws link",
    "wsource",
    "zh-cat",
    "zh-dial",
    "zh-der",
    "zh-hg",
])

# Templates ({{name|...}}) that will be replaced by the value of their
# first argument when cleaning up titles/values.
clean_arg1_tags = [
    "1",
    "W",
    "Wikipedia",
    "wtorw",
    "glossary",
    "overwrite",
    "pedlink",
    "pedlink",
    "slim-wikipedia",
    "smc",
    "sub",  # XXX change
    "sup",  # XXX change
    "swp",
    "taxlink",
    "taxlinknew",
    "unsupported",
    "upright",
    "verb",
    "vern",
    "zh-m",
    "zh-classifier",
]

# Templates that will be replaced by their second argument when cleaning up
# titles/values.
clean_arg2_tags = [
    "defn",
    "t+",
]

# Templates that will be replaced by their third argument when cleaning up
# titles/values.
clean_arg3_tags = [
]

# Templates that will be replaced by a value when cleaning up titles/values.
# The replacements may refer to the first argument of the template using \1.
#
# Note that there is a non-zero runtime cost for each replacement in this
# dictionary; keep its size reasonable.
clean_replace_map = {
    '18th c.': ['18th century'],
    'c.': ["c. {arg1}"],
    'ca.': ["c. {arg1}"],
    'a.': ["a. {arg1}"],
    'en dash': [' - '],
    'em dash': [' - '],
    'ndash': [' - '],
    '\\': [' / '],
    '...': [' [...] '],
    '…': [' [...] '],
    '..': [' [...] '],
    'nb...': [' [...] '],
    'sic': [' [sic, meaning {arg1}]', ' [sic] '],
    "'": ["'"],
    '@': ['@'],
    'mdash': ['--'],
    'BCE': ['BCE'],
    'B.C.E.': ['B.C.E.'],
    'CE': ['CE'],
    'C.E.': ['C.E.'],
    'BC': ['BC'],
    'BCE': ['BCE'],
    'B.C.': ['B.C.'],
    'A.D.': ['A.D.'],
    'AD': ['AD'],
    'C.': ['{arg1}{arg2} century', '{arg1}th century'],
    "sqbrace": ['[{arg1}]'],
    'CURRENTDAY': ["15"],
    'CURRENTMONTHNAME': ["February"],
    'CURRENTYEAR': ["1873"],
    'nc': ["{arg3}", "{arg2}"],
    "prefix": ["{arg1} + {arg2}"],
    "morse code for": ['morse code for "{arg1}" ({gloss})',
                       'morse code for "{arg1}"',
                       'morse code for "{gloss}"'],
    "zh-l": ["{arg1}; {arg2} ({arg3}; {arg4})",
             "{arg1} ({arg2}; {arg3})",
             "{arg1} ({arg2})",
             "{arg1} ({tr}; {gloss})",
             "{arg1} ({gloss})",
             "{arg1}"],
    "ja-l": ["{arg1}; {arg2} ({arg3}; {arg4})",
             "{arg1} ({arg2}; {arg3})",
             "{arg1} ({arg2})",
             "{arg1} ({tr}; {gloss})",
             "{arg1} ({gloss})",
             "{arg1}"],
    "ko-l": ["{arg1}; {arg2} ({arg3}; {arg4})",
             "{arg1} ({arg2}; {arg3})",
             "{arg1} ({arg2})",
             "{arg1} ({tr}; {gloss})",
             "{arg1} ({gloss})",
             "{arg1}"],
    "th-l": ["{arg1}; {arg2} ({arg3}; {arg4})",
             "{arg1} ({arg2}; {arg3})",
             "{arg1} ({arg2})",
             "{arg1} ({tr}; {gloss})",
             "{arg1} ({gloss})",
             "{arg1}"],
    "vi-l": ["{arg1}; {arg2} ({arg3}; {arg4})",
             "{arg1} ({arg2}; {arg3})",
             "{arg1} ({arg2})",
             "{arg1} ({tr}; {gloss})",
             "{arg1} ({gloss})",
             "{arg1}"],
    "l/gl": ["{arg1}"],
    "specieslite": ["{arg1}", "{word}"],
    #'sumti': [r'x\1'],
    'initialism of': [r'initialism of "{arg3}" ({arg4})',
                      r'initialism of "{arg2}" ({arg4})',
                      r'initialism of "{arg3}"',
                      r'initialism of "{arg2}"'],
    'init of': [r'initialism of "{arg3}" ({arg4})',
                r'initialism of "{arg2}" ({arg4})',
                r'initialism of "{arg3}"',
                r'initialism of "{arg2}"'],
    'Nom form of': [r'Vietnamese Nôm form of "{arg1}" ({arg2})',
                    r'Vietnamese Nôm form of "{arg1}"'],
    'Han tu form of': [r'Vietnamese Hán reading "{arg1}" ({arg2})',
                       r'Vietnamese Hán reading "{arg1}"'],
    'Han form of': [r'Vietnamese Hán reading "{arg1}" ({arg2})',
                    r'Vietnamese Hán reading "{arg1}"'],
    'hanja form of': [r'Korean hanja form of "{arg1}" ({arg2})',
                      r'Korean hanja form of "{arg1}"'],
    'present participle of': [r'present participle of "{arg2}"'],
    'past participle of': [r'past participle of "{arg2}"'],
    'synonym of': [r'synonym of "{arg2}"'],
    'syn of': [r'synonym of "{arg2}"'],
    'given name': [r'{arg2} given name', r'{gender} given name',
                   r'{from} given name', r"given name"],
    'forename': [r'{arg2} forename', r'{gender} forename'],
    'historical given name': [r'{arg2} historical given name',
                              r"historical given name"],
    'compound': ['{arg1} + {arg2} + {arg3}',
                 '{arg1} + {arg2}'],
    'suf': ['{arg1} + {arg2}'],
    'suffix': ['{arg2} + {arg3}', "_ + {arg3}"],
    "confix": ['{arg2} + {arg3}'],
    'surname': ['{A} surname',
                'surname'],
    'spelling of': ['{arg2} spelling of "{arg3}" ({t})',
                    '{arg2} spelling of "{arg3}"'],
    'form of': ['{arg2} of "{arg3}"'],
    'abbreviated': ['(abbreviated {arg2})'],
    'abbr': ['{arg1}'],
    'clipping': ['clipping of "{arg2}" ({arg4})',
                 'clipping of "{arg2}"'],
    'clipping of': ['clipping of "{arg2}" ({arg4})',
                    'clipping of "{arg2}"'],
    'clip of': ['clipping of "{arg2}" ({arg4})',
                'clipping of "{arg2}"'],
    'contraction of': ['contraction of "{arg2}" ({arg4})',
                       'contraction of "{arg2}"'],
    'aphetic form of': ['aphetic form of "{arg2}" ({arg4})',
                        'aphetic form of "{arg2}"'],
    'abbreviation of': ['abbreviation of "{arg3}" ({arg4})',
                        'abbreviation of "{arg2}" ({arg4})',
                        'abbreviation of "{arg3}"',
                        'abbreviation of "{arg2}"'],
    'abbr of': ['abbreviation of "{arg3}" ({arg4})',
                'abbreviation of "{arg2}" ({arg4})',
                'abbreviation of "{arg3}"',
                'abbreviation of "{arg2}"'],
    'ellipsis of': ['ellipsis of "{arg3}" ({arg4})',
                    'ellipsis of "{arg2}" ({arg4})',
                    'ellipsis of "{arg3}"',
                    'ellipsis of "{arg2}"'],
    'abbr of': ['abbreviation of "{arg2}" ({arg4})',
                'abbreviation of "{arg2}"'],
    'acronym of': ['acronym of "{arg3}" ({arg4})',
                   'acronym of "{arg2}" ({arg4})',
                   'acronym of "{arg3}"',
                   'acronym of "{arg2}"'],
    'obsolete typography of': ['obsolete typography of "{arg3}" ({arg4})',
                               'obsolete typography of "{arg2}" ({arg4})',
                               'obsolete typography of "{arg3}"',
                               'obsolete typography of "{arg2}"'],
    'alternative typography of': ['alternative typography of "{arg3}" ({arg4})',
                                  'alternative typography of "{arg2}" ({arg4})',
                                  'alternative typography of "{arg3}"',
                                  'alternative typography of "{arg2}"'],
    'misconstruction of': ['misconstruction of "{arg3}" ({arg4})',
                           'misconstruction of "{arg2}" ({arg4})',
                           'misconstruction of "{arg3}"',
                           'misconstruction of "{arg2}"'],
    'alt case': ['alternative case of "{arg3}" ({arg4})',
                 'alternative case of "{arg2}" ({arg4})',
                 'alternative case of "{arg3}"',
                 'alternative case of "{arg2}"'],
    'soft mutation of': ['soft mutation of "{arg3}" ({arg4})',
                         'soft mutation of "{arg2}" ({arg4})',
                         'soft mutation of "{arg3}"',
                         'soft mutation of "{arg2}"'],
    'mixed mutation of': ['mixed mutation of "{arg3}" ({arg4})',
                          'mixed mutation of "{arg2}" ({arg4})',
                          'mixed mutation of "{arg3}"',
                          'mixed mutation of "{arg2}"'],
    'hard mutation of': ['hard mutation of "{arg3}" ({arg4})',
                         'hard mutation of "{arg2}" ({arg4})',
                         'hard mutation of "{arg3}"',
                         'hard mutation of "{arg2}"'],
    'obsolete spelling of': ['obsolete spelling of "{arg2}" ({arg4})',
                             'obsolete spelling of "{arg2}"'],
    'obs sp': ['obsolete spelling of "{arg2}" ({arg4})',
               'obsolete spelling of "{arg2}"'],
    'obs form': ['obsolete form of "{arg2}" ({arg4})',
                 'obsolete form of "{arg2}"'],
    'alt sp': ['alternative spelling of "{arg2}" ({arg4})',
               'alternative spelling of "{arg2}"'],
    'obsolete form of': ['obsolete form of "{arg2}" ({arg4})',
                         'obsolete form of "{arg2}"'],
    'pronunciation spelling of': ['pronunciation spelling of "{arg2}" ({arg4})',
                                  'pronunciation spelling of "{arg2}"'],
    'apocopic form of': ['apocopic form of "{arg2}" ({arg4})',
                         'apocopic form of "{arg2}"'],
    'alternative form of': ['alternative form of "{arg2}" ({arg4})',
                            'alternative form of "{arg2}"'],
    'alternative_form_of': ['alternative form of "{arg2}" ({arg4})',
                            'alternative form of "{arg2}"'],
    'alternative case form of': ['alternative case form of "{arg2}" ({arg4})',
                                 'alternative case form of "{arg2}"'],
    'Template:alternative case form of': [
        'alternative case form of "{arg2}" ({arg4})',
        'alternative case form of "{arg2}"'],
    'honor alt case': ['honorific alternative case form of "{arg2}" ({arg4})',
                       'honorific alternative case form of "{arg2}"'],
    'elongated form of': ['elongated form of "{arg2}" ({arg4})',
                          'nonstandard form of "{arg2}"'],
    'nonstandard form of': ['nonstandard form of "{arg2}" ({arg4})',
                            'nonstandard form of "{arg2}"'],
    'nonstandard form of': ['nonstandard form of "{arg2}" ({arg4})',
                            'nonstandard form of "{arg2}"'],
    'nonstandard spelling of': ['nonstandard spelling of "{arg2}" ({arg4})',
                                'nonstandard spelling of "{arg2}"'],
    'standard form of': ['standard form of "{arg2}" ({arg4})',
                         'standard form of "{arg2}"'],
    'standard spelling of': ['standard spelling of "{arg2}" ({arg4})',
                             'standard spelling of "{arg2}"'],
    'stand sp': ['standard spelling of "{arg2}" ({arg4})',
                             'standard spelling of "{arg2}"'],
    'uncommon spelling of': ['uncommon spelling of "{arg2}" ({arg4})',
                             'uncommon spelling of "{arg2}"'],
    'uncommon form of': ['uncommon form of "{arg2}" ({arg4})',
                         'uncommon form of "{arg2}"'],
    'rare spelling of': ['rare spelling of "{arg2}" ({arg4})',
                         'rare spelling of "{arg2}"'],
    'rare form of': ['rare form of "{arg2}" ({arg4})',
                     'rare form of "{arg2}"'],
    'alt form': ['alternative form of "{arg2}" ({arg4})',
                 'alternative form of "{arg2}"'],
    'altform': ['alternative form of "{arg2}" ({arg4})',
                'alternative form of "{arg2}"'],
    'short for': ['short for "{arg2}" ({arg4})',
                  'short for "{arg2}"'],
    'informal form of': ['informal form of "{arg2}" ({arg4})',
                         'informal form of "{arg2}"'],
    'informal spelling of': ['informal spelling of "{arg2}" ({arg4})',
                             'informal spelling of "{arg2}"'],
    'used only in': ['used only in "{arg2}" ({arg4})',
                     'used only in "{arg2}"'],
    'only used in': ['only used in "{arg2}" ({arg4})',
                     'only used in "{arg2}"'],
    'alternative spelling of': ['alternative spelling of "{arg2}" ({arg4})',
                                'alternative spelling of "{arg2}"'],
    'alternative plural of': ['alternative plural of "{arg2}" ({arg4})',
                              'alternative plural of "{arg2}"'],
    'former name of': ['former name of "{arg2}" ({arg4})',
                       'former name of "{arg2}"'],
    'misspelling of': ['misspelling of "{arg2}" ({arg4})',
                       'misspelling of "{arg2}"'],
    'misspelling': ['misspelling of "{arg2}" ({arg4})',
                    'misspelling of "{arg2}"'],
    'missp': ['misspelling of "{arg2}" ({arg4})',
              'misspelling of "{arg2}"'],
    'misspelling form of': ['misspelling form of "{arg2}" ({arg4})',
                            'misspelling form of "{arg2}"'],
    'lenition of': ['lenition of "{arg2}" ({arg4})',
                    'lenition of "{arg2}"'],
    'city nickname': ['A nickname for "{arg2}"'],
    'deliberate misspelling of': ['deliberate misspelling of "{arg2}" ({arg4})',
                                  'deliberate misspelling of "{arg2}"'],
    'superseded spelling of': ['superseded spelling of "{arg2}" ({arg4})',
                               'superseded spelling of "{arg2}"'],
    'sup sp': ['superseded spelling of "{arg2}" ({arg4})',
                               'superseded spelling of "{arg2}"'],
    'archaic spelling of': ['archaic spelling of "{arg2}" ({arg4})',
                            'archaic spelling of "{arg2}"'],
    'archaic form of': ['archaic form of "{arg2}" ({arg4})',
                        'archaic form of "{arg2}"'],
    'dated form of': ['dated form of "{arg2}" ({arg4})',
                      'dated form of "{arg2}"'],
    'dated spelling of': ['dated spelling of "{arg2}" ({arg4})',
                          'dated form of "{arg2}"'],
    'syncopic form of': ['syncopic form of "{arg2}" ({arg4})',
                         'syncopic form of "{arg2}"'],
    'euphemistic form of': ['euphemistic form of "{arg2}" ({arg4})',
                            'euphemistic form of "{arg2}"'],
    'euphemistic spelling of': ['euphemistic spelling of "{arg2}" ({arg4})',
                                'euphemistic spelling of "{arg2}"'],
    'combining form of': ['combining form of "{arg2}" ({arg4})',
                          'combining form of "{arg2}"'],
    'present tense of': ['present tense of "{arg2}" ({arg4})',
                         'present tense of "{arg2}"'],
    'past tense of': ['past tense of "{arg2}" ({arg4})',
                      'past tense of "{arg2}"'],
    'imperative of': ['imperative of "{arg2}" ({arg4})',
                      'imperative of "{arg2}"'],
    'neuter singular of': ['neuter singular of "{arg2}" ({arg4})',
                           'neuter singular of "{arg2}"'],
    'feminine of': ['feminine of "{arg2}" ({arg4})',
                    'feminine of "{arg2}"'],
    'feminine singular of': ['feminine singular of "{arg2}" ({arg4})',
                           'feminine singular of "{arg2}"'],
    'feminine plural of': ['feminine plural of "{arg2}" ({arg4})',
                           'feminine plural of "{arg2}"'],
    'masculine plural of': ['masculine plural of "{arg2}" ({arg4})',
                            'masculine plural of "{arg2}"'],
    'masculine plural past participle of':
    ['masculine plural past participle of "{arg2}" ({arg4})',
     'masculine plural past participle of "{arg2}"'],
    'masculine singular past participle of':
    ['masculine singular past participle of "{arg2}" ({arg4})',
     'masculine singular past participle of "{arg2}"'],
    'feminine plural past participle of':
    ['feminine plural past participle of "{arg2}" ({arg4})',
     'feminine plural past participle of "{arg2}"'],
    'feminine singular past participle of':
    ['feminine singular past participle of "{arg2}" ({arg4})',
     'feminine singular past participle of "{arg2}"'],
    'masculine singular past participle of':
    ['masculine singular past participle of "{arg2}" ({arg4})',
     'masculine singular past participle of "{arg2}"'],
    'supine of':
    ['supine of "{arg2}" ({arg4})',
     'supine of "{arg2}"'],
    'definite singular of': ['definite singular of "{arg2}" ({arg4})',
                             'definite singular of "{arg2}"'],
    'definite plural of': ['definite plural of "{arg2}" ({arg4})',
                           'definite plural of "{arg2}"'],
    'indefinite plural of': ['indefinite plural of "{arg2}" ({arg4})',
                             'indefinite plural of "{arg2}"'],
    'genitive singular of': ['genitive singular of "{arg2}" ({arg4})',
                             'genitive singular of "{arg2}"'],
    'genitive of': ['genitive of "{arg2}" ({arg4})',
                    'genitive of "{arg2}"'],
    'dative singular of': ['dative singular of "{arg2}" ({arg4})',
                           'dative singular of "{arg2}"'],
    'dative plural of': ['dative plural of "{arg2}" ({arg4})',
                         'dative plural of "{arg2}"'],
    'dative of': ['dative of "{arg2}" ({arg4})',
                  'dative of "{arg2}"'],
    'augmentative of': ['augmentative of "{arg2}" ({arg4})',
                        'augmentative of "{arg2}"'],
    'accusative singular of': ['accusative singular of "{arg2}" ({arg4})',
                               'accusative singular of "{arg2}"'],
    'accusative plural of': ['accusative plural of "{arg2}" ({arg4})',
                             'accusative plural of "{arg2}"'],
    'superlative predicative of': ['superlative predicative of "{arg2}" ({arg4})',
                                   'superlative predicative of "{arg2}"'],
    'attributive form of': ['attributive form of "{arg3}" ({arg4})',
                            'attributive form of "{arg2}" ({arg4})',
                            'attributive form of "{arg3}"',
                            'attributive form of "{arg2}"'],
    'predicative form of': ['predicative form of "{arg3}" ({arg4})',
                            'predicative form of "{arg2}" ({arg4})',
                            'predicative form of "{arg3}"',
                            'predicative form of "{arg2}"'],
    'comparative of': ['comparative of "{arg2}" ({arg4})',
                       'comparative of "{arg2}"'],
    'superlative of': ['superlative of "{arg2}" ({arg4})',
                       'superlative of "{arg2}"'],
    'gerund of': ['gerund of "{arg2}" ({arg4})',
                  'gerund of "{arg2}"'],
    'reflexive of': ['reflexive of "{arg2}" ({arg4})',
                     'reflexive of "{arg2}"'],
    'plural of': ['plural of "{arg3}" ({arg4})',
                  'plural of "{arg2}" ({arg4})',
                  'plural of "{arg3}"',
                  'plural of "{arg2}"'],
    'singular of': ['singular of "{arg3}" ({arg4})',
                    'singular of "{arg2}" ({arg4})',
                    'singular of "{arg3}"',
                    'singular of "{arg2}"'],
    'singulative of': ['singulative of "{arg3}" ({arg4})',
                       'singulative of "{arg2}" ({arg4})',
                       'singulative of "{arg3}"',
                       'singulative of "{arg2}"'],
    'agent noun of': ['agent noun of "{arg2}" ({arg4})',
                      'agent noun of "{arg2}"'],
    'verbal noun of': ['verbal noun of "{arg2}" ({arg4})',
                       'verbal noun of "{arg2}"'],
    'eclipsis of': ['eclipsis of "{arg2}" ({arg4})',
                    'eclipsis of "{arg2}"'],
    'ga-lenition of': ['lenition of "{arg1}"'],
    't-prothesis of': ['t-prothesis of "{arg2}"'],
    'h-prothesis of': ['h-prothesis of "{arg2}"'],
    'abstract noun of': ['abstract noun of "{arg2}" ({arg4})',
                         'abstract noun of "{arg2}"'],
    'feminine noun of': ['feminine noun of "{arg2}" ({arg4})',
                         'feminine noun of "{arg2}"'],
    'masculine noun of': ['masculine noun of "{arg2}" ({arg4})',
                          'masculine noun of "{arg2}"'],
    'female equivalent of': ['female equivalent of "{arg2}" ({arg4})',
                             'female equivalent of "{arg2}"'],
    'diminutive of': ['diminutive of "{arg2}" ({arg4})',
                      'diminutive of "{arg2}"'],
    'dim of': ['diminutive of "{arg2}" ({arg4})',
               'diminutive of "{arg2}"'],
    'pejorative of': ['pejorative of "{arg2}" ({arg4})',
                      'pejorative of "{arg2}"'],
    'eye dialect of': ['eye dialect of "{arg2}" ({arg4})',
                       'eye dialect of "{arg2}"'],
    'native or resident of': ['native or resident of {arg1}'],
    'diminutive plural of': ['diminutive plural of "{arg2}"'],
    #'blend of': ['blend of {arg2}'],
    'transterm': ['[transl. {arg1}]', '[transl. {arg2}]'],
    'phrasal verb': ['used in "{arg1}"'],
    'ISBN': ['ISBN {arg1}'],
    'ISSN': ['ISSN {arg1}'],
    'en-comparative of': ['comparative of "{arg1}"'],
    'en-superlative of': ['superlative of "{arg1}"'],
    'en-third-person singular of': ['third person singular of "{arg1}"'],
    'en-third person singular of': ['third person singular of "{arg1}"'],
    'en-past of': ['past of "{arg1}"'],
    'en-ing form of': ['ing form of "{arg1}"'],
    'en-irregular plural of': ['irregular plural of "{arg1}"'],
    'en-archaic third-person singular of':
    ['archaic third-person singular of "{arg1}"'],
    'en-archaic second-person singular of':
    ['archaic second-person singular of "{arg1}"'],
    'en-archaic second-person singular past of':
    ['archaic second-person singular past of "{arg1}"'],
    'en-simple past of': ['simple past of "{arg1}"'],
    'sv-noun-form-def': ['definite form of "{arg1}"'],
    'sv-noun-form-def-pl': ['definite plural form of "{arg1}"'],
    'sv-noun-form-indef-pl': ['indefinite plural of "{arg1}"'],
    'sv-noun-form-indef-gen': ['indefinite genitive of "{arg1}"'],
    'sv-noun-form-indef-gen-pl': ['indefinite plural genitive of "{arg1}"'],
    'sv-noun-form-def-gen-pl': ['definite genitive plural of "{arg1}"'],
    'sv-noun-form-gen': ['genitive of "{arg1}"'],
    'sv-noun-form-def-gen': ['definite genitive of "{arg1}"'],
    'sv-noun-form-abs-def+pl': ['definite absolutive plural of "{arg1}"'],
    'sv-noun-form-abs-pl': ['absolutive plural of "{arg1}"'],
    'sv-proper-noun-gen': ['genitive of "{arg1}"'],
    'sv-adj-form-abs-def-m': ['definite masculine absolutive of "{arg1}"'],
    'sv-adj-form-abs-indef-n': ['indefinite neuter absolutive of "{arg1}"'],
    'sv-adj-form-abs-def+pl': ['definite absolutive plural of "{arg1}"'],
    'sv-adj-form-abs-pl': ['absolutive plural of "{arg1}"'],
    'sv-adj-form-abs-def': ['definite absolutive of "{arg1}"'],
    'sv-adj-form-comp': ['comparative of "{arg1}"'],
    'sv-adj-form-sup': ['superlative of "{arg1}"'],
    'sv-adj-form-sup-attr': ['attributive superlative of "{arg1}"'],
    'sv-adj-form-sup-attr-m': ['attributive superlative masculine of "{arg1}"'],
    'sv-adj-form-sup-pred': ['predicative superlative of "{arg1}"'],
    'sv-adv-form-comp': ['comparative of "{arg1}"'],
    'sv-adv-form-sup': ['superlative of "{arg1}"'],
    'sv-verb-form-pre': ['present tense of "{arg1}"'],
    'sv-verb-form-past': ['past tense of "{arg1}"'],
    'sv-verb-form-imp': ['imperative of "{arg1}"'],
    'sv-verb-form-sup': ['supine of "{arg1}"'],
    'sv-verb-form-sup-pass': ['passive supine of "{arg1}"'],
    'sv-verb-form-subjunctive': ['subjunctive of "{arg1}"'],
    'sv-verb-form-inf-pass': ['passive infinitive of "{arg1}"'],
    'sv-verb-form-pre-pass': ['present passive of "{arg1}"'],
    'sv-verb-form-past-pass': ['past passive of "{arg1}"'],
    'sv-verb-form-prepart': ['present participle of "{arg1}"'],
    'sv-verb-form-pastpart': ['past participle of "{arg1}"'],
    'de-zu-infinitive of': ['zu-infinitive of "{arg1}"'],
    'de-superseded spelling of': ['superseded spelling of "{arg1}"'],
    'de-umlautless spelling of': ['umlautless spelling of "{arg1}"'],
    'pt-obsolute-hellenism': ['obsolete hellenism of "{arg1}"'],
    'pt-obsolute hellenism': ['obsolete hellenism of "{arg1}"'],
    'ar-verbal noun of': ['verbal noun of "{arg1}"'],
    'mul-semaphore for': ['semaphore for "{arg1}"'],
    #'pt-superseded-silent-letter-1990':
    #'pt-superseded-hyphen',
    #'pt-superseded-paroxytone'
    #'pt-obsolete-éia',
    #'pt-obsolete-ü',
    #'pt-obsolete-ôo',
    #'pt-obsolete-secondary-stress',
    #'pt-obsolete-differential-accent',
    #'pt-obsolete-silent-letter-1911',
    'w': ['{arg2}', '{arg1}', '{word}'],
    'wp': ['{arg2}', '{arg1}', '{word}'],
    'w2': [r'{arg3}', r'{arg2}'],
    'wikipedia': ['{arg2}', '{arg1}', '{word}'],
    'wikisaurus': ['{arg2}', '{arg1}', '{word}'],
    'wikispecies': ['{arg2}', '{arg1}', '{word}'],
    'specieslink': ['({arg2} {arg1})'],
    'm': ['{arg3} ({arg4})', '{arg2} ({arg4})', '{arg3}', '{arg2}'],
    'm+': ['{arg3} ({arg4})', '{arg2} ({arg4})', '{arg3}', '{arg2}'],
    'm-self': ['{arg3} ({arg4})', '{arg2} ({arg4})', '{arg3}', '{arg2}'],
    'mention': ['{arg3} ({arg4})', '{arg2} ({arg4})', '{arg3}', '{arg2}'],
    "he-m": [r'{arg1} \ {dwv} ({tr}) ({gloss})',
             r'{arg1} \ {dwv} ({tr})',
             r'{arg1} \ {dwv} ({gloss})',
             r'{arg1} \ {dwv}',
             r'{arg1} ({tr}) ({gloss})',
             r'{arg1} ({tr})',
             r'{arg1} ({gloss})',
             r'{arg1}'],
    'ryu-def': [r'{arg1}:'],
    'ja-kyujitai spelling of': [r'Kyujitai form of {arg1}'],
    'l': ['{arg3} ({arg4})', '{arg2} ({arg4})', '{arg3}', '{arg2}'],
    "ja-def": [
        r'{arg1}, {arg2}, {arg3}, {arg4}, {arg5}, {arg6}, {arg7}, {arg8}, '
        r'{arg9}, {arg10}:',
        r'{arg1}, {arg2}, {arg3}, {arg4}, {arg5}, {arg6}, {arg7}, {arg8}, '
        r'{arg9}:',
        r'{arg1}, {arg2}, {arg3}, {arg4}, {arg5}, {arg6}, {arg7}, {arg8}:',
        r'{arg1}, {arg2}, {arg3}, {arg4}, {arg5}, {arg6}, {arg7}:',
        r'{arg1}, {arg2}, {arg3}, {arg4}, {arg5}, {arg6}:',
        r'{arg1}, {arg2}, {arg3}, {arg4}, {arg5}:',
        r'{arg1}, {arg2}, {arg3}, {arg4}:',
        r'{arg1}, {arg2}, {arg3}:',
        r'{arg1}, {arg2}:',
        r'{arg1}:'],
    # ja-r is more complicated than this with % and ^ markers
    "ja-r": [r'{arg1} ({arg2}; {lit}; {gloss})',
             r'{arg1} ({arg2}; {lit}; {arg3})',
             r'{arg1} ({arg2}; {gloss})',
             r'{arg1} ({arg2}; {arg3})',
             r'{arg1} ({gloss})',
             r'{arg1} ({arg3})',
             r'{arg1} ({arg2})',
             r'{arg1}'],
    "ryu-r": [r'{arg1} ({arg2}; {lit}; {gloss})',
              r'{arg1} ({arg2}; {lit}; {arg3})',
              r'{arg1} ({arg2}; {gloss})',
              r'{arg1} ({arg2}; {arg3})',
              r'{arg1} ({gloss})',
              r'{arg1} ({arg3})',
              r'{arg1} ({arg2})',
              r'{arg1}'],
    'la-part-form': [r'participle of "{arg1}"'],
    'l-self': ['{arg3} ({arg4})', '{arg2} ({arg4})', '{arg3}', '{arg2}'],
    'll': ['{arg3} ({arg4})', '{arg2} ({arg4})', '{arg3}', '{arg2}'],
    'link': ['{arg3} ({arg4})', '{arg2} ({arg4})', '{arg3}', '{arg2}'],
    'SI-unit': ['SI unit of {arg4}', 'SI unit of measurement'],  # XXX
    'SI-unit-abb': ['SI unit of {arg3}'],  # XXX
    'SI-unit-abbnp': ['SI unit of {arg3}'],  # XXX
    'SI-unit-abb2': ['SI unit of {arg4}'],  # XXX
    'SI-unit-2': ['SI unit of {arg3}'],  # XXX
    'SI-unit-np': ['SI unit of {arg4}'],  # XXX
    'taxon': [r'taxonomic {arg1}'],  # XXX needs special formatting

    'Passeriformes Hypernyms':
    ['"Eukaryota" - superkingdom; "Animalia" - kingdom; '
     '"Bilateria" - subkingdom; "Deuterostomia" - infrakingdom; '
     '"Chordata" - phylum; "Vertebrata" - subphylum; '
     '"Gnathostomata" - infraphylum; "Reptilia" - class; '
     '"Aves" - subclass; "Neognathae" - infraclass; '
     '"Neoaves" - superorder; "Passeriformes" - order'],

    'Thraupidae Hypernyms':
    ['"Eukaryota" - superkingdom; "Animalia" - kingdom; '
     '"Bilateria" - subkingdom; "Deuterostomia" - infrakingdom; '
     '"Chordata" - phylum; "Vertebrata" - subphylum; '
     '"Gnathostomata" - infraphylum; "Reptilia" - class; '
     '"Aves" - subclass; "Neognathae" - infraclass; '
     '"Neoaves" - superorder; "Passeriformes" - order; '
     '"Passeri" - suborder; "Passerida" - infraorder; '
     '"Passeroidea" - superfamily; "Thraupidae" - family'],

    'Tyrannidae Hypernyms':
    ['"Eukaryota" - superkingdom; "Animalia" - kingdom; '
     '"Bilateria" - subkingdom; "Deuterostomia" - infrakingdom; '
     '"Chordata" - phylum; "Vertebrata" - subphylum; '
     '"Gnathostomata" - infraphylum; "Reptilia" - class; '
     '"Aves" - subclass; "Neognathae" - infraclass; '
     '"Neoaves" - superorder; "Passeriformes" - order; '
     '"Tyranni" - suborder; "Tyrannides"; infraorder; '
     '"Tyrannida" - parvorder; "Tyrannidae" - family'],

    'Trochilidae Hypernyms':
    ['"Eukaryota" - superkingdom; "Animalia" - kingdom; '
     '"Bilateria" - subkingdom; "Deuterostomia" - infrakingdom; '
     '"Chordata" - phylum; "Vertebrata" - subphylum; '
     '"Gnathostomata" - infraphylum; "Reptilia" - class; '
     '"Aves" - subclass; "Neognathae" - infraclass; '
     '"Neoaves" - superorder; "Apodiformes" - order; '
     '"Trochilidae" - family'],

    'angiosperms Hypernyms':
    ['"Eukaryota" - superkingdom; "Plantae" - kingdom; '
     '"Viridiplantae" - subkingdom; "Streptophyta" - infrakingdom; '
     '"Embryophyta" - superphylum; "Tracheophyta" - phylum; '
     '"Spermatophytina" - subphylum; "angiosperms"'],

    'Fabaceae Hypernyms':
    ['"Eukaryota" - superkingdom; "Plantae" - kingdom; '
     '"Viridiplantae" - subkingdom; "Streptophyta" - infrakingdom; '
     '"Embryophyta" - superphylum; "Tracheophyta" - phylum; '
     '"Spermatophytina" - subphylum; "angiosperms", "eudicots", '
     '"core eudicots", "rosids", "eurosids I" - clades; '
     '"Fabales" - order; "Fabaceae" - family'],

}

default_tags = set([
    '&lit',
    "comcatlite",
    "glossary",
    "glink",
    'IPAfont',
    'keyword',
    'math',
    'n-g',
    'ngd',
    "nobr",
    'non-gloss',
    'non gloss definition',
    'non-gloss definition',
    "nowrap",
    'place',
    'quote',
    'small',
    'zh-div',
    'zh-short-comp',
    'zh-syn-saurus',
    ])

default_parenthesize_tags = set([
    'a',
    'i',
    'gloss',
    'gl',
    'label',
    'lb',
    'lbl',
    'llmul',
    'q',
    'qf',
    'qual',
    'qualifier',
    's',
    'sense',
    "Sense",
    'term-label',
    'tlb',
    'noun form of',  # XXX needs special formatting
    'verb form of',  # XXX
    'inflection of',  # XXX
    'fi-form of',  # XXX needs special formatting
    'fi-participle of', # XXX needs special formatting
    'fi-infinitive of', # XXX needs special formatting
    'fi-verb form of',  # XXX needs special formatting
    'de-verb form of',  # XXX needs special formatting
    'es-compound of',  # XXX needs special formatting
    'es-verb form of',  # XXX needs special formatting
    'es-adj form of',  # XXX needs special formatting
    'es-noun',  # XXX needs special formatting
    'it-adj form of',  # XXX needs special formatting
    'pt-verb form of',  # XXX needs special formatting
    'et-verb form of',  # XXX needs special formatting
    'el-form-of-verb',  # XXX needs special formatting
    'nl-verb form of',  # XXX
    'nl-noun form of',  # XXX
    'nl-adj form of',  # XXX
    'lv-inflection of',  # XXX
    'pt-verb-form-of',  # XXX
    'ca-verb form of',  # XXX
    'nn-verb-form of',  # XXX
    'eo-form of',  # XXX
    'za-sawndip form of',  # XXX
    'lib-conjugation of',  # XXX
    'hu-participle',  # XXX
    'enm-plural subjunctive of',  # XXX
    'enm-plural of',  # XXX
    'nn-inf',  # XXX
    'iu-spel',  # XXX
    'infl of',  # XXX needs special formatting
    't',  # XXX needs special formatting
    'Latn-def', # XXX needs special handling
    ])
