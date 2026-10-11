"""Four complete witness-pattern cases for n19/R5 minimum4,total>=80."""
import hashlib,itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from model_snapshot import build,extract,write_csv
from esgp_v2 import validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
patterns=[(3,1,0,0,0),(2,2,0,0,0),(2,1,1,0,0),(1,1,1,1,0)]
assert sorted(set(tuple(sorted(x,reverse=True)) for x in itertools.product(range(4),repeat=5) if sum(x)==4))==sorted(patterns)
(root/'configuration.json').write_text(json.dumps(dict(players=19,rounds=5,minimum_target=4,total_target=80,patterns=patterns,seconds_per_case=1200,workers=4,seed=101,execution='Two concurrent cases, four workers each; up to two waves of 1200 seconds',hint=None,sha256={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ('run.py','model_snapshot.py')}),indent=2)+'\n')
def run_case(pattern):
 name='_'.join(map(str,pattern))
 directory=root/name;directory.mkdir(exist_ok=False)
 model,groups,tee_maps,tees=build(80,None)
 spreads={int(v.name.split('_')[1]):model.GetIntVarFromProtoIndex(i)
          for i,v in enumerate(model.Proto().variables) if v.name.startswith('spread_')}
 assert set(spreads)==set(range(1,20))
 selected={p:model.NewBoolVar(f'selected_{p}') for p in range(1,20)}
 model.Add(sum(selected.values())==4)
 triple_witnesses={r:[] for r in range(5)}
 for p in range(1,20):
  model.Add(spreads[p]==5).OnlyEnforceIf(selected[p])
  for r in range(5):
   triple=model.NewBoolVar(f'triple_{r}_{p}')
   model.Add(tees[r,p]==0).OnlyEnforceIf(triple)
   model.Add(tees[r,p]!=0).OnlyEnforceIf(triple.Not())
   joint=model.NewBoolVar(f'selected_triple_{r}_{p}')
   model.Add(joint<=selected[p]);model.Add(joint<=triple)
   model.Add(joint>=selected[p]+triple-1)
   triple_witnesses[r].append(joint)
 for r,count in enumerate(pattern):model.Add(sum(triple_witnesses[r])==count)
 assert not model.Validate(),model.Validate()
 model.ExportToFile(str(directory/'model.pbtxt'))
 solver=cp_model.CpSolver()
 solver.parameters.max_time_in_seconds=1200
 solver.parameters.num_search_workers=4
 solver.parameters.random_seed=101
 solver.parameters.log_search_progress=True
 solver.parameters.log_to_stdout=False
 print(f'Starting case {name}',flush=True)
 with (directory/'solver.log').open('w') as log:
  solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
  status=solver.Solve(model)
 result=dict(case=name,pattern=pattern,status=solver.StatusName(status),solver_seconds=solver.WallTime(),configured_seconds=1200)
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  schedule=extract(solver,tees);result.update(validate(schedule,19,5))
  assert result['minimum_spread']>=4 and result['total_spread']>=80
  chosen=[p for p in range(1,20) if solver.Value(selected[p])]
  assert len(chosen)==4
  assert all(len({g for row in schedule for g,members in enumerate(row) if p in members})==5 for p in chosen)
  actual=[sum(p in row[0] for p in chosen) for row in schedule]
  assert actual==list(pattern)
  result['selected_witness_players']=chosen
  write_csv(directory/'schedule.csv',schedule)
  extension=[[[p+1 for p in range(20) if solver.Value(groups[r][p])==g] for g in range(5)] for r in range(5)]
  result['extension_audit']=validate(extension,20,5)
  write_csv(directory/'extension20.csv',extension)
 (directory/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result),flush=True)
 return result

from concurrent.futures import ThreadPoolExecutor,as_completed
results=[]
with ThreadPoolExecutor(max_workers=2) as executor:
 futures={executor.submit(run_case,pattern):pattern for pattern in patterns}
 for future in as_completed(futures):
  result=future.result();results.append(result)
  (root/'results.json').write_text(json.dumps(results,indent=2)+'\n')
  with (root/'README.md').open('a') as f:f.write(f'\nCase {result["case"]}: {result["status"]}, {result["solver_seconds"]:.6f} seconds.\n')
  (root/'progress.json').write_text(json.dumps(dict(completed=results,pending=['_'.join(map(str,p)) for task,p in futures.items() if not task.done()]),indent=2)+'\n')
summary=dict(completed=True,cases=results,all_infeasible=all(r['status']=='INFEASIBLE' for r in results),improvement_found=any('total_spread' in r for r in results),unresolved_cases=[r['case'] for r in results if r['status']=='UNKNOWN'])
(root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(root/'progress.json').write_text(json.dumps(dict(pending=[],completed=results),indent=2)+'\n')
with (root/'README.md').open('a') as f:f.write('\nAll four cases completed. '+('(4,79) globally optimal.' if summary['all_infeasible'] else 'An improvement was found; global total optimality is not implied.' if summary['improvement_found'] else 'UNKNOWN cases leave total optimality unresolved.')+'\n')
print(json.dumps(summary),flush=True)
