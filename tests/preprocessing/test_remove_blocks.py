import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.remove_blocks import RuleRemoveBlocks
from tests.preprocessing.data_provider import RuleCase, assert_rule_case, data_provider


CASES = [
    RuleCase(
        name="removes_multiline_wikidata_banner_link",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_blocks=[
                "Wikipedia:Wiki_Loves_Earth_",
                "Wikidata:Events/Coordinate_Me_",
            ],
        ),
        markdown=(
            "[\n"
            "| Nimm teil am Wiki\u00addata-Wett\u00adbewerb |\n"
            "| --- | ](https://www.wikidata.org/wiki/Wikidata:Events/Coordinate_Me_2026)\n"
            "\n"
            "# Boeing 707\n"
        ),
        expected="# Boeing 707\n",
        url="https://de.wikipedia.org/wiki/Boeing_707",
    ),
    RuleCase(
        name="removes_multiple_matching_blocks",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_blocks=["promo-banner", "generated-sidebar"],
        ),
        markdown=(
            "Keep this\n"
            "\n"
            "[promo](https://example.test/promo-banner)\n"
            "\n"
            "generated-sidebar\n"
            "details\n"
            "\n"
            "Keep that\n"
        ),
        expected="Keep this\nKeep that\n",
    ),
]


class RuleRemoveBlocksTests(unittest.TestCase):
    @data_provider(CASES)
    def test_remove_blocks(self, case: RuleCase) -> None:
        assert_rule_case(self, RuleRemoveBlocks, case)
