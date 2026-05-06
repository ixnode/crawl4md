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

from html_to_markdown import convert as convert_html_to_markdown

from ..config import MarkdownPreprocessingConfig
from .preprocessing import MarkdownPreprocessing


class KreuzbergDevMarkdownConverter:
    def __init__(
        self,
        config: MarkdownPreprocessingConfig,
        parse_type: str = "markdown",
    ) -> None:
        self.config = config
        self.parse_type = parse_type

    async def convert(
        self,
        html: str,
        url: str | None = None,
    ) -> str:
        if self.parse_type != "markdown":
            raise ValueError(
                "kreuzberg-dev parser supports only parse_type 'markdown'"
            )

        result = convert_html_to_markdown(html)
        markdown = result.content or ""
        preprocessing = MarkdownPreprocessing(self.config)

        return preprocessing.process(markdown, url=url, html=html)

    def convert_sync(
        self,
        html: str,
        url: str | None = None,
    ) -> str:
        return asyncio.run(self.convert(html=html, url=url))
