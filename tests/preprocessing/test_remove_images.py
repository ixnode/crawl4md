import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.remove_images import RuleRemoveImages
from crawl4md.paths import load_markdown_file


class RuleRemoveImagesTests(unittest.TestCase):
    def test_remove_images(self) -> None:
        raw = load_markdown_file("tests/data/preprocessing/remove_images/all/raw.md")
        expected = load_markdown_file("tests/data/preprocessing/remove_images/all/expected.md")

        if raw is None or expected is None:
            self.fail("Missing remove_images all fixture files.")

        config = MarkdownPreprocessingConfig(enabled=True, remove_images=True)
        cleaned = RuleRemoveImages(config).apply(raw)

        self.maxDiff = None
        self.assertEqual(cleaned.strip(), expected.strip())
