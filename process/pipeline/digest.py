#!/usr/bin/env python3
import json
from collections import defaultdict
cands=json.load(open("candidates.json"))
by=defaultdict(list)
for c in cands: by[c["ticker"]].append(c)
lines=[]
for tk in sorted(by):
    grp=by[tk]
    lines.append(f"\n===== {tk}  ({grp[0]['issuer']})  [{len(grp)} filing(s)] =====")
    for c in grp:
        # date from adsh? use period not available; show adsh
        lines.append(f"  ADSH {c['adsh']} | {c['owner']} | val={c['value'] if c['value_known'] else '?'} sh={c['shares']:.0f}")
        for a in c["acq"]:
            lines.append(f"      ACQ {a}")
        for fid,ft in c["footnotes"].items():
            lines.append(f"      [{fid}] {ft}")
open("digest.txt","w").write("\n".join(lines))
print("wrote digest.txt lines:",len(lines))
