import yaml

from pydantic import BaseModel, Field
from typing import Literal


ParseType = Literal["markdown", "markdown-fit"]

class CrawlConfig(BaseModel):
    parse_type: ParseType = "markdown"

class MarkdownPreprocessingConfig(BaseModel):
    enabled: bool = False

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
