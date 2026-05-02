import logging
import re

from html import unescape
from html.parser import HTMLParser
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from urllib.parse import unquote, urljoin, urlparse

from .config import MarkdownPreprocessingConfig, ParseType


logging.getLogger("crawl4ai").setLevel(logging.ERROR)


H1_PATTERN = re.compile(r"^# ", re.MULTILINE)
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


class _TitleHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._active_tag: str | None = None
        self._capturing_h1 = False
        self._seen_h1 = False
        self._h1_parts: list[str] = []
        self._title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._active_tag = tag

        if tag == "h1" and not self._seen_h1:
            self._capturing_h1 = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1" and self._capturing_h1:
            self._capturing_h1 = False
            self._seen_h1 = True

        if tag == self._active_tag:
            self._active_tag = None

    def handle_data(self, data: str) -> None:
        if self._capturing_h1:
            self._h1_parts.append(data)

        if self._active_tag == "title":
            self._title_parts.append(data)

    @property
    def h1_text(self) -> str:
        return "".join(self._h1_parts)

    @property
    def title_text(self) -> str:
        return "".join(self._title_parts)


def has_h1(markdown: str) -> bool:
    return bool(H1_PATTERN.search(markdown))


def _normalize_title(value: str) -> str | None:
    normalized = " ".join(unescape(value).split()).strip()
    return normalized or None


def extract_title_from_html(html: str) -> str | None:
    parser = _TitleHTMLParser()
    parser.feed(html)
    parser.close()

    return _normalize_title(parser.h1_text) or _normalize_title(parser.title_text)


def fallback_title_from_url(url: str) -> str:
    parsed = urlparse(url)
    segment = parsed.path.rstrip("/").rsplit("/", maxsplit=1)[-1]
    candidate = unquote(segment).replace("-", " ").replace("_", " ")
    normalized = _normalize_title(candidate)

    if normalized:
        return normalized

    return parsed.netloc or "index"


def ensure_h1(markdown: str, html: str | None, url: str) -> str:
    if has_h1(markdown):
        return markdown

    title = extract_title_from_html(html) if html else None
    if not title:
        title = fallback_title_from_url(url)

    return f"# {title}\n\n{markdown}"


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

        if (
            preprocessing
            and preprocessing.enabled
            and preprocessing.ensure_h1
        ):
            html = result.html
            if not html and not has_h1(markdown):
                html = (
                    await crawler.arun(
                        url=url,
                        config=CrawlerRunConfig(),
                    )
                ).html

            markdown = ensure_h1(markdown, html, url)

        return markdown
