from .RuleBase import RuleBase


class RuleEnsureH1(RuleBase):
    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        if self.has_h1(markdown):
            return markdown

        title = None
        if html:
            title = self.extract_title_from_html(html)

        if not title and url:
            try:
                fetched_html = self.fetch_html(url)
            except Exception:
                fetched_html = None

            if fetched_html:
                title = self.extract_title_from_html(fetched_html)

        if not title and url:
            title = self.fallback_title_from_url(url)

        if not title:
            title = "index"

        return f"# {title}\n\n{markdown}"

