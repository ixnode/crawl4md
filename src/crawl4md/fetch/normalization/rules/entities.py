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

from crawl4md.fetch.normalization.rules.base.rule_base import RuleBase


class RuleEntities(RuleBase):
    """
    Fix MediaWiki entity spans like:
    <span typeof="mw:Entity" id="mwdg">&nbsp;</span>

    → replaced with a single whitespace " "
    """

    _pattern = re.compile(
        r'<span\b[^>]*\btypeof=["\']mw:Entity["\'][^>]*>\s*(?:&nbsp;|\u00a0)\s*</span>',
        re.IGNORECASE,
    )

    def normalize(self, html: str) -> str:
        return self._pattern.sub(" ", html)
