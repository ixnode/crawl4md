import logging
import re

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from urllib.parse import urljoin, urlparse

from .config import MarkdownPreprocessingConfig, ParseType


logging.getLogger("crawl4ai").setLevel(logging.ERROR)


SKIP_CONTENT_FRAGMENTS = {
    "bodycontent",
    "content",
    "content-start",
    "main",
    "main-content",
    "maincontent",
}
MARKDOWN_LINK_PATTERN = re.compile(
    r"\[(.*?)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)",
    re.DOTALL,
)
WIKIPEDIA_SUBTITLE = "aus Wikipedia, der freien Enzyklopädie"


def _is_jump_to_content_target(link_target: str, page_url: str) -> bool:
    resolved = urlparse(urljoin(page_url, link_target))
    page = urlparse(page_url)

    if not resolved.fragment:
        return False

    if resolved.fragment.lower() not in SKIP_CONTENT_FRAGMENTS:
        return False

    same_page = (
        resolved.scheme == page.scheme
        and resolved.netloc == page.netloc
        and resolved.path == page.path
    )
    fragment_only = not resolved.scheme and not resolved.netloc and not resolved.path

    return same_page or fragment_only


def _is_wiki_loves_earth_target(link_target: str, page_url: str) -> bool:
    resolved = urlparse(urljoin(page_url, link_target))
    return (
        (
            resolved.netloc == "de.wikipedia.org"
            and resolved.path.startswith("/wiki/Wikipedia:Wiki_Loves_Earth_")
        )
        or (
            resolved.netloc == "www.wikidata.org"
            and resolved.path.startswith("/wiki/Wikidata:Events/Coordinate_Me_")
        )
    )


def remove_jump_to_content_links(markdown: str, page_url: str) -> str:
    cleaned_lines: list[str] = []

    for line in markdown.splitlines():
        cleaned_line = MARKDOWN_LINK_PATTERN.sub(
            lambda match: ""
            if _is_jump_to_content_target(match.group(2), page_url)
            else match.group(0),
            line,
        )

        if cleaned_line.strip():
            cleaned_lines.append(cleaned_line)

    suffix = "\n" if markdown.endswith("\n") else ""
    return "\n".join(cleaned_lines) + suffix


def remove_wiki_loves_earth_banner(markdown: str, page_url: str) -> str:
    cleaned_markdown = MARKDOWN_LINK_PATTERN.sub(
        lambda match: ""
        if _is_wiki_loves_earth_target(match.group(2), page_url)
        else match.group(0),
        markdown,
    )

    cleaned_lines = [
        line for line in cleaned_markdown.splitlines() if line.strip()
    ]

    suffix = "\n" if markdown.endswith("\n") else ""
    return "\n".join(cleaned_lines) + suffix


def remove_wikipedia_subtitle(markdown: str) -> str:
    cleaned_lines: list[str] = []

    for line in markdown.splitlines():
        cleaned_line = re.sub(r"\s{2,}", " ", line.replace(WIKIPEDIA_SUBTITLE, "")).rstrip()

        if cleaned_line.strip():
            cleaned_lines.append(cleaned_line)

    suffix = "\n" if markdown.endswith("\n") else ""
    return "\n".join(cleaned_lines) + suffix


async def fetch_markdown(
    url: str,
    parse_type: ParseType = "markdown",
    preprocessing: MarkdownPreprocessingConfig | None = None,
) -> str:
    if parse_type == "markdown-fit":
        markdown_generator = DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(
                threshold=0.5
            ),
            options={"ignore_links": False},
        )
        config = CrawlerRunConfig(
            markdown_generator=markdown_generator,
        )
    else:
        config = CrawlerRunConfig()

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            config=config,
        )

        if parse_type == "markdown-fit":
            markdown = result.markdown.fit_markdown or result.markdown.raw_markdown or ""
        else:
            markdown = result.markdown.raw_markdown or ""

        if (
            preprocessing
            and preprocessing.enabled
            and preprocessing.remove_jump_to_content
        ):
            markdown = remove_jump_to_content_links(markdown, url)

        if (
            preprocessing
            and preprocessing.enabled
            and preprocessing.remove_wikipedia_subtitle
        ):
            markdown = remove_wikipedia_subtitle(markdown)

        if (
            preprocessing
            and preprocessing.enabled
            and preprocessing.remove_wiki_loves_earth_banner
        ):
            markdown = remove_wiki_loves_earth_banner(markdown, url)

        return markdown
