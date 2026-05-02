import logging

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from .config import MarkdownPreprocessingConfig, ParseType
from .preprocessing import MarkdownPreprocessor


logging.getLogger("crawl4ai").setLevel(logging.ERROR)


async def fetch_markdown(
    url: str,
    parse_type: ParseType = "markdown",
    preprocessing: MarkdownPreprocessingConfig | None = None,
) -> str:
    if parse_type == "markdown-fit":
        markdown_generator = DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(threshold=0.5),
            options={"ignore_links": False},
        )
        config = CrawlerRunConfig(markdown_generator=markdown_generator)
    else:
        config = CrawlerRunConfig()

    preprocessor = None
    if preprocessing and preprocessing.enabled:
        preprocessor = MarkdownPreprocessor(preprocessing)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)

        if parse_type == "markdown-fit":
            markdown = result.markdown.fit_markdown or result.markdown.raw_markdown or ""
        else:
            markdown = result.markdown.raw_markdown or ""

        if not preprocessor:
            return markdown

        html = result.html
        if preprocessor.needs_html(markdown, html):
            html = (await crawler.arun(url=url, config=CrawlerRunConfig())).html

        return preprocessor.apply(markdown, url, html)
