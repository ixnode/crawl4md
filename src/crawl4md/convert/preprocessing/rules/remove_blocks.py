# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-12)
# @since 1.0.0 (2026-05-12) First version

import re
from functools import cached_property

from .base.rule_base import RuleBase


class RuleRemoveBlocks(RuleBase):
    @cached_property
    def block_pattern(self) -> re.Pattern[str] | None:
        if not self.config.remove_blocks:
            return None

        block_patterns = (
            [self.config.remove_blocks]
            if isinstance(self.config.remove_blocks, str)
            else self.config.remove_blocks
        )
        if not block_patterns:
            return None

        pattern = "|".join(f"(?:{block_pattern})" for block_pattern in block_patterns)
        return re.compile(pattern, re.DOTALL)

    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
        language: str | None = None,
    ) -> str:
        if self.block_pattern is None:
            return markdown

        cleaned_blocks = [
            block
            for block in re.split(r"\n\s*\n", markdown)
            if block.strip() and not self.block_pattern.search(block)
        ]

        return self.join_lines(
            [
                line
                for block in cleaned_blocks
                for line in block.splitlines()
                if line.strip()
            ],
            markdown,
        )
