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


class RuleRemoveLines(RuleBase):
    @cached_property
    def line_pattern(self) -> re.Pattern[str] | None:
        if not self.config.remove_lines:
            return None

        line_patterns = (
            [self.config.remove_lines]
            if isinstance(self.config.remove_lines, str)
            else self.config.remove_lines
        )
        if not line_patterns:
            return None

        pattern = "|".join(f"(?:{line_pattern})" for line_pattern in line_patterns)
        return re.compile(pattern)

    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        if self.line_pattern is None:
            return markdown

        cleaned_lines: list[str] = []

        for line in markdown.splitlines():
            cleaned_line = re.sub(
                r"\s{2,}",
                " ",
                self.line_pattern.sub("", line),
            ).rstrip()

            if cleaned_line.strip():
                cleaned_lines.append(cleaned_line)

        return self.join_lines(cleaned_lines, markdown)
