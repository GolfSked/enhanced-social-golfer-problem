"""Search distinct n20/R5 structures and optimize all their n19 deletions."""
import csv, hashlib, itertools, json, sys, time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from esgp_v2 import read_schedule,validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent

def save_schedule(path,schedule):
 with path.open('w',newline='') as f:
  w=csv.writer(f)
  for r,row in enumerate(schedule,1):
   for g,members in enumerate(row,1):w.writerow([r,g,*members])

def canonical(schedule):
 """Exact canonical form under player, round and within-round group relabelling.

 Any two rounds form a 5x5 grid with exactly one missing cell in every row
 and column. Choose the ordered round pair and row ordering; missing cells
 force column ordering. Players then have unique off-diagonal coordinates.
 Sorting all remaining group/round partitions removes the residual labels.
 All 20*120 possibilities are covered.
 """
 best=None
 for a,b in itertools.permutations(range(5),2):
  columns={p:g for g,members in enumerate(schedule[b]) for p in members}
  missing=[next(iter(set(range(5))-{columns[p] for p in members}))
           for members in schedule[a]]
  assert len(set(missing))==5
  for order in itertools.permutations(range(5)):
   colmap={missing[old]:new for new,old in enumerate(order)}
   mapping={p:5*i+colmap[columns[p]] for i,old in enumerate(order)
            for p in schedule[a][old]}
   encoding=tuple(sorted(tuple(sorted(tuple(sorted(mapping[p] for p in members))
                  for members in schedule[r])) for r in range(5) if r not in (a,b)))
   if best is None or encoding<best:best=encoding
 return best

def optimize(original,removed,directory):
 remaining=[p for p in range(1,21) if p!=removed]
 labels={p:i+1 for i,p in enumerate(remaining)}
 groups=[sorted([[labels[p] for p in g if p!=removed] for g in row],key=len)
         for row in original]
 validate(groups,19,5)
 model=cp_model.CpModel()
 slots=[]
 for r in range(5):
  row=[model.NewIntVar(0,0,f'slot_{r}_0')]+[
    model.NewIntVar(1,4,f'slot_{r}_{g}') for g in range(1,5)]
  model.AddAllDifferent(row)
  if r==0:
   for g in range(5):model.Add(row[g]==g)
  slots.append(row)
 spreads=[]
 for p in range(1,20):
  positions=[slots[r][next(g for g,members in enumerate(groups[r]) if p in members)] for r in range(5)]
  used=[]
  for tee in range(5):
   occurrences=[]
   for r,pos in enumerate(positions):
    b=model.NewBoolVar(f'eq_{p}_{tee}_{r}')
    model.Add(pos==tee).OnlyEnforceIf(b)
    model.Add(pos!=tee).OnlyEnforceIf(b.Not());occurrences.append(b)
   u=model.NewBoolVar(f'used_{p}_{tee}')
   model.AddMaxEquality(u,occurrences);used.append(u)
  spread=model.NewIntVar(1,5,f'spread_{p}')
  model.Add(spread==sum(used));spreads.append(spread)
 minimum=model.NewIntVar(1,4,'minimum')
 model.AddMinEquality(minimum,spreads)
 model.Maximize(96*minimum+sum(spreads))
 solver=cp_model.CpSolver()
 solver.parameters.max_time_in_seconds=60
 solver.parameters.num_search_workers=10
 solver.parameters.random_seed=101
 solver.parameters.log_search_progress=True
 solver.parameters.log_to_stdout=False
 directory.mkdir()
 with (directory/'solver.log').open('w') as log:
  solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
  status=solver.Solve(model)
 result=dict(removed=removed,status=solver.StatusName(status),
    seconds=solver.WallTime(),bound=solver.BestObjectiveBound(),player_mapping=labels)
 ordered=None
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  ordered=[]
  for r in range(5):
   row=[None]*5
   for g,members in enumerate(groups[r]):row[solver.Value(slots[r][g])]=members
   ordered.append(row)
  result.update(validate(ordered,19,5))
  save_schedule(directory/'schedule.csv',ordered)
 (directory/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 return result,ordered

def generate_model():
 model=cp_model.CpModel()
 cells=[(i,j) for i in range(5) for j in range(5) if i!=j]
 slots=[[model.NewIntVar(0,4,f'g_{r}_{p}') for p in range(20)] for r in range(5)]
 for p,(i,j) in enumerate(cells):
  model.Add(slots[0][p]==i);model.Add(slots[1][p]==j)
 for r in range(2,5):
  for g in range(5):
   members=[]
   for p in range(20):
    b=model.NewBoolVar(f'in_{r}_{g}_{p}')
    model.Add(slots[r][p]==g).OnlyEnforceIf(b)
    model.Add(slots[r][p]!=g).OnlyEnforceIf(b.Not());members.append(b)
   model.Add(sum(members)==4)
  # Canonical group names in each remaining round: order of first appearance.
  model.Add(slots[r][0]==0)
  maximum=slots[r][0]
  for p in range(1,20):
   model.Add(slots[r][p]<=maximum+1)
   nxt=model.NewIntVar(0,4,f'prefix_{r}_{p}')
   model.AddMaxEquality(nxt,[maximum,slots[r][p]]);maximum=nxt
 for r,s in itertools.combinations(range(5),2):
  encodings=[]
  for p in range(20):
   code=model.NewIntVar(0,24,f'pair_{r}_{s}_{p}')
   model.Add(code==5*slots[r][p]+slots[s][p]);encodings.append(code)
  model.AddAllDifferent(encodings)
 return model,slots

