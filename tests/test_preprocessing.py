import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing import MarkdownPreprocessing
from crawl4md.convert.preprocessing.rules.ensure_h1 import RuleEnsureH1
from crawl4md.convert.preprocessing.rules.normalize_linebreak import RuleNormalizeLinebreak
from crawl4md.convert.preprocessing.rules.normalize_tables import RuleNormalizeTables
from crawl4md.convert.preprocessing.rules.normalize_whitespace import RuleNormalizeWhitespace
from crawl4md.convert.preprocessing.rules.remove_cite_links import RuleRemoveCiteLinks
from crawl4md.convert.preprocessing.rules.remove_html_comments import RuleRemoveHtmlComments
from crawl4md.convert.preprocessing.rules.remove_jump_to_content import RuleRemoveJumpToContent
from crawl4md.convert.preprocessing.rules.remove_reference_sections import RuleRemoveReferenceSections
from crawl4md.convert.preprocessing.rules.remove_wiki_loves_earth_banner import RuleRemoveWikiLovesEarthBanner
from crawl4md.convert.preprocessing.rules.remove_wikipedia_edit_links import RuleRemoveWikipediaEditLinks
from crawl4md.convert.preprocessing.rules.remove_wikipedia_featured_badge import RuleRemoveWikipediaFeaturedBadge
from crawl4md.convert.preprocessing.rules.remove_wikipedia_subtitle import RuleRemoveWikipediaSubtitle


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


class RuleRemoveHtmlCommentsTests(unittest.TestCase):
    def test_removes_inline_html_comment(self) -> None:
        rule = RuleRemoveHtmlComments(
            MarkdownPreprocessingConfig(enabled=True, remove_html_comments=True)
        )
        markdown = "Text <!-- hidden --> mehr Text\n"

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, "Text  mehr Text\n")

    def test_removes_multiline_html_comment(self) -> None:
        rule = RuleRemoveHtmlComments(
            MarkdownPreprocessingConfig(enabled=True, remove_html_comments=True)
        )
        markdown = "Text\n<!-- first line\nsecond line -->\nMehr Text\n"

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, "Text\n\nMehr Text\n")


class RuleRemoveWikipediaSubtitleTests(unittest.TestCase):
    def test_removes_wikipedia_subtitle(self) -> None:
        rule = RuleRemoveWikipediaSubtitle(
            MarkdownPreprocessingConfig(enabled=True, remove_wikipedia_subtitle=True)
        )
        markdown = "Boeing 707 aus Wikipedia, der freien Enzyklopädie\n"

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, "Boeing 707\n")


class RuleRemoveWikipediaFeaturedBadgeTests(unittest.TestCase):
    def test_removes_wikipedia_featured_badge(self) -> None:
        rule = RuleRemoveWikipediaFeaturedBadge(
            MarkdownPreprocessingConfig(
                enabled=True,
                remove_wikipedia_featured_badge=True,
            )
        )
        markdown = (
            "[![Dies ist ein als lesenswert ausgezeichneter Artikel.]"
            "(https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/"
            "Qsicon_lesenswert.svg/20px-Qsicon_lesenswert.svg.png)]"
            "(#Vorlage_Lesenswert \"Dies ist ein als lesenswert ausgezeichneter Artikel.\")\n"
            "\n"
            "# Boeing 707\n"
        )

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, "# Boeing 707\n")


class RuleRemoveWikipediaEditLinksTests(unittest.TestCase):
    def test_removes_wikipedia_section_edit_links(self) -> None:
        rule = RuleRemoveWikipediaEditLinks(
            MarkdownPreprocessingConfig(
                enabled=True,
                remove_wikipedia_edit_links=True,
            )
        )
        markdown = (
            "## Geschichte\n"
            "\n"
            "[[Bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            "veaction=edit&section=1 \"Abschnitt bearbeiten: Geschichte\") | "
            "[Quelltext bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            "action=edit&section=1 \"Quellcode des Abschnitts bearbeiten: Geschichte\")]\n"
            "\n"
            "Text\n"
        )

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, "## Geschichte\n\nText\n")


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


