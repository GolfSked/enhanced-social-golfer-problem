"""Resumable exact-class enumeration pilot, 1200 seconds per invocation."""
import hashlib,itertools,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from helpers_snapshot import generate_model,canonical,optimize,save_schedule
from esgp_v2 import read_schedule,validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
cells=[(i,j) for i in range(5) for j in range(5) if i!=j]

def orbit(schedule):
 """All model assignments equivalent to this design, after round sorting."""
 assignments=set()
 for a,b in itertools.permutations(range(5),2):
  columns={p:g for g,row in enumerate(schedule[b]) for p in row}
  missing=[next(iter(set(range(5))-{columns[p] for p in row})) for row in schedule[a]]
  for order in itertools.permutations(range(5)):
   colmap={missing[old]:new for new,old in enumerate(order)}
   labels={p:cells.index((i,colmap[columns[p]])) for i,old in enumerate(order) for p in schedule[a][old]}
   rows=[]
   for r in range(5):
    if r in (a,b):continue
    raw=[None]*20
    for g,members in enumerate(schedule[r]):
     for p in members:raw[labels[p]]=g
    names={};normalized=[]
    for value in raw:
     if value not in names:names[value]=len(names)
     normalized.append(names[value])
    rows.append(tuple(normalized))
   assignments.add(tuple(v for row in sorted(rows) for v in row))
 return sorted(assignments)

def lex_le(model,left,right,name):
 equal=model.NewBoolVar(name+'_prefix0');model.Add(equal==1)
 for i,(a,b) in enumerate(zip(left,right)):
  model.Add(a<=b).OnlyEnforceIf(equal)
  same=model.NewBoolVar(f'{name}_same{i}')
  model.Add(a==b).OnlyEnforceIf(same)
  model.Add(a!=b).OnlyEnforceIf(same.Not())
  nxt=model.NewBoolVar(f'{name}_prefix{i+1}')
  model.Add(nxt<=equal);model.Add(nxt<=same);model.Add(nxt>=equal+same-1)
  equal=nxt

def persist():
 (root/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')

started=time.monotonic();deadline=started+1200
if (root/'checkpoint.json').exists():
 state=json.loads((root/'checkpoint.json').read_text())
else:
 state=dict(classes=[],attempts=[],best_score=[4,79],exhausted=False)
 sources=[root.parent/'n19_via20_ordering_20261011/source.csv']
 old=root.parent/'n19_via20_diverse_20261011'
 sources += [old/('candidate_%02d'%item['attempt'])/'schedule.csv'
  for item in json.loads((old/'candidates.json').read_text()) if item['new_class']]
 blocked=set()
 for source in sources:
  schedule=read_schedule(source,20,5);validate(schedule,20,5)
  assignments=orbit(schedule)
  assert not blocked.intersection(assignments),'Different prior classes overlap'
  blocked.update(assignments)
  state['classes'].append(dict(id=len(state['classes']),source=str(source),
   inherited=True,ordering_complete=True,canonical_sha256=hashlib.sha256(repr(canonical(schedule)).encode()).hexdigest(),
   assignments=[list(a) for a in assignments]))
 persist()
model,slots=generate_model()
lex_le(model,slots[2],slots[3],'round23')
lex_le(model,slots[3],slots[4],'round34')
variables=[v for row in slots[2:] for v in row]
for item in state['classes']:model.AddForbiddenAssignments(variables,item['assignments'])
assert not model.Validate(),model.Validate()
(root/'configuration.json').write_text(json.dumps(dict(seconds_per_invocation=1200,
 generation_workers=10,ordering_workers=10,parallel_cases=1,
 source_sha256={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ('run.py','helpers_snapshot.py')},
 inherited_classes=8,scope='Exact class exclusion; exhaustion only if final model INFEASIBLE'),indent=2)+'\n')
session=len(list(root.glob('session_*.json')))+1
new_classes=0;stop='time budget reached'
while time.monotonic()<deadline and not state['exhausted']:
 # Finish ordering a previously checkpointed class before advancing.
 pending=next((x for x in state['classes'] if not x['ordering_complete']),None)
 if pending:
  directory=root/('class_%03d'%pending['id'])
  schedule=read_schedule(directory/'source.csv',20,5)
  results=[]
  for removed in range(1,21):
   target=directory/('delete_%02d'%removed)
   if (target/'result.json').exists():
    result=json.loads((target/'result.json').read_text());ordered=None
   else:
    if time.monotonic()>=deadline:break
    result,ordered=optimize(schedule,removed,target)
   results.append(result)
   if 'minimum_spread' in result:
    score=[result['minimum_spread'],result['total_spread']]
    if score>state['best_score']:
     state['best_score']=score
     if ordered is None:ordered=read_schedule(target/'schedule.csv',19,5)
     save_schedule(root/'best_schedule.csv',ordered)
     (root/'best_result.json').write_text(json.dumps(dict(class_id=pending['id'],**result),indent=2)+'\n')
  pending['ordering_complete']=len(results)==20
  pending['ordering_results']=results
  pending['all_orderings_proven']=len(results)==20 and all(x['status']=='OPTIMAL' for x in results)
  persist()
  if not pending['ordering_complete']:break
  continue
 solver=cp_model.CpSolver()
 solver.parameters.max_time_in_seconds=min(60,max(.01,deadline-time.monotonic()))
 solver.parameters.num_search_workers=10
 solver.parameters.random_seed=101+len(state['attempts'])
 solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
 attempt=len(state['attempts'])+1
 with (root/('generation_%04d.log'%attempt)).open('w') as log:
  solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
  status=solver.Solve(model)
 state['attempts'].append(dict(attempt=attempt,status=solver.StatusName(status),seconds=solver.WallTime()))
 if status==cp_model.INFEASIBLE:
  state['exhausted']=True;stop='All normalized structures excluded';persist();break
 if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):persist();continue
 schedule=[[[p+1 for p in range(20) if solver.Value(slots[r][p])==g] for g in range(5)] for r in range(5)]
 validate(schedule,20,5)
 assignments=orbit(schedule)
 found=tuple(solver.Value(v) for v in variables)
 assert found in assignments
 key=hashlib.sha256(repr(canonical(schedule)).encode()).hexdigest()
 assert key not in {x['canonical_sha256'] for x in state['classes']}
 item=dict(id=len(state['classes']),inherited=False,ordering_complete=False,
  canonical_sha256=key,assignments=[list(a) for a in assignments])
 directory=root/('class_%03d'%item['id']);directory.mkdir()
 save_schedule(directory/'source.csv',schedule)
 state['classes'].append(item);persist()
 model.AddForbiddenAssignments(variables,assignments)
 new_classes+=1
 print(json.dumps(dict(new_class=item['id'],orbit_assignments=len(assignments))),flush=True)
summary=dict(session=session,elapsed_seconds=time.monotonic()-started,
 new_classes_this_session=new_classes,total_classes=len(state['classes']),
 best_score=state['best_score'],exhausted=state['exhausted'],
 ordering_complete=all(x['ordering_complete'] for x in state['classes']),
 all_orderings_proven=all(x.get('all_orderings_proven',x['inherited']) for x in state['classes']),stop=stop)
(root/('session_%03d.json'%session)).write_text(json.dumps(summary,indent=2)+'\n')
(root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
with (root/'README.md').open('a') as f:f.write('\nSession result: '+json.dumps(summary)+'\n')
print(json.dumps(summary),flush=True)
