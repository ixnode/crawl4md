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
from crawl4md.paths import load_markdown_file
from tests.preprocessing.support.data_provider import RuleCase


CASES = [
    RuleCase(
        name="all__combined_image_cases",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
    ),
]


class RuleRemoveImagesTests(unittest.TestCase):
    def test_remove_images(self) -> None:
        total = len(CASES)

        for index, case in enumerate(CASES, start=1):
            started_at = time.perf_counter()
            try:
                raw = load_markdown_file(f"tests/data/preprocessing/remove_images/{case.name.split('__', 1)[0]}/raw.md")
                expected = load_markdown_file(
                    f"tests/data/preprocessing/remove_images/{case.name.split('__', 1)[0]}/expected.md"
                )

                if raw is None or expected is None:
                    raise ValueError(f"Missing fixture for case '{case.name}'.")

                cleaned = RuleRemoveImages(case.config).apply(raw, url=case.url, html=case.html)
                self.maxDiff = None
                self.assertEqual(cleaned.strip(), expected.strip())
            except Exception:
                duration_ms = (time.perf_counter() - started_at) * 1000
                print(f"\n[{index}/{total}] [{case.name}] ❌ ({duration_ms:.0f} ms)")
                raise

            duration_ms = (time.perf_counter() - started_at) * 1000
            print(f"\n[{index}/{total}] [{case.name}] ✅ ({duration_ms:.0f} ms)", end="")