class RuleRemoveCiteLinksTests(unittest.TestCase):
    def test_removes_cite_links_with_leading_spaces(self) -> None:
        rule = RuleRemoveCiteLinks(
            MarkdownPreprocessingConfig(enabled=True, remove_cite_links=True)
        )
        markdown = (
            "Stückzahl 1010 [[17]](#cite_note-17) [[10]](#cite_note-10)\n"
            "Text[[1]](#cite_note-1)\n"
        )

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, "Stückzahl 1010\nText\n")


class RuleNormalizeLinebreakTests(unittest.TestCase):
    def test_normalizes_blank_lines(self) -> None:
        rule = RuleNormalizeLinebreak(
            MarkdownPreprocessingConfig(enabled=True, normalize_linebreak=True)
        )
        markdown = "\n\n# Title\n\n\nText\n   \n\n## Section\n\n\nMore text\n\n"

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, "# Title\n\nText\n\n## Section\n\nMore text\n")

    def test_adds_spacing_around_table_and_code_block(self) -> None:
        rule = RuleNormalizeLinebreak(
            MarkdownPreprocessingConfig(enabled=True, normalize_linebreak=True)
        )
        markdown = (
            "# Title\n"
            "| A | B |\n"
            "| --- | --- |\n"
            "| 1 | 2 |\n"
            "```py\n"
            "x = 1  \n"
            "print(x)\n"
            "```\n"
            "Text\n"
        )

        cleaned = rule.apply(markdown)

        self.assertEqual(
            cleaned,
            "# Title\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n\n```py\nx = 1  \nprint(x)\n```\n\nText\n",
        )

    def test_adds_blank_line_after_single_column_table(self) -> None:
        rule = RuleNormalizeLinebreak(
            MarkdownPreprocessingConfig(enabled=True, normalize_linebreak=True)
        )
        markdown = (
            "| Boeing 707 |\n"
            "| --- |\n"
            "| Row |\n"
            "Die **Boeing 707** ist ein Flugzeug.\n"
        )

        cleaned = rule.apply(markdown)

        self.assertEqual(
            cleaned,
            "| Boeing 707 |\n| --- |\n| Row |\n\nDie **Boeing 707** ist ein Flugzeug.\n",
        )

    def test_splits_adjacent_paragraph_lines_with_blank_lines(self) -> None:
        rule = RuleNormalizeLinebreak(
            MarkdownPreprocessingConfig(enabled=True, normalize_linebreak=True)
        )
        markdown = (
            "### Vorgeschichte\n\n"
            "[Boeing 367](//de.wikipedia.org/wiki/Boeing_C-97 \"Boeing C-97\") (C-97)\n"
            "Seit dem Jungfernflug des ersten strahlgetriebenen Flugzeugs.\n"
            "Gleichzeitig verfolgte Boeing in dieser Zeit Überlegungen.\n"
        )

        cleaned = rule.apply(markdown)

        self.assertEqual(
            cleaned,
            "### Vorgeschichte\n\n"
            "[Boeing 367](//de.wikipedia.org/wiki/Boeing_C-97 \"Boeing C-97\") (C-97)\n\n"
            "Seit dem Jungfernflug des ersten strahlgetriebenen Flugzeugs.\n\n"
            "Gleichzeitig verfolgte Boeing in dieser Zeit Überlegungen.\n",
        )

    def test_removes_blank_lines_between_list_items(self) -> None:
        rule = RuleNormalizeLinebreak(
            MarkdownPreprocessingConfig(enabled=True, normalize_linebreak=True)
        )
        markdown = (
            "# Checklist\n\n"
            "Before release:\n"
            " * Run the converter tests\n\n"
            " * Review the generated Markdown\n\n"
            " * Update the changelog\n\n"
            "Deployment order:\n\n"
            " 1. Build the package\n\n"
            " 2. Publish the artifact\n\n"
            " 3. Verify the installation\n"
        )

        cleaned = rule.apply(markdown)

        self.assertEqual(
            cleaned,
            "# Checklist\n\n"
            "Before release:\n\n"
            " * Run the converter tests\n"
            " * Review the generated Markdown\n"
            " * Update the changelog\n\n"
            "Deployment order:\n\n"
            " 1. Build the package\n"
            " 2. Publish the artifact\n"
            " 3. Verify the installation\n",
        )


