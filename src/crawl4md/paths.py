from urllib.parse import urlparse
from pathlib import Path


def url_to_path(base: Path, project: str, url: str) -> Path:
    parsed = urlparse(url)

    path = parsed.path.strip("/")
    if not path:
        path = "index"

    file_path = Path(base) / project / f"{path}.md"
    return file_path
