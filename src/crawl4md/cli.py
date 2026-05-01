import typer
import asyncio
from pathlib import Path

from crawler.config import load_config
from crawler.sitemap import parse_sitemap
from crawler.crawler import fetch_markdown
from crawler.paths import url_to_path
from crawler.writer import write_markdown

app = typer.Typer()


@app.command()
def crawl(project: str):
    config = load_config()

    if project not in config.projects:
        typer.echo(f"Project '{project}' not found")
        raise typer.Exit(1)

    proj = config.projects[project]

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
        typer.echo(f"{i}/{total} Crawl {url}")

        try:
            typer.echo("- Fetching ...", nl=False)
            md = asyncio.run(fetch_markdown(url))
            typer.echo(" done")

            typer.echo("- Processing ... done")

            path = url_to_path(Path("docs"), project, url)

            typer.echo(f"- Writing {path} ...", nl=False)
            write_markdown(path, md)
            typer.echo(" done")

            success += 1

        except Exception as e:
            typer.echo(f"- Error: {e}")
            failed += 1

    typer.echo("\nDone.")
    typer.echo(f"- Success: {success}")
    typer.echo(f"- Failed: {failed}")
    typer.echo(f"- Output: docs/{project}")
