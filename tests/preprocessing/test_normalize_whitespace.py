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
from crawl4md.convert.preprocessing.rules.normalize_whitespace import RuleNormalizeWhitespace
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case
from tests.support.progress import run_progress_cases


CASES = [
    RuleCase(
        name="normalizes_trailing_spaces",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_whitespace=True),
        markdown="# Title   \nText   \n\n",
        expected="# Title\nText\n\n",
    ),
    RuleCase(
        name="inserts_space_before_link_when_text_touches_link",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_whitespace=True),
        markdown=(
            "_Eine Boeing 707 der"
            '[Air India](https://de.wikipedia.org/wiki/Air_India "Air India")_\n'
        ),
        expected=(
            "_Eine Boeing 707 der "
            '[Air India](https://de.wikipedia.org/wiki/Air_India "Air India")_\n'
        ),
    ),
    RuleCase(
        name="inserts_space_before_link_after_number_text",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_whitespace=True),
        markdown=(
            "Vereinigte Staaten 48"
            "[Vereinigte Staaten]"
            '(https://de.wikipedia.org/wiki/Vereinigte_Staaten "Vereinigte Staaten")\n'
        ),
        expected=(
            "Vereinigte Staaten 48 "
            "[Vereinigte Staaten]"
            '(https://de.wikipedia.org/wiki/Vereinigte_Staaten "Vereinigte Staaten")\n'
        ),
    ),
    RuleCase(
        name="keeps_emphasis_before_link_unchanged",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_whitespace=True),
        markdown=(
            'In dem Film *[Airport](https://de.wikipedia.org/wiki/Airport_(Film) '
            '"Airport (Film)")* spielt eine Boeing 707 eine wichtige Nebenrolle.\n'
        ),
        expected=(
            'In dem Film *[Airport](https://de.wikipedia.org/wiki/Airport_(Film) '
            '"Airport (Film)")* spielt eine Boeing 707 eine wichtige Nebenrolle.\n'
        ),
    ),
    RuleCase(
        name="inserts_space_before_parentheses",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_whitespace=True),
        markdown="| Produktionszeit | 1957 bis 1982/1991(zivil / militärisch) |\n",
        expected="| Produktionszeit | 1957 bis 1982/1991 (zivil / militärisch) |\n",
    ),
    RuleCase(
        name="keeps_parentheses_inside_link_targets_unchanged",
        config=MarkdownPreprocessingConfig(enabled=True, normalize_whitespace=True),
        markdown=(
            "[![](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/"
            "Boeing_707-124_%28Continental_Airlines%29_LAX.jpg/"
            "250px-Boeing_707-124_%28Continental_Airlines%29_LAX.jpg)]"
            "(https://de.wikipedia.org/wiki/Datei:Boeing_707-124_"
            "(Continental_Airlines)_LAX.jpg)\n"
        ),
        expected=(
            "[![](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/"
            "Boeing_707-124_%28Continental_Airlines%29_LAX.jpg/"
            "250px-Boeing_707-124_%28Continental_Airlines%29_LAX.jpg)]"
            "(https://de.wikipedia.org/wiki/Datei:Boeing_707-124_"
            "(Continental_Airlines)_LAX.jpg)\n"
        ),
    ),
]


class RuleNormalizeWhitespaceTests(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_normalize_whitespace(self) -> None:
        names = [case.name for case in CASES]

        def _run(index: int) -> None:
            case = CASES[index]
            assert_rule_case(self, RuleNormalizeWhitespace, case)

        run_progress_cases(names, _run)
