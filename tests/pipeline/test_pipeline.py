import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing import MarkdownPreprocessing
from tests.support.progress import run_progress_cases


class MarkdownPreprocessingPipelineTests(unittest.TestCase):
    """Tests the orchestration behavior of the Markdown preprocessing pipeline."""

    def setUp(self) -> None:
        self.maxDiff = None

    def test_pipeline(self) -> None:
        checks = [
            (
                "test_returns_markdown_unchanged_when_disabled",
                self._test_returns_markdown_unchanged_when_disabled,
            ),
            ("test_runs_multiple_enabled_rules", self._test_runs_multiple_enabled_rules),
            ("test_runs_remove_images_before_remove_links", self._test_runs_remove_images_before_remove_links),
        ]
        names = [name for name, _ in checks]

        def _run(index: int) -> None:
            _, check = checks[index]
            check()

        run_progress_cases(names, _run)

    def _test_returns_markdown_unchanged_when_disabled(self) -> None:
        """A disabled pipeline returns the original Markdown even when individual rules are configured."""
        config = MarkdownPreprocessingConfig(
            enabled=False,
            remove_sections=["Einzelnachweise"],
        )
        preprocessing = MarkdownPreprocessing(config)
        markdown = "## Geschichte\n\nText\n\n## Einzelnachweise\n\n1. Quelle\n"

        cleaned = preprocessing.process(markdown)

        self.assertEqual(cleaned, markdown)

    def _test_runs_multiple_enabled_rules(self) -> None:
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

    def _test_runs_remove_images_before_remove_links(self) -> None:
        """Image syntax is resolved before remaining Markdown links are processed."""
        config = MarkdownPreprocessingConfig(
            enabled=True,
            remove_images=True,
            remove_links="unwrap:Air India",
        )
        preprocessing = MarkdownPreprocessing(config)
        markdown = (
            "[![Air India](https://upload.wikimedia.org/image.jpg)]"
            "(https://de.wikipedia.org/wiki/Air_India)\n"
        )

        cleaned = preprocessing.process(markdown)

        self.assertEqual(cleaned, "Air India\n")
