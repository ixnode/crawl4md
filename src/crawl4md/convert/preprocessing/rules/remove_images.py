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


class RuleRemoveImages(RuleBase):
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

        markdown = self.LINKED_IMAGE_PATTERN.sub(self._replace_linked_image, markdown)
        return self.IMAGE_PATTERN.sub(self._replace_image, markdown)

    def _replace_linked_image(self, match: re.Match[str]) -> str:
        replacements = [
            self._image_text(image_match)
            for image_match in self.IMAGE_PATTERN.finditer(match.group("content"))
        ]
        link_text = " ".join(replacement for replacement in replacements if replacement).strip()
        return f"[{link_text}]({match.group('target')})"

    def _replace_image(self, match: re.Match[str]) -> str:
        return self._image_text(match)

    def _image_text(self, match: re.Match[str]) -> str:
        alt = match.group("alt").strip()
        if alt:
            return alt

        title = self._extract_title(match.group("target"))
        if title:
            return title

        return ""

    def _extract_title(self, target: str) -> str:
        match = self.TITLE_PATTERN.search(target.strip())
        if match is None:
            return ""

        return next((group.strip() for group in match.groups() if group is not None), "")
