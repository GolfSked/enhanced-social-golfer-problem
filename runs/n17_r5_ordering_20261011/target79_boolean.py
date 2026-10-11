"""Independent Boolean-model cross-check of the global score-79 exclusion."""
import itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from cp_sat_caseB_v2 import build_model
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
zero=[m for m in json.loads((root/'round_pair_classes.json').read_text())['representatives'] if sum(m[g][g] for g in range(5))==0]
assert len(zero)==1
case=root/'target79_boolean';case.mkdir(exist_ok=False)
model,solver,X,sizes,R=build_model(17,rounds=5,fair_spread=True,strengthen=True,time_limit=60,workers=8,seed=101)
second=[[] for _ in sizes];start=17
for row,size in zip(zero[0],sizes):
 members=list(range(start-size+1,start+1));start-=size
 for g,occupied in enumerate(row):
  if occupied:second[g].append(members.pop(0))
for g,members in enumerate(second):
 for p in range(1,18):model.Add(X[1,g,p]==int(p in members))
distinct={int(v.name.rsplit('_',1)[1]):model.GetIntVarFromProtoIndex(i) for i,v in enumerate(model.Proto().variables) if v.name.startswith('distinct_pos_')}
for p in range(1,18):
 model.Add(distinct[p]>=4)
 extra=model.NewBoolVar(f'extra_four_target_{p}')
 model.Add(sum(X[r,g,p] for r in range(5) for g in (3,4))==2+extra)
 model.Add(distinct[p]<=5-extra)
 # Equivalent integer slots expose implied pair-repeat constraints directly.
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
model.Add(sum(distinct.values())==79)
model.ClearObjective();model.ExportToFile(str(case/'model.pbtxt'))
solver.parameters.log_to_stdout=False
with (case/'solver.log').open('w') as log:
 solver.log_callback=lambda message:(log.write(message+'\n'),log.flush())
 status=solver.Solve(model)
result={'status':solver.StatusName(status),'solver_seconds':solver.WallTime(),'minimum_target':4,'total_target':79}
(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True)
