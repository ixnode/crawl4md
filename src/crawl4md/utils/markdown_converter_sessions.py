from pathlib import Path
from typing import Any

import yaml

from crawl4md.config import apply_profile_defaults
from crawl4md.fetch.base.base_html_fetcher import BaseHtmlFetcher
from crawl4md.fetch.html_fetcher_crawl4ai import HtmlFetcherCrawl4AI
from crawl4md.fetch.html_fetcher_kreuzberg_dev import HtmlFetcherKreuzbergDev
from crawl4md.models.markdown_converter_session import MarkdownConverterSession
from crawl4md.models.markdown_converter_session import MarkdownConverterSessionConfig


MARKDOWN_CONVERTER_SESSION_ROOT = Path(__file__).resolve().parents[3] / "tests" / "data" / "markdown_converter"


def load_and_normalize_html(html_path: Path, url: str | None, fetcher: Any) -> str:
    html = html_path.read_text()

    if not url:
        return html

    return fetcher.normalize_html(html, url=url)


def load_markdown_converter_session(path: Path) -> MarkdownConverterSession:
    data = yaml.safe_load(path.read_text())
    data["config"] = apply_profile_defaults(data["config"])
    return MarkdownConverterSession(**data)


def build_markdown_fetcher(config: MarkdownConverterSessionConfig) -> BaseHtmlFetcher:
    if config.crawl.parser == "crawl4ai":
        return HtmlFetcherCrawl4AI(
            config=config.preprocessing.markdown,
            normalization=config.normalization,
            parse_type=config.crawl.parse_type,
            content_selector=config.crawl.content_selector,
        )

    if config.crawl.parser == "kreuzberg-dev":
        return HtmlFetcherKreuzbergDev(
            config=config.preprocessing.markdown,
            normalization=config.normalization,
            parse_type=config.crawl.parse_type,
            content_selector=config.crawl.content_selector,
        )

    raise ValueError(f"Unknown markdown converter parser: {config.crawl.parser}")


def find_markdown_converter_sessions(group: str | None = None) -> list[Path]:
    root = resolve_markdown_converter_session_root(group)
    return sorted(path.parent for path in root.rglob("config.yml"))


def resolve_markdown_converter_session_root(group: str | None = None) -> Path:
    if not group:
        return MARKDOWN_CONVERTER_SESSION_ROOT

    group_path = Path(group)
    if group_path.is_absolute() or ".." in group_path.parts:
        raise ValueError(f"Invalid markdown converter test group: {group}")

    root = MARKDOWN_CONVERTER_SESSION_ROOT / group_path
    if not root.is_dir():
        raise ValueError(
            f"Markdown converter test group not found: {group}\n"
            f"Expected directory: {root.as_posix()}"
        )

    if not any(root.rglob("config.yml")):
        raise ValueError(
            f"Markdown converter test group contains no sessions: {group}\n"
            f"Expected at least one config.yml below: {root.as_posix()}"
        )

    return root
