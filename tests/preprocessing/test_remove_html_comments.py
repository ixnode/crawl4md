import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.remove_html_comments import RuleRemoveHtmlComments
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case, data_provider


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
    @data_provider(CASES)
    def test_remove_html_comments(self, case: RuleCase) -> None:
        assert_rule_case(self, RuleRemoveHtmlComments, case)
