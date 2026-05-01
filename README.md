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
