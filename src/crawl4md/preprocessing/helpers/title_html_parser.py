from html.parser import HTMLParser


class _TitleHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._active_tag: str | None = None
        self._capturing_h1 = False
        self._seen_h1 = False
        self._h1_parts: list[str] = []
        self._title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._active_tag = tag

        if tag == "h1" and not self._seen_h1:
            self._capturing_h1 = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1" and self._capturing_h1:
            self._capturing_h1 = False
            self._seen_h1 = True

        if tag == self._active_tag:
            self._active_tag = None

    def handle_data(self, data: str) -> None:
        if self._capturing_h1:
            self._h1_parts.append(data)

        if self._active_tag == "title":
            self._title_parts.append(data)

    @property
    def h1_text(self) -> str:
        return "".join(self._h1_parts)

    @property
    def title_text(self) -> str:
        return "".join(self._title_parts)
