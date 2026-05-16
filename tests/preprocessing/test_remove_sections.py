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

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.remove_sections import RuleRemoveSections
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case
from crawl4md.utils.progress_runner import run_progress_cases


CASES = [
    RuleCase(
        name="removes_reference_section_from_matching_heading",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_sections=["Einzelnachweise", "Weblinks"],
        ),
        markdown=(
            "## Geschichte\n\n"
            "Text\n\n"
            "## Einzelnachweise\n\n"
            "1. Quelle A\n"
            "2. Quelle B\n"
        ),
        expected="## Geschichte\n\nText\n",
    ),
    RuleCase(
        name="supports_heading_levels_numbering_and_anchor_suffixes",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_sections=["Weblinks"],
        ),
        markdown=(
            "## Geschichte\n\n"
            "Text mit **Formatierung** und [Link](https://example.com).\n\n"
            "### 8. Weblinks {#weblinks}\n\n"
            "- https://example.com\n"
        ),
        expected=(
            "## Geschichte\n\n"
            "Text mit **Formatierung** und [Link](https://example.com).\n"
        ),
    ),
    RuleCase(
        name="matches_remove_sections_case_insensitively",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_sections=["external links"],
        ),
        markdown="# Title\n\nContent\n\n#### External Links\n\n- Link\n",
        expected="# Title\n\nContent\n",
    ),
]


class RuleRemoveSectionsTests(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_remove_sections(self) -> None:
        names = [case.name for case in CASES]

        def _run(index: int) -> None:
            case = CASES[index]
            assert_rule_case(self, RuleRemoveSections, case)

        run_progress_cases(names, _run)
