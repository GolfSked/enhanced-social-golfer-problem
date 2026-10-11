"""All balanced two-player deletions of the complete n20/R5 catalogue."""
import csv,hashlib,itertools,json,sys,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from esgp_v2 import read_schedule,validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent

def save(path,schedule):
 with path.open('w',newline='') as f:
  writer=csv.writer(f)
  for r,row in enumerate(schedule,1):
   for g,members in enumerate(row,1):writer.writerow([r,g,*members])

def optimize(task):
 model=cp_model.CpModel();schedule=task['schedule'];slots=[]
 for r in range(5):
  row=[model.NewIntVar(0,1,f'slot_{r}_{g}') for g in range(2)]+[
       model.NewIntVar(2,4,f'slot_{r}_{g}') for g in range(2,5)]
  model.AddAllDifferent(row)
  if r==0:
   for g in range(5):model.Add(row[g]==g)
  slots.append(row)
 spreads=[]
 for p in range(1,19):
  positions=[slots[r][next(g for g,members in enumerate(schedule[r]) if p in members)] for r in range(5)]
  used=[]
  for tee in range(5):
   occurrences=[]
   for r,pos in enumerate(positions):
    b=model.NewBoolVar(f'at_{p}_{r}_{tee}')
    model.Add(pos==tee).OnlyEnforceIf(b)
    model.Add(pos!=tee).OnlyEnforceIf(b.Not());occurrences.append(b)
   u=model.NewBoolVar(f'used_{p}_{tee}')
   model.AddMaxEquality(u,occurrences);used.append(u)
  spread=model.NewIntVar(1,5,f'spread_{p}')
  model.Add(spread==sum(used));spreads.append(spread)
 minimum=model.NewIntVar(1,4,'minimum')
 model.AddMinEquality(minimum,spreads)
 model.Maximize(91*minimum+sum(spreads))
 assert not model.Validate(),model.Validate()
 directory=root/task['name'];directory.mkdir()
 save(directory/'input.csv',schedule)
 solver=cp_model.CpSolver()
 solver.parameters.max_time_in_seconds=60
 solver.parameters.num_search_workers=5
 solver.parameters.random_seed=101
 solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
 with (directory/'solver.log').open('w') as log:
  solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
  status=solver.Solve(model)
 result=dict(case=task['name'],class_id=task['class_id'],removed=task['removed'],
  player_mapping=task['player_mapping'],status=solver.StatusName(status),
  seconds=solver.WallTime(),objective_bound=solver.BestObjectiveBound())
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  ordered=[]
  for r in range(5):
   row=[None]*5
   for g,members in enumerate(schedule[r]):row[solver.Value(slots[r][g])]=members
   ordered.append(row)
  result.update(validate(ordered,18,5))
  save(directory/'schedule.csv',ordered)
 (directory/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 return result

started=time.monotonic()
catalogue=root.parent/'n19_via20_enumeration_pilot_20261011/checkpoint.json'
classes=json.loads(catalogue.read_text())['classes'];tasks=[];counts={};sources=[]
for c in classes:
 source=Path(c['source']) if c['inherited'] else catalogue.parent/('class_%03d'%c['id'])/'source.csv'
 original=read_schedule(source,20,5);validate(original,20,5)
 partners={p:set() for p in range(1,21)}
 for row in original:
  for group in row:
   for p in group:partners[p].update(set(group)-{p})
 counts[c['id']]=0
 for a,b in itertools.combinations(range(1,21),2):
  if b in partners[a]:continue
  if partners[a]|partners[b]!=set(range(1,21))-{a,b}:continue
  labels={p:i+1 for i,p in enumerate(p for p in range(1,21) if p not in (a,b))}
  trimmed=[sorted([[labels[p] for p in group if p not in (a,b)] for group in row],key=len) for row in original]
  validate(trimmed,18,5)
  tasks.append(dict(name=f'class_{c["id"]:02d}_delete_{a:02d}_{b:02d}',class_id=c['id'],removed=[a,b],player_mapping=labels,schedule=trimmed))
  counts[c['id']]+=1
 sources.append(dict(class_id=c['id'],path=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
assert len(tasks)==228
(root/'configuration.json').write_text(json.dumps(dict(cases=len(tasks),counts_by_class=counts,
 workers_per_case=5,concurrent_cases=2,seconds_per_case=60,seed=101,
 source_catalogue_sha256=hashlib.sha256(catalogue.read_bytes()).hexdigest(),
 script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),sources=sources),indent=2)+'\n')
(root/'manifest.json').write_text(json.dumps([{k:v for k,v in t.items() if k!='schedule'} for t in tasks],indent=2)+'\n')
results=[];best=(4,72)
with ThreadPoolExecutor(max_workers=2) as executor:
 futures=[executor.submit(optimize,t) for t in tasks]
 for future in as_completed(futures):
  result=future.result();results.append(result)
  if 'minimum_spread' in result:
   score=(result['minimum_spread'],result['total_spread'])
   if score>best:
    best=score
    (root/'best_schedule.csv').write_bytes((root/result['case']/'schedule.csv').read_bytes())
    (root/'best_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(improvement=best,case=result['case'])),flush=True)
  (root/'progress.json').write_text(json.dumps(dict(completed=len(results),total=len(tasks),best_known=best),indent=2)+'\n')
  if len(results)%20==0:print(f'Completed {len(results)}/{len(tasks)}',flush=True)
summary=dict(completed=len(results),total_cases=len(tasks),elapsed_seconds=time.monotonic()-started,
 all_orderings_proven=all(r['status']=='OPTIMAL' for r in results),
 best_in_family=max((r['minimum_spread'],r['total_spread']) for r in results if 'minimum_spread' in r),
 best_known=best,scope='All balanced n18/R5 structures extendable to n20; not all n18 structures',
 counts_by_class=counts)
(root/'results.json').write_text(json.dumps(results,indent=2)+'\n')
(root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
with (root/'README.md').open('a') as f:f.write('\nCompleted: '+json.dumps(summary)+'\n')
print(json.dumps(summary),flush=True)
