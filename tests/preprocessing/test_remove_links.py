import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.remove_links import RuleRemoveLinks
from tests.preprocessing.data_provider import RuleCase, assert_rule_case, data_provider


CASES = [
    RuleCase(
        name="removes_standalone_skip_link_line",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links="anchor:#bodyContent",
        ),
        markdown=(
            "[Zum Inhalt springen](https://de.wikipedia.org/wiki/Boeing_707#bodyContent)\n"
            "\n"
            "# Boeing 707\n"
        ),
        expected="# Boeing 707\n",
        url="https://de.wikipedia.org/wiki/Boeing_707",
    ),
    RuleCase(
        name="removes_wikipedia_featured_badge",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=["#[Vv]orlage_[Ll]esenswert", "#[Vv]orlage_[Ee]xzellent"],
        ),
        markdown=(
            "[![Dies ist ein als lesenswert ausgezeichneter Artikel.]"
            "(https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/"
            "Qsicon_lesenswert.svg/20px-Qsicon_lesenswert.svg.png)]"
            "(#Vorlage_Lesenswert "
            '"Dies ist ein als lesenswert ausgezeichneter Artikel.")\n'
            "\n"
            "# Boeing 707\n"
        ),
        expected="# Boeing 707\n",
    ),
    RuleCase(
        name="removes_wikipedia_section_edit_links",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=["anchor:veaction=edit[^)]*section=", "anchor:action=edit[^)]*section="],
        ),
        markdown=(
            "## Geschichte\n"
            "\n"
            "[[Bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'veaction=edit&section=1 "Abschnitt bearbeiten: Geschichte") | '
            "[Quelltext bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'action=edit&section=1 "Quellcode des Abschnitts bearbeiten: Geschichte")]\n'
            "\n"
            "Text\n"
        ),
        expected="## Geschichte\n\nText\n",
    ),
    RuleCase(
        name="removes_cite_links_with_leading_spaces",
        config=MarkdownPreprocessingConfig(enabled=True, remove_links="cite_note"),
        markdown=(
            "Stückzahl 1010 [[17]](#cite_note-17) [[10]](#cite_note-10)\n"
            "Text[[1]](#cite_note-1)\n"
        ),
        expected="Stückzahl 1010\nText\n",
    ),
    RuleCase(
        name="keeps_links_when_disabled",
        config=MarkdownPreprocessingConfig(enabled=True, remove_links=False),
        markdown="Stückzahl 1010 [[17]](#cite_note-17)\n",
        expected="Stückzahl 1010 [[17]](#cite_note-17)\n",
    ),
    RuleCase(
        name="removes_links_matching_custom_target_pattern",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=r"custom-link",
        ),
        markdown="Text [custom](#custom-link) [keep](#other-link)\n",
        expected="Text [keep](#other-link)\n",
    ),
    RuleCase(
        name="removes_links_matching_anchor_prefix_target_pattern",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=r"anchor:#custom-link",
        ),
        markdown="Text [custom](#custom-link) [keep](#other-link)\n",
        expected="Text [keep](#other-link)\n",
    ),
    RuleCase(
        name="removes_links_matching_text_prefix_pattern",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=r"text:Zum Inhalt springen",
        ),
        markdown="Text [Zum Inhalt springen](#bodyContent) [keep](#bodyContent)\n",
        expected="Text [keep](#bodyContent)\n",
    ),
    RuleCase(
        name="removes_links_matching_multiple_target_patterns",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=["cite_note", r"custom-link"],
        ),
        markdown=(
            "Text [[17]](#cite_note-17) [custom](#custom-link) "
            "[keep](#other-link)\n"
        ),
        expected="Text [keep](#other-link)\n",
    ),
    RuleCase(
        name="removes_wikipedia_veaction_edit_link_with_parentheses_in_title",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links="veaction=edit[^)]*section=",
        ),
        markdown=(
            "[[Bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'veaction=edit&section=15 "Abschnitt bearbeiten: 707-020 (720)") | '
            "[Quelltext\n"
            "  bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'action=edit&section=15 "Quellcode des Abschnitts bearbeiten: 707-020 (720)")]\n'
        ),
        expected=(
            " | "
            "[Quelltext\n"
            "  bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'action=edit&section=15 "Quellcode des Abschnitts bearbeiten: 707-020 (720)")]\n'
        ),
    ),
    RuleCase(
        name="removes_wikipedia_action_edit_link_with_multiline_text_and_parentheses_in_title",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links="action=edit[^)]*section=",
        ),
        markdown=(
            "[[Bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'veaction=edit&section=15 "Abschnitt bearbeiten: 707-020 (720)") | '
            "[Quelltext\n"
            "  bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'action=edit&section=15 "Quellcode des Abschnitts bearbeiten: 707-020 (720)")]\n'
        ),
        expected=(
            "[[Bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'veaction=edit&section=15 "Abschnitt bearbeiten: 707-020 (720)") | \n'
        ),
    ),
    RuleCase(
        name="removes_both_wikipedia_edit_links_and_orphan_separator",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=[
                "veaction=edit[^)]*section=",
                "action=edit[^)]*section=",
            ],
        ),
        markdown=(
            "[[Bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'veaction=edit&section=15 "Abschnitt bearbeiten: 707-020 (720)") | '
            "[Quelltext bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'action=edit&section=15 "Quellcode des Abschnitts bearbeiten: 707-020 (720)")]\n'
        ),
        expected="\n",
    ),
    RuleCase(
        name="keeps_separator_when_other_link_remains_after_wikipedia_edit_link",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links="veaction=edit[^)]*section=",
        ),
        markdown=(
            "[[Bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'veaction=edit&section=15 "Abschnitt bearbeiten: 707-020 (720)") | '
            "[Quelltext bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'action=edit&section=15 "Quellcode des Abschnitts bearbeiten: 707-020 (720)")]\n'
        ),
        expected=(
            " | "
            "[Quelltext bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&"
            'action=edit&section=15 "Quellcode des Abschnitts bearbeiten: 707-020 (720)")]\n'
        ),
    ),
    RuleCase(
        name="unwraps_simple_markdown_link",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links="unwrap:Boeing",
        ),
        markdown='Die Boeing 707 wurde von [Boeing](https://de.wikipedia.org/wiki/Boeing "Boeing") gebaut.\n',
        expected="Die Boeing 707 wurde von Boeing gebaut.\n",
    ),
    RuleCase(
        name="unwraps_markdown_link_with_double_quote_title",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links="unwrap:Air India",
        ),
        markdown='[Air India](https://de.wikipedia.org/wiki/Air_India "Air India")\n',
        expected="Air India\n",
    ),
    RuleCase(
        name="unwraps_markdown_link_with_single_quote_title",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links="unwrap:Air India",
        ),
        markdown="[Air India](https://de.wikipedia.org/wiki/Air_India 'Air India')\n",
        expected="Air India\n",
    ),
    RuleCase(
        name="unwraps_markdown_link_with_parenthesized_title",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links="unwrap:Air India",
        ),
        markdown="[Air India](https://de.wikipedia.org/wiki/Air_India (Air India))\n",
        expected="Air India\n",
    ),
    RuleCase(
        name="unwraps_multiple_links_in_one_line",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=["unwrap:Boeing", "unwrap:Air India"],
        ),
        markdown=(
            "[Boeing](https://de.wikipedia.org/wiki/Boeing) und "
            "[Air India](https://de.wikipedia.org/wiki/Air_India)\n"
        ),
        expected="Boeing und Air India\n",
    ),
    RuleCase(
        name="unwraps_links_by_regex_matching_visible_text",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=r"unwrap:^Air India$",
        ),
        markdown=(
            "[Boeing](https://de.wikipedia.org/wiki/Boeing) und "
            '[Air India](https://de.wikipedia.org/wiki/Air_India "Air India")\n'
        ),
        expected="[Boeing](https://de.wikipedia.org/wiki/Boeing) und Air India\n",
    ),
    RuleCase(
        name="applies_mixed_anchor_text_and_unwrap_rules",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=[
                "anchor:cite_note",
                "text:Zum Inhalt springen",
                "unwrap:Boeing|Air India",
            ],
        ),
        markdown=(
            "[Zum Inhalt springen](#bodyContent) "
            "[Boeing](https://de.wikipedia.org/wiki/Boeing) "
            "[Air India](https://de.wikipedia.org/wiki/Air_India) "
            "[[17]](#cite_note-17) "
            "[keep](https://example.test)\n"
        ),
        expected="Boeing Air India [keep](https://example.test)\n",
    ),
    RuleCase(
        name="unwrap_removes_url_and_title",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links="unwrap:Air India",
        ),
        markdown='Text [Air India](https://de.wikipedia.org/wiki/Air_India "Air India") after\n',
        expected="Text Air India after\n",
    ),
    RuleCase(
        name="unwrap_star_unwraps_all_remaining_links",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links="unwrap:*",
        ),
        markdown=(
            "[Boeing](https://de.wikipedia.org/wiki/Boeing) und "
            '[Air India](https://de.wikipedia.org/wiki/Air_India "Air India")\n'
        ),
        expected="Boeing und Air India\n",
    ),
    RuleCase(
        name="applies_anchor_removals_before_unwrap_star",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=[
                "anchor:cite_note",
                "anchor:#(?:[Bb]ody[Cc]ontent|content|content-start|main|main-content|maincontent)",
                "anchor:#[Vv]orlage_[Ll]esenswert",
                "anchor:#[Vv]orlage_[Ee]xzellent",
                "anchor:veaction=edit[^)]*section=",
                "anchor:action=edit[^)]*section=",
                "unwrap:*",
            ],
        ),
        markdown=(
            "[Zum Inhalt springen](#bodyContent)\n"
            "[[17]](#cite_note-17)\n"
            "[Boeing](https://de.wikipedia.org/wiki/Boeing) und "
            '[Air India](https://de.wikipedia.org/wiki/Air_India "Air India")\n'
        ),
        expected="Boeing und Air India\n",
    ),
]


class RuleRemoveLinksTests(unittest.TestCase):
    @data_provider(CASES)
    def test_remove_links(self, case: RuleCase) -> None:
        assert_rule_case(self, RuleRemoveLinks, case)
