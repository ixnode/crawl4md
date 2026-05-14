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

import httpx

from typing import List

from .normalize.base.normalizer_base import NormalizerBase


class HtmlFetcher:
    def __init__(
        self,
        timeout: float = 30.0,
        user_agent: str = (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        normalizers: List[NormalizerBase] | None = None,
    ) -> None:
        self.timeout = timeout
        self.headers =  {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
        }
        self.normalizers = normalizers or []

    async def fetch(self, url: str) -> str:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=self.timeout,
            headers=self.headers,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            html = response.text

        return self._apply_normalizers(html)

    def fetch_sync(self, url: str) -> str:
        with httpx.Client(
            follow_redirects=True,
            timeout=self.timeout,
            headers=self.headers,
        ) as client:
            response = client.get(url)
            response.raise_for_status()
            html = response.text

        return self._apply_normalizers(html)

    def _apply_normalizers(self, html: str) -> str:
        for normalizer in self.normalizers:
            html = normalizer.normalize(html)
        return html

    def normalize_html(self, html: str) -> str:
        return self._apply_normalizers(html)
