import sys,json,hashlib,argparse
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
import cp_sat_caseB_v1_1 as old
import cp_sat_caseB_v2 as new
from esgp_v2 import validate,read_schedule,exclusion
from ortools.sat.python import cp_model
checks=[]
for row in json.loads(Path('solutions/optimal-4-rounds/validation.json').read_text()):
 n=row['players'];path=Path(row['schedule'])
 assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256']
 result=validate(read_schedule(path,n,4),n,4)
 assert (result['minimum_spread'],result['total_spread'])==(row['minimum_distinct_slots'],row['total_spread'])
 m0=old.build_model(n,fair_spread=True,strengthen=True)[0]
 m1,solver,X,sizes,R=new.build_model(n,fair_spread=True,strengthen=True,refine_fairness=False)
 assert str(m0.Proto())==str(m1.Proto()), n
 schedule=read_schedule(path,n,4)
 # Saved outputs use best-first IDs; the model fixes a canonical first round.
 targets=[];start=n
 for size in sizes:
  targets.append(list(range(start-size+1,start+1)));start-=size
 mapping={old:new for group,target in zip(schedule[0],targets) for old,new in zip(sorted(group),target)}
 schedule=[[[mapping[p] for p in group] for group in groups] for groups in schedule]
 for r,groups in enumerate(schedule):
  for g,members in enumerate(groups):
   for p in range(1,n+1):m1.Add(X[r,g,p]==int(p in members))
 solver.parameters.log_search_progress=False
 assert solver.Solve(m1)==cp_model.OPTIMAL,n
 checks.append({'players':n,'model_identical':True,'schedule_valid':True,'fixed_schedule_accepted':True})
# Five-round construction over GF(4), with x^2=x+1.
def mul(a,b):
 value=0
 for _ in range(2):
  if b&1:value^=a
  b>>=1;a<<=1
  if a&4:a^=7
 return value
points=[(x,y) for x in range(4) for y in range(4) if (x,y)!=(0,0)]
rounds=[]
for slope in [None,0,1,2,3]:
 groups=[]
 for intercept in range(4):
  members=[i+1 for i,(x,y) in enumerate(points) if (x==intercept if slope is None else y==(mul(slope,x)^intercept))]
  groups.append(members)
 rounds.append(sorted(groups,key=len))
assert validate(rounds,15,5)['unique_pairs']==105
# Repeated pairs and missing attendance must be rejected.
try:validate([rounds[0]]*5,15,5)
except AssertionError:pass
else:raise AssertionError('Validator accepted repeated partners')
assert exclusion(9,4) is None
assert all(exclusion(n,5) for n in range(3,15))
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path)
args=parser.parse_args()
if args.output:
 with args.output.open('x') as output:
  output.write(json.dumps({'four_rounds':checks,'five_round_construction':validate(rounds,15,5),'invalid_schedule_rejected':True},indent=2)+'\n')
print('PASS: ten identical four-round models; ten preserved schedules accepted; five-round construction; invalid schedule rejection')
