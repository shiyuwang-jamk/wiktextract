from unittest import TestCase
from unittest.mock import patch

from wikitextprocessor import Wtp
from wiktextract.config import WiktionaryConfig
from wiktextract.extractor.fr.form_line import (
    extract_form_line,
    process_zh_mot_template,
)
from wiktextract.extractor.fr.models import WordEntry
from wiktextract.wxr_context import WiktextractContext


class TestFormLine(TestCase):
    def setUp(self) -> None:
        self.wxr = WiktextractContext(
            Wtp(lang_code="fr"), WiktionaryConfig(dump_file_lang_code="fr")
        )

    def tearDown(self) -> None:
        self.wxr.wtp.close_db_conn()

    def test_ipa(self):
        self.wxr.wtp.start_page("bonjour")
        self.wxr.wtp.add_page("Modèle:pron", 10, "\\bɔ̃.ʒuʁ\\")
        root = self.wxr.wtp.parse("'''bonjour''' {{pron|bɔ̃.ʒuʁ|fr}}")
        page_data = [WordEntry(word="bonjour", lang_code="fr", lang="Français")]
        extract_form_line(self.wxr, page_data, root.children)
        self.assertEqual(
            [d.model_dump(exclude_defaults=True) for d in page_data[-1].sounds],
            [{"ipa": "\\bɔ̃.ʒuʁ\\"}],
        )

    def test_gender(self):
        self.wxr.wtp.start_page("bonjour")
        self.wxr.wtp.add_page("Modèle:m", 10, "masculin")
        root = self.wxr.wtp.parse("'''bonjour''' {{m}}")
        page_data = [WordEntry(word="bonjour", lang_code="fr", lang="Français")]
        extract_form_line(self.wxr, page_data, root.children)
        self.assertEqual(page_data[-1].tags, ["masculine"])

    def test_zh_mot(self):
        self.wxr.wtp.start_page("马")
        self.wxr.wtp.add_page("Modèle:zh-mot", 10, body="{{lang}} {{pron}}")
        self.wxr.wtp.add_page("Modèle:lang", 10, body="mǎ")
        self.wxr.wtp.add_page("Modèle:pron", 10, body="\\ma̠˨˩˦\\")
        root = self.wxr.wtp.parse("{{zh-mot|马|mǎ}}")
        page_data = [WordEntry(word="test", lang_code="fr", lang="Français")]
        process_zh_mot_template(self.wxr, root.children[0], page_data)
        self.assertEqual(
            [d.model_dump(exclude_defaults=True) for d in page_data[-1].sounds],
            [
                {"tags": ["Pinyin"], "zh_pron": "mǎ"},
                {"ipa": "\\ma̠˨˩˦\\"},
            ],
        )

    def test_ipa_location_tag(self):
        # https://fr.wiktionary.org/wiki/basket-ball
        self.wxr.wtp.start_page("basket-ball")
        self.wxr.wtp.add_page("Modèle:pron", 10, body="{{{1}}}")
        self.wxr.wtp.add_page(
            "Modèle:FR", 10, body="""<span id="région">''(France)''</span>"""
        )
        self.wxr.wtp.add_page(
            "Modèle:CA", 10, body="""<span id="région">''(Canada)''</span>"""
        )
        self.wxr.wtp.add_page("Modèle:m", 10, body="masculin")
        root = self.wxr.wtp.parse(
            "{{pron|bas.kɛt.bol|fr}} {{FR|nocat=1}} ''ou'' {{pron|bas.kɛt.bɔl|fr}} {{FR|nocat=1}} ''ou'' {{pron|bas.kɛt.bɑl|fr}} {{CA|nocat=1}} {{m}}"
        )
        page_data = [
            WordEntry(word="basket-ball", lang_code="fr", lang="Français")
        ]
        extract_form_line(self.wxr, page_data, root.children)
        self.assertEqual(
            page_data[-1].model_dump(exclude_defaults=True),
            {
                "word": "basket-ball",
                "lang_code": "fr",
                "lang": "Français",
                "tags": ["masculine"],
                "sounds": [
                    {"ipa": "bas.kɛt.bol", "raw_tags": ["France"]},
                    {"ipa": "bas.kɛt.bɔl", "raw_tags": ["France"]},
                    {"ipa": "bas.kɛt.bɑl", "raw_tags": ["Canada"]},
                ],
            },
        )

    def test_template_in_pron_argument(self):
        # https://fr.wiktionary.org/wiki/minéral_argileux
        self.wxr.wtp.start_page("")
        self.wxr.wtp.add_page("Modèle:pron", 10, body="{{{1}}}")
        self.wxr.wtp.add_page("Modèle:liaison", 10, body="‿")
        root = self.wxr.wtp.parse(
            "'''minéral argileux''' {{pron|mi.ne.ʁa.l{{liaison|fr}}aʁ.ʒi.lø|fr}}"
        )
        page_data = [WordEntry(word="test", lang_code="fr", lang="Français")]
        extract_form_line(self.wxr, page_data, root.children)
        self.assertEqual(
            page_data[-1].sounds[0].model_dump(exclude_defaults=True),
            {"ipa": "mi.ne.ʁa.l‿aʁ.ʒi.lø"},
        )

    @patch(
        "wikitextprocessor.Wtp.node_to_wikitext",
        return_value='\'\'(pour un homme, on dit\'\' : <bdi lang="fr" xml:lang="fr" class="lang-fr">[[auteur#fr|auteur]]</bdi> ; \'\'pour une personne non-binaire, on peut dire\'\' : <bdi lang="fr" xml:lang="fr" class="lang-fr">[[autaire#fr|autaire]]</bdi>, <bdi lang="fr" xml:lang="fr" class="lang-fr">[[auteurice#fr|auteurice]]</bdi>, <bdi lang="fr" xml:lang="fr" class="lang-fr">[[auteur·ice#fr|auteur·ice]]</bdi>\'\')\'\'',
    )
    def test_equiv_pour_template(self, mock_node_to_wikitext):
        self.maxDiff = None
        self.wxr.wtp.start_page("autrice")
        root = self.wxr.wtp.parse(
            "{{équiv-pour|un homme|auteur|2egenre=une personne non-binaire|2egenre1=autaire|2egenre2=auteurice|2egenre3=auteur·ice|lang=fr}}"
        )
        page_data = [WordEntry(word="autrice", lang_code="fr", lang="Français")]
        extract_form_line(self.wxr, page_data, root.children)
        self.assertEqual(
            page_data[-1].model_dump(exclude_defaults=True),
            {
                "word": "autrice",
                "lang_code": "fr",
                "lang": "Français",
                "forms": [
                    {
                        "form": "auteur",
                        "tags": ["masculine"],
                        "source": "form line template 'équiv-pour'",
                    },
                    {
                        "form": "autaire",
                        "tags": ["neuter"],
                        "source": "form line template 'équiv-pour'",
                    },
                    {
                        "form": "auteurice",
                        "tags": ["neuter"],
                        "source": "form line template 'équiv-pour'",
                    },
                    {
                        "form": "auteur·ice",
                        "tags": ["neuter"],
                        "source": "form line template 'équiv-pour'",
                    },
                ],
            },
        )

    def test_italic_tag(self):
        self.wxr.wtp.start_page("飢える")
        page_data = [WordEntry(word="飢える", lang_code="ja", lang="Japonais")]
        root = self.wxr.wtp.parse("'''飢える''' ''ichidan''")
        extract_form_line(self.wxr, page_data, root.children)
        self.assertEqual(page_data[-1].raw_tags, ["ichidan"])

    def test_not_region_tag_after_ipa(self):
        self.wxr.wtp.start_page("5-0")
        self.wxr.wtp.add_page("Modèle:pron", 10, body="{{{1}}}")
        self.wxr.wtp.add_page(
            "Modèle:indénombrable", 10, body="(Indénombrable)"
        )
        page_data = [WordEntry(word="5-0", lang_code="en", lang="Anglais")]
        root = self.wxr.wtp.parse(
            "'''5-0''' {{pron|ˈfaɪvˌoʊ|en}} {{indénombrable|en}}"
        )
        extract_form_line(self.wxr, page_data, root.children)
        self.assertEqual(page_data[-1].tags, ["uncountable"])
