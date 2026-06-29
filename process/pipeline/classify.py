#!/usr/bin/env python3
import json, re
rows=json.load(open("parsed.json"))

# Genuine election-of-equity-instead-of-cash language
ELECT = [
    r"in lieu of (?:cash|the cash|a cash|director|board|annual|quarterly|his|her|their|any cash|all or)",
    r"in lieu of .{0,30}(?:fees|retainer|salary|compensation|bonus)",
    r"shares? .{0,20}in lieu of",
    r"elect(?:ed|s|ion)? to receive",
    r"elect(?:ed|s|ion)? to (?:defer and )?receive",
    r"elected to (?:take|convert)",
    r"in lieu of cash",
    r"received in lieu of",
    r"voluntarily elected",
    r"elected .{0,40}(?:in lieu of|instead of) cash",
]
# Disqualifiers
KILL_CASH = [r"payable only in cash", r"cash-?settled", r"settled in cash", r"settled only in cash",
             r"phantom", r"in cash only", r"payable solely in cash"]
TENB5 = [r"10b5-1", r"10b5‑1", r"rule 10b5"]
FRACTIONAL = re.compile(r"in lieu of fractional", re.I)

def anymatch(pats, text):
    for p in pats:
        if re.search(p, text, re.I): return True
    return False

def truthy(v): return v in ("1","true","True")

out=[]
for r in rows:
    foot_all=" ".join(r.get("footnotes",{}).values())
    foot_clean = FRACTIONAL.sub("", foot_all)  # don't let fractional trigger election
    role_dir = any(truthy(o["isDirector"]) for o in r["owners"])
    role_off = any(truthy(o["isOfficer"]) for o in r["owners"])
    role_other = any(truthy(o.get("isOther")) for o in r["owners"])
    role_ok = role_dir or role_off
    has_elect = anymatch(ELECT, foot_clean)
    kill_cash = anymatch(KILL_CASH, foot_all)
    is_10b5 = anymatch(TENB5, foot_all)
    # qualifying acquire transactions
    aq=[t for t in r["txns"] if (t["code"] in ("A","P")) and t["ad"]=="A"]
    # dollar value from acquire txns
    val=0.0; val_known=False; tot_shares=0.0
    for t in aq:
        try:
            sh=float(t["shares"]) if t["shares"] else 0
            tot_shares+=sh
            pr=float(t["price"]) if t["price"] else 0
            if pr>0: val+=sh*pr; val_known=True
        except: pass
    has_P = any(t["code"]=="P" for t in aq)
    keep = bool(aq) and has_elect and (not kill_cash) and (not is_10b5) and role_ok
    out.append({
        "adsh":r["adsh"],"issuer":r["issuer"],"ticker":r["ticker"],
        "owners":[{"name":o["name"],"dir":truthy(o["isDirector"]),"off":truthy(o["isOfficer"]),"title":o["title"]} for o in r["owners"]],
        "role_ok":role_ok,"has_elect":has_elect,"kill_cash":kill_cash,"is_10b5":is_10b5,
        "n_acquire":len(aq),"codes":sorted({t["code"] for t in r["txns"]}),
        "acquire_codes":sorted({t["code"] for t in aq}),
        "has_P":has_P,"shares":tot_shares,"value":round(val,2),"value_known":val_known,
        "keep":keep,"footnotes":r.get("footnotes",{})
    })

kept=[o for o in out if o["keep"]]
json.dump(out, open("classified.json","w"), indent=1)
json.dump(kept, open("survivors.json","w"), indent=1)
print(f"total={len(out)} kept={len(kept)}")
print("--- reasons dropped ---")
for o in out:
    if not o["keep"]:
        why=[]
        if not o["n_acquire"]: why.append("no A/P-acquire")
        if not o["has_elect"]: why.append("no-election-lang")
        if o["kill_cash"]: why.append("cash/phantom")
        if o["is_10b5"]: why.append("10b5-1")
        if not o["role_ok"]: why.append("not-dir/off")
print("kept tickers:", [ (o["ticker"],o["issuer"]) for o in kept])
