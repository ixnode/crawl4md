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


class RuleHiddens(RuleBase):
    """
    Remove hidden MediaWiki spans like:
    <span style="display:none;">...</span>

    → completely removed (including content)
    """

    _pattern = re.compile(
        r'<span\b[^>]*style=["\'][^"\']*display\s*:\s*none[^"\']*["\'][^>]*>.*?</span>',
        re.IGNORECASE | re.DOTALL,
    )

    def normalize(self, html: str) -> str:
        return self._pattern.sub("", html)
