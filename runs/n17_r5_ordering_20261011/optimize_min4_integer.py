"""Independent integer encoding of the exhaustive minimum-four classes."""
import csv,itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from integer_model_snapshot import build_model
from esgp_v2 import read_schedule,validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
# Positive cross-check: the pilot is feasible with exact computed distinct counts.
data=build_model(17)
schedule=read_schedule(root/'schedule.csv',17,5)
for r,groups in enumerate(schedule):
 for g,members in enumerate(groups):
  for p in members:data['model'].Add(data['slots'][r,p]==g)
solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=5
assert solver.Solve(data['model'])==cp_model.OPTIMAL
for p in range(1,18):
 assert solver.Value(data['distinct'][p])==len({g for groups in schedule for g,members in enumerate(groups) if p in members})
results=[]
for index,matrix in enumerate(json.loads((root/'round_pair_classes.json').read_text())['representatives']):
 case=root/f'min4_integer_opt_case{index}';case.mkdir(exist_ok=False)
 data=build_model(17);model=data['model'];start=17
 for row,size in zip(matrix,data['sizes']):
  members=list(range(start-size+1,start+1));start-=size
  for g,occupied in enumerate(row):
   if occupied:model.Add(data['slots'][1,members.pop(0)]==g)
  assert not members
 for p in range(1,18):
  model.Add(data['distinct'][p]>=4)
  equalities=[]
  for r,s in itertools.combinations(range(5),2):
   same=model.NewBoolVar(f'repeat_{p}_{r}_{s}')
   model.Add(data['slots'][r,p]==data['slots'][s,p]).OnlyEnforceIf(same)
   model.Add(data['slots'][r,p]!=data['slots'][s,p]).OnlyEnforceIf(same.Not())
   equalities.append(same)
  model.AddAtMostOne(equalities)
 model.Maximize(sum(data['distinct'].values()))
 model.ExportToFile(str(case/'model.pbtxt'))
 solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=60;solver.parameters.num_search_workers=1;solver.parameters.random_seed=101
 solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
 with (case/'solver.log').open('w') as log:
  solver.log_callback=lambda message:log.write(message+'\n')
  status=solver.Solve(model)
 result={'case':index,'status':solver.StatusName(status),'solver_seconds':solver.WallTime(),'positive_crosscheck':'passed','objective_value':solver.ObjectiveValue(),'objective_bound':solver.BestObjectiveBound()}
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  schedule=[[[p for p in range(1,18) if solver.Value(data['slots'][r,p])==g] for g in range(5)] for r in range(5)]
  result.update(validate(schedule,17,5))
  with (case/'schedule.csv').open('w',newline='') as output:
   writer=csv.writer(output)
   for r,groups in enumerate(schedule,1):
    for g,members in enumerate(groups,1):writer.writerow([r,g,*members])
 (case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 results.append(result);(root/'min4_integer_opt_results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(result),flush=True)
