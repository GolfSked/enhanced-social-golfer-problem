"""Complete n19/R5 target using its normalized n20 extension."""
import csv,hashlib,itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from esgp_v2 import read_schedule,validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent
cells=[(i,j) for i in range(5) for j in range(5) if i!=j]

def normalize(schedule):
 extended=[[g+[20] if len(g)==3 else list(g) for g in row] for row in schedule]
 validate(extended,20,5)
 columns={p:g for g,members in enumerate(extended[1]) for p in members}
 missing=[next(iter(set(range(5))-{columns[p] for p in members})) for members in extended[0]]
 deleted_row=next(g for g,members in enumerate(extended[0]) if 20 in members)
 deleted_column=columns[20]
 row_one=missing.index(deleted_column)
 assert row_one!=deleted_row
 order=[deleted_row,row_one]+[i for i in range(5) if i not in (deleted_row,row_one)]
 rowmap={old:new for new,old in enumerate(order)}
 colmap={missing[old]:rowmap[old] for old in range(5)}
 player_map={p:cells.index((rowmap[g],colmap[columns[p]]))
             for g,members in enumerate(extended[0]) for p in members}
 assert player_map[20]==0
 structural=[];permutations=[]
 for r,row in enumerate(extended):
  if r==0:groupmap=rowmap
  elif r==1:groupmap=colmap
  else:
   deleted_group=next(g for g,members in enumerate(row) if 20 in members)
   order=[deleted_group]+[g for g in range(5) if g!=deleted_group]
   groupmap={old:new for new,old in enumerate(order)}
  assignments=[None]*20;tees=[None]*5
  for old,members in enumerate(row):
   tees[groupmap[old]]=rowmap[old]
   for p in members:assignments[player_map[p]]=groupmap[old]
  structural.append(assignments);permutations.append(tees)
 return structural,permutations

def build(target, hint):
 model=cp_model.CpModel()
 groups=[[model.NewIntVar(0,4,f'g_{r}_{p}') for p in range(20)] for r in range(5)]
 for p,(i,j) in enumerate(cells):
  model.Add(groups[0][p]==i);model.Add(groups[1][p]==j)
 for r in range(2,5):
  model.Add(groups[r][0]==0)
  for g in range(5):
   members=[]
   for p in range(20):
    b=model.NewBoolVar(f'member_{r}_{g}_{p}')
    model.Add(groups[r][p]==g).OnlyEnforceIf(b)
    model.Add(groups[r][p]!=g).OnlyEnforceIf(b.Not());members.append(b)
   model.Add(sum(members)==4)
 for r,s in itertools.combinations(range(5),2):
  codes=[]
  for p in range(20):
   code=model.NewIntVar(0,24,f'pair_{r}_{s}_{p}')
   model.Add(code==5*groups[r][p]+groups[s][p]);codes.append(code)
  model.AddAllDifferent(codes)
 tee_maps=[[model.NewIntVar(0,4,f'tee_map_{r}_{g}') for g in range(5)] for r in range(5)]
 for r in range(5):
  model.AddAllDifferent(tee_maps[r])
  deleted_group=1 if r==1 else 0
  model.Add(tee_maps[r][deleted_group]==0)
  if r==0:
   for g in range(5):model.Add(tee_maps[r][g]==g)
 tees={};spreads=[]
 for p in range(1,20):
  for r in range(5):
   tees[r,p]=model.NewIntVar(0,4,f'tee_{r}_{p}')
   model.AddElement(groups[r][p],tee_maps[r],tees[r,p])
  used=[]
  for g in range(5):
   occurrences=[]
   for r in range(5):
    b=model.NewBoolVar(f'at_{r}_{p}_{g}')
    model.Add(tees[r,p]==g).OnlyEnforceIf(b)
    model.Add(tees[r,p]!=g).OnlyEnforceIf(b.Not());occurrences.append(b)
   u=model.NewBoolVar(f'used_{p}_{g}')
   model.AddMaxEquality(u,occurrences);used.append(u)
  spread=model.NewIntVar(4,5,f'spread_{p}')
  model.Add(spread==sum(used));spreads.append(spread)
 model.Add(sum(spreads)>=target)
 model.Add(sum(spreads)<=91)
 if hint:
  assignments,permutations=hint
  for r in range(5):
   for p in range(20):model.AddHint(groups[r][p],assignments[r][p])
   for g in range(5):model.AddHint(tee_maps[r][g],permutations[r][g])
 assert not model.Validate(),model.Validate()
 return model,groups,tee_maps,tees

def extract(solver,tees):
 return [[[p for p in range(1,20) if solver.Value(tees[r,p])==g]
          for g in range(5)] for r in range(5)]

def write_csv(path,schedule):
 with path.open('w',newline='') as f:
  writer=csv.writer(f)
  for r,row in enumerate(schedule,1):
   for g,members in enumerate(row,1):writer.writerow([r,g,*members])

