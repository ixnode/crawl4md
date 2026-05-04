from pathlib import Path
import unittest
import warnings

import yaml
from pydantic import BaseModel, Field

from crawl4md.config import ParseType, PreprocessingConfig
from crawl4md.convert.markdown import MarkdownConverter


SESSION_ROOT = Path(__file__).parent / "data" / "markdown_converter"


class MarkdownConverterSessionConfig(BaseModel):
    parse_type: ParseType = "markdown"
    url: str | None = None
    preprocessing: PreprocessingConfig = Field(default_factory=PreprocessingConfig)


class MarkdownConverterSessionTests(unittest.IsolatedAsyncioTestCase):
    maxDiff = None

    async def test_converts_all_configured_sessions(self) -> None:
        sessions = sorted(path for path in SESSION_ROOT.iterdir() if path.is_dir())

        self.assertGreater(len(sessions), 0, "No markdown converter test sessions found.")

        for session in sessions:
            with self.subTest(session=session.name):
                config = self._load_config(session / "config.yml")
                html = (session / "data.html").read_text()
                expected_markdown = (session / "data.md").read_text()

                converter = MarkdownConverter(
                    config=config.preprocessing.markdown,
                    parse_type=config.parse_type,
                )

                warnings.filterwarnings(
                    "ignore",
                    category=ResourceWarning,
                    message=r"unclosed database in <sqlite3\.Connection object at .*",
                    module=r"playwright\._impl\._local_utils",
                )
                markdown = await converter.convert(html=html, url=config.url)

                self.assertEqual(markdown, expected_markdown)

    def _load_config(self, path: Path) -> MarkdownConverterSessionConfig:
        return MarkdownConverterSessionConfig(**yaml.safe_load(path.read_text()))


if __name__ == "__main__":
    unittest.main()
