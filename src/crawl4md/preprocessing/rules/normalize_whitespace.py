import re

from .rule_base import RuleBase


TABLE_SEPARATOR_PATTERN = re.compile(r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?\s*$")


class RuleNormalizeWhitespace(RuleBase):
    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
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
                blocks.append(line.rstrip())
                index += 1
                continue

            if self._is_table_start(lines, index):
                block_lines = [lines[index].rstrip()]
                index += 1

                while index < len(lines):
                    current = lines[index]
                    if not current.strip():
                        break
                    if self.HEADING_PATTERN.match(current) or self._is_fence(current):
                        break
                    if "|" not in current:
                        break

                    block_lines.append(current.rstrip())
                    index += 1

                blocks.append("\n".join(block_lines))
                continue

            block_lines = [line.rstrip()]
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

                block_lines.append(current.rstrip())
                index += 1

            blocks.append("\n".join(block_lines))

        if not blocks:
            return ""

        return "\n\n".join(blocks) + "\n"

    def _is_fence(self, line: str) -> bool:
        stripped = line.lstrip()
        return stripped.startswith("```") or stripped.startswith("~~~")

    def _is_table_start(self, lines: list[str], index: int) -> bool:
        if index + 1 >= len(lines):
            return False

        return "|" in lines[index] and bool(TABLE_SEPARATOR_PATTERN.match(lines[index + 1]))
