# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-16)
# @since 1.0.0 (2026-05-16) First version

import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing import MarkdownPreprocessing
from tests.base.progress_checks_test_case import ProgressChecksTestCase


class PipelineChecks:
    CHECK_METHODS = (
        "returns_markdown_unchanged_when_disabled",
        "runs_multiple_enabled_rules",
        "runs_remove_images_before_remove_links",
    )

    @staticmethod
    def returns_markdown_unchanged_when_disabled(test_case: unittest.TestCase) -> None:
        """A disabled pipeline returns the original Markdown even when individual rules are configured."""
        config = MarkdownPreprocessingConfig(
            enabled=False,
            remove_sections=["Einzelnachweise"],
        )
        preprocessing = MarkdownPreprocessing(config)
        markdown = "## Geschichte\n\nText\n\n## Einzelnachweise\n\n1. Quelle\n"

        cleaned = preprocessing.process(markdown)

        test_case.assertEqual(cleaned, markdown)

    @staticmethod
    def runs_multiple_enabled_rules(test_case: unittest.TestCase) -> None:
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

        test_case.assertEqual(cleaned, "# Boeing 707\n\nText\n")

    @staticmethod
    def runs_remove_images_before_remove_links(test_case: unittest.TestCase) -> None:
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

        test_case.assertEqual(cleaned, 'Figure: "Air India"\n')


class PipelineTests(ProgressChecksTestCase):
    """Tests the orchestration behavior of the Markdown preprocessing pipeline."""

    def test_pipeline(self) -> None:
        self.run_progress_check_methods(PipelineChecks)
