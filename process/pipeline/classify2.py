#!/usr/bin/env python3
import json, re
rows=json.load(open("parsed.json"))
dates=json.load(open("dates.json"))

# Tickers dropped after reading footnotes, with reason
DROP={
 "EQR":"elects equity AWARD VEHICLE (RUs) for annual LTI grant, not in lieu of cash",
 "COP":"'elected' = deferral payment schedule + 16a-11 dividend-equiv units; no cash->equity election",
 "CECO":"merger-consideration stock election (Thermon/CECO merger), not board comp",
 "DTSS":"company paid comp/accrued salary in stock (no personal election); mixed w/ IP-purchase & merger conversion",
 "NVRI":"election settles as Deferred Stock Unit (Cash) -> 'value, in cash' = cash-settled",
 "VAC":"election is to reinvest DIVIDENDS into share awards, not fees/salary into stock",
 "OHI":"elects Profits Interest Units as LTI award vehicle, not in lieu of cash fees",
 "NIQ":"plain RSU grant; 'elected to receive upon redemption' = indirect->direct holding, not cash election",
 "MOS":"settlement-form split of an RSU award; director elected 35-50% as CASH (opposite of conviction)",
 "HL":"elects direct-vs-trust delivery of a director stock award; no in-lieu-of-cash language",
 "BGS":"elected board fee in OPTIONS (not stock/share-settled units) -> tracked separately",
}

ELECT=[
 r"in lieu of cash",
 r"in lieu of (?:a |the )?(?:director|board)[^.]{0,30}fee",
 r"in lieu of director fees",
 r"in lieu of[^.]{0,30}(?:retainer|salary|fees|compensation)",
 r"in lieu of[^.]{0,15}cash",
 r"salary is being paid in stock",
 r"received in lieu of",
 r"shares?[^.]{0,25}in lieu of cash",
 r"deferred in lieu of cash",
]
# routine (NOT elective) grant language -> exclude such a txn unless it ALSO has elect lang
ROUTINE=[
 r"granted annually", r"annual (?:common stock|equity) grant", r"annual grant of (?:long-term|common)",
 r"time-based restricted", r"annual director compensation\.?\s*$",
]
# per-transaction cash-settled kill
CASHKILL=[r"value, in cash", r"in the form of cash", r"\bphantom\b", r"cash-?settled"]
# option exclusion handled via security text

def hit(pats,t):
    return any(re.search(p,t,re.I) for p in pats)

def truthy(v): return v in ("1","true","True")

out=[]
for r in rows:
    tk=r["ticker"]
    role_dir=any(truthy(o["isDirector"]) for o in r["owners"])
    role_off=any(truthy(o["isOfficer"]) for o in r["owners"])
    owner=r["owners"][0]["name"] if r["owners"] else "?"
    title=r["owners"][0]["title"] if r["owners"] else None
    foots=r["footnotes"]
    if tk in DROP:
        continue
    if not (role_dir or role_off):
        continue
    elective_sh=0.0; elective_val=0.0; val_known=False; prices=set()
    rows_kept=[]
    for t in r["txns"]:
        if t["code"] not in ("A","P") or t["ad"]!="A": continue
        sec=(t["security"] or "")
        if "Option" in sec: continue  # skip option rows
        ftext=" ".join(foots.get(f,"") for f in t["footRefs"]) or " ".join(foots.values())
        if hit(CASHKILL, ftext):  # cash-settled comp
            continue
        is_elect = hit(ELECT, ftext)
        is_routine = hit(ROUTINE, ftext) and not hit(ELECT, ftext)
        if not is_elect or is_routine:
            continue
        try: sh=float(t["shares"]) if t["shares"] else 0
        except: sh=0
        try: pr=float(t["price"]) if t["price"] else 0
        except: pr=0
        elective_sh+=sh
        if pr>0: elective_val+=sh*pr; val_known=True; prices.add(pr)
        rows_kept.append({"sh":sh,"pr":pr,"sec":sec,"code":t["code"]})
    if elective_sh<=0 and not val_known and not rows_kept:
        continue
    out.append({"adsh":r["adsh"],"ticker":tk,"issuer":r["issuer"],"owner":owner,
        "role":"Dir+Off" if (role_dir and role_off) else ("Director" if role_dir else "Officer"),
        "title":title,"dates":dates.get(r["adsh"],[]),
        "elective_shares":round(elective_sh,2),"elective_value_filed":round(elective_val,2),
        "value_known":val_known,"grant_prices":sorted(prices),"rows":rows_kept})

# group
from collections import defaultdict
byt=defaultdict(list)
for o in out: byt[o["ticker"]].append(o)
json.dump(out,open("elective.json","w"),indent=1)
print("kept filings:",len(out)," tickers:",len(byt))
for tk in sorted(byt):
    g=byt[tk]
    alld=sorted({d for o in g for d in o["dates"]})
    n_ins=len({o["owner"] for o in g})
    sweep = (n_ins>=3 and len(alld)==1)
    cluster = (n_ins>=2 and len(alld)>=2)
    tag = "SWEEP" if sweep else ("CLUSTER" if cluster else "")
    tot=sum(o["elective_value_filed"] for o in g)
    print(f"{tk:6s} ins={n_ins} dates={alld} filedVal=${tot:,.0f} {tag}")
