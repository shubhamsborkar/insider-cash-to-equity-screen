# Insider Cash-to-Equity Screen

A reproducible screen that finds a specific insider signal most feeds never show you:
a director or officer electing to take their retainer, fees, or salary in stock
instead of cash. It produces no open-market buy, so it never hits an insider feed.
The only record is a free-text footnote on an SEC Form 4, and commercial vendors
strip footnotes out.

This repo is the full working record behind the Alpha with AI edition
"I Taught Claude Code to Catch the Insider Buy That Never Shows Up on an Insider Feed."
Everything here traces to a primary SEC filing. Nothing is from model memory or a
search snippet.

## What this does

1. Searches SEC EDGAR full-text search for Form 4 filings whose footnotes contain
   genuine election language ("in lieu of cash", "in lieu of director fees",
   "elected to receive").
2. Downloads the raw Form 4 XML for each hit and reads the footnote, because the
   signal lives in the footnote, not in any structured field.
3. Throws out the fakes. This is the actual work. It removes routine board grants,
   whole-board same-day sweeps, dispositions, and the most common trap of all:
   cash-settled "phantom" units that read like equity but pay out in cash.
4. Keeps only genuine, elective, share-settled elections by a director or officer,
   then surfaces the ones that matter most: individual elections into a falling
   stock, the version that costs the insider something to make.

## What the screen found (trailing 30 days)

- ~160 filings discovered
- 125 verified genuine elections
- Of those, the large majority are whole-board sweeps (routine, one corporate
  event each). Only ~24 are genuine individual elections.
- 0 of the 125 were paired with an open-market purchase. There is no hard
  confirmation anywhere in this batch. The signal is soft on its own.

The honest read: this is a tool for generating questions worth chasing, not
answers worth trading. A cash-to-equity election is weaker than an open-market
buy. It points you at a short list of names, then hands you back to your own
judgment.

## Repo structure

- `/process` — how the screen works: the full plain-English prompt, the discovery
  phrases, and the filter rules (inclusion checklist + false-positive controls).
- `/data` — the full survivor list, with genuine individual elections separated
  from board sweeps.
- `/filings` — the raw Form 4 XML, kept as-is so any claim can be checked against
  the original.
- `/verification` — the manual checks done by hand, outside the automated run.
  See below. This is the most important folder.

## Machine vs. human

The point of this project is that the machine does the reading and the human does
the judging. The repo keeps those honest and separate.

The automated run produced the survivor data, the footnotes, and the price
changes. But the decisive forensic steps were done by hand, by opening primary
filings the screen could not interpret:

- The Agenus (AGEN) case. The Form 4s show the CEO electing salary in stock into
  a falling price, which looks like conviction. Opening the company's proxy by
  hand reveals Agenus lists "equity-in-lieu-of-cash compensation" as a way to cut
  cash burn, alongside a going-concern disclosure. The clean signal had a second,
  equally valid reading the footnote could never show. That check is in
  `/verification`.
- The Enviri (NVRI) trap. The security is titled "Deferred Stock Unit (Cash)" and
  the footnote says it pays "the value, in cash, of 1 share." Verified against the
  raw filing as the textbook example of the phantom trap.

Every figure in `/verification` points to a primary filing with its accession
number or EDGAR link.

## Disclaimer

This is research and educational material, not investment advice, and not a
recommendation to buy or sell any security. No price targets. It covers US-listed
securities and reflects personal views only. AI tools were used in the analysis,
and that use is disclosed. Conduct your own due diligence and consult a licensed
advisor before acting. All figures are as-filed and believed accurate as of the
filing dates; amendments may follow.

---

Built with Claude Code, against SEC EDGAR. Part of the Alpha with AI proof series.
