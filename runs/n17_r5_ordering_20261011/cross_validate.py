"""Cross-force an integer-model witness into the v2 Boolean model."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from cp_sat_caseB_v2 import build_model
from esgp_v2 import read_schedule,validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
source=root/'min4_integer_opt_case2/schedule.csv'
schedule=read_schedule(source,17,5);metrics=validate(schedule,17,5)
model,solver,X,_,_=build_model(17,rounds=5,fair_spread=True,strengthen=True,time_limit=10,workers=1)
for r,groups in enumerate(schedule):
 for g,members in enumerate(groups):
  for p in range(1,18):model.Add(X[r,g,p]==int(p in members))
solver.parameters.log_search_progress=False
status=solver.Solve(model)
assert status==cp_model.OPTIMAL
assert solver.ObjectiveValue()==86*metrics['minimum_spread']+metrics['total_spread']
# Mutating two rounds to be identical must be rejected by the reference model.
model,bad_solver,X,_,_=build_model(17,rounds=5,time_limit=10,workers=1)
bad_solver.parameters.log_search_progress=False
mutant=[schedule[0],schedule[0],*schedule[2:]]
for r,groups in enumerate(mutant):
 for g,members in enumerate(groups):
  for p in range(1,18):model.Add(X[r,g,p]==int(p in members))
assert bad_solver.Solve(model)==cp_model.INFEASIBLE
result={'source':str(source),'metrics':metrics,'boolean_fixed_schedule_status':solver.StatusName(status),'objective_value':solver.ObjectiveValue(),'duplicate_round_rejected':True}
(root/'cross_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
