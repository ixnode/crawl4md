import re

from .rule_base import RuleBase


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
