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

        link_patterns = (
            [self.config.remove_links]
            if isinstance(self.config.remove_links, str)
            else self.config.remove_links
        )
        if not link_patterns:
            return None

        link_match_patterns: list[str] = []
        for pattern in link_patterns:
            match_type, match_pattern = self._split_match_pattern(pattern)
            if match_type == "text":
                link_match_patterns.append(
                    rf"\s*!?\[[^\n]*(?:{match_pattern})[^\n]*?\]\([^)\n]*\)"
                )
                continue

            link_match_patterns.append(
                rf"\s*!?\[[^\n]*?\]\([^)\n]*(?:{match_pattern})[^)\n]*\)"
            )

        return re.compile("|".join(f"(?:{pattern})" for pattern in link_match_patterns))

    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        if self.link_pattern is None:
            return markdown

        cleaned_lines: list[str] = []
        skip_next_blank = False

        for line in markdown.splitlines():
            if skip_next_blank and not line.strip():
                skip_next_blank = False
                continue

            skip_next_blank = False
            cleaned_line = self.link_pattern.sub("", line).rstrip()
            line_changed = cleaned_line != line

            if line_changed and self._is_empty_link_line(cleaned_line):
                skip_next_blank = True
                continue

            cleaned_lines.append(cleaned_line)

        return self.join_lines(cleaned_lines, markdown)

    def _is_empty_link_line(self, line: str) -> bool:
        return not line.strip() or all(character in "[]| " for character in line)

    def _split_match_pattern(self, pattern: str) -> tuple[str, str]:
        if pattern.startswith("text:"):
            return "text", pattern.removeprefix("text:")

        if pattern.startswith("anchor:"):
            return "anchor", pattern.removeprefix("anchor:")

        return "anchor", pattern
