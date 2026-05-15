# Combined remove_links Cases

This fixture combines key `remove_links` variants in a single file:

- `anchor:` (remove by target/URL)
- `text:` (remove by visible link text)
- `unwrap:*` (convert links to plain visible text)
- known artifact cases from Wikipedia-style markup

## 1. Anchor: bodyContent

This link should be removed completely.

## 2. Text + Anchor in one line

- `custom` should be removed by `anchor:#custom-link`.
- `Remove me` should be removed by `text:Remove me`.
- `keep` should remain and be converted to plain text by `unwrap:*`.

Text keep

## 3. Unwrap regular links

Both links should keep their visible text, but lose URL wrappers.

Boeing und Air India

## 4. Anchor: cite_note

Cite-note link should be removed.

## 5. Anchor: Citation_needed (bracketed emphasis)

This case should produce the marker `

## 6. Anchor: Verifiability inside a table cell

This case covers marker/artifact normalization in table rows.

| Name | Value |
|------|-------|
| Cruise speed[**] | value |

## 7. Riyadh combined case

Link text is kept through `unwrap:*`, citation marker is removed/normalized.

Riyadh.[**]
