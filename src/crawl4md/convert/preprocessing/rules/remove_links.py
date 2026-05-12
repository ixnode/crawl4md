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
from functools import cached_property

from .base.rule_base import RuleBase


class RuleRemoveLinks(RuleBase):
    @cached_property
    def link_pattern(self) -> re.Pattern[str] | None:
        if not self.config.remove_links:
            return None

        link_target_patterns = (
            [self.config.remove_links]
            if isinstance(self.config.remove_links, str)
            else self.config.remove_links
        )
        if not link_target_patterns:
            return None

        target_pattern = "|".join(f"(?:{pattern})" for pattern in link_target_patterns)

        return re.compile(
            rf"\s*!?\[[^\n]*?\]\([^)\n]*(?:{target_pattern})[^)\n]*\)"
        )

    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        if self.link_pattern is None:
            return markdown

        return self.link_pattern.sub("", markdown)
