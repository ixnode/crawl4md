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

from ..base.rule_base import RuleBase
from .patterns import build_link_pattern, build_unwrap_patterns


class RuleRemoveLinks(RuleBase):
    # Internal placeholder while removing links.
    # We use a marker first and clean it in a second pass per line.
    # Example:
    #   "Text [x](#target)" -> "Text \0C4MD_REMOVED_LINK\0"
    REMOVED_LINK_MARKER = "\0C4MD_REMOVED_LINK\0"

    # Markdown link grammar helpers used to build robust regexes.
    # MARKDOWN_LINK_TARGET supports nested parentheses in URLs.
    # Example target:
    #   https://example.org/wiki/Air_India_(film)
    MARKDOWN_LINK_TARGET = r"(?:\\.|[^()\\\n]|\([^()\n]*\))*"
    MARKDOWN_LINK_TEXT = rf"(?:!\[[^\]\n]*\]\({MARKDOWN_LINK_TARGET}\)|(?:(?!\]\().))*"
    UNWRAP_LINK_TEXT = r"(?:\\.|[^\]\\\n])*"

    # Used for unwrap-rules:
    #   [Text](url) -> Text
    UNWRAP_LINK_PATTERN = re.compile(
        rf"(?P<leading>[^\S\n]*)\[(?P<text>{UNWRAP_LINK_TEXT})\]\({MARKDOWN_LINK_TARGET}\)",
    )

    # Special forms that should collapse to [**] when removed by anchor/text rules.
    # Examples:
    #   [*[citation needed](...)*] -> [**]
    #   *[citation needed](...)*   -> [**]
    BRACKETED_EMPHASIS_LINK_PATTERN = re.compile(
        rf"^\[\*\[(?P<text>{MARKDOWN_LINK_TEXT})\]\({MARKDOWN_LINK_TARGET}\)\*\]$",
        re.DOTALL,
    )
    EMPHASIS_LINK_PATTERN = re.compile(
        rf"^\*\[(?P<text>{MARKDOWN_LINK_TEXT})\]\({MARKDOWN_LINK_TARGET}\)\*$",
        re.DOTALL,
    )
    INLINE_CODE_PATTERN = re.compile(r"`[^`\n]*`")

    @cached_property
    def link_pattern(self) -> re.Pattern[str] | None:
        # Combined pattern for remove-rules (anchor/text).
        # unwrap-rules are handled in a dedicated second phase.
        return build_link_pattern(
            self._link_patterns(),
            self.MARKDOWN_LINK_TEXT,
            self.MARKDOWN_LINK_TARGET,
        )

    @cached_property
    def unwrap_patterns(self) -> list[re.Pattern[str]]:
        # All unwrap-rules, e.g. unwrap:* or unwrap:^Air India$
        return build_unwrap_patterns(self._link_patterns())

    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        # Nothing configured -> no-op.
        if self.link_pattern is None and not self.unwrap_patterns:
            return markdown

        cleaned_lines: list[str] = []
        skip_next_blank = False

        # Phase 1: remove links that match anchor/text patterns.
        # Example:
        #   "abc [x](#cite_note-1)" -> "abc \0C4MD_REMOVED_LINK\0"
        cleaned_markdown, code_replacements = self._mask_inline_code(markdown)
        if self.link_pattern is not None:
            cleaned_markdown = self.link_pattern.sub(self._replace_link, cleaned_markdown)

        # Phase 2: unwrap links that match unwrap patterns.
        # Example:
        #   "[Air India](...)" + unwrap:* -> "Air India"
        if self.unwrap_patterns:
            cleaned_markdown = self.UNWRAP_LINK_PATTERN.sub(self._replace_unwrapped_link, cleaned_markdown)

        cleaned_markdown = self._restore_inline_code(cleaned_markdown, code_replacements)

        # Phase 3: line-wise cleanup after marker-based removals.
        for line in cleaned_markdown.splitlines():
            # If the previous line was removed and this line is only blank,
            # drop it too to avoid artificial double-empty lines.
            if skip_next_blank and not line.strip():
                skip_next_blank = False
                continue

            skip_next_blank = False
            line_changed = self.REMOVED_LINK_MARKER in line
            cleaned_line = line.replace(self.REMOVED_LINK_MARKER, "")

            # If a removed link was at line start, trim leading spaces (except tables).
            if (
                line_changed
                and self._starts_with_removed_link(line)
                and not cleaned_line.lstrip().startswith("|")
            ):
                cleaned_line = cleaned_line.lstrip()

            # Drop lines that became semantically empty after link removal.
            # Example:
            #   "[[17]](#cite_note-17)" -> removed line
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
        # Called for anchor/text matched links.
        matched = match.group(0)
        leading = re.match(r"[^\S\n]*", matched).group(0)
        body = matched[len(leading):]
        before = match.string[: match.start()]
        previous = before.rstrip()[-1:] if before.strip() else ""

        # Keep table separators stable:
        # "... | [Link](...)" should not inject marker noise near pipes.
        if previous == "|":
            return leading

        # Collapse citation-like emphasis constructs to neutral marker.
        # Examples:
        #   [*[citation needed](...)*] -> [**]
        #   *[citation needed](...)*   -> [**]
        emphasized = self.BRACKETED_EMPHASIS_LINK_PATTERN.match(body)
        if emphasized:
            return f"{leading}[**]"

        emphasized = self.EMPHASIS_LINK_PATTERN.match(body)
        if emphasized:
            return f"{leading}[**]"

        # Default remove-path: leave internal marker for phase-3 cleanup.
        return self.REMOVED_LINK_MARKER

    def _replace_unwrapped_link(self, match: re.Match[str]) -> str:
        # Called for unwrap phase only.
        text = match.group("text")
        if not any(pattern.search(text) for pattern in self.unwrap_patterns):
            return match.group(0)

        # Keep original indentation and only remove link target/title.
        # Example:
        #   "  [Boeing](https://...)" -> "  Boeing"
        return f"{match.group('leading')}{text}"

    def _link_patterns(self) -> list[str]:
        # Normalize config to a simple list:
        # remove_links: "anchor:cite_note" -> ["anchor:cite_note"]
        # remove_links: ["a", "b"]        -> ["a", "b"]
        if not self.config.remove_links:
            return []

        if isinstance(self.config.remove_links, str):
            return [self.config.remove_links]

        return self.config.remove_links

    def _mask_inline_code(self, markdown: str) -> tuple[str, list[str]]:
        replacements: list[str] = []

        def _replace(match: re.Match[str]) -> str:
            replacements.append(match.group(0))
            return f"\0C4MD_INLINE_CODE_{len(replacements) - 1}\0"

        return self.INLINE_CODE_PATTERN.sub(_replace, markdown), replacements

    def _restore_inline_code(self, markdown: str, replacements: list[str]) -> str:
        restored = markdown
        for index, value in enumerate(replacements):
            restored = restored.replace(f"\0C4MD_INLINE_CODE_{index}\0", value)
        return restored
