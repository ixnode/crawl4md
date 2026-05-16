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
        remove_lines: false
        remove_blocks: false
        remove_sections: false
        remove_links: false
        remove_images: false
        remove_html_comments: false
        normalize_tables: false
        normalize_linebreak: false
        normalize_whitespace: false
```

### `ensure_h1`

Adds a missing top-level `#` heading when the generated Markdown has no H1.

The rule prefers the first HTML `<h1>`, then falls back to the HTML `<title>`, then to the URL path.

> ### Removal Scope
> 
> Use the removal option that matches the Markdown level you want to remove:
> 
> | Option | Removes | Best for |
> | --- | --- | --- |
> | `remove_lines` | Matching text inside individual lines; empty result lines are removed | Short boilerplate text, labels, subtitles, generated line fragments |
> | `remove_blocks` | Whole blocks separated by blank lines | Banners, promo boxes, generated multi-line link or table blocks |
> | `remove_sections` | A heading and everything after it | References, appendices, web links, literature sections |
> 
> Prefer the narrowest option that fully covers the unwanted content. Use `remove_lines` for small text fragments, `remove_blocks` when a whole paragraph-like block should disappear, and `remove_sections` only when the rest of the document after a heading should be removed.

### `remove_lines`

Removes configured text or regular-expression matches from Markdown lines.

The option accepts `false`, a string, or a list of strings:

```yaml
remove_lines: false
```

Keeps all lines unchanged.

```yaml
remove_lines:
    - "[Aa]us Wikipedia, der freien Enzyklopädie"
    - "[Ff]rom Wikipedia, the free encyclopedia"
```

Removes German and English Wikipedia subtitle text:

```markdown
Boeing 707 aus Wikipedia, der freien Enzyklopädie
```

Becomes:

```markdown
Boeing 707
```

If a line is empty after the configured text was removed, the whole line is removed.

Multiple patterns can be configured:

```yaml
remove_lines:
    - "[Aa]us Wikipedia, der freien Enzyklopädie"
    - "[Ff]rom Wikipedia, the free encyclopedia"
```

### `remove_blocks`

Removes whole Markdown blocks whose content matches the configured regular expression.

Blocks are separated by blank lines. If a block matches, the whole block is removed.

The option accepts `false`, a string, or a list of strings:

```yaml
remove_blocks: false
```

Keeps all blocks unchanged.

```yaml
remove_blocks:
    - "Wikipedia:Wiki_Loves_Earth_"
    - "Wikidata:Events/Coordinate_Me_"
```

Removes generated Wiki Loves Earth or Wikidata banner blocks:

```markdown
[
| Nimm teil am Wikidata-Wettbewerb |
| --- | ](https://www.wikidata.org/wiki/Wikidata:Events/Coordinate_Me_2026)

# Boeing 707
```

Becomes:

```markdown
# Boeing 707
```

### `remove_sections`

Removes configured sections and everything after the matching heading.

The option accepts `false`, a string, or a list of strings:

```yaml
remove_sections: false
```

Keeps all sections unchanged.

```yaml
remove_sections: "Einzelnachweise"
```

Or:

```yaml
remove_sections:
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
remove_links: "unwrap:Air India"
remove_links: "unwrap:*"
```

`"#content"` and `"anchor:#content"` both check the link target. `"text:Zum Inhalt springen"` checks the visible link text.
`"unwrap:Air India"` checks the visible link text and removes only the Markdown link syntax.
`"unwrap:*"` unwraps all remaining Markdown links.

Processing behavior:

1. Image syntax is handled by `remove_images: true`.
2. `remove_links` rules are applied to Markdown links.
3. `anchor:` and `text:` remove the whole matching link, including visible text.
4. `unwrap:` keeps the visible link text and removes the URL and optional title.

`remove_images` removes only Markdown image syntax. If an image is wrapped by a Markdown link, the outer link remains and can be processed later by `remove_links`.

Rules are applied in this order: complete link removals (`anchor:` and `text:`) run first, then `unwrap:` runs on the remaining links. This means a catch-all `unwrap:*` can be placed after specific removal rules:

```yaml
remove_links:
    - "anchor:cite_note"
    - "anchor:#(?:[Bb]ody[Cc]ontent|content|content-start|main|main-content|maincontent)"
    - "anchor:#[Vv]orlage_[Ll]esenswert"
    - "anchor:#[Vv]orlage_[Ee]xzellent"
    - "anchor:&veaction=edit[^)]*section="
    - "anchor:&action=edit[^)]*section="
    - "unwrap:*"
```

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

