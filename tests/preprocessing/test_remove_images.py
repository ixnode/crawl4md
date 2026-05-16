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
from tests.support.progress import run_progress_cases


CASES = [
    RuleCase(
        name="all__combined_image_cases",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        fixture_group="remove_images",
    ),
]


class RuleRemoveImagesTests(unittest.TestCase):
    def test_remove_images(self) -> None:
        names = [case.name for case in CASES]

        def _run(index: int) -> None:
            case = CASES[index]
            case.fixture_group = "remove_images"
            assert_rule_case(self, RuleRemoveImages, case)

        run_progress_cases(names, _run)
