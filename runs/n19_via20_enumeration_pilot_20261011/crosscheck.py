"""Independent Boolean enumeration without any orbit exclusion constraints."""
import json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from esgp_v2 import read_schedule,validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
checkpoint=json.loads((root/'checkpoint.json').read_text())
expected={tuple(a) for c in checkpoint['classes'] for a in c['assignments']}
assert len(expected)==sum(len(c['assignments']) for c in checkpoint['classes'])
model=cp_model.CpModel()
X={(r,g,p):model.NewBoolVar(f'X_{r}_{g}_{p}') for r in range(5) for g in range(5) for p in range(20)}
for r in range(5):
 for p in range(20):model.AddExactlyOne(X[r,g,p] for g in range(5))
 for g in range(5):model.Add(sum(X[r,g,p] for p in range(20))==4)
cells=[(i,j) for i in range(5) for j in range(5) if i!=j]
for p,(i,j) in enumerate(cells):
 model.Add(X[0,i,p]==1);model.Add(X[1,j,p]==1)
for p in range(20):
 for q in range(p+1,20):
  meetings=[]
  for r in range(5):
   for g in range(5):
    y=model.NewBoolVar(f'meet_{p}_{q}_{r}_{g}')
    model.Add(y<=X[r,g,p]);model.Add(y<=X[r,g,q])
    model.Add(y>=X[r,g,p]+X[r,g,q]-1);meetings.append(y)
  model.AddAtMostOne(meetings)
slots=[]
for r in range(2,5):
 row=[]
 for p in range(20):
  v=model.NewIntVar(0,4,f'slot_{r}_{p}')
  model.Add(v==sum(g*X[r,g,p] for g in range(5)));row.append(v)
  for g in range(1,5):
   model.Add(X[r,g,p]<=sum(X[r,g-1,q] for q in range(p)))
 slots.append(row)
# Lex order of the three remaining rounds, with fully determined auxiliaries.
for index,(left,right) in enumerate(zip(slots,slots[1:])):
 prefix=model.NewBoolVar(f'prefix_{index}_0');model.Add(prefix==1)
 for p,(a,b) in enumerate(zip(left,right)):
  model.Add(a<=b).OnlyEnforceIf(prefix)
  equal=model.NewBoolVar(f'equal_{index}_{p}')
  model.Add(a==b).OnlyEnforceIf(equal)
  model.Add(a!=b).OnlyEnforceIf(equal.Not())
  nxt=model.NewBoolVar(f'prefix_{index}_{p+1}')
  model.Add(nxt<=prefix);model.Add(nxt<=equal)
  model.Add(nxt>=prefix+equal-1);prefix=nxt
assert not model.Validate(),model.Validate()
model.ExportToFile(str(root/'crosscheck_model.pbtxt'))
class Enumeration(cp_model.CpSolverSolutionCallback):
 def __init__(self):super().__init__();self.assignments=set();self.callbacks=0
 def on_solution_callback(self):
  assignment=tuple(self.Value(v) for row in slots for v in row)
  assert assignment in expected,'Previously unrepresented structure'
  self.assignments.add(assignment);self.callbacks+=1
callback=Enumeration()
solver=cp_model.CpSolver()
solver.parameters.max_time_in_seconds=120
solver.parameters.num_search_workers=1
solver.parameters.enumerate_all_solutions=True
solver.parameters.log_search_progress=True
solver.parameters.log_to_stdout=False
with (root/'crosscheck_solver.log').open('w') as log:
 solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
 status=solver.Solve(model,callback)
result=dict(status=solver.StatusName(status),solver_seconds=solver.WallTime(),
 expected_assignments=len(expected),enumerated_assignments=len(callback.assignments),
 callbacks=callback.callbacks,missing_assignments=len(expected-callback.assignments),
 exact_match=callback.assignments==expected,
 complete_enumeration=status==cp_model.OPTIMAL)
# Audit every inherited/new deletion witness and its reported optimal bound.
audited=0;best=(0,0)
for c in checkpoint['classes']:
 if c['inherited'] and c['id']==0:
  directory=root.parent/'n19_via20_ordering_20261011'
  source=read_schedule(directory/'source.csv',20,5)
  for removed in range(1,21):
   d=directory/('delete_%02d'%removed)
   metrics=validate(read_schedule(d/'schedule.csv',19,5),19,5)
   saved=json.loads((d/'result.json').read_text())
   assert saved['status']=='OPTIMAL'
   assert saved['objective_bound']==96*metrics['minimum_spread']+metrics['total_spread']
   best=max(best,(metrics['minimum_spread'],metrics['total_spread']));audited+=1
 elif c['inherited']:
  directory=Path(c['source']).parent
  validate(read_schedule(directory/'schedule.csv',20,5),20,5)
  for removed in range(1,21):
   d=directory/('delete_%02d'%removed)
   metrics=validate(read_schedule(d/'schedule.csv',19,5),19,5)
   saved=json.loads((d/'result.json').read_text())
   assert saved['status']=='OPTIMAL'
   assert saved['bound']==96*metrics['minimum_spread']+metrics['total_spread']
   best=max(best,(metrics['minimum_spread'],metrics['total_spread']));audited+=1
 else:
  directory=root/('class_%03d'%c['id'])
  validate(read_schedule(directory/'source.csv',20,5),20,5)
  for removed in range(1,21):
   d=directory/('delete_%02d'%removed)
   metrics=validate(read_schedule(d/'schedule.csv',19,5),19,5)
   saved=json.loads((d/'result.json').read_text())
   assert saved['status']=='OPTIMAL'
   assert saved['bound']==96*metrics['minimum_spread']+metrics['total_spread']
   best=max(best,(metrics['minimum_spread'],metrics['total_spread']));audited+=1
result.update(audited_deletion_optima=audited,best_score=best)
(root/'crosscheck_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True)
