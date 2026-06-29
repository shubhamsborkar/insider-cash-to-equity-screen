# Manual checks — human verification, NOT machine-generated

> Everything in this file was verified **by hand**, by opening primary SEC filings
> directly. It did **not** come out of the automated screen. The machine run produced
> the survivor data, the footnote extracts, and the 90-day price numbers; the items
> below are the human steps the screen could not do. They are recorded here so the repo
> is honest and complete.

---

## 1. Agenus (AGEN) — the proxy cash-conservation context  ·  MANUAL FILING REVIEW

**What the machine run found (in `data/survivors.csv`):** two Form 4 filings by Garo H.
Armen, Chairman & CEO, taking salary in stock in lieu of cash.
- Accession `0001193125-26-252375` (pay period ending 2026-05-29)
- Accession `0001193125-26-271889` (pay period ending 2026-06-12)
- Footnote, verbatim: *"At his request and with the approval of the Agenus Inc.
  Compensation Committee, Garo H. Armen's salary is being paid in stock, in lieu of cash."*

**The human step the screen could not do — reading the proxy.** I opened the company's
proxy statement by hand and found that Agenus lists **equity-in-lieu-of-cash compensation
as an explicit cash-conservation lever**, presented alongside a **going-concern**
disclosure. The proxy's executive summary states the company leaned on equity to
*"minimize cash expense"* and cut net cash burn from **over $200M to about $50M**.

- Proxy source (primary filing):
  https://www.sec.gov/Archives/edgar/data/0001098972/000119312526164318/agen-20260420.htm

**Why it matters:** it reframes the signal. Armen's election is genuine and voluntary
("at his request"), but the same primary record shows the company is using equity comp to
preserve cash under going-concern pressure. A reader should weigh the conviction read
against the cash-conservation read — both trace to primary filings.

*Verified manually against the primary proxy filing above. Not produced by the screen.*

---

## 2. Enviri (NVRI) — the cash-settled "phantom trap" example  ·  MANUALLY CONFIRMED

The verified example of the trap the filter is designed to kill: a unit that files as an
**acquisition** but settles in **cash**, never in shares.

- Accession `0002104052-26-000103`
- Insider: John S. Quinn (non-employee Director)
- Security title, as filed: **"Deferred Stock Unit (Cash)"**
- Footnote, verbatim: *"Deferred Stock Units represent deferred cash compensation … Each
  Deferred Stock Unit, following vesting, represents **the right to receive the value, in
  cash, of 1 share** of the Issuer's common stock …"*

Confirmed by hand against the raw filing (`filings/0002104052-26-000103.xml`). Because it
pays in cash, it is economically neutral and was correctly **excluded** from the genuine
election list. This is the example to show a reader who asks "how do you know a unit is
real stock and not a cash IOU?"

*Verified manually against the raw Form 4 XML. Not a description — the quote and the
"(Cash)" security label are in the filing.*

---

## 3. Provenance — machine run vs. manual verification

The credibility of this project is that **every claim retraces to a primary SEC filing.**
Here is exactly which is which.

### Traces to the machine run (automated, reproducible)
| Item | Where |
|---|---|
| The 160-filing candidate set and dedupe | `data/intermediate/all_hits.jsonl`, `dedup.json` |
| The 125 survivors, roles, dates, elected shares | `data/survivors.csv`, `survivors_full.json` |
| Verbatim election footnotes | extracted into `data/survivors_full.json`, `intermediate/digest.txt` |
| 90-day price change figures | `data/prices.csv` (Yahoo chart endpoint) |
| Board-sweep vs. individual classification | `data/board-sweeps.csv`, `individual-elections.csv` |
| "Zero open-market (code-P) buys in the set" | derived from parsed XML, `data/intermediate/parsed.json` |

### Verified manually by opening primary filings (the human step)
| Item | Primary source |
|---|---|
| Agenus proxy lists equity-in-lieu-of-cash as a cash-conservation lever | proxy `agen-20260420.htm` (link above) |
| Agenus going-concern flag; burn cut from >$200M to ~$50M | same proxy, executive summary |
| Enviri security titled "Deferred Stock Unit (Cash)"; pays "value, in cash" | Form 4 accession `0002104052-26-000103` |

### Deliberately omitted (could not be traced to a filing)
- **Market capitalization** — not in the filings and not retrievable from a free,
  no-auth, citable source. Left out rather than sourced from memory or a search snippet.

> Rule for the whole repo: every figure and every quote points to a primary SEC filing
> with its accession number or EDGAR link. If it can't be traced, it isn't here.
