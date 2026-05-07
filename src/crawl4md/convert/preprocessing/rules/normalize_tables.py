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


TABLE_SEPARATOR_CELL_PATTERN = re.compile(r"^:?-{3,}:?$")


class RuleNormalizeTables(RuleBase):
    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        lines = markdown.splitlines()
        cleaned_lines: list[str] = []
        index = 0

        while index < len(lines):
            if self._is_table_start(lines, index):
                table_lines, index = self._collect_table_lines(lines, index)
                cleaned_lines.extend(self._normalize_table(table_lines))
                continue

            cleaned_lines.append(lines[index])
            index += 1

        return self.join_lines(cleaned_lines, markdown)

    def _is_table_start(self, lines: list[str], index: int) -> bool:
        if index + 1 >= len(lines):
            return False

        if "|" not in lines[index] or "|" not in lines[index + 1]:
            return False

        return self._is_separator_row(lines[index + 1])

    def _is_separator_row(self, line: str) -> bool:
        cells = self._split_row(line)
        return bool(cells) and all(TABLE_SEPARATOR_CELL_PATTERN.match(cell) for cell in cells)

    def _collect_table_lines(self, lines: list[str], index: int) -> tuple[list[str], int]:
        table_lines: list[str] = []

        while index < len(lines):
            line = lines[index]

            if not line.strip() or "|" not in line:
                break

            table_lines.append(line)
            index += 1

        return table_lines, index

    def _normalize_table(self, lines: list[str]) -> list[str]:
        if len(lines) < 2:
            return lines

        column_count = max(len(self._split_row(lines[0])), len(self._split_row(lines[1])))
        normalized_lines = [
            self._format_row(self._normalize_cells(self._split_row(lines[0]), column_count)),
            self._format_row(["---"] * column_count),
        ]

        for line in lines[2:]:
            cells = self._normalize_cells(self._split_row(line), column_count)

            if self._is_empty_row(cells):
                continue

            normalized_lines.append(self._format_row(cells))

        return normalized_lines

    def _split_row(self, line: str) -> list[str]:
        stripped = line.strip()

        if stripped.startswith("|"):
            stripped = stripped[1:]

        if stripped.endswith("|"):
            stripped = stripped[:-1]

        return [cell.strip() for cell in stripped.split("|")]

    def _normalize_cells(self, cells: list[str], column_count: int) -> list[str]:
        normalized = cells[:column_count]

        while len(normalized) < column_count:
            normalized.append("")

        return normalized

    def _is_empty_row(self, cells: list[str]) -> bool:
        return all(not cell for cell in cells)

    def _format_row(self, cells: list[str]) -> str:
        row = "|"

        for cell in cells:
            if cell:
                row += f" {cell} |"
            else:
                row += " |"

        return row
