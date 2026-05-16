# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-14)
# @since 1.0.0 (2026-05-14) First version

import re

from .base.rule_base import RuleBase
from crawl4md.language import extract_language_from_html
from crawl4md.language_variables import get_figure_label


class RuleRemoveImages(RuleBase):
    REMOVED_IMAGE_MARKER = "\0C4MD_REMOVED_IMAGE\0"
    FIGURE_PREFIX = '{label}: "{text}"'
    MARKDOWN_TARGET = r"(?:\\.|[^()\\\n]|\([^()\n]*\))*"
    IMAGE_INNER_PATTERN = rf"!\[[^\]\n]*\]\({MARKDOWN_TARGET}\)"
    IMAGE_PATTERN = re.compile(rf"!\[(?P<alt>[^\]\n]*)\]\((?P<target>{MARKDOWN_TARGET})\)")
    LINKED_IMAGE_PATTERN = re.compile(
        rf"\[(?P<content>(?:\s*{IMAGE_INNER_PATTERN})+\s*)\]\((?P<target>{MARKDOWN_TARGET})\)"
    )
    TITLE_PATTERN = re.compile(r"""\s+(?:"([^"]*)"|'([^']*)'|\(([^)]*)\))\s*$""")

    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        if not self.config.remove_images:
            return markdown

        language = extract_language_from_html(html) if html else "en"
        figure_label = get_figure_label(language)
        original = markdown
        markdown = self.LINKED_IMAGE_PATTERN.sub(
            lambda match: self._replace_linked_image(match, figure_label),
            markdown,
        )
        markdown = self.IMAGE_PATTERN.sub(
            lambda match: self._replace_image(match, figure_label),
            markdown,
        )
        return self._cleanup_removed_image_lines(markdown, source=original)

    def _replace_linked_image(self, match: re.Match[str], figure_label: str) -> str:
        replacements = [
            self._image_text(image_match, figure_label)
            for image_match in self.IMAGE_PATTERN.finditer(match.group("content"))
        ]
        link_text = " ".join(
            replacement
            for replacement in replacements
            if replacement and replacement != self.REMOVED_IMAGE_MARKER
        ).strip()
        return f"[{link_text}]({match.group('target')})"

    def _replace_image(self, match: re.Match[str], figure_label: str) -> str:
        return self._image_text(match, figure_label)

    def _image_text(self, match: re.Match[str], figure_label: str) -> str:
        alt = match.group("alt").strip()
        if alt:
            return self.FIGURE_PREFIX.format(label=figure_label, text=alt)

        title = self._extract_title(match.group("target"))
        if title:
            return self.FIGURE_PREFIX.format(label=figure_label, text=title)

        return self.REMOVED_IMAGE_MARKER

    def _extract_title(self, target: str) -> str:
        match = self.TITLE_PATTERN.search(target.strip())
        if match is None:
            return ""

        return next((group.strip() for group in match.groups() if group is not None), "")

    def _cleanup_removed_image_lines(self, markdown: str, *, source: str) -> str:
        cleaned_lines: list[str] = []
        skip_next_blank = False

        for line in markdown.splitlines():
            if skip_next_blank and not line.strip():
                skip_next_blank = False
                continue

            skip_next_blank = False
            had_marker = self.REMOVED_IMAGE_MARKER in line
            cleaned_line = line.replace(self.REMOVED_IMAGE_MARKER, "")

            if had_marker and not cleaned_line.strip():
                skip_next_blank = True
                continue

            cleaned_lines.append(cleaned_line)

        return self.join_lines(cleaned_lines, source)
