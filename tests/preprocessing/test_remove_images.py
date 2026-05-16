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
from crawl4md.convert.preprocessing.rules.remove_images import RuleRemoveImages
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case
from crawl4md.utils.progress_runner import run_progress_cases


CASES = [
    RuleCase(
        name="all__combined_image_cases",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
    ),
    RuleCase(
        name="uses_english_figure_label_by_default",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        markdown="![Air India](image.jpg)",
        expected='Figure: "Air India"',
    ),
    RuleCase(
        name="uses_german_figure_label_from_html",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        markdown='![Boeing 707 Cockpit](image.jpg)',
        expected='Abbildung: "Boeing 707 Cockpit"',
        html='<html lang="de"></html>',
    ),
    RuleCase(
        name="uses_spanish_figure_label_from_html",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        markdown='![Cabina](image.jpg)',
        expected='Ilustración: "Cabina"',
        html='<html lang="es"></html>',
    ),
]


class RuleRemoveImagesTests(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_remove_images(self) -> None:
        names = [case.name for case in CASES]

        def _run(index: int) -> None:
            case = CASES[index]
            if case.fixture_group is None:
                case.fixture_group = "remove_images"
            assert_rule_case(self, RuleRemoveImages, case)

        run_progress_cases(names, _run)
