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
import time

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.remove_images import RuleRemoveImages
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case


CASES = [
    RuleCase(
        name="all__combined_image_cases",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        fixture_group="remove_images",
    ),
]


class RuleRemoveImagesTests(unittest.TestCase):
    def test_remove_images(self) -> None:
        total = len(CASES)

        for index, case in enumerate(CASES, start=1):
            started_at = time.perf_counter()
            try:
                case.fixture_group = "remove_images"
                assert_rule_case(self, RuleRemoveImages, case)
            except Exception:
                duration_ms = (time.perf_counter() - started_at) * 1000
                print(f"\n[{index}/{total}] [{case.name}] ❌ ({duration_ms:.0f} ms)")
                raise

            duration_ms = (time.perf_counter() - started_at) * 1000
            print(f"\n[{index}/{total}] [{case.name}] ✅ ({duration_ms:.0f} ms)", end="")
