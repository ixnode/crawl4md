import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.normalize_tables import RuleNormalizeTables
from tests.preprocessing.data_provider import RuleCase, assert_rule_case, data_provider


CASES = [
    RuleCase(
        name="removes_empty_table_rows",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_tables=True),
        markdown=(
            "| Boeing 707 | |\n"
            "| --- | --- |\n"
            "| Typ | Schmalrumpfflugzeug |\n"
            "| | |\n"
            "| Hersteller | Boeing Airplane Company |\n"
        ),
        expected=(
            "| Boeing 707 | |\n"
            "| --- | --- |\n"
            "| Typ | Schmalrumpfflugzeug |\n"
            "| Hersteller | Boeing Airplane Company |\n"
        ),
    ),
    RuleCase(
        name="pads_short_table_rows",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_tables=True),
        markdown=(
            "| A | B |\n"
            "| --- | --- |\n"
            "| one |\n"
        ),
        expected="| A | B |\n| --- | --- |\n| one | |\n",
    ),
]


class RuleNormalizeTablesTests(unittest.TestCase):
    @data_provider(CASES)
    def test_normalize_tables(self, case: RuleCase) -> None:
        assert_rule_case(self, RuleNormalizeTables, case)
