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
from copy import deepcopy

from pydantic import BaseModel, Field, model_validator
from typing import Literal


ParseType = Literal["markdown", "markdown-fit"]
ProfileName = Literal["wikipedia"]


PREPROCESSING_PROFILES = {
    "wikipedia": {
        "preprocessing": {
            "markdown": {
                "enabled": True,
                "ensure_h1": True,
                "remove_lines": [
                    "[Aa]us Wikipedia, der freien Enzyklopädie",
                    "[Ff]rom Wikipedia, the free encyclopedia",
                ],
                "remove_blocks": [
                    "Wikipedia:Wiki_Loves_Earth_",
                    "Wikidata:Events/Coordinate_Me_",
                ],
                "remove_sections": [
                    "Einzelnachweise",
                    "Weblinks",
                    "Literatur",
                    "Quellen",
                    "References",
                    "External links",
                    "Bibliography",
                ],
                "remove_links": [
                    "cite_note",
                    "anchor:#(?:[Bb]ody[Cc]ontent|content|content-start|main|main-content|maincontent)",
                    "#[Vv]orlage_[Ll]esenswert",
                    "#[Vv]orlage_[Ee]xzellent",
                    "veaction=edit[^)]*section=",
                    "action=edit[^)]*section=",
                ],
                "remove_html_comments": True,
                "normalize_tables": True,
                "normalize_linebreak": True,
                "normalize_whitespace": True,
            }
        }
    }
}

class CrawlConfig(BaseModel):
    parser: str = "kreuzberg-dev"
    parse_type: str = "markdown"
    content_selector: str | None = None

    @model_validator(mode="after")
    def validate_parse_type_for_parser(self) -> "CrawlConfig":
        if self.parser == "crawl4ai" and self.parse_type not in ("markdown", "markdown-fit"):
            raise ValueError(
                "crawl4ai parser supports only parse_type 'markdown' or 'markdown-fit'"
            )

        if self.parser == "kreuzberg-dev" and self.parse_type != "markdown":
            raise ValueError(
                "kreuzberg-dev parser supports only parse_type 'markdown'"
            )

        return self

class MarkdownPreprocessingConfig(BaseModel):
    enabled: bool = False

    ensure_h1: bool = False
    remove_sections: Literal[False] | str | list[str] = False
    remove_links: Literal[False] | str | list[str] = False
    remove_lines: Literal[False] | str | list[str] = False
    remove_blocks: Literal[False] | str | list[str] = False
    remove_html_comments: bool = False
    normalize_tables: bool = False
    normalize_linebreak: bool = False
    normalize_whitespace: bool = False

class PreprocessingConfig(BaseModel):
    markdown: MarkdownPreprocessingConfig = Field(
        default_factory=MarkdownPreprocessingConfig
    )

class ProjectConfig(BaseModel):
    profile: ProfileName | None = None
    type: Literal["sitemap", "pages"]
    sources: list[str]

    crawl: CrawlConfig = Field(default_factory=CrawlConfig)
    preprocessing: PreprocessingConfig = Field(default_factory=PreprocessingConfig)

class AppConfig(BaseModel):
    projects: dict[str, ProjectConfig]


def merge_dict(base: dict, override: dict) -> dict:
    merged = deepcopy(base)

    for key, value in override.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = merge_dict(merged[key], value)
            continue

        merged[key] = deepcopy(value)

    return merged


def apply_profile_defaults(project_data: dict) -> dict:
    profile = project_data.get("profile")
    if profile is None:
        return project_data

    if profile not in PREPROCESSING_PROFILES:
        raise ValueError(f"Unknown project profile: {profile}")

    return merge_dict(PREPROCESSING_PROFILES[profile], project_data)


def apply_profiles(data: dict) -> dict:
    data = deepcopy(data)
    projects = data.get("projects") or {}

    for name, project_data in projects.items():
        projects[name] = apply_profile_defaults(project_data)

    return data


def load_config(path: str = "crawl.yml") -> AppConfig:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return AppConfig(**apply_profiles(data))
