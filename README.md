# crawl4md

crawl4md is a minimal, clean CLI tool that crawls web pages or sitemaps and converts them into structured Markdown files.

The project is intentionally designed to stay simple, deterministic, and easy to extend — without unnecessary complexity or hidden behavior.

---

## Philosophy

- **Minimal**: only what is needed, nothing more  
- **Deterministic**: same input → same output  
- **Transparent**: no magic, clear processing steps  
- **Composable**: ideal as a building block for pipelines (e.g. RAG)

---

## Features

- Crawl from:
  - `sitemap.xml`
  - explicit page lists
- Clean Markdown output via exchangeable parser backends
- Deterministic file structure based on URL paths
- YAML-based project configuration
- CLI-first workflow (uv-compatible)
- Clear, readable progress output

---

## Installation

There are two ways to use `crawl4md`.

### Use the Batch Crawler

If you want to use the project directly for batch crawling via `crawl.yml`, clone the repository:

```bash
git clone git@github.com:ixnode/crawl4md.git && cd crawl4md
```

Then continue with the configuration section below.

### Use the Python Package

If you want to build your own tooling on top of `crawl4md`, install it as a package:

```bash
pip install crawl4md
```

Or with `uv`:

```bash
uv add crawl4md
```

For local development inside the repository:

```bash
uv sync
```

---

## Configuration

The CLI reads a `crawl.yml` file from the current working directory.

Create it from the example:

```bash
cp crawl.yml.example crawl.yml
```

Minimal example:

```yaml
projects:
    planes:
        type: pages
        crawl:
            parser: kreuzberg-dev
            parse_type: markdown
        sources:
            - https://de.wikipedia.org/wiki/Boeing_707
            - https://de.wikipedia.org/wiki/Boeing_717
        preprocessing:
            markdown:
                enabled: true
                remove_html_comments: true
                normalize_whitespace: true

    pydantic:
        type: sitemap
        crawl:
            parser: kreuzberg-dev
            parse_type: markdown
        sources:
            - https://pydantic.dev/sitemap.xml
        preprocessing:
            markdown:
                enabled: false
```

Available project settings:

- `type`: `pages` or `sitemap`
- `sources`: list of page URLs or sitemap URLs
- `profile`: optional defaults such as `wikipedia` for `crawl`, `normalization`, and `preprocessing` (loaded from `profiles/*.yml`)
- `crawl.parser`: `kreuzberg-dev` or `crawl4ai`
- `crawl.parse_type`: `markdown`; `markdown-fit` is available with `crawl4ai`
- `normalization.*`: HTML normalization options (`enabled`, `entities`, `hidden_elements`, `urls`, `references`), all default to `true`
- `preprocessing.markdown.enabled`: enables Markdown cleanup
- `preprocessing.markdown.*`: optional cleanup rules such as `ensure_h1`, `remove_html_comments`, `remove_sections`, and `normalize_whitespace`

For the full configuration, see [`crawl.yml.example`](crawl.yml.example).
For details about all Markdown preprocessing options, see [`docs/markdown_preprocessing.md`](docs/markdown_preprocessing.md).

---

## Usage

After cloning the repository and creating `crawl.yml`, use:

```bash
crawl planes
crawl pydantic
```

Or with `uv` inside the project:

```bash
uv run crawl planes
uv run crawl pydantic
```

---

## Testing

Run the full validation suite with:

```bash
uv run check
```

For focused checks, grouped test commands, parameters, and examples, see:

- [`docs/testing.md`](docs/testing.md)

---

## Python API

`crawl4md` can also be used as a Python package after installing it with `pip install crawl4md` or `uv add crawl4md`.

The public API exports two recommended default classes:

- `MarkdownFetcher`: fetches a URL and returns Markdown
- `MarkdownConverter`: converts an existing HTML string into Markdown

Both currently use the recommended `kreuzberg-dev` backend.

The concrete parser classes are exported too:

- `MarkdownFetcherKreuzbergDev`
- `MarkdownConverterKreuzbergDev`
- `MarkdownFetcherCrawl4AI`
- `MarkdownConverterCrawl4AI`
- `ParseType`
- `MarkdownPreprocessingConfig`
- `NormalizationConfig`

Use the default aliases unless you explicitly need a specific parser backend.

