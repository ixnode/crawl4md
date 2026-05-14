import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing import MarkdownPreprocessing


class MarkdownPreprocessingPipelineTests(unittest.TestCase):
    """Tests the orchestration behavior of the Markdown preprocessing pipeline."""

    def test_returns_markdown_unchanged_when_disabled(self) -> None:
        """A disabled pipeline returns the original Markdown even when individual rules are configured."""
        config = MarkdownPreprocessingConfig(
            enabled=False,
            remove_sections=["Einzelnachweise"],
        )
        preprocessing = MarkdownPreprocessing(config)
        markdown = "## Geschichte\n\nText\n\n## Einzelnachweise\n\n1. Quelle\n"

        cleaned = preprocessing.process(markdown)

        self.assertEqual(cleaned, markdown)

    def test_runs_multiple_enabled_rules(self) -> None:
        """An enabled pipeline runs configured rules together in the expected order."""
        config = MarkdownPreprocessingConfig(
            enabled=True,
            remove_links="anchor:#bodyContent",
            remove_lines=[
                "[Aa]us Wikipedia, der freien Enzyklopädie",
                "[Ff]rom Wikipedia, the free encyclopedia",
            ],
            ensure_h1=True,
            remove_sections=["Einzelnachweise"],
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
