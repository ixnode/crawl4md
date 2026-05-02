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


WIKIPEDIA_SUBTITLE = "aus Wikipedia, der freien Enzyklopädie"


class RuleRemoveWikipediaSubtitle(RuleBase):
    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        cleaned_lines: list[str] = []

        for line in markdown.splitlines():
            cleaned_line = re.sub(
                r"\s{2,}",
                " ",
                line.replace(WIKIPEDIA_SUBTITLE, ""),
            ).rstrip()

            if cleaned_line.strip():
                cleaned_lines.append(cleaned_line)

        return self.join_lines(cleaned_lines, markdown)
