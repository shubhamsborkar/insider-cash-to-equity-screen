#!/bin/bash
cd /Users/shubhamborkar/Obsidian/Vault/output/insider-elections
UA="Shubham Borkar Research shubhamsborkar@gmail.com"
mkdir -p raw
ok=0; fail=0
while IFS=$'\t' read -r adsh fname cik; do
  out="raw/${adsh}.xml"
  if [ -s "$out" ] && grep -q "</ownershipDocument>" "$out" 2>/dev/null; then ok=$((ok+1)); continue; fi
  nodash="${adsh//-/}"
  url="https://www.sec.gov/Archives/edgar/data/${cik}/${nodash}/${fname}"
  tries=0
  while [ $tries -lt 4 ]; do
    curl -sL --max-time 30 -H "User-Agent: $UA" "$url" -o "$out"
    if grep -q "</ownershipDocument>" "$out" 2>/dev/null; then break; fi
    tries=$((tries+1)); sleep $((tries*3))
  done
  if grep -q "</ownershipDocument>" "$out" 2>/dev/null; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $adsh"; fi
  sleep 0.4
done < worklist.tsv
echo "DONE ok=$ok fail=$fail"
