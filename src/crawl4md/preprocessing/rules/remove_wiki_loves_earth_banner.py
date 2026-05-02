from .RuleBase import RuleBase


class RuleRemoveWikiLovesEarthBanner(RuleBase):
    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        if not url:
            return markdown

        cleaned_markdown = self.MARKDOWN_LINK_PATTERN.sub(
            lambda match: ""
            if self._is_banner_target(match.group(2), url)
            else match.group(0),
            markdown,
        )

        cleaned_lines = [
            line for line in cleaned_markdown.splitlines() if line.strip()
        ]
        return self.join_lines(cleaned_lines, markdown)

    def _is_banner_target(self, link_target: str, page_url: str) -> bool:
        resolved = self.resolve_url(page_url, link_target)
        return (
            (
                resolved.netloc == "de.wikipedia.org"
                and resolved.path.startswith("/wiki/Wikipedia:Wiki_Loves_Earth_")
            )
            or (
                resolved.netloc == "www.wikidata.org"
                and resolved.path.startswith("/wiki/Wikidata:Events/Coordinate_Me_")
            )
        )

