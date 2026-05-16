from pathlib import Path
from typing import Any

import yaml

from crawl4md.config import apply_profile_defaults
from crawl4md.models.markdown_converter_session import MarkdownConverterSession


def load_and_normalize_html(html_path: Path, url: str | None, fetcher: Any) -> str:
    html = html_path.read_text()

    if not url:
        return html

    html_fetcher = fetcher.build_html_fetcher(url=url)
    return html_fetcher.normalize_html(html)


def load_markdown_converter_session(path: Path) -> MarkdownConverterSession:
    data = yaml.safe_load(path.read_text())
    data["config"] = apply_profile_defaults(data["config"])
    return MarkdownConverterSession(**data)
