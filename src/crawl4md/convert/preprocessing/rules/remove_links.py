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
    REMOVED_LINK_MARKER = "\0C4MD_REMOVED_LINK\0"
    MARKDOWN_LINK_TARGET = r"(?:\\.|[^()\\\n]|\([^()\n]*\))*"
    MARKDOWN_LINK_TEXT = rf"(?:!\[[^\]\n]*\]\({MARKDOWN_LINK_TARGET}\)|(?:(?!\]\().))*"

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
            target_boundary = (
                r"(?<![A-Za-z0-9_])"
                if re.match(r"[A-Za-z0-9_]", match_pattern)
                else ""
            )
            if match_type == "text":
                link_match_patterns.append(
                    rf"[^\S\n]*(?:\[)?!?\[(?:(?!\]\().)*(?:{match_pattern})(?:(?!\]\().)*\]"
                    rf"\({self.MARKDOWN_LINK_TARGET}\)(?:\])?"
                )
                continue

            link_match_patterns.append(
                rf"[^\S\n]*(?:\[)?!?\[{self.MARKDOWN_LINK_TEXT}\]\("
                rf"(?={self.MARKDOWN_LINK_TARGET}{target_boundary}(?:{match_pattern}))"
                rf"{self.MARKDOWN_LINK_TARGET}\)\]?"
            )

        return re.compile("|".join(f"(?:{pattern})" for pattern in link_match_patterns), re.DOTALL)

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

        cleaned_markdown = self.link_pattern.sub(self._replace_link, markdown)

        for line in cleaned_markdown.splitlines():
            if skip_next_blank and not line.strip():
                skip_next_blank = False
                continue

            skip_next_blank = False
            line_changed = self.REMOVED_LINK_MARKER in line
            cleaned_line = line.replace(self.REMOVED_LINK_MARKER, "")

            if line_changed and self._is_empty_link_line(cleaned_line):
                skip_next_blank = True
                continue

            cleaned_lines.append(cleaned_line)

        return self.join_lines(cleaned_lines, markdown)

    def _is_empty_link_line(self, line: str) -> bool:
        return not line.strip() or ("|" not in line and all(character in "[] " for character in line))

    def _replace_link(self, match: re.Match[str]) -> str:
        leading = re.match(r"[^\S\n]*", match.group(0)).group(0)
        before = match.string[: match.start()]
        previous = before.rstrip()[-1:] if before.strip() else ""

        if previous == "|":
            return leading

        return self.REMOVED_LINK_MARKER

    def _split_match_pattern(self, pattern: str) -> tuple[str, str]:
        if pattern.startswith("text:"):
            return "text", pattern.removeprefix("text:")

        if pattern.startswith("anchor:"):
            return "anchor", pattern.removeprefix("anchor:")

        return "anchor", pattern
