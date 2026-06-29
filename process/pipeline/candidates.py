#!/usr/bin/env python3
import json
rows=json.load(open("parsed.json"))
def truthy(v): return v in ("1","true","True")

cands=[]
for r in rows:
    role_dir=any(truthy(o["isDirector"]) for o in r["owners"])
    role_off=any(truthy(o["isOfficer"]) for o in r["owners"])
    if not (role_dir or role_off):
        continue
    aq=[t for t in r["txns"] if t["code"] in ("A","P") and t["ad"]=="A"]
    if not aq:
        continue
    # describe acquire txns compactly
    desc=[]
    val=0.0; vk=False; sh_tot=0.0
    for t in aq:
        try:
            sh=float(t["shares"]) if t["shares"] else 0; sh_tot+=sh
            pr=float(t["price"]) if t["price"] else 0
            if pr>0: val+=sh*pr; vk=True
        except: pass
        desc.append(f"{t['code']}/{'D' if t['deriv'] else 'N'} {t['shares']}@{t['price']} '{t['security']}' refs={t['footRefs']}")
    cands.append({
        "adsh":r["adsh"],"ticker":r["ticker"],"issuer":r["issuer"],
        "owner":"; ".join(f"{o['name']}({'D' if truthy(o['isDirector']) else ''}{'O' if truthy(o['isOfficer']) else ''}{(':'+o['title']) if o['title'] else ''})" for o in r["owners"]),
        "acq":desc,"shares":sh_tot,"value":round(val,2),"value_known":vk,
        "footnotes":r["footnotes"]
    })
cands.sort(key=lambda c:(c["ticker"] or "zzz", c["adsh"]))
json.dump(cands,open("candidates.json","w"),indent=1)
print("candidates (role + A/P-acquire):", len(cands))
from collections import Counter
print("by ticker:", dict(Counter(c["ticker"] for c in cands)))
