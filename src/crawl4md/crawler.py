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

import logging

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from .config import ParseType
from .fetch.html import HtmlFetcher
from .fetch.normalize.mediawiki_entity import MediawikiEntityNormalizer
from .fetch.normalize.mediawiki_hidden_span import MediawikiHiddenSpanNormalizer
from .fetch.normalize.url import UrlNormalizer

logging.getLogger("crawl4ai").setLevel(logging.ERROR)


async def fetch_markdown(
    url: str,
    parse_type: ParseType = "markdown",
) -> str:
    fetcher = HtmlFetcher(
        normalizers=[
            MediawikiEntityNormalizer(),
            MediawikiHiddenSpanNormalizer(),
            UrlNormalizer(url=url)
        ]
    )
    raw_html = await fetcher.fetch(url=url)
    raw_html_url = f"raw:{raw_html}"

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
