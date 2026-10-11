"""Exhaustive low-trace classes for existence of minimum spread >=4."""
import csv,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from cp_sat_caseB_v2 import build_model
from esgp_v2 import validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
matrices=json.loads((root/'round_pair_classes.json').read_text())['representatives']
results=[]
for index,matrix in enumerate(matrices):
 case=root/f'min4_case{index}'
 case.mkdir(exist_ok=False)
 model,solver,X,sizes,R=build_model(17,rounds=5,fair_spread=True,strengthen=True,time_limit=60,workers=1,seed=101)
 # Fix round two by assigning each first-round row's players to its occupied columns.
 second=[[] for _ in sizes];start=17
 for row,size in zip(matrix,sizes):
  members=list(range(start-size+1,start+1));start-=size
  for g,occupied in enumerate(row):
   if occupied:second[g].append(members.pop(0))
  assert not members
 for g,members in enumerate(second):
  for p in range(1,18):model.Add(X[1,g,p]==int(p in members))
 for i,variable in enumerate(model.Proto().variables):
  if variable.name.startswith('distinct_pos_'):model.Add(model.GetIntVarFromProtoIndex(i)>=4)
 model.ClearObjective()
 model.ExportToFile(str(case/'model.pbtxt'))
 solver.parameters.log_to_stdout=False
 with (case/'solver.log').open('w') as log:
  solver.log_callback=lambda message:log.write(message+'\n')
  status=solver.Solve(model)
 result={'case':index,'matrix':matrix,'status':solver.StatusName(status),'solver_seconds':solver.WallTime()}
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  schedule=[[[p for p in range(1,18) if solver.Value(X[r,g,p])] for g in range(5)] for r in range(5)]
  result.update(validate(schedule,17,5))
  with (case/'schedule.csv').open('w',newline='') as output:
   writer=csv.writer(output)
   for r,groups in enumerate(schedule,1):
    for g,members in enumerate(groups,1):writer.writerow([r,g,*members])
 (case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 results.append(result)
 (root/'min4_classes_results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(result),flush=True)
