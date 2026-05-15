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

from urllib.parse import urlparse
from pathlib import Path


def url_to_path(base: Path, project: str, url: str) -> Path:
    parsed = urlparse(url)

    path = parsed.path.strip("/")
    if not path:
        path = "index"

    file_path = Path(base) / project / f"{path}.md"
    return file_path

def get_root_path() -> Path:
    return Path(__file__).resolve().parents[2]

def load_markdown_file(path: str) -> str | None:
    markdown_path = get_root_path() / path

    if not markdown_path.exists():
        return None

    return markdown_path.read_text(encoding="utf-8")
