from .RuleBase import RuleBase


SKIP_CONTENT_FRAGMENTS = {
    "bodycontent",
    "content",
    "content-start",
    "main",
    "main-content",
    "maincontent",
}


class RuleRemoveJumpToContent(RuleBase):
    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        if not url:
            return markdown

        cleaned_lines: list[str] = []

        for line in markdown.splitlines():
            cleaned_line = self.MARKDOWN_LINK_PATTERN.sub(
                lambda match: ""
                if self._is_jump_to_content_target(match.group(2), url)
                else match.group(0),
                line,
            )

            if cleaned_line.strip():
                cleaned_lines.append(cleaned_line)

        return self.join_lines(cleaned_lines, markdown)

    def _is_jump_to_content_target(self, link_target: str, page_url: str) -> bool:
        resolved = self.resolve_url(page_url, link_target)
        page = self.resolve_url(page_url, page_url)

        if not resolved.fragment:
            return False

        if resolved.fragment.lower() not in SKIP_CONTENT_FRAGMENTS:
            return False

        same_page = (
            resolved.scheme == page.scheme
            and resolved.netloc == page.netloc
            and resolved.path == page.path
        )
        fragment_only = not resolved.scheme and not resolved.netloc and not resolved.path

        return same_page or fragment_only

