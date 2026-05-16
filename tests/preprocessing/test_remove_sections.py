import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.remove_sections import RuleRemoveSections
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case
from tests.support.progress import run_progress_cases


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
