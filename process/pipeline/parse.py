#!/usr/bin/env python3
import os, glob, json, xml.etree.ElementTree as ET

RAW="raw"
def txt(el, path):
    x = el.find(path)
    return x.text.strip() if x is not None and x.text else None

def get_val(el, path):
    # value wrapped element: path/value
    v = el.find(path+"/value")
    if v is not None and v.text: return v.text.strip()
    x = el.find(path)
    if x is not None and x.text: return x.text.strip()
    return None

rows=[]
for fp in sorted(glob.glob(os.path.join(RAW,"*.xml"))):
    adsh=os.path.basename(fp)[:-4]
    try:
        tree=ET.parse(fp); root=tree.getroot()
    except Exception as e:
        rows.append({"adsh":adsh,"parse_error":str(e)}); continue
    issuer=root.find("issuer")
    issuerName=txt(issuer,"issuerName") if issuer is not None else None
    ticker=txt(issuer,"issuerTradingSymbol") if issuer is not None else None
    # may have multiple reporting owners
    owners=[]
    for ro in root.findall("reportingOwner"):
        name=txt(ro,"reportingOwnerId/rptOwnerName")
        rel=ro.find("reportingOwnerRelationship")
        d=o=tenpct=other=None; title=None
        if rel is not None:
            d=txt(rel,"isDirector"); o=txt(rel,"isOfficer"); tenpct=txt(rel,"isTenPercentOwner"); other=txt(rel,"isOther")
            title=txt(rel,"officerTitle")
        owners.append({"name":name,"isDirector":d,"isOfficer":o,"isTenPct":tenpct,"isOther":other,"title":title})
    # footnotes
    foots={}
    fn=root.find("footnotes")
    if fn is not None:
        for f in fn.findall("footnote"):
            foots[f.get("id")] = (f.text or "").strip()
    def collect(table, tag, deriv=False):
        out=[]
        t=root.find(table)
        if t is None: return out
        for tr in t.findall(tag):
            code=txt(tr,"transactionCoding/transactionCode")
            formtype=txt(tr,"transactionCoding/transactionFormType")
            eq=txt(tr,"transactionCoding/equitySwapInvolved")
            shares=get_val(tr,"transactionAmounts/transactionShares")
            price=get_val(tr,"transactionAmounts/transactionPricePerShare")
            ad=get_val(tr,"transactionAmounts/transactionAcquiredDisposedCode")
            sec=get_val(tr,"securityTitle")
            postshares=get_val(tr,"postTransactionAmounts/sharesOwnedFollowingTransaction")
            # footnote refs anywhere in this transaction
            refs=sorted({fid.get("id") for fid in tr.iter("footnoteId")})
            out.append({"deriv":deriv,"code":code,"formType":formtype,"equitySwap":eq,"shares":shares,
                        "price":price,"ad":ad,"security":sec,"postShares":postshares,"footRefs":refs})
        return out
    txns=collect("nonDerivativeTable","nonDerivativeTransaction",False)
    txns+=collect("derivativeTable","derivativeTransaction",True)
    # holdings (for share-settled units that are holdings, not txns) - capture refs too
    rows.append({"adsh":adsh,"issuer":issuerName,"ticker":ticker,"owners":owners,
                 "txns":txns,"footnotes":foots})

json.dump(rows, open("parsed.json","w"), indent=1)
print("parsed", len(rows), "filings")
print("with parse_error:", sum(1 for r in rows if r.get("parse_error")))
print("total txns:", sum(len(r.get('txns',[])) for r in rows))
