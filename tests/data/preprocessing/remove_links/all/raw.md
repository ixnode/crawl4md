# Combined remove_links Cases

This fixture combines key `remove_links` variants in a single file:

- `anchor:` (remove by target/URL)
- `text:` (remove by visible link text)
- `unwrap:*` (convert links to plain visible text)
- known artifact cases from Wikipedia-style markup

## 1. Anchor: bodyContent

This link should be removed completely.

[Zum Inhalt springen](#bodyContent)

## 2. Text + Anchor in one line

- `custom` should be removed by `anchor:#custom-link`.
- `Remove me` should be removed by `text:Remove me`.
- `keep` should remain and be converted to plain text by `unwrap:*`.

Text [custom](#custom-link) [keep](#other-link) [Remove me](#remove-link)

## 3. Unwrap regular links

Both links should keep their visible text, but lose URL wrappers.

[Boeing](https://de.wikipedia.org/wiki/Boeing "Boeing") und [Air India](https://de.wikipedia.org/wiki/Air_India "Air India")

## 4. Anchor: cite_note

Cite-note link should be removed.

[[17]](#cite_note-17)

## 5. Anchor: Citation_needed (bracketed emphasis)

This case should produce the marker `[**]`.

[*[citation needed](/wiki/Wikipedia:Citation_needed "Wikipedia:Citation needed")*]

## 6. Anchor: Verifiability inside a table cell

This case covers marker/artifact normalization in table rows.

| Name | Value |
|------|-------|
| Cruise speed*[better source needed](/wiki/Wikipedia:Verifiability#Questionable_sources "Wikipedia:Verifiability")* | value |

## 7. Riyadh combined case

Link text is kept through `unwrap:*`, citation marker is removed/normalized.

[Riyadh](/wiki/Riyadh "Riyadh").[*[citation needed](/wiki/Wikipedia:Citation_needed "Wikipedia:Citation needed")*]

## 8. Wikipedia edit-link pair in one bracket

Both edit links should be removed by `anchor:veaction=edit` and `anchor:action=edit`.
After removal, the orphan separator should not remain.

[[Bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&veaction=edit&section=15 "Abschnitt bearbeiten: 707-020 (720)") | [Quelltext bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&action=edit&section=15 "Quellcode des Abschnitts bearbeiten: 707-020 (720)")]

## 9. Left edit-link fragment with trailing separator

This fragment ends with a trailing `|` and has only the `veaction` edit link.
The link should be removed, and no orphan separator should survive.

[[Bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&veaction=edit&section=15 "Abschnitt bearbeiten: 707-020 (720)") |

## 10. Right edit-link fragment with leading separator

This fragment starts with a leading `|` and has only the `action` edit link.
The link should be removed. Standalone orphan `|` lines should be removed as well.

| [Quelltext bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&action=edit&section=15 "Quellcode des Abschnitts bearbeiten: 707-020 (720)")]

## 11. Multiline edit-link pair in one bracket

This case uses a multiline visible text in the second edit link (`Quelltext` line break `bearbeiten`).
Both edit links should still be removed by the configured anchor rules.

[[Bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&veaction=edit&section=15 "Abschnitt bearbeiten: 707-020 (720)") | [Quelltext
  bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&action=edit&section=15 "Quellcode des Abschnitts bearbeiten: 707-020 (720)")]

## 12. Unwrap with single-quoted title

This case shows that an inline link with a single-quoted title is unwrapped to plain text.

[Air India](https://de.wikipedia.org/wiki/Air_India 'Air India')

## 13. Regex-style unwrap example

This section documents the regex-style unwrap scenario for visible text matching.
Within this combined fixture, `unwrap:*` is active, so both links are unwrapped.

[Boeing](https://de.wikipedia.org/wiki/Boeing) und [Air India](https://de.wikipedia.org/wiki/Air_India "Air India")

## 14. Featured badge image link

This case adds the Wikipedia featured-article badge as a linked image.
With `anchor:#[Vv]orlage_[Ll]esenswert`, the whole construct should be removed.

[![Dies ist ein als lesenswert ausgezeichneter Artikel.](https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Qsicon_lesenswert.svg/20px-Qsicon_lesenswert.svg.png)](#Vorlage_Lesenswert "Dies ist ein als lesenswert ausgezeichneter Artikel.")
[Dies ist ein als lesenswert ausgezeichneter Artikel.](#Vorlage_Lesenswert "Dies ist ein als lesenswert ausgezeichneter Artikel.")
