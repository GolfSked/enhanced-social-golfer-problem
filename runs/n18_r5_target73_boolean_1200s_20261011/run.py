"""Global n18/R5 target73 test with complete all-five-player symmetry reduction."""
import csv,hashlib,itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from boolean_model_snapshot import build_model
from esgp_v2 import validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
model,solver,X,sizes,rounds=build_model(18,rounds=5,fair_spread=True,strengthen=True,time_limit=1200,workers=8,seed=101)
assert sizes==[3,3,4,4,4] and rounds==5
distinct={int(v.name.rsplit('_',1)[1]):model.GetIntVarFromProtoIndex(i) for i,v in enumerate(model.Proto().variables) if v.name.startswith('distinct_pos_')}
assert set(distinct)==set(range(1,19))
for p in range(1,19):
 model.Add(distinct[p]>=4)
 extra=model.NewBoolVar(f'target_extra_four_{p}')
 model.Add(sum(X[r,g,p] for r in range(5) for g,size in enumerate(sizes) if size==4)==3+extra)
 model.Add(distinct[p]<=5-extra)
 slots=[]
 for r in range(5):
  slot=model.NewIntVar(0,4,f'target_slot_{r}_{p}')
  model.Add(slot==sum(g*X[r,g,p] for g in range(5)))
  slots.append(slot)
 equalities=[]
 for r,s in itertools.combinations(range(5),2):
  same=model.NewBoolVar(f'target_repeat_{p}_{r}_{s}')
  model.Add(slots[r]==slots[s]).OnlyEnforceIf(same)
  model.Add(slots[r]!=slots[s]).OnlyEnforceIf(same.Not())
  equalities.append(same)
 model.AddAtMostOne(equalities)
model.Add(sum(distinct.values())>=73)
model.Add(sum(distinct.values())<=84)
# Every improving schedule has a five-slot player. Rename them18 and reorder
# rounds by their tee slots, then relabel other players within round zero.
for r in range(5):model.Add(X[r,r,18]==1)
model.ClearObjective()
assert not model.Validate(),model.Validate()
model.ExportToFile(str(root/'model.pbtxt'))
config={'players':18,'rounds':5,'sizes':sizes,'minimum_target':4,'total_target':73,'upper_bound':84,'seconds':1200,'workers':8,'seed':101,'strengthen':True,'hint':None,'source_sha256':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ('run.py','boolean_model_snapshot.py')}}
(root/'configuration.json').write_text(json.dumps(config,indent=2)+'\n')
solver.parameters.log_to_stdout=False
with (root/'solver.log').open('w') as log:
 solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
 status=solver.Solve(model)
result={'status':solver.StatusName(status),'solver_seconds':solver.WallTime(),'minimum_target':4,'total_target':73,'configured_seconds':1200}
if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
 schedule=[[[p for p in range(1,19) if solver.Value(X[r,g,p])] for g in range(5)] for r in range(5)]
 result.update(validate(schedule,18,5))
 assert result['minimum_spread']>=4 and result['total_spread']>=73
 with (root/'schedule.csv').open('w',newline='') as f:
  writer=csv.writer(f)
  for r,groups in enumerate(schedule,1):
   for g,members in enumerate(groups,1):writer.writerow([r,g,*members])
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n')
meaning=('(4,72) globally optimal: every remaining improvement excluded.' if status==cp_model.INFEASIBLE else 'Validated improvement found; total optimum not established by feasibility status.' if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else 'Unresolved: UNKNOWN does not exclude an improvement.')
with (root/'README.md').open('a') as f:f.write(f'\nCompleted: {solver.StatusName(status)} after {solver.WallTime():.6f} seconds. {meaning}\n')
print(json.dumps(result,indent=2),flush=True)
