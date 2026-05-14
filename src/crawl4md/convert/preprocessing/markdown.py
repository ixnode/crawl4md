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

from .rules.base.rule_base import RuleBase
from .rules.ensure_h1 import RuleEnsureH1
from .rules.normalize_linebreak import RuleNormalizeLinebreak
from .rules.normalize_tables import RuleNormalizeTables
from .rules.normalize_whitespace import RuleNormalizeWhitespace
from .rules.remove_blocks import RuleRemoveBlocks
from .rules.remove_images import RuleRemoveImages
from .rules.remove_links import RuleRemoveLinks
from .rules.remove_lines import RuleRemoveLines
from .rules.remove_html_comments import RuleRemoveHtmlComments
from .rules.remove_sections import RuleRemoveSections
from crawl4md.config import MarkdownPreprocessingConfig


class MarkdownPreprocessing:
    def __init__(self, config: MarkdownPreprocessingConfig):
        self.config = config
        self.rules: list[RuleBase] = []

        if config.remove_html_comments:
            self.rules.append(RuleRemoveHtmlComments(config))

        if config.remove_sections:
            self.rules.append(RuleRemoveSections(config))

        if config.remove_blocks:
            self.rules.append(RuleRemoveBlocks(config))

        if config.remove_images:
            self.rules.append(RuleRemoveImages(config))

        if config.remove_links:
            self.rules.append(RuleRemoveLinks(config))

        if config.remove_lines:
            self.rules.append(RuleRemoveLines(config))

        if config.ensure_h1:
            self.rules.append(RuleEnsureH1(config))

        if config.normalize_tables:
            self.rules.append(RuleNormalizeTables(config))

        if config.normalize_linebreak:
            self.rules.append(RuleNormalizeLinebreak(config))

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
