"""Parallel explicit triangle/five-cycle structural enumeration cases."""
import hashlib,itertools,json,sys,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from structural_snapshot import build,orbit,decode,bipartite
from ordering_snapshot import optimize,save
from esgp_v2 import read_schedule,validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
prior=root.parent/'n18_nonextendable_enumeration_pilot_20261011'
checkpoint=json.loads((prior/'checkpoint.json').read_text())
inherited=[]
for item in checkpoint['classes']:
 assignments=json.loads((prior/item['directory']/'orbit.json').read_text())
 inherited.append(assignments)
 (root/f'inherited_orbit_{item["id"]:04d}.json').write_text(json.dumps(assignments)+'\n')
(root/'configuration.json').write_text(json.dumps(dict(cycle_lengths=[3,5],workers_per_case=5,
 parallel_cases=2,seconds_per_case=1200,ordering_seconds=60,inherited_classes=len(inherited),
 cycle_witness_counts={'3':120,'5':3024},sha256={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ('run.py','structural_snapshot.py','ordering_snapshot.py')}),indent=2)+'\n')

def run_case(length):
 directory=root/f'cycle_{length}';directory.mkdir(exist_ok=False)
 started=time.monotonic();deadline=started+1200
 model,slots=build(cycle_length=length)
 variables=[v for row in slots[1:] for v in row]
 for assignments in inherited:model.AddForbiddenAssignments(variables,assignments)
 assert not model.Validate(),model.Validate()
 model.ExportToFile(str(directory/'initial_model.pbtxt'))
 state=dict(cycle_length=length,classes=[],attempts=[],exhausted=False,best_known=[4,72])
 def persist():(directory/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
 persist();print(f'Starting explicit cycle length {length}',flush=True)
 while time.monotonic()<deadline:
  solver=cp_model.CpSolver()
  solver.parameters.max_time_in_seconds=max(.01,deadline-time.monotonic())
  solver.parameters.num_search_workers=5
  solver.parameters.random_seed=101+len(state['attempts'])
  solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
  attempt=len(state['attempts'])+1
  with (directory/f'generation_{attempt:04d}.log').open('w') as log:
   solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
   status=solver.Solve(model)
  state['attempts'].append(dict(status=solver.StatusName(status),seconds=solver.WallTime()))
  if status==cp_model.INFEASIBLE:state['exhausted']=True;persist();break
  if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):persist();break
  assignment=tuple(solver.Value(v) for v in variables)
  schedule=decode(assignment);assert not bipartite(schedule)
  # Independent explicit graph check for a cycle of the requested length.
  adj={v:set() for v in range(10)}
  for r in range(5):adj[2*r].add(2*r+1);adj[2*r+1].add(2*r)
  for p in range(1,19):
   nodes=[2*r+g for r,row in enumerate(schedule) for g,members in enumerate(row[:2]) if p in members]
   if len(nodes)==2:
    a,b=nodes;adj[a].add(b);adj[b].add(a)
  witness=None
  for subset in itertools.combinations(range(10),length):
   for rest in itertools.permutations(subset[1:]):
    if rest[0]>rest[-1]:continue
    cycle=(subset[0],)+rest
    if all(cycle[(i+1)%length] in adj[cycle[i]] for i in range(length)):
     witness=cycle;break
   if witness:break
  assert witness is not None
  assignments=orbit(schedule);assert assignment in assignments
  item=dict(id=len(state['classes']),canonical_sha256=hashlib.sha256(repr(assignments[0]).encode()).hexdigest(),orbit_size=len(assignments),cycle_witness=witness,ordering_complete=False)
  assert item['canonical_sha256'] not in {c['canonical_sha256'] for c in state['classes']}
  target=directory/f'class_{item["id"]:04d}';target.mkdir()
  save(target/'source.csv',schedule)
  (target/'orbit.json').write_text(json.dumps(assignments)+'\n')
  state['classes'].append(item);persist()
  model.AddForbiddenAssignments(variables,assignments)
  task=dict(name=f'cycle_{length}/class_{item["id"]:04d}/ordering',schedule=schedule,class_id=item['id'],removed=[],player_mapping={p:p for p in range(1,19)})
  result=optimize(task);item['ordering_result']=result;item['ordering_complete']=True
  if 'minimum_spread' in result:
   score=[result['minimum_spread'],result['total_spread']]
   if score>state['best_known']:
    state['best_known']=score
    (directory/'best_schedule.csv').write_bytes((root/task['name']/'schedule.csv').read_bytes())
  persist()
  print(json.dumps(dict(length=length,new_class=item['id'],ordering_status=result['status'],score=[result.get('minimum_spread'),result.get('total_spread')])),flush=True)
 summary=dict(cycle_length=length,completed=True,elapsed_seconds=time.monotonic()-started,
  new_classes=len(state['classes']),best_known=state['best_known'],exhausted=state['exhausted'],
  all_orderings_proven=all(c.get('ordering_result',{}).get('status')=='OPTIMAL' for c in state['classes']),attempts=state['attempts'])
 (directory/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 return summary

results=[]
with ThreadPoolExecutor(max_workers=2) as executor:
 futures=[executor.submit(run_case,n) for n in (3,5)]
 for future in as_completed(futures):
  result=future.result();results.append(result)
  (root/'results.json').write_text(json.dumps(results,indent=2)+'\n')
  with (root/'README.md').open('a') as f:f.write('\nCompleted length case: '+json.dumps(result)+'\n')
summary=dict(completed=True,cases=results,scope='Triangle and five-cycle families only; seven/nine-cycle-only structures remain unless separately excluded')
(root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary),flush=True)