All fetchers provide:

- `fetch(url)`: async URL fetch and Markdown conversion
- `fetch_sync(url)`: sync URL fetch and Markdown conversion

All converters provide:

- `convert(html, url=None)`: async HTML-to-Markdown conversion
- `convert_sync(html, url=None)`: sync HTML-to-Markdown conversion

Common constructor arguments:

- `config`: a `MarkdownPreprocessingConfig`
- `normalization`: optional `NormalizationConfig` for HTML normalization (`MarkdownFetcher*` only)
- `parse_type`: usually `"markdown"`
- `content_selector`: optional CSS selector for selecting only part of the HTML before conversion

### Configure Parse Type

When using `crawl.yml`, use `projects.<name>.crawl.parser` to choose the parser:

- `"kreuzberg-dev"`: recommended default, supports `parse_type: markdown`
- `"crawl4ai"`: supports `parse_type: markdown` and `parse_type: markdown-fit`

In Python, use the concrete class when you need a specific parser backend. Use `ParseType` to control how Markdown is generated:

- `"markdown"`: raw markdown output
- `"markdown-fit"`: cleaned and reduced markdown output via `crawl4ai`

### Configure Preprocessing

Use `MarkdownPreprocessingConfig` to enable optional cleanup steps.

For the full list of preprocessing options, see [`docs/markdown_preprocessing.md`](docs/markdown_preprocessing.md).

Simple example:

```python
from crawl4md import MarkdownPreprocessingConfig

config = MarkdownPreprocessingConfig(
    enabled=True,
    remove_html_comments=True,
    normalize_whitespace=True,
)
```

### Configure Normalization

Use `NormalizationConfig` to control HTML normalization before Markdown conversion (for fetchers).
If omitted, `MarkdownFetcher*` uses `NormalizationConfig()` defaults.

Explicit example:

```python
from crawl4md import MarkdownFetcher, MarkdownPreprocessingConfig, NormalizationConfig

fetcher = MarkdownFetcher(
    config=MarkdownPreprocessingConfig(enabled=True),
    normalization=NormalizationConfig(
        enabled=True,
        entities=True,
        hidden_elements=True,
        urls=True,
        references=True,
    ),
    parse_type="markdown",
)
```

Default example (implicit normalization defaults):

```python
from crawl4md import MarkdownFetcher, MarkdownPreprocessingConfig

fetcher = MarkdownFetcher(
    config=MarkdownPreprocessingConfig(enabled=True),
    parse_type="markdown",
)
```

### Fetch Markdown From a URL

Use `MarkdownFetcher` if you want to fetch a page and directly receive Markdown.

```python
from crawl4md import MarkdownFetcher, MarkdownPreprocessingConfig

config = MarkdownPreprocessingConfig(enabled=True)
fetcher = MarkdownFetcher(config=config, parse_type="markdown")

markdown = fetcher.fetch_sync("https://example.com")
print(markdown)
```

Async version:

```python
import asyncio

from crawl4md import MarkdownFetcher, MarkdownPreprocessingConfig

config = MarkdownPreprocessingConfig(enabled=True)
fetcher = MarkdownFetcher(config=config, parse_type="markdown")

markdown = asyncio.run(fetcher.fetch("https://example.com"))
print(markdown)
```

### Convert HTML to Markdown

Use `MarkdownConverter` if you already have HTML and only want the conversion step.

```python
from crawl4md import MarkdownConverter, MarkdownPreprocessingConfig

html = "<html><body><h1>Hello</h1><p>World</p></body></html>"

config = MarkdownPreprocessingConfig(enabled=True, ensure_h1=True)
converter = MarkdownConverter(config=config, parse_type="markdown")

markdown = converter.convert_sync(html=html, url="https://example.com")
print(markdown)
```

Async version:

```python
import asyncio

from crawl4md import MarkdownConverter, MarkdownPreprocessingConfig

html = "<html><body><h1>Hello</h1><p>World</p></body></html>"

config = MarkdownPreprocessingConfig(enabled=True, ensure_h1=True)
converter = MarkdownConverter(config=config, parse_type="markdown")

markdown = asyncio.run(
    converter.convert(html=html, url="https://example.com")
)
print(markdown)
```

### Limit Conversion to Part of the HTML

