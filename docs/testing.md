# Testing

Reliable, deterministic output is a core goal of `crawl4md`.  
Before merging changes, run the relevant checks to ensure behavior stays stable.

## Recommended Workflow

1. Run a focused check while implementing (`check-preprocessing remove_lines`, etc.).
2. Run a group check (`check-preprocessing`, `check-profile`, `check-pipeline`, ...).
3. Run the full suite (`check`) before finalizing changes.

## Test Commands Overview

| Command | Scope | Parameter(s) | What it validates |
| --- | --- | --- | --- |
| `uv run check` | Full project | none | Runs all project checks (converter, profile, pipeline, preprocessing, language, ruff). |
| `uv run check-markdown-converter` | Converter fixture suite | optional `group`, optional `--update` | End-to-end HTML → Markdown fixture validation under `tests/data/markdown_converter`. |
| `uv run check-markdown-converter <group>` | Converter subgroup | `group` path (e.g. `wikipedia`, `preprocessing`) | Runs only fixture sessions inside one fixture subtree. |
| `uv run check-markdown-converter <group> --update` | Converter subgroup + fixture update | `group`, `--update` | Rewrites expected `data.md` outputs for that group to current converter output. |
| `uv run check-profile` | Profile merging tests | none | Validates profile defaults, overrides, and unknown-profile error handling. |
| `uv run check-pipeline` | Preprocessing pipeline orchestration | none | Verifies rule ordering and enabled/disabled pipeline behavior. |
| `uv run check-preprocessing` | All preprocessing rule groups | none | Runs grouped rule tests (`ensure_h1`, `remove_links`, `normalize_tables`, etc.). |
| `uv run check-preprocessing <rule>` | Single preprocessing rule group | `rule` name (e.g. `remove_lines`) | Runs only one rule test module (`tests/preprocessing/test_<rule>.py`). |
| `uv run check-language` | HTML language detection | none | Validates metadata-based language extraction against `tests/data/html/*`. |
| `uv run check-ruff` | Linting | none | Runs static checks (`ruff check`). |

## Practical Examples

Run one preprocessing rule while iterating:

```bash
uv run check-preprocessing remove_lines
uv run check-preprocessing normalize_tables
```

Run all preprocessing checks before touching shared logic:

```bash
uv run check-preprocessing
```

Run only Wikipedia converter fixtures:

```bash
uv run check-markdown-converter wikipedia
```

Update expected markdown snapshots after intentional converter changes:

```bash
uv run check-markdown-converter wikipedia --update
```

Final verification before commit:

```bash
uv run check
```

## Why this matters

- Prevents accidental regressions in Markdown output.
- Keeps profile defaults and overrides trustworthy.
- Ensures parser and preprocessing changes remain deterministic.
- Makes refactoring safer by validating behavior instead of assumptions.
