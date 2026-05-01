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
    parse_type: markdown | markdown-fit

- preprocessing:
    markdown:
        enabled: bool
        remove_reference_sections: bool
        remove_html_comments: bool
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
