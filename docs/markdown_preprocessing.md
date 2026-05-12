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
        remove_wikipedia_subtitle: false
        remove_wiki_loves_earth_banner: false
        remove_reference_sections: false
        remove_links: false
        remove_html_comments: false
        normalize_tables: false
        normalize_linebreak: false
        normalize_whitespace: false
```

### `ensure_h1`

Adds a missing top-level `#` heading when the generated Markdown has no H1.

The rule prefers the first HTML `<h1>`, then falls back to the HTML `<title>`, then to the URL path.

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

### `remove_links`

Removes Markdown links whose target or text matches the configured regular expression.

The link target is the value inside the parentheses of a Markdown link:

```markdown
[link text](link-target)
```

By default, `remove_links` checks only `link-target`, not `link text`.

The configured value does not have to match at the beginning. It matches anywhere inside the checked target or text because the rule wraps the pattern with `.*`-like matching around it.

The option accepts `false`, a string, or a list of strings:

```yaml
remove_links: false
```

Keeps all Markdown links unchanged.

```yaml
remove_links: "cite_note"
```

Removes links whose target contains `cite_note`. This is useful for inline Wikipedia citation links:

```markdown
Text [[17]](#cite_note-17) [[10]](#cite_note-10)
```

Becomes:

```markdown
Text
```

The leading space before a removed link is removed too.

The configured string is used as a regular expression. This makes it possible to remove other link groups without adding a new preprocessing option.

Pattern prefixes:

```yaml
remove_links: "#content"
remove_links: "anchor:#content"
remove_links: "text:Zum Inhalt springen"
```

`"#content"` and `"anchor:#content"` both check the link target. `"text:Zum Inhalt springen"` checks the visible link text.

Remove skip-to-content links by target:

```yaml
remove_links: "anchor:#(?:[Bb]ody[Cc]ontent|content|content-start|main|main-content|maincontent)"
```

```markdown
[Zum Inhalt springen](https://de.wikipedia.org/wiki/Boeing_707#bodyContent)

# Boeing 707
```

Becomes:

```markdown
# Boeing 707
```

Remove skip-to-content links by text:

```yaml
remove_links: "text:Zum Inhalt springen"
```

```markdown
[Zum Inhalt springen](#bodyContent) [keep](#bodyContent)
```

Becomes:

```markdown
[keep](#bodyContent)
```

Remove links to a specific anchor prefix:

```yaml
remove_links: "custom-link"
```

```markdown
Text [custom](#custom-link) [keep](#other-link)
```

Becomes:

```markdown
Text [keep](#other-link)
```

Remove links to generated Wikipedia anchors:

```yaml
remove_links: "wiki_[a-z]+"
```

```markdown
Text [one](#wiki_intro) [two](#wiki_history) [keep](#plain)
```

Becomes:

```markdown
Text [keep](#plain)
```

Remove Wikipedia featured/readable article badges:

```yaml
remove_links:
    - "#[Vv]orlage_[Ll]esenswert"
    - "#[Vv]orlage_[Ee]xzellent"
```

```markdown
[![Dies ist ein als lesenswert ausgezeichneter Artikel.](...)](#Vorlage_Lesenswert "Dies ist ein als lesenswert ausgezeichneter Artikel.")

# Boeing 707
```

Becomes:

```markdown
# Boeing 707
```

Remove Wikipedia section edit links:

```yaml
remove_links:
    - "veaction=edit[^)]*section="
    - "action=edit[^)]*section="
```

```markdown
## Geschichte

[[Bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&veaction=edit&section=1) | [Quelltext bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&action=edit&section=1)]

Text
```

Becomes:

```markdown
## Geschichte

Text
```

Remove image links by target:

```yaml
remove_links: "upload\\.wikimedia\\.org"
```

```markdown
Text [![Image](https://upload.wikimedia.org/image.jpg)](https://upload.wikimedia.org/file.jpg)
```

Becomes:

```markdown
Text
```

Remove multiple link variants in one run:

```yaml
remove_links:
    - "cite_note"
    - "custom-link"
    - "upload\\.wikimedia\\.org"
    - "veaction=edit[^)]*section="
    - "action=edit[^)]*section="
```

```markdown
Text [[17]](#cite_note-17) [custom](#custom-link) [image](https://upload.wikimedia.org/file.jpg) [keep](#plain)
```

Becomes:

```markdown
Text [keep](#plain)
```

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
        remove_wikipedia_subtitle: true
        remove_wiki_loves_earth_banner: true
        remove_reference_sections: true
        remove_links:
            - "cite_note"
            - "anchor:#(?:[Bb]ody[Cc]ontent|content|content-start|main|main-content|maincontent)"
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
