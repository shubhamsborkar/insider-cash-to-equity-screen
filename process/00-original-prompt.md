# The original brief

This is the verbatim request that defined the screen. It is preserved so a reader can
judge the output against what was actually asked for.

---

> I'm hunting for a specific insider signal that doesn't show up on any normal
> insider feed: a director or officer who elected to take their board retainer,
> fees, or salary in stock instead of cash. It's a real choice to own the stock
> over guaranteed money, but it settles as compensation, so it never files as an
> open-market buy. The only trace is a free-text footnote on a Form 4, and the
> commercial vendors strip footnotes out. I want to find these from EDGAR myself.
>
> First, discover. Use SEC EDGAR full-text search (efts.sec.gov) to pull Form 4
> filings from the last 30 days whose footnote text contains election language
> like "in lieu of cash", "in lieu of director fees", "shares in lieu of", or
> "elected to receive". Dedupe by accession number. Set a descriptive User-Agent
> header on every request and stay under EDGAR's rate limit.
>
> Then actually read each one. Fetch the raw Form 4 XML and read the footnote
> text, not just the structured fields. The whole signal lives in the footnote.
>
> Now throw out the fakes. Keep a filing only if all of this is true: the
> transaction code is A or P and the shares were acquired not disposed; it settles
> in actual stock or share-settled units, NOT cash (if the footnote says "payable
> only in cash", "cash-settled", or "phantom", kill it); a footnote explicitly
> says the person chose equity instead of cash; it's not a Rule 10b5-1 automatic
> trade; and the filer is a director or officer. Also drop routine annual board
> grants with no election language, and drop tax-withholding and option-exercise
> rows. When a whole board files the identical election on the same day under a
> standing program, collapse it and flag it as a board sweep.
>
> For everything that survives, pull the current price, market cap, and the
> trailing 90-day price change. Rank by dollar value converted, and surface the
> shape that matters: elective, real common stock or share-settled units, NOT a
> board sweep, meaningful dollar value, and the stock DOWN over the trailing
> window. Also flag anyone who made an actual open-market purchase (code P) in the
> same window, and flag any company where two or more insiders elected on
> DIFFERENT days (a real cluster, not a board sweep).
>
> A cash-to-equity election is softer than an open-market buy. Be skeptical. No
> price targets.

---

A follow-up request asked for genuine cash-settled / phantom examples from the
*excluded* set (see `data/cash-settled-examples.md`), and this packaging request.
