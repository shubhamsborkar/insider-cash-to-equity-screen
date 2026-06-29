#!/usr/bin/env python3
import json, csv, re
elective=json.load(open("elective.json"))
parsed={r["adsh"]:r for r in json.load(open("parsed.json"))}

# prices
px={}
for row in csv.DictReader(open("prices.csv")):
    try: px[row["ticker"]]={"cur":float(row["current"]),"c90":float(row["close90"]),"pct":float(row["pct90"])}
    except: px[row["ticker"]]=None

# worklist for cik/link
cik={}
for line in open("worklist.tsv"):
    a,f,c=line.rstrip("\n").split("\t"); cik[a]=c.lstrip("0")

ELECT=re.compile(r"in lieu of|elect|in the form of stock|paid in stock",re.I)
def pick_footnote(adsh):
    fs=parsed[adsh]["footnotes"]
    best=None
    for fid,t in fs.items():
        if ELECT.search(t):
            # prefer ones explicitly about cash/fees/salary
            score=("in lieu of cash" in t.lower())*3+("in lieu of director fees" in t.lower())*3+("retainer" in t.lower())+("salary" in t.lower())*2
            if best is None or score>best[0]: best=(score,t)
    return (best[1] if best else (next(iter(fs.values())) if fs else "")).replace("\n"," ").strip()

# --- inject CW (regex missed: 'in the form of stock' not 'in lieu of cash') ---
cw_specs=[
 {"adsh":"0001628280-26-039795","ticker":"CW","issuer":"CURTISS WRIGHT CORP","owner":"Wallace Peter C","role":"Director","title":None,
  "dates":["2026-06-01"],"elective_shares":221.0,"elective_value_filed":221*719.99,"value_known":True,"grant_prices":[719.99],"rows":[]},
 {"adsh":"0001628280-26-039799","ticker":"CW","issuer":"CURTISS WRIGHT CORP","owner":"MINOR GLENDA J","role":"Director","title":None,
  "dates":["2026-05-29"],"elective_shares":20.0,"elective_value_filed":20*747.61,"value_known":True,"grant_prices":[747.61],"rows":[]},
]
elective+=cw_specs

# --- fix SLVM: elective portion is 6,331 RSUs (not full 10,207) ---
for e in elective:
    if e["ticker"]=="SLVM":
        e["elective_shares"]=6331.0; e["elective_value_filed"]=round(6331*38.70,2); e["note"]="filing total 10,207 RSUs; 6,331 are the elected-in-lieu-of-cash portion (3,876 are routine time-based)"

# value each filing
for e in elective:
    p=px.get(e["ticker"])
    if e["value_known"] and e["elective_value_filed"]>0:
        e["value"]=round(e["elective_value_filed"],0); e["basis"]="grant price (filed)"
    elif p:
        e["value"]=round(e["elective_shares"]*p["cur"],0); e["basis"]="current price x elective shares"
    else:
        e["value"]=None; e["basis"]="no price"
    e["pct90"]=p["pct"] if p else None
    e["cur"]=p["cur"] if p else None
    e["footnote"]=pick_footnote(e["adsh"])
    c=cik.get(e["adsh"],"")
    nod=e["adsh"].replace("-","")
    e["link"]=f"https://www.sec.gov/Archives/edgar/data/{c}/{nod}/{e['adsh']}-index.htm"

# group by ticker
from collections import defaultdict
byt=defaultdict(list)
for e in elective: byt[e["ticker"]].append(e)

summary=[]
for tk,g in byt.items():
    ins=sorted({e["owner"] for e in g})
    alld=sorted({d for e in g for d in e["dates"]})
    tot=sum(e["value"] for e in g if e["value"] is not None)
    n=len(ins)
    if n>=3 and len(alld)==1: kind="BOARD SWEEP"
    elif n>=3 and len(alld)<=2 and tk in ("ADSK","INKT"): kind="BOARD SWEEP (date spread)"
    elif n>=2 and len(alld)>=2: kind="CLUSTER (diff days)"
    elif n>=3: kind="BOARD SWEEP"
    else: kind="single/small"
    summary.append({"ticker":tk,"issuer":g[0]["issuer"],"insiders":n,"dates":alld,
        "total_value":tot,"pct90":g[0]["pct90"],"kind":kind})

summary.sort(key=lambda s:-(s["total_value"] or 0))
json.dump(elective,open("survivors_full.json","w"),indent=1)

# survivors.csv (per insider)
with open("survivors.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["ticker","company","insider","role","elective_shares","est_value_usd","value_basis","txn_date","group_type","pct_90d","open_market_buy","election_footnote","edgar_link","accession"])
    for s in summary:
        g=byt[s["ticker"]]
        for e in sorted(g,key=lambda x:-(x["value"] or 0)):
            w.writerow([e["ticker"],e["issuer"],e["owner"],e["role"],round(e["elective_shares"],1),
                int(e["value"]) if e["value"] is not None else "NA",e["basis"],
                ";".join(e["dates"]),s["kind"],e["pct90"],"No",
                e["footnote"],e["link"],e["adsh"]])

print(f"{'TICKER':6} {'INS':>3} {'TOTAL$':>12} {'90d%':>7}  KIND  DATES")
for s in summary:
    print(f"{s['ticker']:6} {s['insiders']:>3} {('$'+format(int(s['total_value']),',')) if s['total_value'] else 'NA':>12} {str(s['pct90'])+'%':>7}  {s['kind']:<24} {','.join(s['dates'])}")
print("\nfilings:",len(elective)," tickers:",len(byt))
