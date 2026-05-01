import unittest

from crawl4md.crawler import (
    remove_jump_to_content_links,
    remove_wikipedia_subtitle,
)


class RemoveJumpToContentLinksTests(unittest.TestCase):
    def test_removes_standalone_skip_link_line(self) -> None:
        markdown = (
            "[Zum Inhalt springen](https://de.wikipedia.org/wiki/Boeing_707#bodyContent)\n"
            "\n"
            "# Boeing 707\n"
            "\n"
            "Die Boeing 707 ist ein Verkehrsflugzeug.\n"
        )

        cleaned = remove_jump_to_content_links(
            markdown,
            "https://de.wikipedia.org/wiki/Boeing_707",
        )

        self.assertNotIn("Zum Inhalt springen", cleaned)
        self.assertNotIn("#bodyContent", cleaned)
        self.assertIn("# Boeing 707", cleaned)

    def test_removes_fragment_only_skip_link_language_independent(self) -> None:
        markdown = (
            "[Skip to content](#main-content)\n"
            "Some text\n"
        )

        cleaned = remove_jump_to_content_links(
            markdown,
            "https://example.com/article",
        )

        self.assertEqual(cleaned, "Some text\n")

    def test_keeps_regular_section_links(self) -> None:
        markdown = (
            "[References](https://example.com/article#references)\n"
            "[Read more](https://example.com/other-page#bodyContent)\n"
        )

        cleaned = remove_jump_to_content_links(
            markdown,
            "https://example.com/article",
        )

        self.assertEqual(cleaned, markdown)


class RemoveWikipediaSubtitleTests(unittest.TestCase):
    def test_removes_standalone_wikipedia_subtitle_line(self) -> None:
        markdown = (
            "aus Wikipedia, der freien Enzyklopädie\n"
            "\n"
            "# Boeing 707\n"
        )

        cleaned = remove_wikipedia_subtitle(markdown)

        self.assertEqual(cleaned, "# Boeing 707\n")

    def test_removes_wikipedia_subtitle_inline_and_keeps_rest(self) -> None:
        markdown = (
            "Boeing 707 aus Wikipedia, der freien Enzyklopädie\n"
        )

        cleaned = remove_wikipedia_subtitle(markdown)

        self.assertEqual(cleaned, "Boeing 707\n")


if __name__ == "__main__":
    unittest.main()
