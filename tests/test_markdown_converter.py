# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-05)
# @since 1.0.0 (2026-05-05) First version

from contextlib import redirect_stderr, redirect_stdout
import io
import os
from pathlib import Path
import time
import unittest
import warnings

import yaml
from pydantic import BaseModel, Field

from crawl4md.config import CrawlConfig, PreprocessingConfig, apply_profile_defaults
from crawl4md.convert.markdown_converter_crawl4ai import MarkdownConverterCrawl4AI
from crawl4md.convert.markdown_converter_kreuzberg_dev import MarkdownConverterKreuzbergDev


SESSION_ROOT = Path(__file__).parent / "data" / "markdown_converter"


class MarkdownConverterSessionConfig(BaseModel):
    profile: str | None = None
    crawl: CrawlConfig = Field(default_factory=CrawlConfig)
    url: str | None = None
    preprocessing: PreprocessingConfig = Field(default_factory=PreprocessingConfig)


class MarkdownConverterSession(BaseModel):
    id: str
    title: str
    description: str
    config: MarkdownConverterSessionConfig


class MarkdownConverterSessionTests(unittest.IsolatedAsyncioTestCase):

    async def test_converts_all_configured_sessions(self) -> None:
        group = os.environ.get("CRAWL4MD_MARKDOWN_CONVERTER_GROUP")
        sessions = self._find_sessions(group=group)

        if group:
            self.assertGreater(
                len(sessions),
                0,
                f"No markdown converter test sessions found for group '{group}'.",
            )
        else:
            self.assertGreater(len(sessions), 0, "No markdown converter test sessions found.")

        for index, session in enumerate(sessions, start=1):
            session_name = session.relative_to(SESSION_ROOT).as_posix()

            with self.subTest(session=session_name):
                test_session = self._load_config(session / "config.yml")
                config = test_session.config
                html = (session / "data.html").read_text()
                expected_markdown = (session / "data.md").read_text()

                converter = self._build_converter(config)

                warnings.filterwarnings(
                    "ignore",
                    category=ResourceWarning,
                    message=r"unclosed database in <sqlite3\.Connection object at .*",
                    module=r"playwright\._impl\._local_utils",
                )

                output = io.StringIO()
                with redirect_stdout(output), redirect_stderr(output):
                    started_at = time.perf_counter()
                    markdown = await converter.convert(html=html, url=config.url)
                    duration_ms = (time.perf_counter() - started_at) * 1000

                print(
                    f"\n[{index}/{len(sessions)}] [{test_session.id}] {test_session.title} "
                    f"({duration_ms:.0f} ms)\n"
                    f"{test_session.description}"
                )

                self.assertEqual(markdown, expected_markdown)

    def _load_config(self, path: Path) -> MarkdownConverterSession:
        data = yaml.safe_load(path.read_text())
        data["config"] = apply_profile_defaults(data["config"])
        return MarkdownConverterSession(**data)

    async def test_crawl4ai_converter_supports_content_selector(self) -> None:
        config = MarkdownConverterSessionConfig(
            crawl=CrawlConfig(
                parser="crawl4ai",
                parse_type="markdown",
                content_selector="main",
            )
        )
        converter = self._build_converter(config)
        html = (
            "<html><body>"
            "<nav><h1>Navigation</h1><p>Ignore me</p></nav>"
            "<main><h1>Content</h1><p>Keep me</p></main>"
            "</body></html>"
        )

        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output):
            markdown = await converter.convert(html=html, url="https://example.test")

        self.assertIn("# Content", markdown)
        self.assertIn("Keep me", markdown)
        self.assertNotIn("Navigation", markdown)
        self.assertNotIn("Ignore me", markdown)

    def test_crawl4ai_config_allows_content_selector(self) -> None:
        config = CrawlConfig(
            parser="crawl4ai",
            parse_type="markdown",
            content_selector="main",
        )

        self.assertEqual(config.content_selector, "main")

    def _build_converter(self, config: MarkdownConverterSessionConfig) -> MarkdownConverterCrawl4AI:
        if config.crawl.parser == "crawl4ai":
            return MarkdownConverterCrawl4AI(
                config=config.preprocessing.markdown,
                parse_type=config.crawl.parse_type,
                content_selector=config.crawl.content_selector,
            )

        if config.crawl.parser == "kreuzberg-dev":
            return MarkdownConverterKreuzbergDev(
                config=config.preprocessing.markdown,
                parse_type=config.crawl.parse_type,
                content_selector=config.crawl.content_selector,
            )

        raise ValueError(f"Unknown markdown converter parser: {config.crawl.parser}")

    def _find_sessions(self, group: str | None = None) -> list[Path]:
        if not group:
            root = SESSION_ROOT
        else:
            group_path = Path(group)
            if group_path.is_absolute() or ".." in group_path.parts:
                return []
            root = SESSION_ROOT / group_path

        return sorted(path.parent for path in root.rglob("config.yml"))


if __name__ == "__main__":
    unittest.main()
