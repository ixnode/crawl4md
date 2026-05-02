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

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from ..config import ParseType


async def convert_markdown(
    html: str,
    parse_type: ParseType = "markdown",
) -> str:
    raw_html_url = f"raw:{html}"

    if parse_type == "markdown-fit":
        markdown_generator = DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(threshold=0.5),
            options={"ignore_links": False},
        )
        config = CrawlerRunConfig(markdown_generator=markdown_generator)
    else:
        config = CrawlerRunConfig()

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=raw_html_url, config=config)

        if parse_type == "markdown-fit":
            markdown = result.markdown.fit_markdown or result.markdown.raw_markdown or ""
        else:
            markdown = result.markdown.raw_markdown or ""

        return markdown
