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

from urllib.parse import urlparse

from crawl4md.fetch.normalize.base.normalizer_base import NormalizerBase


class UrlNormalizer(NormalizerBase):
    """
    Normalize protocol-relative URLs like:
    href="//de.wikipedia.org/wiki/Air_India"

    → href="https://de.wikipedia.org/wiki/Air_India"

    The scheme is extracted from the given page URL.
    """

    _pattern = re.compile(
        r'(?P<attr>\b(?:href|src)=["\'])//',
        re.IGNORECASE,
    )

    def __init__(self, url: str) -> None:
        parsed = urlparse(url)
        self.scheme = parsed.scheme or "https"

    def normalize(self, html: str) -> str:
        return self._pattern.sub(
            rf'\g<attr>{self.scheme}://',
            html,
        )