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

import re

from html import unescape
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import urlopen

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.helpers.title_html_parser import _TitleHTMLParser


class RuleBase:
    MARKDOWN_LINK_PATTERN = re.compile(
        r"\[(.*?)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)",
        re.DOTALL,
    )
    H1_PATTERN = re.compile(r"^# ", re.MULTILINE)
    HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
    TRAILING_ANCHOR_PATTERN = re.compile(r"\s*\{#[^}]+\}\s*$")
    LEADING_NUMBER_PATTERN = re.compile(r"^\d+(?:[.)]\s*|\s+)")

    def __init__(self, config: MarkdownPreprocessingConfig):
        self.config = config

    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
        language: str | None = None,
    ) -> str:
        raise NotImplementedError

    def join_lines(self, lines: list[str], original: str) -> str:
        suffix = "\n" if original.endswith("\n") else ""
        return "\n".join(lines) + suffix

    def normalize_heading(self, heading: str) -> str:
        normalized = self.TRAILING_ANCHOR_PATTERN.sub("", heading).strip().casefold()
        normalized = self.LEADING_NUMBER_PATTERN.sub("", normalized)
        return " ".join(normalized.split())

    def has_h1(self, markdown: str) -> bool:
        return bool(self.H1_PATTERN.search(markdown))

    def normalize_title(self, value: str) -> str | None:
        normalized = " ".join(unescape(value).split()).strip()
        return normalized or None

    def extract_title_from_html(self, html: str) -> str | None:
        parser = _TitleHTMLParser()
        parser.feed(html)
        parser.close()
        return self.normalize_title(parser.h1_text) or self.normalize_title(parser.title_text)

    def fallback_title_from_url(self, url: str) -> str:
        parsed = urlparse(url)
        segment = parsed.path.rstrip("/").rsplit("/", maxsplit=1)[-1]
        candidate = unquote(segment).replace("-", " ").replace("_", " ")
        normalized = self.normalize_title(candidate)

        if normalized:
            return normalized

        return parsed.netloc or "index"

    def fetch_html(self, url: str) -> str | None:
        with urlopen(url, timeout=30) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")

    def resolve_url(self, page_url: str, link_target: str):
        return urlparse(urljoin(page_url, link_target))
