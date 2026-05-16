from pathlib import Path
import time
import unittest

from crawl4md.language import extract_language_from_html


class LanguageTests(unittest.TestCase):
    def test_extract_language_from_html_fixtures(self) -> None:
        html_root = Path("tests/data/html")
        files = sorted(html_root.rglob("*.html"))

        self.assertTrue(files, "No HTML fixture files found in tests/data/html")
        total = len(files)

        for index, file_path in enumerate(files, start=1):
            started_at = time.perf_counter()
            case_name = file_path.relative_to(html_root).as_posix()
            with self.subTest(file=file_path.as_posix()):
                try:
                    expected = file_path.relative_to(html_root).parts[0]
                    html = file_path.read_text(encoding="utf-8", errors="ignore")
                    detected = extract_language_from_html(html)
                    self.assertEqual(detected, expected)
                except Exception:
                    duration_ms = (time.perf_counter() - started_at) * 1000
                    print(f"\n[{index}/{total}] [{case_name}] ❌ ({duration_ms:.0f} ms)", flush=True)
                    raise

                duration_ms = (time.perf_counter() - started_at) * 1000
                print(f"\n[{index}/{total}] [{case_name}] ✅ ({duration_ms:.0f} ms)", end="", flush=True)

        print(flush=True)
