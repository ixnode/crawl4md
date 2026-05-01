from pydantic import BaseModel
from typing import Literal
import yaml


class ProjectConfig(BaseModel):
    type: Literal["sitemap", "pages"]
    sources: list[str]


class AppConfig(BaseModel):
    projects: dict[str, ProjectConfig]


def load_config(path: str = "crawl.yml") -> AppConfig:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)