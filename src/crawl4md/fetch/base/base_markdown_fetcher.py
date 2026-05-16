# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-08)
# @since 1.0.0 (2026-05-08) First version

from abc import ABC, abstractmethod
from typing import Any

import httpx

from crawl4md.config import MarkdownPreprocessingConfig, NormalizationConfig, ParseTypeKreuzbergDev, ParseTypeCrawl4AI
from crawl4md.fetch.normalization.html import HtmlNormalization
from crawl4md.fetch.normalization.rules.base.rule_base import RuleBase


class BaseMarkdownFetcher(ABC):
    def __init__(
        self,
        config: MarkdownPreprocessingConfig,
        normalization: NormalizationConfig | None = None,
        parse_type: ParseTypeKreuzbergDev | ParseTypeCrawl4AI = "markdown",
        content_selector: str | None = None,
    ) -> None:
        self.config = config
        self.normalization = normalization or NormalizationConfig()
        self.parse_type = parse_type
        self.content_selector = content_selector
        self.timeout = 30.0
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
        }

    def _build_html_normalizers(self, url: str) -> list[RuleBase]:
        html_normalization = HtmlNormalization(self.normalization, url=url)
        return html_normalization.rules

    def normalize_html(self, html: str, *, url: str) -> str:
        for normalizer in self._build_html_normalizers(url):
            html = normalizer.normalize(html)
        return html

    async def fetch_html(self, url: str) -> str:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=self.timeout,
            headers=self.headers,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            html = response.text

        return self.normalize_html(html, url=url)

    def fetch_html_sync(self, url: str) -> str:
        with httpx.Client(
            follow_redirects=True,
            timeout=self.timeout,
            headers=self.headers,
        ) as client:
            response = client.get(url)
            response.raise_for_status()
            html = response.text

        return self.normalize_html(html, url=url)

    @abstractmethod
    def build_markdown_converter(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def fetch(self, url: str) -> str:
        html = await self.fetch_html(url)
        converter = self.build_markdown_converter()
        return await converter.convert(html=html, url=url)

    @abstractmethod
    def fetch_sync(self, url: str) -> str:
        html = self.fetch_html_sync(url)
        converter = self.build_markdown_converter()
        return converter.convert_sync(html=html, url=url)
