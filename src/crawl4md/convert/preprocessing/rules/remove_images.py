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
    IMAGE_PATTERN = re.compile(rf"!\[[^\]\n]*\]\({MARKDOWN_TARGET}\)")
    LINKED_IMAGE_PATTERN = re.compile(
        rf"\[(?:\s*{IMAGE_PATTERN.pattern})+\s*\]\({MARKDOWN_TARGET}\)"
    )

    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        if not self.config.remove_images:
            return markdown

        markdown = self.LINKED_IMAGE_PATTERN.sub("", markdown)
        return self.IMAGE_PATTERN.sub("", markdown)
