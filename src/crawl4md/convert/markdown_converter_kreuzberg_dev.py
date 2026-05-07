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
from lxml import html as lxml_html

from ..config import MarkdownPreprocessingConfig
from .preprocessing import MarkdownPreprocessing


class MarkdownConverterKreuzbergDev:
    def __init__(
        self,
        config: MarkdownPreprocessingConfig,
        parse_type: str = "markdown",
        content_selector: str | None = None,
    ) -> None:
        self.config = config
        self.parse_type = parse_type
        self.content_selector = content_selector

    async def convert(
        self,
        html: str,
        url: str | None = None,
    ) -> str:
        if self.parse_type != "markdown":
            raise ValueError(
                "kreuzberg-dev parser supports only parse_type 'markdown'"
            )

        html = self._select_content(html)
        options = html_to_markdown.ConversionOptions(
            heading_style=html_to_markdown.HeadingStyle.Atx,
            extract_metadata=False,
        )
        result = html_to_markdown.convert(html, options, None)
        markdown = result.content or ""
        preprocessing = MarkdownPreprocessing(self.config)

        return preprocessing.process(markdown, url=url, html=html)

    def convert_sync(
        self,
        html: str,
        url: str | None = None,
    ) -> str:
        return asyncio.run(self.convert(html=html, url=url))

    def _select_content(self, html: str) -> str:
        if not self.content_selector:
            return html

        document = lxml_html.fromstring(html)
        matches = document.cssselect(self.content_selector)

        if not matches:
            raise ValueError(
                f"Content selector did not match any element: {self.content_selector}"
            )

        return "\n".join(
            lxml_html.tostring(match, encoding="unicode")
            for match in matches
        )
