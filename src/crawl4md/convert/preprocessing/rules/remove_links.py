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
    UNWRAP_LINK_PATTERN = re.compile(
        rf"(?P<leading>[^\S\n]*)\[(?P<text>{MARKDOWN_LINK_TEXT})\]\({MARKDOWN_LINK_TARGET}\)",
        re.DOTALL,
    )

    @cached_property
    def link_pattern(self) -> re.Pattern[str] | None:
        link_patterns = self._link_patterns()
        if not link_patterns:
            return None

        link_match_patterns: list[str] = []
        for pattern in link_patterns:
            match_type, match_pattern = self._split_match_pattern(pattern)
            if match_type == "unwrap":
                continue

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

        if not link_match_patterns:
            return None

        return re.compile("|".join(f"(?:{pattern})" for pattern in link_match_patterns), re.DOTALL)

    @cached_property
    def unwrap_patterns(self) -> list[re.Pattern[str]]:
        return [
            re.compile(".*", re.DOTALL) if match_pattern == "*" else re.compile(match_pattern, re.DOTALL)
            for pattern in self._link_patterns()
            for match_type, match_pattern in [self._split_match_pattern(pattern)]
            if match_type == "unwrap"
        ]

    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        if self.link_pattern is None and not self.unwrap_patterns:
            return markdown

        cleaned_lines: list[str] = []
        skip_next_blank = False

        cleaned_markdown = markdown
        if self.link_pattern is not None:
            cleaned_markdown = self.link_pattern.sub(self._replace_link, cleaned_markdown)

        if self.unwrap_patterns:
            cleaned_markdown = self.UNWRAP_LINK_PATTERN.sub(self._replace_unwrapped_link, cleaned_markdown)

        for line in cleaned_markdown.splitlines():
            if skip_next_blank and not line.strip():
                skip_next_blank = False
                continue

            skip_next_blank = False
            line_changed = self.REMOVED_LINK_MARKER in line
            cleaned_line = line.replace(self.REMOVED_LINK_MARKER, "")
            if (
                line_changed
                and self._starts_with_removed_link(line)
                and not cleaned_line.lstrip().startswith("|")
            ):
                cleaned_line = cleaned_line.lstrip()

            if line_changed:
                cleaned_line = cleaned_line.replace("*]", "[**]")
                cleaned_line = re.sub(r"(?<![\w*])\*\*(?![\w*])", "[**]", cleaned_line)
                cleaned_line = cleaned_line.replace("[[**]]", "[**]")

            if line_changed and self._is_empty_link_line(cleaned_line):
                skip_next_blank = True
                continue

            cleaned_lines.append(cleaned_line)

        return self.join_lines(cleaned_lines, markdown)

    def _is_empty_link_line(self, line: str) -> bool:
        return not line.strip() or all(character in "[]| " for character in line)

    def _starts_with_removed_link(self, line: str) -> bool:
        marker_index = line.find(self.REMOVED_LINK_MARKER)
        return marker_index >= 0 and not line[:marker_index].strip()

    def _replace_link(self, match: re.Match[str]) -> str:
        matched = match.group(0)
        leading = re.match(r"[^\S\n]*", matched).group(0)
        body = matched[len(leading):]
        before = match.string[: match.start()]
        previous = before.rstrip()[-1:] if before.strip() else ""

        if previous == "|":
            return leading

        # Keep a valid bracketed emphasis marker when removing links like:
        # [*[citation needed](...)*] -> [**]
        if body.startswith("[*[") and body.endswith("*]"):
            return f"{leading}[**]"

        return self.REMOVED_LINK_MARKER

    def _replace_unwrapped_link(self, match: re.Match[str]) -> str:
        text = match.group("text")
        if not any(pattern.search(text) for pattern in self.unwrap_patterns):
            return match.group(0)

        return f"{match.group('leading')}{text}"

    def _split_match_pattern(self, pattern: str) -> tuple[str, str]:
        if pattern.startswith("text:"):
            return "text", pattern.removeprefix("text:")

        if pattern.startswith("unwrap:"):
            return "unwrap", pattern.removeprefix("unwrap:")

        if pattern.startswith("anchor:"):
            return "anchor", pattern.removeprefix("anchor:")

        return "anchor", pattern

    def _link_patterns(self) -> list[str]:
        if not self.config.remove_links:
            return []

        if isinstance(self.config.remove_links, str):
            return [self.config.remove_links]

        return self.config.remove_links
