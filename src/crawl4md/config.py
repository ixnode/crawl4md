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

import yaml

from pydantic import BaseModel, Field
from typing import Literal


ParseType = Literal["markdown", "markdown-fit"]

class CrawlConfig(BaseModel):
    parse_type: ParseType = "markdown"

class MarkdownPreprocessingConfig(BaseModel):
    enabled: bool = False

    ensure_h1: bool = False
    remove_jump_to_content: bool = False
    remove_wikipedia_subtitle: bool = False
    remove_wiki_loves_earth_banner: bool = False
    remove_reference_sections: bool = False
    remove_html_comments: bool = False
    normalize_whitespace: bool = False

    reference_headings: list[str] = Field(default_factory=list)

class PreprocessingConfig(BaseModel):
    markdown: MarkdownPreprocessingConfig = Field(
        default_factory=MarkdownPreprocessingConfig
    )

class ProjectConfig(BaseModel):
    type: Literal["sitemap", "pages"]
    sources: list[str]

    crawl: CrawlConfig = Field(default_factory=CrawlConfig)
    preprocessing: PreprocessingConfig = Field(default_factory=PreprocessingConfig)

class AppConfig(BaseModel):
    projects: dict[str, ProjectConfig]

def load_config(path: str = "crawl.yml") -> AppConfig:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)
