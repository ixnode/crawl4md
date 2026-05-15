import unittest
import time

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.remove_links import RuleRemoveLinks
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case


CASES = [
    # Tests with no links.
    RuleCase(
        name="no_links__disabled_preprocessing",
        config=MarkdownPreprocessingConfig(
            enabled=False,
            remove_links=False,
        ),
    ),
    RuleCase(
        name="no_links__disabled_remove_links",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=False,
        ),
    ),
    RuleCase(
        name="no_links__enabled_single",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=r"anchor:#custom-link",
        ),
    ),
    RuleCase(
        name="no_links__enabled_multiple",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=[
                r"anchor:#custom-link",
                r"anchor:cite_note",
            ],
        ),
    ),

    # Tests with no effect.
    RuleCase(
        name="no_effect",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=[
                r"anchor:#custom-link",
                r"anchor:cite_note",
            ],
        ),
    ),

    # Tests with anchor replacements.
    RuleCase(
        name="anchor",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=[
                "anchor:cite_note",
                "anchor:Citation_needed",
                "anchor:Verifiability",
                "anchor:#(?:[Bb]ody[Cc]ontent|content|content-start|main|main-content|maincontent)",
                "anchor:#[Vv]orlage_[Ll]esenswert",
                "anchor:#[Vv]orlage_[Ee]xzellent",
                "anchor:&veaction=edit[^)]*section=",
                "anchor:&action=edit[^)]*section=",
                "anchor:#custom-link",
            ],
        ),
    ),

    # Tests with all replacements.
    RuleCase(
        name="all__combined_anchor_text_unwrap_and_artifacts",
        config=MarkdownPreprocessingConfig(
            enabled=True,
            remove_links=[
                "anchor:cite_note",
                "anchor:Citation_needed",
                "anchor:Verifiability",
                "anchor:#bodyContent",
                "anchor:#custom-link",
                "anchor:veaction=edit[^)]*section=",
                "anchor:action=edit[^)]*section=",
                "text:Remove me",
                "unwrap:*",
            ],
        ),
    ),

]


class RuleRemoveLinksTests(unittest.TestCase):
    def test_remove_links(self) -> None:
        total = len(CASES)

        for index, case in enumerate(CASES, start=1):
            started_at = time.perf_counter()
            try:
                assert_rule_case(self, RuleRemoveLinks, case)
            except Exception:
                duration_ms = (time.perf_counter() - started_at) * 1000
                print(f"\n[{index}/{total}] [{case.name}] ❌ ({duration_ms:.0f} ms)")
                raise

            duration_ms = (time.perf_counter() - started_at) * 1000
            print(f"\n[{index}/{total}] [{case.name}] ✅ ({duration_ms:.0f} ms)", end="")
