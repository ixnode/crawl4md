# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-16)
# @since 1.0.0 (2026-05-16) First version

import unittest

from crawl4md.core.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.normalize_tables import RuleNormalizeTables
from crawl4md.utils.preprocessing_test_cases import RuleCase, assert_rule_case
from crawl4md.utils.progress_runner import run_progress_cases


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
