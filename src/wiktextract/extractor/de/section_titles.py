from ...config import POSSubtitleData

# argument of title template https://de.wiktionary.org/wiki/Vorlage:Wortart
POS_SECTIONS: dict[str, POSSubtitleData] = {
    "Abkürzung (Deutsch)": {"pos": "abbrev", "tags": ["abbreviation"]},
    "Abkürzung": {"pos": "abbrev", "tags": ["abbreviation"]},
    "Abtönungspartikel": {"pos": "particle"},
    "Adjektiv": {"pos": "adj"},
    "Adverb": {"pos": "adv"},
    "Affix": {"pos": "affix"},
    "Antwortpartikel": {"pos": "particle"},
    "Artikel": {"pos": "det"},
    "Bruchzahlwort": {"pos": "num"},
    "Buchstabe": {"pos": "character"},
    "Demonstrativpronomen": {"pos": "pron"},
    "Eigenname ": {"pos": "name"},
    "Eigenname": {"pos": "name"},
    "Enklitikon": {"pos": "suffix", "tags": ["morpheme"]},
    "Fokuspartikel": {"pos": "particle"},
    "Formel": {"pos": "phrase"},
    "Geflügeltes Wort": {"pos": "phrase"},
    "Gentilname": {"pos": "name"},
    "Gradpartikel": {"pos": "particle"},
    "Grußformel": {"pos": "phrase"},
    "Hilfsverb": {"pos": "verb", "tags": ["auxiliary"]},
    "Hiragana": {"pos": "character"},
    "Indefinitpronomen": {"pos": "pron"},
    "Infinitiv": {"pos": "verb"},
    "Infix": {"pos": "infix"},
    "Interfix": {"pos": "interfix"},
    "Interjektion": {"pos": "intj"},
    "Interrogativadverb": {"pos": "adv"},
    "Interrogativpronomen": {"pos": "pron"},
    "Kardinalzahl": {"pos": "num"},
    "Kausaladverb": {"pos": "adv"},
    "Kognomen": {"pos": "name"},
    "Konjunktion": {"pos": "conj"},
    "Konjunktionaladverb": {"pos": "adv"},
    "Kontraktion": {"pos": "abbrev"},
    "Lokaladverb": {"pos": "adv"},
    "Merkspruch": {"pos": "phrase"},
    "Modaladverb": {"pos": "adv"},
    "Modalpartikel": {"pos": "particle"},
    "Nachname": {"pos": "name"},
    "Negationspartikel": {"pos": "particle"},
    "Numerale": {"pos": "num"},
    "Onomatopoetikum": {"pos": "intj"},
    "Ortsnamengrundwort": {"pos": "name"},
    "Ordinalzahl": {"pos": "num"},
    "Partikel": {"pos": "particle"},
    "Partikelverb": {"pos": "verb"},
    "Patronym": {"pos": "name"},
    "Personalpronomen": {"pos": "pron"},
    "Possessivpronomen": {"pos": "pron"},
    "Postposition": {"pos": "postp"},
    "Präfix": {"pos": "prefix", "tags": ["morpheme"]},
    "Präfixoid": {"pos": "prefix", "tags": ["morpheme"]},
    "Präposition": {"pos": "prep"},
    "Pronomen": {"pos": "pron"},
    "Pronominaladverb": {"pos": "adv"},
    "Redewendung": {"pos": "phrase"},
    "Reflexives Personalpronomen": {"pos": "pron"},
    "Reflexivpronomen": {"pos": "pron"},
    "Relativpronomen": {"pos": "pron"},
    "Reziprokpronomen": {"pos": "pron"},
    "Schriftzeichen": {"pos": "character"},
    "Sprichwort": {"pos": "phrase"},
    "Straßenname": {"pos": "name"},
    "Subjunktion": {"pos": "conj"},
    "Substantiv": {"pos": "noun"},
    "Suffix": {"pos": "suffix", "tags": ["morpheme"]},
    "Suffixoid": {"pos": "suffix", "tags": ["morpheme"]},
    "Symbol": {"pos": "symbol"},
    "Temporaladverb": {"pos": "adv"},
    "Temporaldverb": {"pos": "adv"},
    "Toponym": {"pos": "name"},
    "Verb": {"pos": "verb"},
    "Vergleichspartikel": {"pos": "particle"},
    "Vervielfältigungszahlwort": {"pos": "num"},
    "Vorname": {"pos": "name"},
    "Wiederholungszahlwort": {"pos": "num"},
    "Wortverbindung": {"pos": "phrase"},
    "Zahlklassifikator": {"pos": "noun"},
    "Zahlzeichen": {"pos": "num"},
    "Zirkumfix": {"pos": "circumfix", "tags": ["morpheme"]},
    "Zirkumposition": {"pos": "circumpos"},
}

LINKAGE_TITLES: dict[str, str] = {
    "Gegenwörter": "antonyms",
    "Holonyme": "holonyms",
    "Oberbegriffe": "hypernyms",
    "Redewendungen": "expressions",
    "Sinnverwandte Redewendungen": "synonyms",
    "Sinnverwandte Wörter": "coordinate_terms",
    "Sinnverwandte Zeichen": "synonyms",
    "Sprichwörter": "proverbs",
    "Synonyme": "synonyms",
    "Unterbegriffe": "hyponyms",
    "Wortbildungen": "derived",
    "Abgeleitete Symbole": "derived",
    "Geflügelte Worte": "proverbs",
    "Meronyme": "meronyms",
}

FORM_TITLES = {
    "Nebenformen": ["variant"],
    "Namensvarianten": ["variant"],
    "Weibliche Wortformen": ["feminine"],
    "Weibliche Namensvarianten": ["feminine"],
    "Männliche Wortformen": ["masculine"],
    "Verkleinerungsformen": ["diminutive"],
    "Vergrößerungsformen": ["augmentative"],
    "Kurzformen": ["abbreviation"],
    "Koseformen": ["affective"],
    "Hanja": ["hanja"],
    "Männliche Namensvarianten": ["masculine"],
    "Nicht mehr gültige Schreibweisen": ["obsolete"],
    "Symbole": ["symbol"],
}
