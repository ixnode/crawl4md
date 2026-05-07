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

from .base.rule_base import RuleBase


MISSING_SPACE_BEFORE_PAREN_PATTERN = re.compile(r"(?<=[\w\)])\(")


class RuleNormalizeWhitespace(RuleBase):
    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        lines = markdown.splitlines()
        normalized_lines: list[str] = []
        in_fence = False

        for line in lines:
            if self._is_fence(line):
                normalized_lines.append(line)
                in_fence = not in_fence
                continue

            if in_fence:
                normalized_lines.append(line)
                continue

            normalized_lines.append(self._normalize_line(line))

        return self.join_lines(normalized_lines, markdown)

    def _is_fence(self, line: str) -> bool:
        stripped = line.lstrip()
        return stripped.startswith("```") or stripped.startswith("~~~")

    def _normalize_line(self, line: str) -> str:
        line = line.rstrip()
        parts: list[str] = []
        last_end = 0

        for match in self.MARKDOWN_LINK_PATTERN.finditer(line):
            parts.append(line[last_end:match.start()])

            if (
                match.start() > 0
                and not line[match.start() - 1].isspace()
                and line[match.start() - 1] not in "!*"
            ):
                parts.append(" ")

            parts.append(match.group(0))
            last_end = match.end()

        parts.append(line[last_end:])
        normalized = "".join(parts)
        return self._normalize_parentheses_outside_links(normalized)

    def _normalize_parentheses_outside_links(self, line: str) -> str:
        parts: list[str] = []
        index = 0

        while index < len(line):
            link_start = self._find_next_markdown_link_start(line, index)

            if link_start is None:
                parts.append(MISSING_SPACE_BEFORE_PAREN_PATTERN.sub(" (", line[index:]))
                break

            link_end = self._find_markdown_link_end(line, link_start)

            if link_end is None:
                parts.append(MISSING_SPACE_BEFORE_PAREN_PATTERN.sub(" (", line[index:]))
                break

            parts.append(MISSING_SPACE_BEFORE_PAREN_PATTERN.sub(" (", line[index:link_start]))
            parts.append(line[link_start:link_end])
            index = link_end

        return "".join(parts)

    def _find_next_markdown_link_start(self, line: str, index: int) -> int | None:
        close_bracket = line.find("](", index)

        while close_bracket != -1:
            open_bracket = line.rfind("[", 0, close_bracket)

            if open_bracket != -1:
                return max(open_bracket, index)

            close_bracket = line.find("](", close_bracket + 2)

        return None

    def _find_markdown_link_end(self, line: str, link_start: int) -> int | None:
        close_bracket = line.find("](", link_start)

        if close_bracket == -1:
            return None

        index = close_bracket + 2
        depth = 1

        while index < len(line):
            character = line[index]

            if character == "\\":
                index += 2
                continue

            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1

                if depth == 0:
                    return index + 1

            index += 1

        return None
