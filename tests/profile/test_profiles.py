import unittest

from crawl4md.config import AppConfig, apply_profiles


class ProfileTests(unittest.TestCase):
    """Tests profile lookup and merging before runtime preprocessing is built."""

    def test_applies_wikipedia_profile_defaults(self) -> None:
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

        self.assertEqual(crawl.parser, "kreuzberg-dev")
        self.assertEqual(crawl.parse_type, "markdown")
        self.assertEqual(crawl.content_selector, ".mw-parser-output")

        self.assertTrue(markdown.enabled)
        self.assertTrue(markdown.ensure_h1)
        self.assertIn("[Ff]rom Wikipedia, the free encyclopedia", markdown.remove_lines)
        self.assertIn("Einzelnachweise", markdown.remove_sections)
        self.assertTrue(markdown.remove_images)
        self.assertTrue(markdown.normalize_whitespace)

    def test_project_preprocessing_overrides_profile_defaults(self) -> None:
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

    def test_project_crawl_overrides_profile_defaults(self) -> None:
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

    def test_unknown_profile_raises_error(self) -> None:
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
