# Markdown Preprocessing

Markdown preprocessing runs after the selected parser has converted HTML into Markdown.

Enable preprocessing with:

```yaml
preprocessing:
    markdown:
        enabled: true
```

If `enabled` is `false`, no Markdown preprocessing rules are applied, even if individual options are set to `true`.

## Options

```yaml
preprocessing:
    markdown:
        enabled: false

        ensure_h1: false
        remove_jump_to_content: false
        remove_wikipedia_featured_badge: false
        remove_wikipedia_edit_links: false
        remove_wikipedia_subtitle: false
        remove_wiki_loves_earth_banner: false
        remove_reference_sections: false
        remove_cite_links: false
        remove_html_comments: false
        normalize_tables: false
        normalize_linebreak: false
        normalize_whitespace: false
```

### `ensure_h1`

Adds a missing top-level `#` heading when the generated Markdown has no H1.

The rule prefers the first HTML `<h1>`, then falls back to the HTML `<title>`, then to the URL path.

### `remove_jump_to_content`

Removes same-page skip links such as:

```markdown
[Zum Inhalt springen](https://de.wikipedia.org/wiki/Boeing_707#bodyContent)
```

### `remove_wikipedia_featured_badge`

Removes Wikipedia top badges for featured or readable articles, for example:

```markdown
[![Dies ist ein als lesenswert ausgezeichneter Artikel.](...)](#Vorlage_Lesenswert "Dies ist ein als lesenswert ausgezeichneter Artikel.")
```

### `remove_wikipedia_edit_links`

Removes Wikipedia section edit links such as:

```markdown
[[Bearbeiten](...) | [Quelltext bearbeiten](...)]
```

### `remove_wikipedia_subtitle`

Removes the German Wikipedia subtitle text:

```markdown
aus Wikipedia, der freien Enzyklopädie
```

### `remove_wiki_loves_earth_banner`

Removes generated Wiki Loves Earth or Wikidata banner links from converted Wikipedia pages.

### `remove_reference_sections`

Removes reference sections and everything after the matching heading.

The headings are configured with `reference_headings`:

```yaml
reference_headings:
    - Einzelnachweise
    - Weblinks
    - Literatur
    - Quellen
    - References
    - External links
    - Bibliography
```

Heading matching is case-insensitive and supports numbered headings and anchor suffixes.

### `remove_cite_links`

Removes inline citation links such as:

```markdown
[[17]](#cite_note-17)
[[10]](#cite_note-10)
```

If there is a leading space before the citation link, that space is removed too.

### `remove_html_comments`

Removes HTML comments from Markdown output:

```markdown
Text <!-- hidden --> more text
```

### `normalize_tables`

Normalizes Markdown tables.

This removes empty table rows such as:

```markdown
| | |
```

It also adjusts rows to the table column count where possible by padding missing cells or trimming extra cells.

### `normalize_linebreak`

Normalizes block-level line breaks.

This rule controls paragraph and block spacing, including:

- collapsing excessive blank lines
- adding spacing around tables and code blocks
- removing blank lines between list items
- splitting adjacent paragraph lines into separate Markdown paragraphs

### `normalize_whitespace`

Normalizes whitespace inside individual lines.

This rule controls inline spacing, including:

- trimming trailing spaces outside code fences
- inserting missing spaces before Markdown links when text touches the link
- inserting missing spaces before opening parentheses outside Markdown link targets

Markdown link targets are protected so URLs such as `Airport_(Film)` are not changed.

## Recommended Wikipedia Setup

For German Wikipedia pages, a typical cleanup setup is:

```yaml
preprocessing:
    markdown:
        enabled: true
        ensure_h1: true
        remove_jump_to_content: true
        remove_wikipedia_featured_badge: true
        remove_wikipedia_edit_links: true
        remove_wikipedia_subtitle: true
        remove_wiki_loves_earth_banner: true
        remove_reference_sections: true
        remove_cite_links: true
        remove_html_comments: true
        normalize_tables: true
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
