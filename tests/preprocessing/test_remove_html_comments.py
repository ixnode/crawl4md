import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.remove_html_comments import RuleRemoveHtmlComments
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case
from tests.support.progress import run_progress_cases


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
