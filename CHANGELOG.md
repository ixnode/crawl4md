# Changelog

All notable changes to this project will be documented in this file.

## [Release]

### Added

* Prefix extracted image text with Figure: "..." in remove_images fixtures
* Localize remove_images figure labels from HTML language with en fallback
* Propagate detected page language through fetch/convert pipeline into all rule apply calls

### Refactored

* Move markdown-converter session group resolution into test suite
* Move internal helper functions to crawl4md.utils.check_helpers
* Move Markdown converter session pydantic models out of tests
* Extract progress printing helper from tests support module
* Extract Markdown converter session loading and HTML normalization helpers
* Extract Markdown converter fetcher/session discovery helpers from tests
* Extract pipeline check cases into helper class without behavior change
* Auto-derive progress checks from helper method list
* Introduce shared ProgressChecksTestCase base for pipeline/profile progress-driven checks
* Inline HTML fetching/normalization into BaseMarkdownFetcher and remove fetch/html.py
* Rename Markdown fetcher modules/classes to HTML fetcher naming and update imports
* Move test progress runner from tests/support into crawl4md.utils and update imports
* Move preprocessing RuleCase/data-provider helpers into crawl4md.utils and update test imports
* Move language label mapping into crawl4md/i18n/labels module
* Move frames module into crawl4md.utils and update check helper imports
* Move check CLI module into crawl4md.commands and update script entry points

### Test

* Migrate crawl4ai content-selector unit checks to session fixtures
* Remove direct unittest main guard from Markdown converter test module
* Replace private _asyncioRunner access with get_running_loop in asyncSetUp

### Style

* Reduce panel title padding in test headers

## [0.1.5] - 2026-05-03

### Added

* Add data-driven Markdown converter tests
* Suppress Crawl4AI output during Markdown conversion
* Add Boeing 707 Wikipedia converter fixture
* Add Boeing 707 markdown-fit converter fixture
* Document Markdown converter fixture conventions
* Add crawl step duration output
* Add group filtering to Markdown converter checks
* Handle missing Markdown converter test groups
* Add list fixture for Markdown preprocessing
* Normalize spacing between Markdown list items
* Add kreuzberg-dev Markdown parser
* Add preprocessing option to normalize Markdown tables
* Split whitespace and linebreak normalization rules
* Add preprocessing option to remove cite links
* Move crawled output to crawled and store docs separately
* Add base classes for markdown converters and fetchers

### Refactored

* Rename Markdown fetcher and converter for Crawl4AI

## [0.1.4] - 2026-05-03

### Fixed

* Suppress crawl4ai SyntaxWarning under Python 3.14

## [0.1.3] - 2026-05-02

### Added

* Add realistic HTTP headers to HtmlFetcher to prevent 403 responses

## [0.1.2] - 2026-05-02

### Added

* Update README for PyPI package usage and clarify batch crawler setup

## [0.1.1] - 2026-05-02

### Added

* Add uv check command for tests and Ruff linting
* Export public Python API and expand README with usage and crawl4ai context

### Refactored

* Split `fetch_markdown` into fetch and convert layers
* Move markdown preprocessing from CLI into convert pipeline
* Refactor markdown fetch/convert into classes and add sync APIs

### Removed

* Crawl4AI Logging

## [0.1.0] - 2026-05-02

### Added

* Initial release
* CLI for crawling single pages and sitemaps
* YAML-based project configuration
* Deterministic Markdown file output
* Support for multiple Markdown extraction modes
* Configurable Markdown preprocessing pipeline
* Automatic cleanup of common wiki and web artifacts
* Automatic removal of reference and appendix sections
* Whitespace and document structure normalization
* Automatic insertion of missing top-level headings
* Clear separation of crawling, preprocessing, and file writing
* Basic test coverage for core Markdown processing
