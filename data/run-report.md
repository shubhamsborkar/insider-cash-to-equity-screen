# Insider "elected stock in lieu of cash" — Form 4 footnote scan

**Window:** 2026-05-30 → 2026-06-29 (last 30 days) · **Generated:** 2026-06-29
**Source:** SEC EDGAR full-text search (efts.sec.gov) + raw Form 4 XML footnotes.

## Method
1. EDGAR full-text search for Form 4s containing: "in lieu of cash", "in lieu of director fees",
   "shares in lieu of", "elected to receive". → 185 hits → **160 unique accessions**.
2. Fetched raw Form 4 XML for all 160; read footnotes (not just structured fields).
3. Kept only: code A/P **acquisitions**, settling in **stock or share-settled units** (not cash/phantom),
   with a footnote showing an **election of equity instead of cash**, by a **director/officer**, not 10b5-1.
   Excluded routine annual grants, options, tax-withholding, cash-settled deferred comp, merger elections,
   dividend-reinvestment elections.
4. Result: **125 surviving filings across 35 issuers.** Valued the **elective portion only**
   (grant price where filed, else current price × elected shares). Pulled 90-day price change (Yahoo chart).

## Honest caveats
- **Zero of the 125 filings carried an open-market purchase (code P).** No "buy alongside" confirmation exists in this set.
- Market cap was **not retrievable** from free no-auth endpoints (Stooq JS-walled, Yahoo quote needs a crumb). Not in the filings either.
- @0-price RSU/DSU filings are valued at **current price** (estimate), labeled as such in the CSV.
- A cash-to-equity election is a **soft** signal — softer than an open-market buy.

## The interesting shape: elective · real stock/units · NOT a board sweep · meaningful $ · stock DOWN 90d

| Ticker | Company | Insider | Role | Elective $ | 90d | Note |
|---|---|---|---|---|---|---|
| AGEN | Agenus | Garo H. Armen | Chair & CEO | ~$32.5k (2 pay pds) | −10.6% | "**At his request**…salary…paid in stock, in lieu of cash." Voluntary, by the top operator. |
| IMNN | Imunon | Tardugno (Exec Chair) + Lindborg (CEO) | Officers | ~$23.4k | −34.2% | Two officers, salary in stock, **two different dates** = genuine cluster. But "granted in lieu of cash" (company-driven). |
| BDTX | Black Diamond Therapeutics | Behbahani + Raman | Directors | ~$28.0k | −15.8% | Both "**elected to receive shares…in lieu of cash compensation**." |
| DLX | Deluxe | Cummins + Brown | Directors | ~$55.0k | −11.3% | RSUs "in lieu of director fees pursuant to an election by the director." |
| SLVM | Sylvamo | David D. Petratis | Director | ~$245k | −2.0% | Largest non-sweep $; "elected…in lieu of a cash retainer" (6,331 of 10,207 RSUs). Barely down. |

## Board sweeps (collapsed — one routine corporate event each, not N signals)
ADSK (9 dirs, −14.6%, ~$927k) · CUBI (11, +19.7%, ~$618k) · PSTL (4, +36.3%, ~$530k) · CROX (3, +60.6%) ·
JXN (3) · TMC (5, −0.5%) · MS (5, +33.9%) · BLDR (9, +10.8%) · GD (8, ~flat) · CSCO (3) · PPTA (5, −19.3%) ·
PK (3) · INKT (5) · CAC (4) · LLY (4) · RSVR (5) · FTAI (3) · SHEN (6).

## Multi-date cluster (≥2 insiders, different days)
- **IMNN** — CEO + Exec Chairman, separate payroll dates (6/5 and 6/18). Recurring salary-in-stock.
- **CW** (Curtiss-Wright) — 2 directors, 5/29 and 6/1, but a standing election program (and one is a deferred 2021 award distribution); not a conviction cluster.

Full per-insider list: **survivors.csv** (125 rows). Open the `edgar_link` column to read each raw filing.
