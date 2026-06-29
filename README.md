# Insider cash-to-equity elections — an EDGAR footnote screen

A reproducible screen for a specific insider signal that commercial insider feeds miss:
**a director or officer who elected to take their board retainer, fees, or salary in
stock instead of cash.** It is a real choice to own the shares over guaranteed money, but
it settles as compensation — so it never files as an open-market buy. The only trace is a
free-text footnote on a Form 4, and most vendors strip footnotes out. This repo finds
them directly from SEC EDGAR.

**Window:** Form 4 filings 2026-05-30 → 2026-06-29 (the 30 days ending on the run date).
**Everything here traces to a primary SEC filing** — accession number or EDGAR link. No
figure or quote comes from memory or a search snippet; if it couldn't be traced, it was
left out.

## What the screen did

1. **Discover.** EDGAR full-text search (efts.sec.gov) for Form 4 footnotes containing
   four election phrases → **185 raw hits → 160 unique accessions.** (`process/discovery-phrases.md`)
2. **Read every footnote.** Downloaded all 160 raw Form 4 XML and read the footnote text,
   not just the structured fields — the signal lives in the footnote. (`filings/`)
3. **Filter.** Kept only genuine elections of equity-for-cash by a director/officer that
   settle in real stock/units. Killed cash-settled "phantom" units, routine grants,
   options, withholding, 10b5-1 trades, merger/award-vehicle/deferral/dividend elections.
   (`process/filter-rules.md`)
4. **Result: 125 surviving filings across 35 issuers.** Valued the elective portion,
   pulled 90-day price change, classified board sweeps vs. individual elections vs.
   multi-date clusters. (`data/`)

## Headline findings

- **No open-market confirmation anywhere.** **Zero** of the 125 filings carried a code-P
  open-market purchase. A cash-to-equity election is a soft signal to begin with; with no
  buy alongside, treat it as a mild tell, not a conviction buy.
- **Most volume is routine.** 95 of the 125 rows are **board sweeps** — whole boards
  taking fees in stock under standing programs (ADSK, CUBI, BLDR, GD, MS, …). Collapsed to
  one event each. (`data/board-sweeps.csv`)
- **30 rows are genuine individual elections** across 17 issuers. (`data/individual-elections.csv`)
- **The interesting shape — elective, real stock, not a sweep, stock DOWN over 90 days:**
  | Ticker | Insider | Role | ~Elective $ | 90d | Accession |
  |---|---|---|---|---|---|
  | AGEN | Garo H. Armen | Chair & CEO | $32.5k (2 pds) | −10.6% | `0001193125-26-252375`, `0001193125-26-271889` |
  | IMNN | Tardugno + Lindborg | Officers | $23.4k | −34.2% | `0001437749-26-020037`, `…-019994`, `…-021484`, `…-021444` |
  | BDTX | Behbahani + Raman | Directors | $28.0k | −15.8% | `0001193125-26-277553`, `0002018686-26-000008` |
  | DLX | Cummins + Brown | Directors | $55.0k | −11.3% | `0000027996-26-000104`, `…-000106` |
  | SLVM | David D. Petratis | Director | $245k | −2.0% | `0001299140-26-000010` |
- **Genuine multi-date cluster:** **IMNN** — CEO and Executive Chairman both took base
  salary in stock on two different dates (2026-06-05 and 2026-06-18).
- **The single most interesting election: AGEN / Garo Armen** — Chairman *and* CEO,
  footnote says the swap is "at his request," applied to his salary, into a falling stock.
  **But** a hand review of the Agenus proxy shows the company uses equity-for-cash as a
  going-concern cash-conservation lever — read the conviction signal against that.
  See `verification/manual-checks.md`.

## Repo layout

```
process/        How the screen works — read this to follow or reproduce it.
  00-original-prompt.md    The verbatim brief that defined the screen.
  discovery-phrases.md     The four phrases, the API, the raw counts.
  filter-rules.md          Inclusion checklist + false-positive kill rules, plain English.
  pipeline/                The actual scripts that ran the screen (bash + python).
data/           The results.
  survivors.csv            All 125 surviving filings, one row per insider-filing.
  individual-elections.csv 30 genuine non-sweep elections (incl. the IMNN cluster).
  board-sweeps.csv         95 routine board-sweep rows, kept but separated.
  survivors_full.json      Full per-filing detail: footnotes, values, EDGAR links.
  prices.csv               Current + ~90-day-prior close and % change per ticker.
  run-report.md            The narrative report from the run.
  cash-settled-examples.md Verbatim cash-settled "phantom trap" footnotes (excluded set).
  intermediate/            The full machine trail: raw API responses, parsed XML,
                           dedupe, footnote digest, classification artifacts.
filings/        All 160 raw Form 4 XML, as-pulled, so any claim can be checked
                against the original.
verification/
  manual-checks.md         Human-verified steps (Agenus proxy, Enviri cash-settled,
                           and a machine-vs-manual provenance table). NOT machine output.
```

## How to reproduce
The scripts in `process/pipeline/` ran in this order: `download.sh` (fetch the 160 XML) →
`parse.py` → `candidates.py` → `classify.py` / `classify2.py` → `digest.py` →
`prices.sh` → `assemble.py`. They require `bash`, `python3`, `jq`, and `curl`, and a
descriptive EDGAR `User-Agent`. EDGAR rate-limits aggressively — run requests sequentially.

## Honest limits
- A cash-to-equity election is **softer than an open-market buy**, and none here had a buy
  alongside.
- Small-cap stock-for-salary (AGEN, IMNN, BDTX) can be **cash conservation by the company**
  rather than insider conviction — the Agenus proxy makes that explicit.
- **Market cap is omitted** — not in the filings, not retrievable from a citable free
  source, so not guessed.
- Discovery is keyed on election language, so pure phantom-stock filings that never use
  election wording are out of scope by construction.

*No price targets. No investment advice. Every number retraces to a filing.*
