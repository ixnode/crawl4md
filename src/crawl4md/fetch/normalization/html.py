# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-14)
# @since 1.0.0 (2026-05-14) First version

from crawl4md.config import NormalizationConfig
from crawl4md.fetch.normalization.rules.base.rule_base import RuleBase
from crawl4md.fetch.normalization.rules.entities import RuleEntities
from crawl4md.fetch.normalization.rules.hiddens import RuleHiddens
from crawl4md.fetch.normalization.rules.references import RuleReferences
from crawl4md.fetch.normalization.rules.urls import RuleUrls


class HtmlNormalization:
    def __init__(self, config: NormalizationConfig, url: str):
        self.config = config
        self.rules: list[RuleBase] = []

        if not config.enabled:
            return

        if config.entities:
            self.rules.append(RuleEntities())

        if config.hidden_spans:
            self.rules.append(RuleHiddens())

        if config.urls:
            self.rules.append(RuleUrls(url=url))

        if config.references:
            self.rules.append(RuleReferences())

    def process(self, html: str) -> str:
        for rule in self.rules:
            html = rule.normalize(html)

        return html
