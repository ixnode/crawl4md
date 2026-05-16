from pydantic import BaseModel, Field

from crawl4md.core.config import CrawlConfig, NormalizationConfig, PreprocessingConfig


class MarkdownConverterSessionConfig(BaseModel):
    profile: str | None = None
    crawl: CrawlConfig = Field(default_factory=CrawlConfig)
    normalization: NormalizationConfig = Field(default_factory=NormalizationConfig)
    url: str | None = None
    preprocessing: PreprocessingConfig = Field(default_factory=PreprocessingConfig)


class MarkdownConverterSession(BaseModel):
    id: str
    title: str
    description: str
    config: MarkdownConverterSessionConfig
