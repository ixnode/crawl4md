import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.preprocessing import MarkdownPreprocessing
from crawl4md.preprocessing.rules.ensure_h1 import RuleEnsureH1
from crawl4md.preprocessing.rules.remove_jump_to_content import RuleRemoveJumpToContent
from crawl4md.preprocessing.rules.remove_reference_sections import RuleRemoveReferenceSections
from crawl4md.preprocessing.rules.remove_wiki_loves_earth_banner import RuleRemoveWikiLovesEarthBanner
from crawl4md.preprocessing.rules.remove_wikipedia_subtitle import RuleRemoveWikipediaSubtitle


class MarkdownPreprocessingTests(unittest.TestCase):
    def test_returns_markdown_unchanged_when_disabled(self) -> None:
        config = MarkdownPreprocessingConfig(
            enabled=False,
            remove_reference_sections=True,
            reference_headings=["Einzelnachweise"],
        )
        preprocessing = MarkdownPreprocessing(config)
        markdown = "## Geschichte\n\nText\n\n## Einzelnachweise\n\n1. Quelle\n"

        cleaned = preprocessing.process(markdown)

        self.assertEqual(cleaned, markdown)

    def test_runs_multiple_enabled_rules(self) -> None:
        config = MarkdownPreprocessingConfig(
            enabled=True,
            remove_jump_to_content=True,
            remove_wikipedia_subtitle=True,
            remove_reference_sections=True,
            ensure_h1=True,
            reference_headings=["Einzelnachweise"],
        )
        preprocessing = MarkdownPreprocessing(config)
        markdown = (
            "[Zum Inhalt springen](https://de.wikipedia.org/wiki/Boeing_707#bodyContent)\n"
            "aus Wikipedia, der freien Enzyklopädie\n"
            "Text\n\n"
            "## Einzelnachweise\n\n"
            "1. Quelle\n"
        )

        cleaned = preprocessing.process(
            markdown,
            url="https://de.wikipedia.org/wiki/Boeing_707",
            html="<html><body><h1>Boeing 707</h1></body></html>",
        )

        self.assertEqual(cleaned, "# Boeing 707\n\nText\n")


class RuleRemoveReferenceSectionsTests(unittest.TestCase):
    def test_removes_reference_section_from_matching_heading(self) -> None:
        config = MarkdownPreprocessingConfig(
            enabled=True,
            remove_reference_sections=True,
            reference_headings=["Einzelnachweise", "Weblinks"],
        )
        rule = RuleRemoveReferenceSections(config)
        markdown = "## Geschichte\n\nText\n\n## Einzelnachweise\n\n1. Quelle A\n2. Quelle B\n"

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, "## Geschichte\n\nText\n")

    def test_supports_heading_levels_numbering_and_anchor_suffixes(self) -> None:
        config = MarkdownPreprocessingConfig(
            enabled=True,
            remove_reference_sections=True,
            reference_headings=["Weblinks"],
        )
        rule = RuleRemoveReferenceSections(config)
        markdown = (
            "## Geschichte\n\n"
            "Text mit **Formatierung** und [Link](https://example.com).\n\n"
            "### 8. Weblinks {#weblinks}\n\n"
            "- https://example.com\n"
        )

        cleaned = rule.apply(markdown)

        self.assertEqual(
            cleaned,
            "## Geschichte\n\nText mit **Formatierung** und [Link](https://example.com).\n",
        )

    def test_matches_reference_headings_case_insensitively(self) -> None:
        config = MarkdownPreprocessingConfig(
            enabled=True,
            remove_reference_sections=True,
            reference_headings=["external links"],
        )
        rule = RuleRemoveReferenceSections(config)
        markdown = "# Title\n\nContent\n\n#### External Links\n\n- Link\n"

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, "# Title\n\nContent\n")


class RuleEnsureH1Tests(unittest.TestCase):
    def test_keeps_existing_h1(self) -> None:
        rule = RuleEnsureH1(MarkdownPreprocessingConfig(enabled=True, ensure_h1=True))
        markdown = "# Existing Title\n\nContent\n"

        cleaned = rule.apply(markdown, url="https://example.com/page")

        self.assertEqual(cleaned, markdown)

    def test_injects_h1_from_html(self) -> None:
        rule = RuleEnsureH1(MarkdownPreprocessingConfig(enabled=True, ensure_h1=True))
        markdown = "## Section\n\nContent\n"
        html = "<html><head><title>Fallback</title></head><body><h1>Main Title</h1></body></html>"

        cleaned = rule.apply(markdown, url="https://example.com/page", html=html)

        self.assertEqual(cleaned, "# Main Title\n\n## Section\n\nContent\n")


class RuleRemoveJumpToContentTests(unittest.TestCase):
    def test_removes_standalone_skip_link_line(self) -> None:
        rule = RuleRemoveJumpToContent(
            MarkdownPreprocessingConfig(enabled=True, remove_jump_to_content=True)
        )
        markdown = (
            "[Zum Inhalt springen](https://de.wikipedia.org/wiki/Boeing_707#bodyContent)\n"
            "\n"
            "# Boeing 707\n"
        )

        cleaned = rule.apply(markdown, url="https://de.wikipedia.org/wiki/Boeing_707")

        self.assertEqual(cleaned, "# Boeing 707\n")


class RuleRemoveWikipediaSubtitleTests(unittest.TestCase):
    def test_removes_wikipedia_subtitle(self) -> None:
        rule = RuleRemoveWikipediaSubtitle(
            MarkdownPreprocessingConfig(enabled=True, remove_wikipedia_subtitle=True)
        )
        markdown = "Boeing 707 aus Wikipedia, der freien Enzyklopädie\n"

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, "Boeing 707\n")


class RuleRemoveWikiLovesEarthBannerTests(unittest.TestCase):
    def test_removes_multiline_wikidata_banner_link(self) -> None:
        rule = RuleRemoveWikiLovesEarthBanner(
            MarkdownPreprocessingConfig(enabled=True, remove_wiki_loves_earth_banner=True)
        )
        markdown = (
            "[\n"
            "| Nimm teil am Wiki\u00addata-Wett\u00adbewerb |\n"
            "| --- | ](https://www.wikidata.org/wiki/Wikidata:Events/Coordinate_Me_2026)\n"
            "\n"
            "# Boeing 707\n"
        )

        cleaned = rule.apply(markdown, url="https://de.wikipedia.org/wiki/Boeing_707")

        self.assertEqual(cleaned, "# Boeing 707\n")


if __name__ == "__main__":
    unittest.main()
