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

import asyncio

import html_to_markdown._html_to_markdown as html_to_markdown

from ..core.config import MarkdownPreprocessingConfig, ParseTypeKreuzbergDev
from .base import BaseMarkdownConverter


class MarkdownConverterKreuzbergDev(BaseMarkdownConverter):
    def __init__(
        self,
        config: MarkdownPreprocessingConfig,
        parse_type: ParseTypeKreuzbergDev = "markdown",
        content_selector: str | None = None,
    ) -> None:
        super().__init__(
            config=config,
            parse_type=parse_type,
            content_selector=content_selector,
        )

    async def convert(
        self,
        html: str,
        url: str | None = None,
        language: str | None = None,
    ) -> str:
        if self.parse_type != "markdown":
            raise ValueError(
                "kreuzberg-dev parser supports only parse_type 'markdown'"
            )

        html = self.select_content(html)
        options = html_to_markdown.ConversionOptions(
            heading_style=html_to_markdown.HeadingStyle.Atx,
            extract_metadata=False,
        )
        result = html_to_markdown.convert(html, options, None)
        markdown = result.content or ""
        return self.preprocess(markdown, url=url, html=html, language=language)

    def convert_sync(
        self,
        html: str,
        url: str | None = None,
        language: str | None = None,
    ) -> str:
        return asyncio.run(self.convert(html=html, url=url, language=language))
