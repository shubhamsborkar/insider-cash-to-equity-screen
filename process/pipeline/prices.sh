#!/bin/bash
cd /Users/shubhamborkar/Obsidian/Vault/output/insider-elections
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Research shubhamsborkar@gmail.com"
T=(AAP ADSK AGEN AMBP ARDX BDTX BLDR CAC CAI CROX CSCO CUBI DLX ECG FTAI GD HSTM IHRT IMNN INKT JXN LLY MS NEPH PK PPTA PSTL RSVR RYN SHEN SLVM TMC XELB YOU)
echo "ticker,current,close90,pct90,asof" > prices.csv
for t in "${T[@]}"; do
  r=$(curl -s --max-time 25 -H "User-Agent: $UA" "https://query1.finance.yahoo.com/v8/finance/chart/${t}?range=3mo&interval=1d")
  line=$(echo "$r" | jq -r '
    .chart.result[0] as $c
    | ($c.indicators.quote[0].close | map(select(.!=null))) as $cl
    | [($c.meta.regularMarketPrice // $cl[-1]), $cl[0], $cl[-1], ($c.timestamp[-1])] | @tsv' 2>/dev/null)
  cur=$(echo "$line" | cut -f1); c0=$(echo "$line" | cut -f2); clast=$(echo "$line" | cut -f3); ts=$(echo "$line" | cut -f4)
  if [ -z "$cur" ] || [ "$cur" = "null" ]; then echo "$t,NA,NA,NA,NA"; echo "$t,NA,NA,NA,NA" >> prices.csv; sleep 0.5; continue; fi
  pct=$(awk -v a="$clast" -v b="$c0" 'BEGIN{if(b>0)printf "%.1f",(a-b)/b*100; else print "NA"}')
  printf "%s,%.2f,%.2f,%s,%s\n" "$t" "$cur" "$c0" "$pct" "$ts" | tee -a prices.csv
  sleep 0.5
done
echo "DONE"
