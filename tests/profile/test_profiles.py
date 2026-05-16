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

from crawl4md.config import AppConfig, apply_profiles
from tests.support.progress import run_progress_cases


class ProfileTests(unittest.TestCase):
    """Tests profile lookup and merging before runtime preprocessing is built."""

    def setUp(self) -> None:
        self.maxDiff = None

    def test_profile(self) -> None:
        checks = [
            (
                "test_applies_wikipedia_profile_defaults",
                self._test_applies_wikipedia_profile_defaults),
            (
                "test_project_preprocessing_overrides_profile_defaults",
                self._test_project_preprocessing_overrides_profile_defaults,
            ),
            (
                "test_project_crawl_overrides_profile_defaults",
                self._test_project_crawl_overrides_profile_defaults),
            (
                "test_unknown_profile_raises_error",
                self._test_unknown_profile_raises_error
            ),
        ]
        names = [name for name, _ in checks]

        def _run(index: int) -> None:
            _, check = checks[index]
            check()

        run_progress_cases(names, _run)

    def _test_applies_wikipedia_profile_defaults(self) -> None:
        """Profile defaults from the built-in wikipedia profile are applied to a project."""
        config = AppConfig(
            **apply_profiles(
                {
                    "projects": {
                        "planes": {
                            "profile": "wikipedia",
                            "type": "pages",
                            "sources": ["https://de.wikipedia.org/wiki/Boeing_707"],
                        }
                    }
                }
            )
        )

        markdown = config.projects["planes"].preprocessing.markdown
        crawl = config.projects["planes"].crawl
        normalization = config.projects["planes"].normalization

        self.assertEqual(crawl.parser, "kreuzberg-dev")
        self.assertEqual(crawl.parse_type, "markdown")
        self.assertEqual(crawl.content_selector, ".mw-parser-output")
        self.assertTrue(normalization.enabled)
        self.assertTrue(normalization.entities)
        self.assertTrue(normalization.hidden_elements)
        self.assertTrue(normalization.urls)
        self.assertTrue(normalization.references)

        self.assertTrue(markdown.enabled)
        self.assertTrue(markdown.ensure_h1)
        self.assertIn("[Ff]rom Wikipedia, the free encyclopedia", markdown.remove_lines)
        self.assertIn("Einzelnachweise", markdown.remove_sections)
        self.assertTrue(markdown.remove_images)
        self.assertTrue(markdown.normalize_whitespace)

    def _test_project_preprocessing_overrides_profile_defaults(self) -> None:
        """Project-level preprocessing values override profile defaults without removing unrelated defaults."""
        config = AppConfig(
            **apply_profiles(
                {
                    "projects": {
                        "planes": {
                            "profile": "wikipedia",
                            "type": "pages",
                            "sources": ["https://de.wikipedia.org/wiki/Boeing_707"],
                            "preprocessing": {
                                "markdown": {
                                    "normalize_tables": False,
                                    "remove_sections": ["Einzelnachweise"],
                                }
                            },
                        }
                    }
                }
            )
        )

        markdown = config.projects["planes"].preprocessing.markdown

        self.assertFalse(markdown.normalize_tables)
        self.assertEqual(markdown.remove_sections, ["Einzelnachweise"])
        self.assertIn("anchor:cite_note", markdown.remove_links)

    def _test_project_crawl_overrides_profile_defaults(self) -> None:
        """Project-level crawl values override profile defaults without removing unrelated defaults."""
        config = AppConfig(
            **apply_profiles(
                {
                    "projects": {
                        "planes": {
                            "profile": "wikipedia",
                            "type": "pages",
                            "sources": ["https://de.wikipedia.org/wiki/Boeing_707"],
                            "crawl": {
                                "content_selector": "#content",
                            },
                        }
                    }
                }
            )
        )

        crawl = config.projects["planes"].crawl

        self.assertEqual(crawl.parser, "kreuzberg-dev")
        self.assertEqual(crawl.parse_type, "markdown")
        self.assertEqual(crawl.content_selector, "#content")

    def _test_unknown_profile_raises_error(self) -> None:
        """Unknown profile names fail during profile application instead of being ignored silently."""
        with self.assertRaisesRegex(ValueError, "Unknown project profile: doesnotexist"):
            apply_profiles(
                {
                    "projects": {
                        "broken": {
                            "profile": "doesnotexist",
                            "type": "pages",
                            "sources": ["https://example.test"],
                        }
                    }
                }
            )
