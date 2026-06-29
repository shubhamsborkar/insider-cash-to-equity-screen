# Discovery: how the candidate set was pulled

## Source
SEC EDGAR full-text search API — `https://efts.sec.gov/LATEST/search-index`
(the JSON backend behind https://efts.sec.gov/LATEST/search-index / the EDGAR FTS UI).

- Form type filter: `forms=4`
- Date window: `startdt=2026-05-30`, `enddt=2026-06-29` (the last 30 days as of the run date, 2026-06-29)
- A descriptive `User-Agent` header was set on every request, and requests were spaced
  to stay under EDGAR's rate limit. (EDGAR returns HTTP 500s when hit too fast or
  concurrently; the run was re-paced to sequential single requests after hitting that.)

## The four election phrases (searched as exact quoted strings)
1. `"in lieu of cash"`
2. `"in lieu of director fees"`
3. `"shares in lieu of"`
4. `"elected to receive"`

## Raw counts (reproducible)
| phrase | hits |
|---|---|
| "in lieu of cash" | 95 |
| "in lieu of director fees" | 20 |
| "shares in lieu of" | 14 |
| "elected to receive" | 56 |
| **raw total** | **185** |
| **unique accessions (deduped)** | **160** |

The raw API responses are preserved at `data/intermediate/p1.json` … `p4.json`.
The combined, deduped hit list is `data/intermediate/all_hits.jsonl` and
`data/intermediate/dedup.json`.

## Then: read every footnote
All 160 unique filings were downloaded as raw Form 4 XML (`filings/<accession>.xml`)
and parsed (`data/intermediate/parsed.json`). The footnote text of each — not just the
structured transaction fields — was read into a human-readable digest
(`data/intermediate/digest.txt`) and judged against the filter rules in `filter-rules.md`.

> Important scope note: because discovery is keyed on *election* language, the candidate
> set does **not** contain pure phantom-stock filings that never use election wording.
> The cash-settled examples that *were* caught (because they also contained election
> language) are documented in `data/cash-settled-examples.md`.
