import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.ensure_h1 import RuleEnsureH1
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case
from tests.support.progress import run_progress_cases


CASES = [
    RuleCase(
        name="keeps_existing_h1",
        config=MarkdownPreprocessingConfig(enabled=True, ensure_h1=True),
        markdown="# Existing Title\n\nContent\n",
        expected="# Existing Title\n\nContent\n",
        url="https://example.com/page",
    ),
    RuleCase(
        name="injects_h1_from_html",
        config=MarkdownPreprocessingConfig(enabled=True, ensure_h1=True),
        markdown="## Section\n\nContent\n",
        expected="# Main Title\n\n## Section\n\nContent\n",
        url="https://example.com/page",
        html=(
            "<html><head><title>Fallback</title></head>"
            "<body><h1>Main Title</h1></body></html>"
        ),
    ),
]


class RuleEnsureH1Tests(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None
    def test_ensure_h1(self) -> None:
        names = [case.name for case in CASES]

        def _run(index: int) -> None:
            case = CASES[index]
            assert_rule_case(self, RuleEnsureH1, case)

        run_progress_cases(names, _run)
