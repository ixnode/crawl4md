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
]


class RuleRemoveLinksTests(unittest.TestCase):
    @data_provider(CASES)
    def test_remove_links(self, case: RuleCase) -> None:
        assert_rule_case(self, RuleRemoveLinks, case)
