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
from crawl4md.convert.preprocessing.rules.remove_blocks import RuleRemoveBlocks
from crawl4md.utils.preprocessing_test_cases import RuleCase, assert_rule_case
from crawl4md.utils.progress_runner import run_progress_cases


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

    def setUp(self) -> None:
        self.maxDiff = None

    def test_remove_blocks(self) -> None:
        names = [case.name for case in CASES]

        def _run(index: int) -> None:
            case = CASES[index]
            assert_rule_case(self, RuleRemoveBlocks, case)

        run_progress_cases(names, _run)
