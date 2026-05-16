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
from crawl4md.convert.preprocessing.rules.remove_links import RuleRemoveLinks
from crawl4md.utils.preprocessing_test_cases import RuleCase, assert_rule_case
from crawl4md.utils.progress_runner import run_progress_cases


CASES = [
    # Tests with no links.
    RuleCase(
        name="no_links__disabled_preprocessing",
        config=MarkdownPreprocessingConfig(
            enabled=False,
            remove_links=False,
        ),
    ),
    RuleCase(
        name="no_links__disabled_remove_links",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=False,
        ),
    ),
    RuleCase(
        name="no_links__enabled_single",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=r"anchor:#custom-link",
        ),
    ),
    RuleCase(
        name="no_links__enabled_multiple",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=[
                r"anchor:#custom-link",
                r"anchor:cite_note",
            ],
        ),
    ),

    # Tests with no effect.
    RuleCase(
        name="no_effect",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=[
                r"anchor:#custom-link",
                r"anchor:cite_note",
            ],
        ),
    ),

    # Tests with anchor replacements.
    RuleCase(
        name="anchor",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=[
                "anchor:cite_note",
                "anchor:Citation_needed",
                "anchor:Verifiability",
                "anchor:#(?:[Bb]ody[Cc]ontent|content|content-start|main|main-content|maincontent)",
                "anchor:#[Vv]orlage_[Ll]esenswert",
                "anchor:#[Vv]orlage_[Ee]xzellent",
                "anchor:&veaction=edit[^)]*section=",
                "anchor:&action=edit[^)]*section=",
                "anchor:#custom-link",
            ],
        ),
    ),

    # Tests with all replacements.
    RuleCase(
        name="all__combined_anchor_text_unwrap_edit_and_badge",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=[
                "anchor:cite_note",
                "anchor:Citation_needed",
                "anchor:Verifiability",
                "anchor:#bodyContent",
                "anchor:#custom-link",
                "anchor:#[Vv]orlage_[Ll]esenswert",
                "anchor:#[Vv]orlage_[Ee]xzellent",
                "anchor:&veaction=edit[^)]*section=",
                "anchor:&action=edit[^)]*section=",
                "text:Remove me",
                "unwrap:*",
            ],
        ),
    ),
]


class RuleRemoveLinksTests(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_remove_links(self) -> None:
        names = [case.name for case in CASES]

        def _run(index: int) -> None:
            case = CASES[index]
            case.fixture_group = "remove_links"
            assert_rule_case(self, RuleRemoveLinks, case)

        run_progress_cases(names, _run)