class RuleNormalizeWhitespaceTests(unittest.TestCase):
    def test_normalizes_trailing_spaces(self) -> None:
        rule = RuleNormalizeWhitespace(
            MarkdownPreprocessingConfig(enabled=True, normalize_whitespace=True)
        )
        markdown = "# Title   \nText   \n\n"

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, "# Title\nText\n\n")

    def test_inserts_space_before_link_when_text_touches_link(self) -> None:
        rule = RuleNormalizeWhitespace(
            MarkdownPreprocessingConfig(enabled=True, normalize_whitespace=True)
        )
        markdown = '_Eine Boeing 707 der[Air India](https://de.wikipedia.org/wiki/Air_India "Air India")_\n'

        cleaned = rule.apply(markdown)

        self.assertEqual(
            cleaned,
            '_Eine Boeing 707 der [Air India](https://de.wikipedia.org/wiki/Air_India "Air India")_\n',
        )

    def test_inserts_space_before_link_after_number_text(self) -> None:
        rule = RuleNormalizeWhitespace(
            MarkdownPreprocessingConfig(enabled=True, normalize_whitespace=True)
        )
        markdown = 'Vereinigte Staaten 48[Vereinigte Staaten](https://de.wikipedia.org/wiki/Vereinigte_Staaten "Vereinigte Staaten")\n'

        cleaned = rule.apply(markdown)

        self.assertEqual(
            cleaned,
            'Vereinigte Staaten 48 [Vereinigte Staaten](https://de.wikipedia.org/wiki/Vereinigte_Staaten "Vereinigte Staaten")\n',
        )

    def test_keeps_emphasis_before_link_unchanged(self) -> None:
        rule = RuleNormalizeWhitespace(
            MarkdownPreprocessingConfig(enabled=True, normalize_whitespace=True)
        )
        markdown = (
            'In dem Film *[Airport](https://de.wikipedia.org/wiki/Airport_(Film) '
            '"Airport (Film)")* spielt eine Boeing 707 eine wichtige Nebenrolle.\n'
        )

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, markdown)

    def test_inserts_space_before_parentheses(self) -> None:
        rule = RuleNormalizeWhitespace(
            MarkdownPreprocessingConfig(enabled=True, normalize_whitespace=True)
        )
        markdown = "| Produktionszeit | 1957 bis 1982/1991(zivil / militärisch) |\n"

        cleaned = rule.apply(markdown)

        self.assertEqual(
            cleaned,
            "| Produktionszeit | 1957 bis 1982/1991 (zivil / militärisch) |\n",
        )

    def test_keeps_parentheses_inside_link_targets_unchanged(self) -> None:
        rule = RuleNormalizeWhitespace(
            MarkdownPreprocessingConfig(enabled=True, normalize_whitespace=True)
        )
        markdown = (
            "[![](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/"
            "Boeing_707-124_%28Continental_Airlines%29_LAX.jpg/"
            "250px-Boeing_707-124_%28Continental_Airlines%29_LAX.jpg)]"
            "(https://de.wikipedia.org/wiki/Datei:Boeing_707-124_"
            "(Continental_Airlines)_LAX.jpg)\n"
        )

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, markdown)


class RuleNormalizeTablesTests(unittest.TestCase):
    def test_removes_empty_table_rows(self) -> None:
        rule = RuleNormalizeTables(
            MarkdownPreprocessingConfig(enabled=True, normalize_tables=True)
        )
        markdown = (
            "| Boeing 707 | |\n"
            "| --- | --- |\n"
            "| Typ | Schmalrumpfflugzeug |\n"
            "| | |\n"
            "| Hersteller | Boeing Airplane Company |\n"
        )

        cleaned = rule.apply(markdown)

        self.assertEqual(
            cleaned,
            "| Boeing 707 | |\n"
            "| --- | --- |\n"
            "| Typ | Schmalrumpfflugzeug |\n"
            "| Hersteller | Boeing Airplane Company |\n",
        )

    def test_pads_short_table_rows(self) -> None:
        rule = RuleNormalizeTables(
            MarkdownPreprocessingConfig(enabled=True, normalize_tables=True)
        )
        markdown = (
            "| A | B |\n"
            "| --- | --- |\n"
            "| one |\n"
        )

        cleaned = rule.apply(markdown)

        self.assertEqual(cleaned, "| A | B |\n| --- | --- |\n| one | |\n")


if __name__ == "__main__":
    unittest.main()
