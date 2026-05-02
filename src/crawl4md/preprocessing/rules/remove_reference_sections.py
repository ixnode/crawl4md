from .RuleBase import RuleBase


class RuleRemoveReferenceSections(RuleBase):
    def __init__(self, config):
        super().__init__(config)
        self.reference_headings = {
            self.normalize_heading(heading)
            for heading in config.reference_headings
            if self.normalize_heading(heading)
        }

    def apply(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        if not self.reference_headings:
            return markdown

        lines = markdown.splitlines()

        for index, line in enumerate(lines):
            match = self.HEADING_PATTERN.match(line)
            if not match:
                continue

            heading = self.normalize_heading(match.group(2))
            if heading in self.reference_headings:
                kept_lines = lines[:index]
                suffix = "\n" if markdown.endswith("\n") and kept_lines else ""
                return "\n".join(kept_lines).rstrip() + suffix

        return markdown
