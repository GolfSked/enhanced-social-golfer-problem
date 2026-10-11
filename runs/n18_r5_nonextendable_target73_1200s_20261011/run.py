"""Complete nonextendable n18/R5 improvement test via an odd-cycle witness."""
import csv,hashlib,itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from boolean_model_snapshot import build_model
from esgp_v2 import read_schedule,validate
from ortools.sat.python import cp_model
root=Path(__file__).resolve().parent

def triple_graph(schedule):
 adjacency={v:set() for v in range(10)}
 for r in range(5):adjacency[2*r].add(2*r+1);adjacency[2*r+1].add(2*r)
 for p in range(1,19):
  triples=[2*r+g for r,row in enumerate(schedule) for g,members in enumerate(row[:2]) if p in members]
  assert len(triples) in (1,2)
  if len(triples)==2:
   a,b=triples;adjacency[a].add(b);adjacency[b].add(a)
 colors={};bipartite=True
 for v in adjacency:
  if v in colors:continue
  colors[v]=0;queue=[v]
  while queue:
   a=queue.pop()
   for b in adjacency[a]:
    if b not in colors:colors[b]=1-colors[a];queue.append(b)
    elif colors[b]==colors[a]:bipartite=False
 return adjacency,bipartite

def build(target,pin_five=True,odd_cycle=True):
 model,solver,X,sizes,rounds=build_model(18,rounds=5,fair_spread=True,strengthen=True,time_limit=1200,workers=10,seed=101)
 assert sizes==[3,3,4,4,4]
 distinct={int(v.name.rsplit('_',1)[1]):model.GetIntVarFromProtoIndex(i) for i,v in enumerate(model.Proto().variables) if v.name.startswith('distinct_pos_')}
 for p in range(1,19):
  model.Add(distinct[p]>=4)
  extra=model.NewBoolVar(f'target_extra_{p}')
  model.Add(sum(X[r,g,p] for r in range(5) for g in range(2,5))==3+extra)
  model.Add(distinct[p]<=5-extra)
 model.Add(sum(distinct.values())>=target)
 model.Add(sum(distinct.values())<=84)
 if pin_five:
  for r in range(5):model.Add(X[r,r,18]==1)
 model.ClearObjective()
 cycle_arcs=[]
 if odd_cycle:
  edges={}
  for a,b in itertools.combinations(range(10),2):
   if a//2==b//2:
    edge=model.NewBoolVar(f'edge_{a}_{b}');model.Add(edge==1)
   else:
    common=[]
    for p in range(1,19):
     joint=model.NewBoolVar(f'common_{a}_{b}_{p}')
     model.Add(joint<=X[a//2,a%2,p]);model.Add(joint<=X[b//2,b%2,p])
     model.Add(joint>=X[a//2,a%2,p]+X[b//2,b%2,p]-1);common.append(joint)
    edge=model.NewBoolVar(f'edge_{a}_{b}')
    model.Add(edge==sum(common))
   edges[a,b]=edge
  arcs=[];used=[]
  for v in range(10):
   inactive=model.NewBoolVar(f'cycle_inactive_{v}')
   arcs.append((v,v,inactive));used.append(1-inactive)
  for (a,b),edge in edges.items():
   for tail,head in ((a,b),(b,a)):
    arc=model.NewBoolVar(f'cycle_arc_{tail}_{head}')
    model.Add(arc<=edge);arcs.append((tail,head,arc))
    cycle_arcs.append((tail,head,arc))
  model.AddCircuit(arcs)
  half=model.NewIntVar(1,4,'cycle_half_length')
  model.Add(sum(used)==2*half+1)
 assert not model.Validate(),model.Validate()
 return model,solver,X,cycle_arcs

def extract(solver,X):
 return [[[p for p in range(1,19) if solver.Value(X[r,g,p])] for g in range(5)] for r in range(5)]

source=root.parent/'n18_r5_integer_fair_1200s_20261011/schedule.csv'
baseline=read_schedule(source,18,5)
assert triple_graph(baseline)[1]
labels={};end=18
for members in baseline[0]:
 for old,new in zip(members,range(end-len(members)+1,end+1)):labels[old]=new
 end-=len(members)
baseline=[[[labels[p] for p in group] for group in row] for row in baseline]
controls=[]
for odd in (False,True):
 model,solver,X,_=build(72,pin_five=False,odd_cycle=odd)
 for r,row in enumerate(baseline):
  for g,members in enumerate(row):
   for p in range(1,19):model.Add(X[r,g,p]==int(p in members))
 solver.parameters.max_time_in_seconds=30
 status=solver.Solve(model)
 assert status==(cp_model.INFEASIBLE if odd else cp_model.OPTIMAL)
 controls.append(dict(odd_cycle_required=odd,status=solver.StatusName(status),seconds=solver.WallTime()))
(root/'controls.json').write_text(json.dumps(controls,indent=2)+'\n')
model,solver,X,cycle_arcs=build(73)
model.ExportToFile(str(root/'model.pbtxt'))
(root/'configuration.json').write_text(json.dumps(dict(players=18,rounds=5,minimum_target=4,total_target=73,seconds=1200,workers=10,seed=101,nonextendability='Existential odd simple cycle in the triple graph',hint=None,sha256={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ('run.py','boolean_model_snapshot.py')}),indent=2)+'\n')
solver.parameters.log_to_stdout=False
print('Positive/negative controls passed; starting nonextendable target73',flush=True)
with (root/'solver.log').open('w') as log:
 solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
 status=solver.Solve(model)
result=dict(status=solver.StatusName(status),solver_seconds=solver.WallTime(),configured_seconds=1200,minimum_target=4,total_target=73)
if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
 schedule=extract(solver,X);result.update(validate(schedule,18,5))
 adjacency,bipartite=triple_graph(schedule)
 assert not bipartite and result['minimum_spread']>=4 and result['total_spread']>=73
 chosen=[(a,b) for a,b,arc in cycle_arcs if solver.Value(arc)]
 assert len(chosen)%2==1 and len(chosen)>=3
 assert all(b in adjacency[a] for a,b in chosen)
 result['odd_cycle_arcs']=chosen;result['independent_graph_bipartite']=bipartite
 with (root/'schedule.csv').open('w',newline='') as f:
  writer=csv.writer(f)
  for r,row in enumerate(schedule,1):
   for g,members in enumerate(row,1):writer.writerow([r,g,*members])
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n')
meaning=('Together with the proved extendable-family bound, (4,72) is globally optimal.' if status==cp_model.INFEASIBLE else 'Validated improvement in the nonextendable family; total optimality not yet proved.' if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else 'UNKNOWN leaves nonextendable improvements unresolved; best remains (4,72).')
with (root/'README.md').open('a') as f:f.write(f'\nCompleted: {result["status"]} after {solver.WallTime():.6f} seconds. {meaning}\n')
print(json.dumps(result,indent=2),flush=True)
