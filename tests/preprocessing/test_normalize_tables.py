import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.normalize_tables import RuleNormalizeTables
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case
from tests.support.progress import run_progress_cases


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

    def setUp(self) -> None:
        self.maxDiff = None
    def test_normalize_tables(self) -> None:
        names = [case.name for case in CASES]

        def _run(index: int) -> None:
            case = CASES[index]
            assert_rule_case(self, RuleNormalizeTables, case)

        run_progress_cases(names, _run)
