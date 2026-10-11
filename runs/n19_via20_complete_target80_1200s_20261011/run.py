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

source=root.parent/'groupmixer_n19_to24_r5_20261011/n19/schedule.csv'
schedule=read_schedule(source,19,5)
assert validate(schedule,19,5)['total_spread']==79
hint=normalize(schedule)
# Check normalization directly, including every retained tee-time assignment.
normalized=[[[p for p in range(1,20) if hint[1][r][hint[0][r][p]]==g]
             for g in range(5)] for r in range(5)]
audit=validate(normalized,19,5)
assert (audit['minimum_spread'],audit['total_spread'])==(4,79)
write_csv(root/'normalized_baseline.csv',normalized)
# Positive-control solve ensures that the new formulation admits the witness.
control,*_,control_tees=build(79,hint)
control_solver=cp_model.CpSolver()
control_solver.parameters.max_time_in_seconds=30
control_solver.parameters.num_search_workers=8
control_status=control_solver.Solve(control)
assert control_status in (cp_model.OPTIMAL,cp_model.FEASIBLE),'Positive control failed'
control_audit=validate(extract(control_solver,control_tees),19,5)
(root/'positive_control.json').write_text(json.dumps(dict(status=control_solver.StatusName(control_status),seconds=control_solver.WallTime(),**control_audit),indent=2)+'\n')
model,groups,tee_maps,tees=build(80,hint)
model.ExportToFile(str(root/'model.pbtxt'))
(root/'configuration.json').write_text(json.dumps(dict(players=19,rounds=5,minimum_target=4,total_target=80,seconds=1200,workers=8,seed=101,deleted_coordinate=[0,1],hint='Normalized validated (4,79) witness; infeasible for target80',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
solver=cp_model.CpSolver()
solver.parameters.max_time_in_seconds=1200
solver.parameters.num_search_workers=8
solver.parameters.random_seed=101
solver.parameters.log_search_progress=True
solver.parameters.log_to_stdout=False
print('Positive control passed; launching complete target80',flush=True)
with (root/'solver.log').open('w') as log:
 solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
 status=solver.Solve(model)
result=dict(status=solver.StatusName(status),solver_seconds=solver.WallTime(),configured_seconds=1200,minimum_target=4,total_target=80)
if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
 witness=extract(solver,tees);result.update(validate(witness,19,5))
 assert result['minimum_spread']>=4 and result['total_spread']>=80
 write_csv(root/'schedule.csv',witness)
 extension=[[[p+1 for p in range(20) if solver.Value(groups[r][p])==g] for g in range(5)] for r in range(5)]
 result['extension_audit']=validate(extension,20,5)
 write_csv(root/'extension20.csv',extension)
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n')
meaning=('(4,79) globally optimal: every improvement excluded.' if status==cp_model.INFEASIBLE else 'Validated improvement; feasibility status alone does not prove its total optimal.' if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else 'UNKNOWN leaves total unresolved; best remains (4,79).')
with (root/'README.md').open('a') as f:f.write(f'\nCompleted: {solver.StatusName(status)} after {solver.WallTime():.6f} seconds. {meaning}\n')
print(json.dumps(result,indent=2),flush=True)