Use `content_selector` to convert only the matching HTML elements before Markdown conversion.

```python
from crawl4md import MarkdownConverter, MarkdownPreprocessingConfig

html = """
<html>
    <body>
        <nav>Navigation</nav>
        <main><h1>Hello</h1><p>World</p></main>
    </body>
</html>
"""

converter = MarkdownConverter(
    config=MarkdownPreprocessingConfig(enabled=True),
    parse_type="markdown",
    content_selector="main",
)

markdown = converter.convert_sync(html=html, url="https://example.com")
print(markdown)
```

The same option is available on `MarkdownFetcher`.

### Use a Specific Parser Backend

Use `MarkdownFetcherKreuzbergDev` or `MarkdownConverterKreuzbergDev` when you want the recommended backend explicitly.

Use `MarkdownFetcherCrawl4AI` or `MarkdownConverterCrawl4AI` when you need `crawl4ai`, for example `parse_type="markdown-fit"`:

```python
from crawl4md import MarkdownFetcherCrawl4AI, MarkdownPreprocessingConfig

fetcher = MarkdownFetcherCrawl4AI(
    config=MarkdownPreprocessingConfig(enabled=True),
    parse_type="markdown-fit",
)

markdown = fetcher.fetch_sync("https://example.com")
print(markdown)
```

---

## Output Structure

Markdown files are stored deterministically based on the URL path:

```bash
crawled/<project>/<url-path>.md
```

Example:

```bash
crawled/planes/wiki/Boeing_707.md
```

Rules:

* Domain is ignored
* URL path is preserved
* `/` → `index.md`
* Query parameters are ignored

---

## Example Output

```bash
1/2 Crawl https://de.wikipedia.org/wiki/Boeing_707
- Fetching ... done
- Processing ... done
- Writing crawled/planes/wiki/Boeing_707.md ... done
```

---

## Use Cases
* RAG data ingestion
* Website snapshotting
* Knowledge base generation
* Offline documentation

---

## Project Structure

```bash
src/crawl4md/
├─ cli.py
├─ config.py
├─ sitemap.py
├─ crawler.py
├─ paths.py
└─ writer.py
```

---

## Notes

* No recursive crawling (by design)
* No hidden caching or transformations
* Focus on clean Markdown output only

---

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.

### Authors

* Björn Hempel <bjoern@hempel.li> - _Initial work_ - [https://github.com/bjoern-hempel](https://github.com/bjoern-hempel)

---

## Parser Backends

`crawl4md` is designed as a small orchestration layer around exchangeable HTML-to-Markdown backends.

It currently integrates the excellent [`crawl4ai`](https://github.com/unclecode/crawl4ai) project and [`html-to-markdown`](https://github.com/kreuzberg-dev/html-to-markdown) by kreuzberg-dev. Both libraries solve the conversion problem from different angles; `crawl4md` keeps the project workflow, preprocessing, path handling, and writing logic independent from the selected parser.

Why use `crawl4md` around these parser backends:

- project-based batch crawling via `crawl.yml`
- support for both page lists and sitemap-driven crawls
- deterministic output paths for generated Markdown files
- optional Markdown cleanup rules for better downstream text quality
- a small CLI and Python API focused on URL or HTML to Markdown workflows
- clearer separation between fetching, conversion, preprocessing, and writing

In short: the parser backend can change, while `crawl4md` keeps the surrounding crawl configuration, deterministic output, and Markdown cleanup workflow stable.

## Troubleshooting

### Wikipedia returns `403 Forbidden`

Some websites, especially Wikimedia/Wikipedia, may block direct HTTP requests depending on the Python runtime, TLS fingerprint, request frequency, IP reputation, or server-side bot detection.

Example error:

```text
httpx.HTTPStatusError: Client error '403 Forbidden'
Please respect our robot policy ...
```

This is not necessarily a `crawl4md` bug. The same request may work in one Python environment and fail in another.

Known workaround:

```bash
uv python install 3.14.0
uv venv --python 3.14.0
uv sync
```

Then run again:

```
uv run crawl <profile>
```

If the problem persists:

* reduce request frequency
* avoid repeated crawling of the same Wikimedia pages
* use a proper User-Agent
* respect Wikimedia's robot policy
* retry later
