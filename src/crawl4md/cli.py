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

import typer
import asyncio
import time
import warnings

from pathlib import Path
from urllib.parse import urlparse

from .config import load_config
from .fetch.markdown_fetcher_crawl4ai import MarkdownFetcherCrawl4AI
from .fetch.markdown_fetcher_kreuzberg_dev import MarkdownFetcherKreuzbergDev
from .paths import url_to_path
from .sitemap import parse_sitemap
from .writer import write_markdown


warnings.filterwarnings(
    "ignore",
    category=SyntaxWarning,
    module=r"crawl4ai\..*",
)

app = typer.Typer()


def format_duration(seconds: float) -> str:
    return f"{seconds * 1000:.0f} ms"


def pretty_name(url: str) -> str:
    return Path(urlparse(url).path).name or "index"


def build_fetcher(proj):
    if proj.crawl.parser == "crawl4ai":
        return MarkdownFetcherCrawl4AI(
            config=proj.preprocessing.markdown,
            normalization=proj.normalization,
            parse_type=proj.crawl.parse_type,
            content_selector=proj.crawl.content_selector,
        )

    if proj.crawl.parser == "kreuzberg-dev":
        return MarkdownFetcherKreuzbergDev(
            config=proj.preprocessing.markdown,
            normalization=proj.normalization,
            parse_type=proj.crawl.parse_type,
            content_selector=proj.crawl.content_selector,
        )

    raise ValueError(f"Unknown crawl parser: {proj.crawl.parser}")

@app.command()
def crawl(project: str):
    config = load_config()

    if project not in config.projects:
        typer.echo(f"Project '{project}' not found")
        raise typer.Exit(1)

    proj = config.projects[project]
    fetcher = build_fetcher(proj)

    # URLs sammeln
    urls: list[str] = []

    if proj.type == "pages":
        urls = proj.sources

    elif proj.type == "sitemap":
        for sitemap_url in proj.sources:
            urls.extend(parse_sitemap(sitemap_url))

    # deduplicate
    urls = list(dict.fromkeys(urls))

    total = len(urls)
    success = 0
    failed = 0

    for i, url in enumerate(urls, start=1):
        name = pretty_name(url)
        typer.echo(f"[{i}/{total}] {name}")

        try:
            typer.echo("  → Fetching...", nl=False)
            fetch_started_at = time.perf_counter()
            md = asyncio.run(fetcher.fetch(url))
            typer.echo(f" done ({format_duration(time.perf_counter() - fetch_started_at)})")

            path = url_to_path(Path("crawled"), project, url)

            typer.echo(f"  → Writing... {path}", nl=False)
            write_started_at = time.perf_counter()
            write_markdown(path, md)
            typer.echo(f" ({format_duration(time.perf_counter() - write_started_at)})")

            success += 1

        except Exception as e:
            typer.echo(f"  → Error: {e}")
            failed += 1

        typer.echo("")

    typer.echo("Done.")
    typer.echo(f"✔ Success: {success}")
    typer.echo(f"✖ Failed: {failed}")
    typer.echo(f"Output: crawled/{project}")
