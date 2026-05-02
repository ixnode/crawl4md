import logging

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from .config import ParseType


logging.getLogger("crawl4ai").setLevel(logging.ERROR)


async def fetch_markdown(
    url: str,
    parse_type: ParseType = "markdown",
) -> str:
    if parse_type == "markdown-fit":
        markdown_generator = DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(threshold=0.5),
            options={"ignore_links": False},
        )
        config = CrawlerRunConfig(markdown_generator=markdown_generator)
    else:
        config = CrawlerRunConfig()

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)

        if parse_type == "markdown-fit":
            markdown = result.markdown.fit_markdown or result.markdown.raw_markdown or ""
        else:
            markdown = result.markdown.raw_markdown or ""

        return markdown
