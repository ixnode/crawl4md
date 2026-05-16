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

from crawl4md.config import MarkdownPreprocessingConfig, NormalizationConfig
from crawl4md.fetch.html import HtmlFetcher
from crawl4md.fetch.normalization.html import HtmlNormalization


class BaseMarkdownFetcher(ABC):
    def __init__(
        self,
        config: MarkdownPreprocessingConfig,
        normalization: NormalizationConfig | None = None,
        parse_type: str = "markdown",
        content_selector: str | None = None,
    ) -> None:
        self.config = config
        self.normalization = normalization or NormalizationConfig()
        self.parse_type = parse_type
        self.content_selector = content_selector

    def build_html_fetcher(self, url: str) -> HtmlFetcher:
        html_normalization = HtmlNormalization(self.normalization, url=url)
        return HtmlFetcher(
            normalizers=html_normalization.rules
        )

    @abstractmethod
    def build_markdown_converter(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def fetch(self, url: str) -> str:
        fetcher = self.build_html_fetcher(url)
        html = await fetcher.fetch(url=url)

        converter = self.build_markdown_converter()

        return await converter.convert(html=html, url=url)

    @abstractmethod
    def fetch_sync(self, url: str) -> str:
        fetcher = self.build_html_fetcher(url)
        html = fetcher.fetch_sync(url=url)

        converter = self.build_markdown_converter()

        return converter.convert_sync(html=html, url=url)
