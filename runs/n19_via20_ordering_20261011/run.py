"""Optimize tee ordering for every deletion from the saved n20/R5 structure."""
import csv, hashlib, itertools, json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from esgp_v2 import read_schedule,validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
source=root.parent/'n19_to24_r5_sweep_20261011/run_n20/n20/schedule.csv'
original=read_schedule(source,20,5)
validate(original,20,5)
(root/'source.csv').write_bytes(source.read_bytes())
(root/'configuration.json').write_text(json.dumps(dict(source=str(source),
 source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
 script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 seconds_per_deletion=60,workers=8,seed=101,
 scope='All tee orderings of these 20 deletion structures; not all n19 structures'),indent=2)+'\n')
results=[]
for removed in range(1,21):
 remaining=[p for p in range(1,21) if p!=removed]
 labels={p:i+1 for i,p in enumerate(remaining)}
 groups=[]
 for round_groups in original:
  trimmed=[[labels[p] for p in g if p!=removed] for g in round_groups]
  groups.append(sorted(trimmed,key=len))
 validate(groups,19,5)
 model=cp_model.CpModel()
 # Triple is tee zero. Each round freely permutes its four fours.
 # A common four-tee permutation preserves score, so round zero is fixed.
 slots=[]
 for r in range(5):
  row=[model.NewIntVar(0,0,f'slot_{r}_0')]+[
   model.NewIntVar(1,4,f'slot_{r}_{g}') for g in range(1,5)]
  model.AddAllDifferent(row)
  if r==0:
   for g in range(5):model.Add(row[g]==g)
  slots.append(row)
 spreads=[]
 for p in range(1,20):
  positions=[slots[r][next(g for g,members in enumerate(groups[r]) if p in members)] for r in range(5)]
  used=[]
  for tee in range(5):
   occurrences=[]
   for r,pos in enumerate(positions):
    b=model.NewBoolVar(f'eq_{p}_{tee}_{r}')
    model.Add(pos==tee).OnlyEnforceIf(b)
    model.Add(pos!=tee).OnlyEnforceIf(b.Not())
    occurrences.append(b)
   u=model.NewBoolVar(f'used_{p}_{tee}')
   model.AddMaxEquality(u,occurrences)
   used.append(u)
  spread=model.NewIntVar(1,5,f'spread_{p}')
  model.Add(spread==sum(used));spreads.append(spread)
 minimum=model.NewIntVar(1,4,'minimum')
 model.AddMinEquality(minimum,spreads)
 model.Maximize(96*minimum+sum(spreads))
 assert not model.Validate(),model.Validate()
 solver=cp_model.CpSolver()
 solver.parameters.max_time_in_seconds=60
 solver.parameters.num_search_workers=8
 solver.parameters.random_seed=101
 solver.parameters.log_search_progress=True
 solver.parameters.log_to_stdout=False
 directory=root/f'delete_{removed:02d}';directory.mkdir(exist_ok=True)
 with (directory/'solver.log').open('w') as log:
  solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
  status=solver.Solve(model)
 result=dict(removed_original_player=removed,status=solver.StatusName(status),
  solver_seconds=solver.WallTime(),objective_bound=solver.BestObjectiveBound(),
  player_mapping=labels)
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  ordered=[]
  for r in range(5):
   row=[None]*5
   for g,members in enumerate(groups[r]):row[solver.Value(slots[r][g])]=members
   ordered.append(row)
  result.update(validate(ordered,19,5))
  with (directory/'schedule.csv').open('w',newline='') as f:
   writer=csv.writer(f)
   for r,row in enumerate(ordered,1):
    for g,members in enumerate(row,1):writer.writerow([r,g,*members])
 (directory/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 results.append(result)
 (root/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(result),flush=True)
best=max((r for r in results if 'minimum_spread' in r),key=lambda r:(r['minimum_spread'],r['total_spread']))
(root/'best_schedule.csv').write_bytes((root/f"delete_{best['removed_original_player']:02d}"/'schedule.csv').read_bytes())
summary=dict(completed=len(results),all_orderings_proven=all(r['status']=='OPTIMAL' for r in results),best=best,
 scope='Fixed source structure and its deletions only; not global optimality')
(root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary),flush=True)
