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
from crawl4md.convert.preprocessing.rules.remove_html_comments import RuleRemoveHtmlComments
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case
from crawl4md.utils.progress_runner import run_progress_cases


CASES = [
    RuleCase(
        name="removes_inline_html_comment",
        config=MarkdownPreprocessingConfig(enabled=True, remove_html_comments=True),
        markdown="Text <!-- hidden --> mehr Text\n",
        expected="Text  mehr Text\n",
    ),
    RuleCase(
        name="removes_multiline_html_comment",
        config=MarkdownPreprocessingConfig(enabled=True, remove_html_comments=True),
        markdown="Text\n<!-- first line\nsecond line -->\nMehr Text\n",
        expected="Text\n\nMehr Text\n",
    ),
]


class RuleRemoveHtmlCommentsTests(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_remove_html_comments(self) -> None:
        names = [case.name for case in CASES]

        def _run(index: int) -> None:
            case = CASES[index]
            assert_rule_case(self, RuleRemoveHtmlComments, case)

        run_progress_cases(names, _run)
