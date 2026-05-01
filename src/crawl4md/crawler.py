import logging

from crawl4ai import AsyncWebCrawler


logging.getLogger("crawl4ai").setLevel(logging.ERROR)

async def fetch_markdown(url: str) -> str:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            markdown=True,
            fit_markdown=True
        )
        return result.markdown or ""
