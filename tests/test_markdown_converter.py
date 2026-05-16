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

import asyncio
import io
import os
import unittest
import warnings

from contextlib import redirect_stderr, redirect_stdout

from crawl4md.utils.markdown_converter_sessions import (
    MARKDOWN_CONVERTER_SESSION_ROOT,
    build_markdown_fetcher,
    find_markdown_converter_sessions,
    load_and_normalize_html,
    load_markdown_converter_session,
)
from tests.support.progress import run_progress_cases_async


class MarkdownConverterSessionTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    async def asyncSetUp(self) -> None:
        loop = asyncio.get_running_loop()
        loop.set_debug(False)

    async def test_converts_all_configured_sessions(self) -> None:
        group = os.environ.get("CRAWL4MD_MARKDOWN_CONVERTER_GROUP")
        update = os.environ.get("CRAWL4MD_MARKDOWN_CONVERTER_UPDATE") == "1"
        sessions = find_markdown_converter_sessions(group=group)

        if group:
            self.assertGreater(
                len(sessions),
                0,
                f"No markdown converter test sessions found for group '{group}'.",
            )
        else:
            self.assertGreater(len(sessions), 0, "No markdown converter test sessions found.")

        session_ids = [
            load_markdown_converter_session(session / "config.yml").id
            for session in sessions
        ]

        async def _run(index: int) -> None:
            session = sessions[index]
            session_name = session.relative_to(MARKDOWN_CONVERTER_SESSION_ROOT).as_posix()

            with self.subTest(session=session_name):
                test_session = load_markdown_converter_session(session / "config.yml")
                config = test_session.config
                fetcher = build_markdown_fetcher(config)
                html = load_and_normalize_html(
                    html_path=session / "data.html",
                    url=config.url,
                    fetcher=fetcher,
                )
                expected_markdown = (session / "data.md").read_text()

                converter = fetcher.build_markdown_converter()

                warnings.filterwarnings(
                    "ignore",
                    category=ResourceWarning,
                    message=r"unclosed database in <sqlite3\.Connection object at .*",
                    module=r"playwright\._impl\._local_utils",
                )

                output = io.StringIO()
                with redirect_stdout(output), redirect_stderr(output):
                    markdown = await converter.convert(html=html, url=config.url)

                if update:
                    (session / "data.md").write_text(markdown)
                    expected_markdown = markdown

                self.assertEqual(markdown, expected_markdown)

        await run_progress_cases_async(session_ids, _run)
