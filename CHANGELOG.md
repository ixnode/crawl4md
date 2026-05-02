# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Add uv check command for tests and Ruff linting

### Refactored

- Split `fetch_markdown` into fetch and convert layers
- Move markdown preprocessing from CLI into convert pipeline

### Removed

- Crawl4AI Logging

## [0.1.0] - 2026-05-02

### Added

- Initial release
- CLI for crawling single pages and sitemaps
- YAML-based project configuration
- Deterministic Markdown file output
- Support for multiple Markdown extraction modes
- Configurable Markdown preprocessing pipeline
- Automatic cleanup of common wiki and web artifacts
- Automatic removal of reference and appendix sections
- Whitespace and document structure normalization
- Automatic insertion of missing top-level headings
- Clear separation of crawling, preprocessing, and file writing
- Basic test coverage for core Markdown processing
