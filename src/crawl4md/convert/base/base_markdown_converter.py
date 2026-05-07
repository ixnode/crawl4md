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

from lxml import html as lxml_html

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing import MarkdownPreprocessing


class BaseMarkdownConverter(ABC):
    def __init__(
        self,
        config: MarkdownPreprocessingConfig,
        parse_type: str = "markdown",
        content_selector: str | None = None,
    ) -> None:
        self.config = config
        self.parse_type = parse_type
        self.content_selector = content_selector

    @abstractmethod
    async def convert(
        self,
        html: str,
        url: str | None = None,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def convert_sync(
        self,
        html: str,
        url: str | None = None,
    ) -> str:
        raise NotImplementedError

    def select_content(self, html: str) -> str:
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

    def preprocess(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        preprocessing = MarkdownPreprocessing(self.config)
        return preprocessing.process(markdown, url=url, html=html)
