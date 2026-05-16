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

from ..config import MarkdownPreprocessingConfig, NormalizationConfig, ParseTypeCrawl4AI
from ..convert.markdown_converter_crawl4ai import MarkdownConverterCrawl4AI
from .base import BaseHtmlFetcher


class HtmlFetcherCrawl4AI(BaseHtmlFetcher):
    def __init__(
        self,
        config: MarkdownPreprocessingConfig,
        normalization: NormalizationConfig | None = None,
        parse_type: ParseTypeCrawl4AI = "markdown",
        content_selector: str | None = None,
    ) -> None:
        super().__init__(
            config=config,
            normalization=normalization,
            parse_type=parse_type,
            content_selector=content_selector,
        )

    def build_markdown_converter(self) -> MarkdownConverterCrawl4AI:
        return MarkdownConverterCrawl4AI(
            config=self.config,
            parse_type=self.parse_type,
            content_selector=self.content_selector,
        )

    async def fetch(self, url: str) -> str:
        return await super().fetch(url)

    def fetch_sync(self, url: str) -> str:
        return super().fetch_sync(url)