Unwrap links by visible text:

```yaml
remove_links: "unwrap:Air India"
```

```markdown
[Air India](https://de.wikipedia.org/wiki/Air_India "Air India")
```

Becomes:

```markdown
Air India
```

`unwrap:` accepts regular expressions:

```yaml
remove_links: "unwrap:^Air India$"
```

Supported Markdown link forms:

```markdown
[Text](url)
[Text](url "Title")
[Text](url 'Title')
[Text](url (Title))
```

All become:

```markdown
Text
```

Unwrap multiple links in one line:

```yaml
remove_links:
    - "unwrap:Boeing"
    - "unwrap:Air India"
```

```markdown
[Boeing](https://de.wikipedia.org/wiki/Boeing) und [Air India](https://de.wikipedia.org/wiki/Air_India)
```

Becomes:

```markdown
Boeing und Air India
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
    - "anchor:&veaction=edit[^)]*section="
    - "anchor:&action=edit[^)]*section="
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
    - "anchor:cite_note"
    - "anchor:custom-link"
    - "anchor:upload\\.wikimedia\\.org"
    - "anchor:&veaction=edit[^)]*section="
    - "anchor:&action=edit[^)]*section="
```

```markdown
Text [[17]](#cite_note-17) [custom](#custom-link) [image](https://upload.wikimedia.org/file.jpg) [keep](#plain)
```

Becomes:

```markdown
Text [keep](#plain)
```

### `remove_images`

Removes Markdown image syntax while preserving semantic image text.

The option accepts `false` or `true`:

```yaml
remove_images: false
```

Keeps all Markdown images unchanged.

```yaml
remove_images: true
```

For each Markdown image, the replacement text is selected with this priority:

```text
alt > title > remove
```

Only the image syntax is removed. No prefix such as `Image:` is added.
If an image is wrapped by a Markdown link, the wrapper link target is kept.

Image with alt text:

```markdown
![Boeing 707 Cockpit](cockpit.jpg)
```

Becomes:

```markdown
Boeing 707 Cockpit
```

Image with title but no alt text:

```markdown
![](image.jpg "Cockpit einer Boeing 707")
```

Becomes:

```markdown
Cockpit einer Boeing 707
```

Image without alt text or title:

```markdown
![](image.jpg)
```

Becomes an empty string.

Linked image with alt text:

```markdown
[![Eine Boeing 707 der Air India](https://upload.wikimedia.org/image.jpg)](https://de.wikipedia.org/wiki/Datei:image.jpg "Eine Boeing 707 der Air India")
```

Becomes:

```markdown
[Eine Boeing 707 der Air India](https://de.wikipedia.org/wiki/Datei:image.jpg "Eine Boeing 707 der Air India")
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

For Wikipedia pages, use the built-in project profile:

```yaml
projects:
    planes:
        profile: wikipedia
        type: pages
        sources:
            - https://de.wikipedia.org/wiki/Boeing_707
        crawl:
            parser: kreuzberg-dev
            parse_type: markdown
            content_selector: ".mw-parser-output"
```

The profile provides defaults for `crawl`, `normalization`, and `preprocessing.markdown`. Project-level `crawl`, `normalization`, and `preprocessing` values override profile defaults, so you can adjust individual options without copying the whole profile. Built-in profiles are loaded from `profiles/*.yml` (for example `profiles/wikipedia.yml`).

The `wikipedia` profile currently applies these Markdown preprocessing defaults:

```yaml
preprocessing:
    markdown:
        enabled: true
        ensure_h1: true
        remove_lines:
            - "[Aa]us Wikipedia, der freien Enzyklopädie"
            - "[Ff]rom Wikipedia, the free encyclopedia"
        remove_blocks:
            - "Wikipedia:Wiki_Loves_Earth_"
            - "Wikidata:Events/Coordinate_Me_"
        remove_sections:
            - Einzelnachweise
            - Weblinks
            - Literatur
            - Quellen
            - References
            - External links
            - Bibliography
        remove_links:
            - "anchor:cite_note"
            - "anchor:#(?:[Bb]ody[Cc]ontent|content|content-start|main|main-content|maincontent)"
            - "anchor:#[Vv]orlage_[Ll]esenswert"
            - "anchor:#[Vv]orlage_[Ee]xzellent"
            - "anchor:&veaction=edit[^)]*section="
            - "anchor:&action=edit[^)]*section="
        remove_images: true
        remove_html_comments: true
        normalize_tables: true
        normalize_linebreak: true
        normalize_whitespace: true
```
