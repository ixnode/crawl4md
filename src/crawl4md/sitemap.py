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

import requests

from lxml import etree


def parse_sitemap(url: str) -> list[str]:
    res = requests.get(url, timeout=30)
    res.raise_for_status()

    root = etree.fromstring(res.content)
    urls = []

    # sitemap index
    if root.tag.endswith("sitemapindex"):
        for loc in root.findall(".//{*}loc"):
            urls.extend(parse_sitemap(loc.text.strip()))
        return urls

    # normal sitemap
    for loc in root.findall(".//{*}loc"):
        urls.append(loc.text.strip())

    return urls
