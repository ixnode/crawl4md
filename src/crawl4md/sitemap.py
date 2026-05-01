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
