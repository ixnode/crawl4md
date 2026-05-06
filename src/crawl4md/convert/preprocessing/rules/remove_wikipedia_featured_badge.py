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

from .base.rule_base import RuleBase


FEATURED_BADGE_TARGETS = {
    "#vorlage_lesenswert",
    "#vorlage_exzellent",
}


class RuleRemoveWikipediaFeaturedBadge(RuleBase):
    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        cleaned_lines: list[str] = []
        skip_next_blank = False

        for line in markdown.splitlines():
            if skip_next_blank and not line.strip():
                skip_next_blank = False
                continue

            skip_next_blank = False

            if self._is_featured_badge_line(line):
                skip_next_blank = True
                continue

            cleaned_lines.append(line)

        return self.join_lines(cleaned_lines, markdown)

    def _is_featured_badge_line(self, line: str) -> bool:
        normalized = line.casefold()
        return (
            normalized.startswith("[![")
            and any(target in normalized for target in FEATURED_BADGE_TARGETS)
        )
