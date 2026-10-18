"""Exclude improvements to the two saved distributions not fixed by min/total."""
from pathlib import Path
import sys,json,csv
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from cp_sat_caseB_v2 import build_model
from esgp_v2 import validate,number_best_first
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
for rounds,total,limit,n in [(4,45,2,15),(5,51,2,16)]:
 out=root/f'n{n}_r{rounds}';out.mkdir(exist_ok=True)
 model,solver,X,sizes,R=build_model(n,rounds=rounds,fair_spread=True,strengthen=True,time_limit=120,seed=101)
 vars={v.name:model.GetIntVarFromProtoIndex(i) for i,v in enumerate(model.Proto().variables)}
 model.Add(vars['minimum_spread']==2)
 model.Add(sum(vars[f'distinct_pos_{p}'] for p in range(1,n+1))==total)
 model.Add(sum(vars[f'at_minimum_{p}'] for p in range(1,n+1))<=limit)
 model.ClearObjective();solver.parameters.log_to_stdout=False
 with (out/'solver.log').open('w') as log:
  solver.log_callback=lambda msg:log.write(msg+'\n');status=solver.Solve(model)
 result={'players':n,'rounds':R,'fixed_minimum':2,'fixed_total':total,'target_players_at_minimum_at_most':limit,'status':solver.StatusName(status),'seconds':solver.WallTime()}
 if status in [cp_model.FEASIBLE,cp_model.OPTIMAL]:
  schedule=[[[p for p in range(1,n+1) if solver.Value(X[r,g,p])] for g in range(len(sizes))] for r in range(R)]
  schedule,mapping=number_best_first(schedule,n);result.update(validate(schedule,n,R));result['old_to_new_player_numbers']=mapping
  with (out/'schedule.csv').open('w') as f:
   w=csv.writer(f,lineterminator='\n')
   for r,gs in enumerate(schedule,1):
    for g,ps in enumerate(gs,1):w.writerow([r,g,*ps])
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
