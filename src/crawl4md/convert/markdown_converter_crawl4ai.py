# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-02)
# @since 1.0.0 (2026-05-02) First version

import asyncio
from contextlib import redirect_stderr, redirect_stdout
import io
import warnings

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from ..config import MarkdownPreprocessingConfig, ParseType
from .preprocessing import MarkdownPreprocessing


warnings.filterwarnings(
    "ignore",
    category=ResourceWarning,
    message=r"unclosed database in <sqlite3\.Connection object at .*",
    module=r"playwright\._impl\._local_utils",
)


class MarkdownConverterCrawl4AI:
    def __init__(
        self,
        config: MarkdownPreprocessingConfig,
        parse_type: ParseType = "markdown",
    ) -> None:
        self.config = config
        self.parse_type = parse_type

    async def convert(
        self,
        html: str,
        url: str | None = None,
    ) -> str:
        raw_html_url = f"raw:{html}"

        if self.parse_type == "markdown-fit":
            markdown_generator = DefaultMarkdownGenerator(
                content_filter=PruningContentFilter(threshold=0.5),
                options={"ignore_links": False},
            )
            crawler_config = CrawlerRunConfig(markdown_generator=markdown_generator)
        else:
            crawler_config = CrawlerRunConfig()

        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output):
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=raw_html_url, config=crawler_config)

        if self.parse_type == "markdown-fit":
            markdown = result.markdown.fit_markdown or result.markdown.raw_markdown or ""
        else:
            markdown = result.markdown.raw_markdown or ""

        preprocessing = MarkdownPreprocessing(self.config)

        return preprocessing.process(markdown, url=url, html=html)

    def convert_sync(
        self,
        html: str,
        url: str | None = None,
    ) -> str:
        return asyncio.run(self.convert(html=html, url=url))
