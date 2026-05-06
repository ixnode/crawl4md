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

from crawl4md.config import ParseType, PreprocessingConfig
from crawl4md.convert.crawl4ai_markdown import Crawl4AIMarkdownConverter


SESSION_ROOT = Path(__file__).parent / "data" / "markdown_converter"


class MarkdownConverterSessionConfig(BaseModel):
    parse_type: ParseType = "markdown"
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

                converter = Crawl4AIMarkdownConverter(
                    config=config.preprocessing.markdown,
                    parse_type=config.parse_type,
                )

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
        return MarkdownConverterSession(**yaml.safe_load(path.read_text()))

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
