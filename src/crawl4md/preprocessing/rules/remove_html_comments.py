import re

from .rule_base import RuleBase


HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)


class RuleRemoveHtmlComments(RuleBase):
    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        return HTML_COMMENT_PATTERN.sub("", markdown)
