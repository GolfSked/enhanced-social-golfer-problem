import csv,json,sys,itertools,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from integer_model_snapshot import build_model
from esgp_v2 import validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
data=build_model(18,rounds=5);model=data['model']
for p in range(1,19):
 model.Add(data['distinct'][p]>=4)
 extra=model.NewBoolVar(f'extra_four_{p}')
 model.Add(sum(data['membership'][r,g,p] for r in range(5) for g in (2,3,4))==3+extra)
 model.Add(data['distinct'][p]<=5-extra)
 equalities=[]
 for r,s in itertools.combinations(range(5),2):
  same=model.NewBoolVar(f'repeat_{p}_{r}_{s}')
  model.Add(data['slots'][r,p]==data['slots'][s,p]).OnlyEnforceIf(same)
  model.Add(data['slots'][r,p]!=data['slots'][s,p]).OnlyEnforceIf(same.Not())
  equalities.append(same)
 model.AddAtMostOne(equalities)
model.Add(sum(data['distinct'].values())<=84)
model.Maximize(sum(data['distinct'].values()))
model.ExportToFile(str(root/'model.pbtxt'))
solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=1200;solver.parameters.num_search_workers=4;solver.parameters.random_seed=202
solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
(root/'configuration.json').write_text(json.dumps({'players':18,'rounds':5,'minimum_target':4,'seconds':1200,'workers':4,'seed':202,'source_sha256':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ('run.py','integer_model_snapshot.py')}},indent=2)+'\n')
with (root/'solver.log').open('w') as log:
 solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
 status=solver.Solve(model)
result={'status':solver.StatusName(status),'solver_seconds':solver.WallTime(),'minimum_target':4}
if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
 schedule=[[[p for p in range(1,19) if solver.Value(data['slots'][r,p])==g] for g in range(5)] for r in range(5)]
 result.update(validate(schedule,18,5))
 with (root/'schedule.csv').open('w',newline='') as f:
  writer=csv.writer(f)
  for r,groups in enumerate(schedule,1):
   for g,members in enumerate(groups,1):writer.writerow([r,g,*members])
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True)
