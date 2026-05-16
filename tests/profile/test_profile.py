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
from tests.base.progress_checks_test_case import ProgressChecksTestCase


class ProfileChecks:
    CHECK_METHODS = (
        "applies_wikipedia_profile_defaults",
        "project_preprocessing_overrides_profile_defaults",
        "project_crawl_overrides_profile_defaults",
        "unknown_profile_raises_error",
    )

    @staticmethod
    def applies_wikipedia_profile_defaults(test_case: unittest.TestCase) -> None:
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

        test_case.assertEqual(crawl.parser, "kreuzberg-dev")
        test_case.assertEqual(crawl.parse_type, "markdown")
        test_case.assertEqual(crawl.content_selector, ".mw-parser-output")
        test_case.assertTrue(normalization.enabled)
        test_case.assertTrue(normalization.entities)
        test_case.assertTrue(normalization.hidden_elements)
        test_case.assertTrue(normalization.urls)
        test_case.assertTrue(normalization.references)

        test_case.assertTrue(markdown.enabled)
        test_case.assertTrue(markdown.ensure_h1)
        test_case.assertIn("[Ff]rom Wikipedia, the free encyclopedia", markdown.remove_lines)
        test_case.assertIn("Einzelnachweise", markdown.remove_sections)
        test_case.assertTrue(markdown.remove_images)
        test_case.assertTrue(markdown.normalize_whitespace)

    @staticmethod
    def project_preprocessing_overrides_profile_defaults(test_case: unittest.TestCase) -> None:
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

        test_case.assertFalse(markdown.normalize_tables)
        test_case.assertEqual(markdown.remove_sections, ["Einzelnachweise"])
        test_case.assertIn("anchor:cite_note", markdown.remove_links)

    @staticmethod
    def project_crawl_overrides_profile_defaults(test_case: unittest.TestCase) -> None:
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

        test_case.assertEqual(crawl.parser, "kreuzberg-dev")
        test_case.assertEqual(crawl.parse_type, "markdown")
        test_case.assertEqual(crawl.content_selector, "#content")

    @staticmethod
    def unknown_profile_raises_error(test_case: unittest.TestCase) -> None:
        """Unknown profile names fail during profile application instead of being ignored silently."""
        with test_case.assertRaisesRegex(ValueError, "Unknown project profile: doesnotexist"):
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


class ProfileTests(ProgressChecksTestCase):
    """Tests profile lookup and merging before runtime preprocessing is built."""

    def test_profile(self) -> None:
        self.run_progress_check_methods(ProfileChecks)
