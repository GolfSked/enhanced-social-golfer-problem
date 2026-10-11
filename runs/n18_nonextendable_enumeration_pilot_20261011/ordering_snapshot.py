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
 solver.parameters.num_search_workers=10
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

