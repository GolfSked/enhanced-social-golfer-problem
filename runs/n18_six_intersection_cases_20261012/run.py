"""Six exhaustive first-two-round intersection orbits, two searches concurrently."""
from structural_snapshot import *
from concurrent.futures import ThreadPoolExecutor

def write(path,value):
 path.write_text(json.dumps(value,indent=2)+'\n')

matrices={}
for rows in itertools.product(*(list(itertools.combinations(range(5),s)) for s in sizes)):
 if [sum(g in row for row in rows) for g in range(5)]!=sizes:continue
 matrix=tuple(tuple(int(g in row) for g in range(5)) for row in rows)
 key=min(tuple(matrix[r][c] for r in ro for c in co) for ro in orders for co in orders)
 vector=tuple(g for row in rows for g in row)
 entry=matrices.setdefault(key,dict(labelled_count=0,representatives=[]))
 entry['labelled_count']+=1
 if vector==names(vector):entry['representatives'].append(vector)
assert len(matrices)==6 and sum(x['labelled_count'] for x in matrices.values())==258
coverage=[]
for i,(key,item) in enumerate(sorted(matrices.items())):
 assert item['representatives']
 coverage.append(dict(case=i,canonical_matrix=[list(key[j:j+5]) for j in range(0,25,5)],labelled_count=item['labelled_count'],normalized_count=len(item['representatives']),second_round=min(item['representatives'])))
write(root/'coverage.json',coverage)
previous=root.parent/'n18_nonextendable_enumeration_pilot_20261011'
inherited=[]
for item in json.loads((previous/'checkpoint.json').read_text())['classes']:
 inherited.append(json.loads((previous/item['directory']/'orbit.json').read_text()))
write(root/'inherited_orbits.json',inherited)
write(root/'configuration.json',dict(case_seconds=1200,concurrent_cases=2,workers_per_case=5,ordering_seconds=60,inherited_classes=len(inherited),sha256={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ('run.py','structural_snapshot.py','ordering_snapshot.py','inherited_orbits.json')}))

def run(case):
 directory=root/f'case_{case["case"]:02d}';directory.mkdir(exist_ok=True)
 started=time.monotonic();deadline=started+1200
 state=dict(case=case['case'],status='RUNNING',classes=[],attempts=[],best_known=[4,72],exhausted=False)
 def persist():write(directory/'checkpoint.json',state)
 persist();print(json.dumps(dict(case=case['case'],status='STARTED')),flush=True)
 model,slots=build();variables=[v for row in slots[1:] for v in row]
 for v,value in zip(slots[1],case['second_round']):model.Add(v==value)
 for assignments in inherited:model.AddForbiddenAssignments(variables,assignments)
 assert not model.Validate(),model.Validate()
 model.ExportToFile(str(directory/'initial_model.pbtxt'))
 while time.monotonic()<deadline:
  solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=max(.01,deadline-time.monotonic())
  solver.parameters.num_search_workers=5;solver.parameters.random_seed=1999+case['case']+len(state['attempts'])
  solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
  with (directory/f'generation_{len(state["attempts"])+1:04d}.log').open('w') as log:
   solver.log_callback=lambda message:(log.write(message+'\n'),log.flush())
   status=solver.Solve(model)
  state['attempts'].append(dict(status=solver.StatusName(status),seconds=solver.WallTime()))
  if status==cp_model.INFEASIBLE:state['exhausted']=True;persist();break
  if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):persist();break
  assignment=tuple(solver.Value(v) for v in variables);schedule=decode(assignment)
  assert not bipartite(schedule)
  assignments=orbit(schedule);assert assignment in assignments
  key=hashlib.sha256(repr(assignments[0]).encode()).hexdigest()
  assert key not in {x['canonical_sha256'] for x in state['classes']}
  number=len(state['classes']);relative=f'case_{case["case"]:02d}/class_{number:04d}'
  dest=root/relative;dest.mkdir();save(dest/'source.csv',schedule);write(dest/'orbit.json',assignments)
  item=dict(id=number,directory=relative,canonical_sha256=key,orbit_size=len(assignments),ordering_complete=False)
  state['classes'].append(item);persist()
  result=optimize(dict(name=relative+'/ordering',schedule=schedule,class_id=number,removed=[],player_mapping={p:p for p in range(1,19)}))
  item['ordering_result']=result;item['ordering_complete']=True
  if 'minimum_spread' in result:
   score=[result['minimum_spread'],result['total_spread']]
   if score>state['best_known']:state['best_known']=score
  model.AddForbiddenAssignments(variables,assignments);persist()
  print(json.dumps(dict(case=case['case'],new_class=number,ordering=result)),flush=True)
 state['status']='COMPLETE';state['elapsed_seconds']=time.monotonic()-started
 state['all_orderings_proven']=all(x.get('ordering_result',{}).get('status')=='OPTIMAL' for x in state['classes'])
 persist();write(directory/'summary.json',state)
 print(json.dumps(dict(case=case['case'],status='COMPLETE',exhausted=state['exhausted'],new_classes=len(state['classes']),best_known=state['best_known'])),flush=True)
 return state

if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,coverage))
 write(root/'summary.json',dict(cases=results,all_cases_exhausted=all(x['exhausted'] for x in results),best_known=max(x['best_known'] for x in results)))
