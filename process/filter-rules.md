# Filter rules: how a filing survives the screen

The signal being isolated: a **director or officer who chose to take board retainer,
fees, or salary in stock instead of cash.** It settles as compensation, so it never
files as an open-market buy — the only trace is a free-text Form 4 footnote.

Discovery (185 raw hits → 160 unique accessions) is only a net. These rules decide what
is real. Of 160 filings, **125 survived.** Every rule below was applied by reading the
footnote text of each filing, not just the structured fields.

---

## Inclusion checklist — KEEP a filing only if ALL are true

1. **Acquisition, not disposition.** Transaction code is **A** (or P), and the
   acquired/disposed flag is **A** (acquired). Disposition rows are dropped.
2. **Settles in real stock or share-settled units.** Common stock, RSUs, DSUs, LTIP
   units, or profits-interest units that deliver *shares*. (See kill-rule 1 for the
   cash-settled trap.)
3. **An explicit election is stated in a footnote.** The footnote must say the person
   *chose* equity instead of cash — e.g. "elected to receive … in lieu of cash,"
   "in lieu of director fees pursuant to an election by the director," "at his request
   … salary is being paid in stock," or "receive their annual retainer … in the form of
   stock." Wording that merely describes a grant is not enough.
4. **Not a Rule 10b5-1 automatic trade.** Any footnote citing a 10b5-1 plan is dropped.
5. **Filer is a director or officer.** Confirmed from the reporting-owner relationship
   flags in the XML (`isDirector` / `isOfficer`).

If any one fails, the filing is dropped.

---

## False-positive kill rules — DROP even if it looks like an election

**1. Cash-settled / phantom (the most important one).**
If the unit settles in **cash**, it is a deferred paycheck dressed up as equity —
economically neutral, not a vote of confidence in the shares. Kill on footnote language
such as "payable only in cash," "cash-settled," "phantom," "in the form of cash," or
"the right to receive the value, in cash, of 1 share."
- Verified example kept for illustration: **Enviri (NVRI)**, accession
  `0002104052-26-000103`, security literally titled *"Deferred Stock Unit (Cash)."*
  See `verification/manual-checks.md` and `data/cash-settled-examples.md`.
- Do **not** kill on incidental cash language: "redeemable for cash *or shares* at the
  issuer's election" is standard unit language (share-settled), and "any fractional
  share paid in cash" is just rounding. These were checked by hand and kept.

**2. Board sweep (collapse, don't multiply).**
When a whole board files the *identical* election on the *same day* under a standing
program, that is **one routine corporate event, not many signals.** It is kept in the
data but flagged `BOARD SWEEP` and collapsed to a single event in the analysis.
Detected as: ≥3 insiders at one issuer, identical footnote, single transaction date.

**3. Routine annual grants with no election language.**
The standard annual director equity award (often filed in the same Form 4 as the
elective piece) is **not** an election. Only the in-lieu-of-cash portion is counted;
the routine grant rows are excluded from the dollar value.

**4. Tax-withholding and option-exercise rows.** Dropped. (Withholding is a disposition;
option exercises are not the signal.)

**5. Not actually a cash-vs-equity choice.** Dropped on reading the footnote:
   - **Merger-consideration elections** (electing stock vs cash in a deal) — e.g. CECO.
   - **Award-vehicle elections** (choosing RUs/PIUs as the form of an annual LTI grant,
     not in lieu of cash) — e.g. EQR, OHI.
   - **Deferral-schedule elections** (choosing *when* to be paid, not *in what*) — e.g. COP.
   - **Dividend-reinvestment elections** (reinvesting dividends on existing awards) — e.g. VAC.
   - **Delivery-destination elections** (direct vs into trust) — e.g. HL.
   - **Company-imposed stock comp with no personal election** — e.g. DTSS.

**6. Elected into options, not stock.** A real election but the instrument is options
(a leveraged derivative), not stock/share-settled units — tracked separately, out of the
main list. e.g. BGS.

---

## Classification applied to survivors

- **Open-market buy alongside (code P):** flagged where present. **Result: zero** of the
  125 surviving filings carried a code-P purchase. No hard-dollar confirmation exists in
  this set.
- **Multi-date cluster:** ≥2 insiders at one issuer electing on *different* days — a real
  cluster, distinct from a same-day board sweep. Flagged `CLUSTER (diff days)`.
- **The interesting shape:** elective · real stock/units · NOT a board sweep · meaningful
  dollar value · stock **DOWN** over the trailing 90 days. An election into a falling
  stock is the one worth a second look.

## Valuation & price data
- Elective dollar value = elected shares × grant price where the filing states a price,
  else × current price (labeled `value_basis` in `data/survivors.csv`).
- 90-day price change: current vs. ~3-months-prior close from the Yahoo chart endpoint.
- **Market cap was not included:** it was not retrievable from free, no-auth price
  endpoints and is not in the filings, so it is omitted rather than guessed.
