# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-14)
# @since 1.0.0 (2026-05-14) First version

from lxml import html as lxml_html
from crawl4md.fetch.normalization.rules.base.rule_base import RuleBase


class RuleReferences(RuleBase):
    """
    Remove MediaWiki annotation/reference footnote blocks:
    <div class="fussnoten-block">...</div>
    """

    def normalize(self, html: str) -> str:
        try:
            document = lxml_html.fromstring(html)
        except (lxml_html.ParserError, ValueError):
            return html

        for element in document.cssselect("div.fussnoten-block"):
            parent = element.getparent()
            if parent is not None:
                parent.remove(element)

        return lxml_html.tostring(document, encoding="unicode")
