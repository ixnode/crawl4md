from .rules.rule_base import RuleBase
from .rules.ensure_h1 import RuleEnsureH1
from .rules.normalize_whitespace import RuleNormalizeWhitespace
from .rules.remove_html_comments import RuleRemoveHtmlComments
from .rules.remove_jump_to_content import RuleRemoveJumpToContent
from .rules.remove_reference_sections import RuleRemoveReferenceSections
from .rules.remove_wiki_loves_earth_banner import RuleRemoveWikiLovesEarthBanner
from .rules.remove_wikipedia_subtitle import RuleRemoveWikipediaSubtitle
from ..config import MarkdownPreprocessingConfig


class MarkdownPreprocessing:
    def __init__(self, config: MarkdownPreprocessingConfig):
        self.config = config
        self.rules: list[RuleBase] = []

        if config.remove_jump_to_content:
            self.rules.append(RuleRemoveJumpToContent(config))

        if config.remove_html_comments:
            self.rules.append(RuleRemoveHtmlComments(config))

        if config.remove_wikipedia_subtitle:
            self.rules.append(RuleRemoveWikipediaSubtitle(config))

        if config.remove_wiki_loves_earth_banner:
            self.rules.append(RuleRemoveWikiLovesEarthBanner(config))

        if config.remove_reference_sections:
            self.rules.append(RuleRemoveReferenceSections(config))

        if config.ensure_h1:
            self.rules.append(RuleEnsureH1(config))

        if config.normalize_whitespace:
            self.rules.append(RuleNormalizeWhitespace(config))

    def process(
        self,
        markdown: str,
        *,
        url: str | None = None,
        html: str | None = None,
    ) -> str:
        if not self.config.enabled:
            return markdown

        for rule in self.rules:
            markdown = rule.apply(markdown, url=url, html=html)

        return markdown
