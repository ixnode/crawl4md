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

import re

from .base.rule_base import RuleBase


CITE_LINK_PATTERN = re.compile(r"\s*\[\[\d+\]\]\(#cite_note-[^)]+\)")


class RuleRemoveCiteLinks(RuleBase):
    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        return CITE_LINK_PATTERN.sub("", markdown)
