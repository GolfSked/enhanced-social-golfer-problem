"""Complete canonical exclusion test for total >=77 at minimum >=4.

Total >=77 gives at most eight repeated-slot pairs, across ten round pairs,
so some round pair has trace zero. There is exactly one trace-zero class.
"""
import csv,itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from integer_model_snapshot import build_model
from esgp_v2 import validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
matrices=json.loads((root/'round_pair_classes.json').read_text())['representatives']
zero=[matrix for matrix in matrices if sum(matrix[g][g] for g in range(5))==0]
assert len(zero)==1
case=root/'target77_integer';case.mkdir(exist_ok=False)
data=build_model(17);model=data['model'];start=17
for row,size in zip(zero[0],data['sizes']):
 members=list(range(start-size+1,start+1));start-=size
 for g,occupied in enumerate(row):
  if occupied:model.Add(data['slots'][1,members.pop(0)]==g)
for p in range(1,18):
 model.Add(data['distinct'][p]>=4)
 extra=model.NewBoolVar(f'extra_four_{p}')
 model.Add(sum(data['membership'][r,g,p] for r in range(5) for g in (3,4))==2+extra)
 model.Add(data['distinct'][p]<=5-extra)
 equalities=[]
 for r,s in itertools.combinations(range(5),2):
  same=model.NewBoolVar(f'repeat_{p}_{r}_{s}')
  model.Add(data['slots'][r,p]==data['slots'][s,p]).OnlyEnforceIf(same)
  model.Add(data['slots'][r,p]!=data['slots'][s,p]).OnlyEnforceIf(same.Not())
  equalities.append(same)
 model.AddAtMostOne(equalities)
model.Add(sum(data['distinct'].values())>=77)
model.Add(sum(data['distinct'].values())<=78)
model.ExportToFile(str(case/'model.pbtxt'))
solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=1200;solver.parameters.num_search_workers=8;solver.parameters.random_seed=101
solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
with (case/'solver.log').open('w') as log:
 solver.log_callback=lambda message:(log.write(message+'\n'),log.flush())
 status=solver.Solve(model)
result={'status':solver.StatusName(status),'solver_seconds':solver.WallTime(),'matrix':zero[0],'minimum_target':4,'total_target':77}
if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
 schedule=[[[p for p in range(1,18) if solver.Value(data['slots'][r,p])==g] for g in range(5)] for r in range(5)]
 result.update(validate(schedule,17,5))
 with (case/'schedule.csv').open('w',newline='') as output:
  writer=csv.writer(output)
  for r,groups in enumerate(schedule,1):
   for g,members in enumerate(groups,1):writer.writerow([r,g,*members])
(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True)
