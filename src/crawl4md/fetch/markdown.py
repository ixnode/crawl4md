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

from ..config import ParseType
from ..fetch.html import HtmlFetcher
from ..fetch.normalize.mediawiki_entity import MediawikiEntityNormalizer
from ..fetch.normalize.mediawiki_hidden_span import MediawikiHiddenSpanNormalizer
from ..fetch.normalize.url import UrlNormalizer
from ..convert.markdown import convert_markdown


async def fetch_markdown(
    url: str,
    parse_type: ParseType = "markdown",
) -> str:
    fetcher = HtmlFetcher(
        normalizers=[
            MediawikiEntityNormalizer(),
            MediawikiHiddenSpanNormalizer(),
            UrlNormalizer(url=url)
        ]
    )
    html = await fetcher.fetch(url=url)

    return await convert_markdown(html=html, parse_type=parse_type)
