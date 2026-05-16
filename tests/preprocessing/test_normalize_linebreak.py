import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.normalize_linebreak import RuleNormalizeLinebreak
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case
from tests.support.progress import run_progress_cases


CASES = [
    RuleCase(
        name="normalizes_blank_lines",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_linebreak=True),
        markdown="\n\n# Title\n\n\nText\n   \n\n## Section\n\n\nMore text\n\n",
        expected="# Title\n\nText\n\n## Section\n\nMore text\n",
    ),
    RuleCase(
        name="adds_spacing_around_table_and_code_block",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_linebreak=True),
        markdown=(
            "# Title\n"
            "| A | B |\n"
            "| --- | --- |\n"
            "| 1 | 2 |\n"
            "```py\n"
            "x = 1  \n"
            "print(x)\n"
            "```\n"
            "Text\n"
        ),
        expected=(
            "# Title\n\n"
            "| A | B |\n"
            "| --- | --- |\n"
            "| 1 | 2 |\n\n"
            "```py\n"
            "x = 1  \n"
            "print(x)\n"
            "```\n\n"
            "Text\n"
        ),
    ),
    RuleCase(
        name="adds_blank_line_after_single_column_table",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_linebreak=True),
        markdown=(
            "| Boeing 707 |\n"
            "| --- |\n"
            "| Row |\n"
            "Die **Boeing 707** ist ein Flugzeug.\n"
        ),
        expected=(
            "| Boeing 707 |\n"
            "| --- |\n"
            "| Row |\n\n"
            "Die **Boeing 707** ist ein Flugzeug.\n"
        ),
    ),
    RuleCase(
        name="splits_adjacent_paragraph_lines_with_blank_lines",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_linebreak=True),
        markdown=(
            "### Vorgeschichte\n\n"
            '[Boeing 367](//de.wikipedia.org/wiki/Boeing_C-97 "Boeing C-97") (C-97)\n'
            "Seit dem Jungfernflug des ersten strahlgetriebenen Flugzeugs.\n"
            "Gleichzeitig verfolgte Boeing in dieser Zeit Überlegungen.\n"
        ),
        expected=(
            "### Vorgeschichte\n\n"
            '[Boeing 367](//de.wikipedia.org/wiki/Boeing_C-97 "Boeing C-97") '
            "(C-97)\n\n"
            "Seit dem Jungfernflug des ersten strahlgetriebenen Flugzeugs.\n\n"
            "Gleichzeitig verfolgte Boeing in dieser Zeit Überlegungen.\n"
        ),
    ),
    RuleCase(
        name="removes_blank_lines_between_list_items",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_linebreak=True),
        markdown=(
            "# Checklist\n\n"
            "Before release:\n"
            " * Run the converter tests\n\n"
            " * Review the generated Markdown\n\n"
            " * Update the changelog\n\n"
            "Deployment order:\n\n"
            " 1. Build the package\n\n"
            " 2. Publish the artifact\n\n"
            " 3. Verify the installation\n"
        ),
        expected=(
            "# Checklist\n\n"
            "Before release:\n\n"
            " * Run the converter tests\n"
            " * Review the generated Markdown\n"
            " * Update the changelog\n\n"
            "Deployment order:\n\n"
            " 1. Build the package\n"
            " 2. Publish the artifact\n"
            " 3. Verify the installation\n"
        ),
    ),
]


class RuleNormalizeLinebreakTests(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None
    def test_normalize_linebreak(self) -> None:
        names = [case.name for case in CASES]

        def _run(index: int) -> None:
            case = CASES[index]
            assert_rule_case(self, RuleNormalizeLinebreak, case)

        run_progress_cases(names, _run)
