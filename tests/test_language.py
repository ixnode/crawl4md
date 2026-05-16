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

from pathlib import Path
import unittest

from crawl4md.core.language import extract_language_from_html
from crawl4md.utils.progress_runner import run_progress_cases


class LanguageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def test_extract_language_from_html_fixtures(self) -> None:
        html_root = Path("tests/data/html")
        files = sorted(html_root.rglob("*.html"))

        self.assertTrue(files, "No HTML fixture files found in tests/data/html")
        names = [file_path.relative_to(html_root).as_posix() for file_path in files]

        def _run(index: int) -> None:
            file_path = files[index]
            with self.subTest(file=file_path.as_posix()):
                expected = file_path.relative_to(html_root).parts[0]
                html = file_path.read_text(encoding="utf-8", errors="ignore")
                detected = extract_language_from_html(html)
                self.assertEqual(detected, expected)

        run_progress_cases(names, _run)
