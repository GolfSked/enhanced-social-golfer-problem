"""Rank current four-round explorer and curated schedules; preserve mapping evidence."""
import sys,json,re,csv,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from rank_explorer_players import rank_entry
from esgp_v2 import validate
out=Path(__file__).resolve().parent
path=ROOT/'web/explorer-sources/four-round.html';s=path.read_text();match=re.search(r'const data=(.*?);\nconst np=',s,re.S);data=json.loads(match[1]);mappings={}
records=json.loads((ROOT/'solutions/optimal-4-rounds/validation.json').read_text())
for n,entry in data.items():
 ranked,mapping=rank_entry(entry);data[n]=ranked;mappings[n]=mapping
 assert validate(entry['rounds'],int(n),4)==validate(ranked['rounds'],int(n),4)
 target=ROOT/f'solutions/optimal-4-rounds/n{n}_sol.csv'
 with target.open('w') as f:
  w=csv.writer(f,lineterminator='\n')
  for r,groups in enumerate(ranked['rounds'],1):
   for g,ps in enumerate(groups,1):w.writerow([r,g,*sorted(ps)])
 copy=out/f'four-round-n{n}.csv';copy.write_text(target.read_text())
 record=next(x for x in records if x['players']==int(n));record.update(source=str(copy.relative_to(ROOT)),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),numbering='descending distinct positions, then previous player ID',old_to_new_player_numbers=mapping)
 # Keep the original optimality evidence, update the selected source and tables.
 def tee(g):return f'10:{g*7:02d}'
 summary=[f'# {n} players — optimal fairness schedule','',f"Minimum distinct tee slots: **{ranked['minimum']}**. Total spread: **{ranked['total']}**. Four rounds; no repeated partners.",'','Player numbers are ordered by descending distinct tee-position count, with previous player ID breaking ties. Names follow roster order.','', '| Group | Tee time | Round 1 players | Round 2 players | Round 3 players | Round 4 players |','|---:|---|---|---|---|---|']
 for g in range(len(ranked['rounds'][0])):summary.append(f'| {g+1} | {tee(g)} | '+' | '.join(', '.join(map(str,sorted(rd[g]))) for rd in ranked['rounds'])+' |')
 summary+=['','| Player | Round 1 | Round 2 | Round 3 | Round 4 | Distinct slots | Three-player rounds | Four-player rounds |','|---:|---|---|---|---|---:|---:|---:|']
 for p,gs in ranked['groups'].items():
  fours=sum(len(ranked['rounds'][r][g])==4 for r,g in enumerate(gs));summary.append(f'| {p} | '+' | '.join(tee(g) for g in gs)+f' | {len(set(gs))} | {4-fours} | {fours} |')
 summary+=['',f'Selected source: [{copy.relative_to(ROOT)}](../../{copy.relative_to(ROOT)}).',f"Original minimum/total optimality evidence: [{record['proof']}](../../{record['proof']}).",'The original evidence proves the first two priorities; see [third-priority results and numbering audit](../../runs/tertiary_fairness_20261019/README.md).','']
 target.with_name(f'n{n}_tee_times.md').write_text('\n'.join(summary))
path.write_text(s[:match.start(1)]+json.dumps(data,separators=(',',':'))+s[match.end(1):])
(ROOT/'solutions/optimal-4-rounds/validation.json').write_text(json.dumps(records,indent=2)+'\n')
(out/'four-round-player-mappings.json').write_text(json.dumps(mappings,indent=2)+'\n')
