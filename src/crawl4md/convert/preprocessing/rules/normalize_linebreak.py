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


TABLE_CELL_PATTERN = re.compile(r"^:?-{3,}:?$")
LIST_ITEM_PATTERN = re.compile(r"^\s*(?:[*+-]|\d+[.)])\s+")


class RuleNormalizeLinebreak(RuleBase):
    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
        language: str | None = None,
    ) -> str:
        lines = markdown.splitlines()
        blocks: list[str] = []
        index = 0

        while index < len(lines):
            line = lines[index]

            if not line.strip():
                index += 1
                continue

            if self._is_fence(line):
                block_lines = [line]
                index += 1

                while index < len(lines):
                    block_lines.append(lines[index])
                    if self._is_fence(lines[index]):
                        index += 1
                        break
                    index += 1

                blocks.append("\n".join(block_lines))
                continue

            if self.HEADING_PATTERN.match(line):
                blocks.append(line)
                index += 1
                continue

            if self._is_table_start(lines, index):
                block_lines = [lines[index]]
                index += 1

                while index < len(lines):
                    current = lines[index]
                    if not current.strip():
                        break
                    if self.HEADING_PATTERN.match(current) or self._is_fence(current):
                        break
                    if "|" not in current:
                        break

                    block_lines.append(current)
                    index += 1

                blocks.append("\n".join(block_lines))
                continue

            if self._is_list_item(line):
                block_lines = [line]
                index += 1

                while index < len(lines):
                    current = lines[index]

                    if not current.strip():
                        next_index = self._next_nonblank_index(lines, index + 1)
                        if next_index is None or not self._is_list_item(lines[next_index]):
                            index += 1
                            break

                        index = next_index
                        current = lines[index]

                    if not self._is_list_item(current):
                        break

                    block_lines.append(current)
                    index += 1

                blocks.append("\n".join(block_lines))
                continue

            block_lines = [line]
            index += 1

            while index < len(lines):
                current = lines[index]
                if not current.strip():
                    index += 1
                    break
                if self.HEADING_PATTERN.match(current):
                    break
                if self._is_fence(current):
                    break
                if self._is_table_start(lines, index):
                    break
                if self._is_list_item(current):
                    break

                block_lines.append(current)
                index += 1

            blocks.append("\n\n".join(block_lines))

        if not blocks:
            return ""

        return "\n\n".join(blocks) + "\n"

    def _is_fence(self, line: str) -> bool:
        stripped = line.lstrip()
        return stripped.startswith("```") or stripped.startswith("~~~")

    def _is_list_item(self, line: str) -> bool:
        return bool(LIST_ITEM_PATTERN.match(line))

    def _next_nonblank_index(self, lines: list[str], index: int) -> int | None:
        while index < len(lines):
            if lines[index].strip():
                return index
            index += 1

        return None

    def _is_table_start(self, lines: list[str], index: int) -> bool:
        if index + 1 >= len(lines):
            return False

        if "|" not in lines[index]:
            return False

        separator_cells = [
            cell.strip()
            for cell in lines[index + 1].strip().strip("|").split("|")
        ]

        if not separator_cells or any(not cell for cell in separator_cells):
            return False

        return all(TABLE_CELL_PATTERN.match(cell) for cell in separator_cells)
