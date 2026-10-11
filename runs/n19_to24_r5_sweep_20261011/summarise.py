"""Audit saved CSVs and derive participation/slot-count upper bounds."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from esgp_v2 import read_schedule,validate
from cp_sat_caseB_v2 import group_distribution
base=Path(__file__).resolve().parent
rows=[]
for n in range(19,25):
    result=json.loads((base/f'run_n{n}/n{n}/result.json').read_text())
    pilot=json.loads((base.parents[0]/f'v2_pilot_20261011/rounds5/n{n}/result.json').read_text())
    sizes=group_distribution(n); triples=sizes.count(3); fours=sizes.count(4)
    low,extra=divmod(5*4*fours,n)
    caps={f:min(5,min(f,fours)+min(5-f,triples)) for f in (low,low+1) if (f==low and n-extra) or (f==low+1 and extra)}
    min_bound=min(caps.values()); total_bound=(n-extra)*caps[low]+(extra*caps[low+1] if extra else 0)
    audit=None
    if result['status'] in ('FEASIBLE','OPTIMAL'):
        audit=validate(read_schedule(base/f'run_n{n}/n{n}/schedule.csv',n,5),n,5)
        assert all(result[k]==audit[k] for k in ('minimum_spread','total_spread','unique_pairs','unmet_pairs'))
    row={'players':n,'group_sizes':sizes,'pilot_score':[pilot['minimum_spread'],pilot['total_spread']], 'new_score':[result.get('minimum_spread'),result.get('total_spread')], 'status':result['status'],'solver_seconds':result.get('solver_seconds'),'solver_objective_bound':result.get('objective_bound'), 'mathematical_minimum_ceiling':min_bound,'mathematical_total_ceiling':total_bound,'individual_ceiling_by_fours_count':caps,'audit':audit}
    row['minimum_proven']=bool(audit and audit['minimum_spread']==min_bound)
    row['total_proven']=bool(result['status']=='OPTIMAL' or (audit and audit['minimum_spread']==min_bound and audit['total_spread']==total_bound))
    gm_dir=base.parent/f'groupmixer_n19_to24_r5_20261011/n{n}'
    if (gm_dir/'audit.json').exists():
        gm_audit=validate(read_schedule(gm_dir/'schedule.csv',n,5),n,5)
        row['groupmixer_audit']=gm_audit
        row['groupmixer_score']=[gm_audit['minimum_spread'],gm_audit['total_spread']]
        row['best_known_score']=max(row['new_score'],row['groupmixer_score'])
        row['best_minimum_proven']=row['best_known_score'][0]==min_bound
    else:
        row['best_known_score']=row['new_score']
        row['best_minimum_proven']=row['minimum_proven']
    rows.append(row)
(base/'comparison.json').write_text(json.dumps(rows,indent=2)+'\n')
lines=['# Five-round sweep: 19–24 players (11 October 2026)','', 'Six sequential local fairness runs, each capped at 120 solver seconds, four workers, seed 101, with the original ten-second pilot CSV as a hint. Prior records were preserved. Each saved CSV was independently validated for attendance, capacities, unique partners and balanced fours participation.','', '| Players | Pilot | Sweep | Status | Minimum ceiling | Total ceiling |','|---|---|---|---|---|---|']
for r in rows:
    lines.append(f"| {r['players']} | {tuple(r['pilot_score'])} | {tuple(r['new_score'])} | {r['status']} | {r['mathematical_minimum_ceiling']} | {r['mathematical_total_ceiling']} |")
lines+=['','## Independent GroupMixer comparison','']
for r in rows:
    if 'groupmixer_score' in r:
        lines.append(f"- n{r['players']}: GroupMixer {tuple(r['groupmixer_score'])}, independently validated from its saved CSV. Best known {tuple(r['best_known_score'])}; minimum {'proven' if r['best_minimum_proven'] else 'unresolved'}, total ceiling {r['mathematical_total_ceiling']}. This result is recorded separately from the local sweep.")
lines+=['','## Mathematical ceilings','','If a player has f four-player appearances in five rounds, their distinct-slot spread cannot exceed min(5, min(f, number of four-player slots) + min(5-f, number of triple slots)). Balanced fours participation determines exactly how many players have each f. The minimum ceiling is the smallest required individual ceiling; the total ceiling sums all individual ceilings. These are upper bounds, not feasibility claims. Matching a ceiling proves that objective component optimal. OPTIMAL also proves the lexicographic solver objective.','','See comparison.json for independent audits and raw solver bounds. Per-count run folders contain source snapshots, configurations, logs, schedules and solver results. No targeted exclusions were run.']
(base/'README.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(rows,indent=2))
