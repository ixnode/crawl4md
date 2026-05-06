# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-07)
# @since 1.0.0 (2026-05-07) First version

from ..config import MarkdownPreprocessingConfig
from ..convert.kreuzberg_dev_markdown import KreuzbergDevMarkdownConverter
from ..fetch.html import HtmlFetcher
from ..fetch.normalize.mediawiki_entity import MediawikiEntityNormalizer
from ..fetch.normalize.mediawiki_hidden_span import MediawikiHiddenSpanNormalizer
from ..fetch.normalize.url import UrlNormalizer


class KreuzbergDevMarkdownFetcher:
    def __init__(
        self,
        config: MarkdownPreprocessingConfig,
        parse_type: str = "markdown",
    ) -> None:
        self.config = config
        self.parse_type = parse_type

    @staticmethod
    def _build_html_fetcher(url: str) -> HtmlFetcher:
        return HtmlFetcher(
            normalizers=[
                MediawikiEntityNormalizer(),
                MediawikiHiddenSpanNormalizer(),
                UrlNormalizer(url=url),
            ]
        )

    def _build_markdown_converter(self) -> KreuzbergDevMarkdownConverter:
        return KreuzbergDevMarkdownConverter(
            config=self.config,
            parse_type=self.parse_type,
        )

    async def fetch(self, url: str) -> str:
        fetcher = self._build_html_fetcher(url)
        html = await fetcher.fetch(url=url)

        converter = self._build_markdown_converter()

        return await converter.convert(html=html, url=url)

    def fetch_sync(self, url: str) -> str:
        fetcher = self._build_html_fetcher(url)
        html = fetcher.fetch_sync(url=url)

        converter = self._build_markdown_converter()

        return converter.convert_sync(html=html, url=url)
