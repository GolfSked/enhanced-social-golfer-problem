"""Full v2 CP-SAT model with a globally valid canonical second round."""
import csv,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from cp_sat_caseB_v2 import build_model,load_hints_from_csv
from esgp_v2 import validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
model,solver,X,sizes,R=build_model(16,rounds=5,fair_spread=True,strengthen=True,time_limit=1200,workers=8,seed=101)
# First round already fixed to [13..16], [9..12], [5..8], [1..4].
# Each second-round group intersects each first-round group once. Renaming
# players within their first-round groups fixes these ordered columns safely.
for g in range(4):
 members={base+g for base in (1,5,9,13)}
 for p in range(1,17):model.Add(X[1,g,p]==int(p in members))
# Relabel the enumerated witness to the retained model's fixed first round.
import esgp_v2
schedule=esgp_v2.read_schedule(root/'global_schedule.csv',16,5)
def relabel(p):return (3-(p-1)//4)*4+(p-1)%4+1
for r,groups in enumerate(schedule):
 for g,members in enumerate(groups):
  members={relabel(p) for p in members}
  for p in range(1,17):model.AddHint(X[r,g,p],int(p in members))
solver.parameters.log_to_stdout=False
model.ExportToFile(str(root/'canonical_model.pbtxt'))
with (root/'canonical_solver.log').open('w') as log:
 solver.log_callback=lambda message:log.write(message+'\n')
 status=solver.Solve(model)
result={'status':solver.StatusName(status),'solver_seconds':solver.WallTime(),'scope':'Global optimum; only player relabelling symmetry is fixed'}
if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
 schedule=[[[p for p in range(1,17) if solver.Value(X[r,g,p])] for g in range(4)] for r in range(5)]
 result.update(validate(schedule,16,5));result.update(objective_value=solver.ObjectiveValue(),objective_bound=solver.BestObjectiveBound())
 with (root/'canonical_schedule.csv').open('w',newline='') as output:
  writer=csv.writer(output)
  for r,groups in enumerate(schedule,1):
   for g,members in enumerate(groups,1):writer.writerow([r,g,*members])
(root/'canonical_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True)
