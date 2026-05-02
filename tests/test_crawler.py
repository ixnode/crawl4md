import unittest

from crawl4md.preprocessing import (
    ensure_h1,
    extract_title_from_html,
    fallback_title_from_url,
    MarkdownPreprocessor,
    remove_jump_to_content_links,
    remove_wiki_loves_earth_banner,
    remove_wikipedia_subtitle,
)
from crawl4md.config import MarkdownPreprocessingConfig


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


class RemoveWikiLovesEarthBannerTests(unittest.TestCase):
    def test_removes_standalone_banner_link_line(self) -> None:
        markdown = (
            "[ Wiki Loves Earth Teile deine Naturfotos fuer Wikipedia! Lade sie zum 30. Juni hier hoch! ]"
            "(https://de.wikipedia.org/wiki/Wikipedia:Wiki_Loves_Earth_2026/Deutschland)\n"
            "\n"
            "# Boeing 707\n"
        )

        cleaned = remove_wiki_loves_earth_banner(
            markdown,
            "https://de.wikipedia.org/wiki/Boeing_707",
        )

        self.assertEqual(cleaned, "# Boeing 707\n")

    def test_removes_multiline_wikidata_banner_link(self) -> None:
        markdown = (
            "[\n"
            "| Nimm teil am Wiki\u00addata-Wett\u00adbewerb und hilf mit, geo\u00adgrafisch "
            "ver\u00adortete Items in 28 L\u00e4ndern und Regionen zu ver\u00adbessern! "
            "Coordinate Me \u276d MAI 2026 |\n"
            "| --- | ](https://www.wikidata.org/wiki/Wikidata:Events/Coordinate_Me_2026)\n"
            "\n"
            "# Boeing 707\n"
        )

        cleaned = remove_wiki_loves_earth_banner(
            markdown,
            "https://de.wikipedia.org/wiki/Boeing_707",
        )

        self.assertEqual(cleaned, "# Boeing 707\n")

    def test_keeps_unrelated_wikipedia_links(self) -> None:
        markdown = (
            "[Boeing 707](https://de.wikipedia.org/wiki/Boeing_707)\n"
        )

        cleaned = remove_wiki_loves_earth_banner(
            markdown,
            "https://de.wikipedia.org/wiki/Boeing_707",
        )

        self.assertEqual(cleaned, markdown)


class EnsureH1Tests(unittest.TestCase):
    def test_keeps_existing_h1(self) -> None:
        markdown = "# Existing Title\n\nContent\n"
        html = "<html><body><h1>Ignored</h1></body></html>"

        cleaned = ensure_h1(markdown, html, "https://example.com/page")

        self.assertEqual(cleaned, markdown)

    def test_injects_h1_when_only_lower_headings_exist(self) -> None:
        markdown = "## Section\n\nContent\n"
        html = "<html><head><title>Fallback Title</title></head><body><h1>Main Title</h1></body></html>"

        cleaned = ensure_h1(markdown, html, "https://example.com/page")

        self.assertEqual(cleaned, "# Main Title\n\n## Section\n\nContent\n")

    def test_extract_title_prefers_h1_and_normalizes_entities(self) -> None:
        html = (
            "<html><head><title>Some Title</title></head>"
            "<body><h1> Boeing &amp; 707 \n Overview </h1></body></html>"
        )

        self.assertEqual(extract_title_from_html(html), "Boeing & 707 Overview")

    def test_falls_back_to_title_then_url_segment(self) -> None:
        title_html = "<html><head><title>Page Title</title></head><body></body></html>"
        self.assertEqual(extract_title_from_html(title_html), "Page Title")
        self.assertEqual(
            fallback_title_from_url("https://example.com/boeing-707_family"),
            "boeing 707 family",
        )


class MarkdownPreprocessorTests(unittest.TestCase):
    def test_needs_html_only_when_ensure_h1_requires_it(self) -> None:
        disabled = MarkdownPreprocessor(
            MarkdownPreprocessingConfig(enabled=True, ensure_h1=False)
        )
        enabled = MarkdownPreprocessor(
            MarkdownPreprocessingConfig(enabled=True, ensure_h1=True)
        )

        self.assertFalse(disabled.needs_html("Content\n", None))
        self.assertTrue(enabled.needs_html("Content\n", None))
        self.assertFalse(enabled.needs_html("# Title\n\nContent\n", None))

    def test_apply_runs_enabled_cleanup_steps(self) -> None:
        preprocessor = MarkdownPreprocessor(
            MarkdownPreprocessingConfig(
                enabled=True,
                ensure_h1=True,
                remove_jump_to_content=True,
                remove_wikipedia_subtitle=True,
            )
        )

        markdown = (
            "[Zum Inhalt springen](https://de.wikipedia.org/wiki/Boeing_707#bodyContent)\n"
            "aus Wikipedia, der freien Enzyklopädie\n"
            "Content\n"
        )

        cleaned = preprocessor.apply(
            markdown,
            "https://de.wikipedia.org/wiki/Boeing_707",
            "<html><body><h1>Boeing 707</h1></body></html>",
        )

        self.assertEqual(cleaned, "# Boeing 707\n\nContent\n")


if __name__ == "__main__":
    unittest.main()
