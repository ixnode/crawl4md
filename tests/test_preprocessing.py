import unittest

from crawl4md.config import AppConfig, MarkdownPreprocessingConfig, apply_profiles
from crawl4md.convert.preprocessing import MarkdownPreprocessing


class MarkdownPreprocessingTests(unittest.TestCase):
    def test_applies_wikipedia_profile_defaults(self) -> None:
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

        self.assertTrue(markdown.enabled)
        self.assertTrue(markdown.ensure_h1)
        self.assertIn("[Ff]rom Wikipedia, the free encyclopedia", markdown.remove_lines)
        self.assertIn("Einzelnachweise", markdown.remove_sections)
        self.assertTrue(markdown.remove_images)
        self.assertTrue(markdown.normalize_whitespace)

    def test_project_preprocessing_overrides_profile_defaults(self) -> None:
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
        self.assertIn("cite_note", markdown.remove_links)

    def test_unknown_profile_raises_error(self) -> None:
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

    def test_returns_markdown_unchanged_when_disabled(self) -> None:
        config = MarkdownPreprocessingConfig(
            enabled=False,
            remove_sections=["Einzelnachweise"],
        )
        preprocessing = MarkdownPreprocessing(config)
        markdown = "## Geschichte\n\nText\n\n## Einzelnachweise\n\n1. Quelle\n"

        cleaned = preprocessing.process(markdown)

        self.assertEqual(cleaned, markdown)

    def test_runs_multiple_enabled_rules(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
