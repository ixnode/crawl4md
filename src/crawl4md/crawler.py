import logging

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from .config import ParseType


logging.getLogger("crawl4ai").setLevel(logging.ERROR)


async def fetch_markdown(url: str, parse_type: ParseType = "markdown") -> str:
    markdown_generator = None

    if parse_type == "markdown-fit":
        markdown_generator = DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(
                threshold=0.4,
                threshold_type="fixed",
                min_word_threshold=5,
            )
        )

    config = CrawlerRunConfig(
        markdown_generator=markdown_generator,
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            config=config,
        )

        if parse_type == "markdown-fit":
            return result.markdown.fit_markdown or result.markdown.raw_markdown or ""

        return result.markdown.raw_markdown or ""
