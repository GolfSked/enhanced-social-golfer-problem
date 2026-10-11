"""Exhaust all tee-slot orderings of the saved five-round structure."""
import csv,itertools,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from esgp_v2 import read_schedule,validate
root=Path(__file__).resolve().parent
source=Path('runs/v2_pilot_20261011/rounds5/n16/schedule.csv')
schedule=read_schedule(source,16,5)
assert validate(schedule,16,5)['unique_pairs']==120
permutations=list(itertools.permutations(range(4)))
# A common permutation of slots leaves the objective unchanged, fixing round one.
initial=[0]*16
for g,members in enumerate(schedule[0]):
 for p in members:initial[p-1]=1<<g
options=[]
for groups in schedule[1:]:
 choices=[]
 for permutation in permutations:
  masks=[0]*16
  for slot,g in enumerate(permutation):
   for p in groups[g]:masks[p-1]=1<<slot
  choices.append(masks)
 options.append(choices)
best=(-1,-1);winner=None;counts={};started=time.monotonic()
for indices in itertools.product(range(24),repeat=4):
 a,b,c,d=(options[r][i] for r,i in enumerate(indices))
 spreads=[(initial[p]|a[p]|b[p]|c[p]|d[p]).bit_count() for p in range(16)]
 score=(min(spreads),sum(spreads))
 counts[str(score)]=counts.get(str(score),0)+1
 if score>best:best=score;winner=indices
ordered=[schedule[0]]+[[schedule[r+1][g] for g in permutations[i]] for r,i in enumerate(winner)]
metrics=validate(ordered,16,5)
with (root/'schedule.csv').open('w',newline='') as output:
 writer=csv.writer(output)
 for r,groups in enumerate(ordered,1):
  for g,members in enumerate(groups,1):writer.writerow([r,g,*members])
result={'scope':'Tee-slot ordering of fixed input structure; not a global proof', 'input':str(source),'orderings_checked':24**4,'elapsed_seconds':time.monotonic()-started,'best':best,'permutation_indices':winner,'score_counts':counts,'validation':metrics}
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='score_counts'},indent=2))
