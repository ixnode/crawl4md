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
- Clean Markdown output (via `crawl4ai`, markdown-fit mode)
- Deterministic file structure based on URL paths
- YAML-based project configuration
- CLI-first workflow (uv-compatible)
- Clear, readable progress output

---

## Installation

```bash
uv sync
```

---

## Configuration

Create your config file from the example:

```bash
cp crawl.yml.example crawl.yml
```

Example:

```yaml
projects:
    planes:
        type: pages
        sources:
            - https://de.wikipedia.org/wiki/Boeing_707
            - https://de.wikipedia.org/wiki/Boeing_717

    pydantic:
        type: sitemap
        sources:
            - https://pydantic.dev/sitemap.xml
```

---

## Usage

```bash
uv run crawl planes
uv run crawl pydantic
```

---

## Python API

`crawl4md` can also be used as a Python package.

The public classes are:

- `MarkdownFetcher`
- `MarkdownConverter`
- `ParseType`
- `MarkdownPreprocessingConfig`

### Configure Parse Type

Use `ParseType` to control how Markdown is generated:

- `"markdown"`: raw markdown output
- `"markdown-fit"`: cleaned and reduced markdown output via `crawl4ai`

### Configure Preprocessing

Use `MarkdownPreprocessingConfig` to enable optional cleanup steps.

Simple example:

```python
from crawl4md import MarkdownPreprocessingConfig

config = MarkdownPreprocessingConfig(
    enabled=True,
    remove_html_comments=True,
    normalize_whitespace=True,
)
```

### Fetch Markdown From a URL

Use `MarkdownFetcher` if you want to fetch a page and directly receive Markdown.

```python
from crawl4md import MarkdownFetcher, MarkdownPreprocessingConfig

config = MarkdownPreprocessingConfig(enabled=True)
fetcher = MarkdownFetcher(config=config, parse_type="markdown-fit")

markdown = fetcher.fetch_sync("https://example.com")
print(markdown)
```

Async version:

```python
import asyncio

from crawl4md import MarkdownFetcher, MarkdownPreprocessingConfig

config = MarkdownPreprocessingConfig(enabled=True)
fetcher = MarkdownFetcher(config=config, parse_type="markdown-fit")

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

---

## Output Structure

Markdown files are stored deterministically based on the URL path:

```bash
docs/<project>/<url-path>.md
```

Example:

```bash
docs/planes/wiki/Boeing_707.md
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
- Writing docs/planes/wiki/Boeing_707.md ... done
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

## Built on top of crawl4ai

This project builds on the excellent [`crawl4ai`](https://github.com/unclecode/crawl4ai) library and extends it with a simpler batch-oriented workflow for repeatable Markdown exports.

Why use `crawl4md` as a complement to `crawl4ai`:

- project-based batch crawling via `crawl.yml`
- support for both page lists and sitemap-driven crawls
- deterministic output paths for generated Markdown files
- optional Markdown cleanup rules for better downstream text quality
- a small CLI and Python API focused on URL or HTML to Markdown workflows
- clearer separation between fetching, conversion, preprocessing, and writing

In short: `crawl4ai` provides the powerful crawling and Markdown generation foundation, while `crawl4md` adds a lightweight structure around it for batch jobs, cleaner output, and easier integration into documentation or RAG pipelines.
