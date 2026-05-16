from pathlib import Path
import unittest

from crawl4md.language import extract_language_from_html


class LanguageTests(unittest.TestCase):
    def test_extract_language_from_html_fixtures(self) -> None:
        html_root = Path("tests/data/html")
        files = sorted(html_root.rglob("*.html"))

        self.assertTrue(files, "No HTML fixture files found in tests/data/html")

        for file_path in files:
            with self.subTest(file=file_path.as_posix()):
                expected = file_path.relative_to(html_root).parts[0]
                html = file_path.read_text(encoding="utf-8", errors="ignore")
                detected = extract_language_from_html(html)
                self.assertEqual(detected, expected)
