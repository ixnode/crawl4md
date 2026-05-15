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
The link should be removed. The current output keeps a standalone `|` line.

| [Quelltext bearbeiten](https://de.wikipedia.org/w/index.php?title=Boeing_707&action=edit&section=15 "Quellcode des Abschnitts bearbeiten: 707-020 (720)")]
