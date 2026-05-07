# AGENTS.md

## Purpose

crawl4md is a minimal CLI tool to crawl web pages or sitemaps and convert them into clean, deterministic Markdown files.

This document defines how contributors and automated agents (LLMs, scripts, CI tools) should interact with and extend the project.

---

## Core Principles

- Keep it simple (no overengineering)
- Deterministic output (same input → same output)
- No hidden behavior or side effects
- Clear separation of concerns:
  - config
  - crawling
  - preprocessing
  - writing
- CLI-first design

---

## Project Structure

src/crawl4md/
- cli.py            → entrypoint (orchestration only)
- config.py         → config models (Pydantic)
- sitemap.py        → sitemap parsing
- crawler.py        → crawl4ai integration
- paths.py          → URL → file path mapping
- writer.py         → file output
- (future) preprocessing.py → markdown cleanup

docs/
- output directory (generated, not versioned except .gitkeep)

crawl.yml.example
- example configuration (must stay in sync with config models)

---

## Responsibilities

### cli.py
- Orchestrates flow
- No business logic
- Reads config, loops URLs, prints output

### crawler.py
- Only responsible for fetching + converting to markdown
- Must not handle filesystem or preprocessing

### preprocessing (future)
- Pure functions: markdown in → markdown out
- No IO, no side effects

### writer.py
- Only writes files
- Must not modify content

---

## Configuration Rules

- All behavior must be configurable via crawl.yml
- crawl.yml is user-specific → never commit
- crawl.yml.example is canonical → always update when config changes

### Config Sections

- type: pages | sitemap
- sources: list[str]

- crawl:
    parser: crawl4ai | kreuzberg-dev
    parse_type: markdown | markdown-fit

- preprocessing:
    markdown:
        enabled: bool
        remove_wikipedia_featured_badge: bool
        remove_wikipedia_edit_links: bool
        remove_reference_sections: bool
        remove_cite_links: bool
        remove_html_comments: bool
        normalize_tables: bool
        normalize_linebreak: bool
        normalize_whitespace: bool
        reference_headings: list[str]

---

## Coding Guidelines

- Python >= 3.11
- Use type hints everywhere
- Prefer explicit over implicit
- No global state (except logging config)
- Keep functions small and focused
- Avoid unnecessary dependencies

---

## Logging & Output

- CLI output must stay minimal and readable
- Avoid noisy logs
- External library logs (e.g. crawl4ai) should be suppressed or reduced

---

## Error Handling

- Errors per URL must not stop the entire run
- Always continue with next URL
- Provide clear summary:
  - success count
  - failure count

---

## File Output Rules

- Output path must be deterministic:
  docs/<project>/<url-path>.md

- URL path rules:
  - "/" → index.md
  - strip leading slash
  - ignore query params

- Always create parent directories

---

## Markdown Converter Fixture Tests

Use the data-driven fixture setup for end-to-end tests of `crawl4md.convert.markdown_converter_crawl4ai.MarkdownConverterCrawl4AI`.

Test sessions live below:

tests/data/markdown_converter/

Each session directory must contain exactly these fixture files:

- config.yml
- data.html
- data.md

The test runner discovers sessions recursively by `config.yml`, so nested grouping is expected and preferred.

### Fixture Layout

Use semantic grouping directories:

- tests/data/markdown_converter/preprocessing/<case>/
- tests/data/markdown_converter/wikipedia/<case>/

For Wikipedia converter fixtures, prefer `markdown-fit` as the default style:

- tests/data/markdown_converter/wikipedia/boeing_707/ → `parse_type: markdown-fit`
- tests/data/markdown_converter/wikipedia/boeing_707_full/ → `parse_type: markdown`

Use the `_full` suffix only for non-fit/full `markdown` output fixtures.

### Fixture Config Shape

Every `config.yml` must use this outer metadata shape:

```yaml
id: "wikipedia_boeing_707"
title: "Wikipedia Boeing 707"
description: "Converts the German Wikipedia Boeing 707 page with markdown-fit and all preprocessing enabled."
config:
    parse_type: markdown-fit
    url: https://de.wikipedia.org/wiki/Boeing_707
    preprocessing:
        markdown:
            enabled: true
            ensure_h1: true
            remove_jump_to_content: true
            remove_wikipedia_featured_badge: false
            remove_wikipedia_edit_links: false
            remove_wikipedia_subtitle: true
            remove_wiki_loves_earth_banner: true
            remove_reference_sections: true
            remove_cite_links: false
            remove_html_comments: true
            normalize_tables: false
            normalize_linebreak: true
            normalize_whitespace: true
            reference_headings:
                - Einzelnachweise
                - Weblinks
                - Literatur
                - Quellen
                - References
                - External links
                - Bibliography
```

The outer `id`, `title`, and `description` are used for test output. The nested `config` object is the actual `MarkdownConverterCrawl4AI` configuration.

### Fixture Expectations

- `data.html` is the exact HTML input for the converter.
- `data.md` is the exact expected output of `converter.convert(html=html, url=config.url)`.
- For new baseline fixtures, generate `data.md` from the current converter once, then commit it as the expected deterministic output.
- For isolated preprocessing tests, set `preprocessing.markdown.enabled: true`, set only the tested flag to `true`, and keep all other preprocessing flags `false`.
- Keep `reference_headings` populated only when the test needs reference-section removal.

### Running Converter Tests

Run only converter fixtures:

```bash
uv run check-markdown-converter
```

Run only one converter fixture group:

```bash
uv run check-markdown-converter preprocessing
uv run check-markdown-converter wikipedia
```

The group argument is resolved relative to `tests/data/markdown_converter/`.

Run the full project check:

```bash
uv run check
```

`uv run check` includes `python -m unittest discover -s tests -v` and `ruff check`, so converter fixtures are included automatically.

---

## Extending the Project

When adding features:

1. First update config models
2. Then update crawl.yml.example
3. Keep backward compatibility (defaults!)
4. Add logic in the correct layer (do not mix concerns)

---

## Anti-Patterns (Avoid)

- Business logic inside cli.py
- Hidden transformations
- Implicit defaults not visible in config
- Mixing crawling and preprocessing
- Writing files outside writer.py

---

## Future Extensions (Planned)

- Markdown preprocessing pipeline
- Frontmatter support
- Parallel crawling
- Retry & rate limiting
- Chunking for RAG
- Database export

---

## Summary

crawl4md is intentionally simple.

Every addition must preserve:
- clarity
- determinism
- separation of concerns
