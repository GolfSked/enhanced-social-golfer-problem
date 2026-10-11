"""Exhaust all five-round structures and tee orderings for 16 players.

Each round consists of four fours. Pair uniqueness forces every pair of
rounds to intersect in a 4x4 all-ones matrix. Global player relabelling can
therefore fix the first two *ordered* rounds as rows and columns of a grid.
Every later group is a permutation transversal of that grid. Enumerate all
partitions into transversals, every pair-compatible triple of partitions,
and every tee ordering of those three rounds. Their round order is immaterial.
"""
import csv,itertools,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from esgp_v2 import validate
root=Path(__file__).resolve().parent
started=time.monotonic()
transversals=[frozenset(r*4+perm[r] for r in range(4)) for perm in itertools.permutations(range(4))]
partitions=set()
def cover(remaining,chosen):
 if not remaining:
  partitions.add(tuple(sorted(tuple(sorted(g)) for g in chosen)))
  return
 first=min(remaining)
 for group in transversals:
  if first in group and group<=remaining:cover(remaining-group,chosen+[group])
cover(frozenset(range(16)),[])
partitions=sorted(partitions)
def compatible(a,b):
 return all(len(set(g)&set(h))<=1 for g in a for h in b)
triples=[indices for indices in itertools.combinations(range(len(partitions)),3)
         if all(compatible(partitions[a],partitions[b]) for a,b in itertools.combinations(indices,2))]
permutations=list(itertools.permutations(range(4)))
options=[]
for groups in partitions:
 choices=[]
 for permutation in permutations:
  mask=[0]*16
  for slot,g in enumerate(permutation):
   for p in groups[g]:mask[p]=1<<slot
  choices.append(mask)
 options.append(choices)
initial=[(1<<(p//4))|(1<<(p%4)) for p in range(16)]
best=(-1,-1);winner=None;counts={};checked=0
for triple in triples:
 for ordering in itertools.product(range(24),repeat=3):
  a,b,c=(options[g][i] for g,i in zip(triple,ordering))
  spread=[(initial[p]|a[p]|b[p]|c[p]).bit_count() for p in range(16)]
  score=(min(spread),sum(spread));checked+=1
  counts[str(score)]=counts.get(str(score),0)+1
  if score>best:best=score;winner=(triple,ordering)
rows=[[r*4+c+1 for c in range(4)] for r in range(4)]
columns=[[r*4+c+1 for r in range(4)] for c in range(4)]
triple,ordering=winner
schedule=[rows,columns]+[[[p+1 for p in partitions[g][index]] for index in permutations[i]] for g,i in zip(triple,ordering)]
metrics=validate(schedule,16,5)
with (root/'global_schedule.csv').open('w',newline='') as output:
 writer=csv.writer(output)
 for r,groups in enumerate(schedule,1):
  for g,members in enumerate(groups,1):writer.writerow([r,g,*members])
result={'scope':'Global exhaustive proof under the prescribed 16-player five-round rules',
 'transversals':len(transversals),'partitions':len(partitions),'compatible_partition_triples':len(triples),
 'orderings_checked':checked,'minimum_spread':best[0],'total_spread':best[1],
 'validation':metrics,'score_counts':counts,'elapsed_seconds':time.monotonic()-started}
(root/'global_result.json').write_text(json.dumps(result,indent=2)+'\n')
(root/'partitions.json').write_text(json.dumps({'partitions':partitions,'compatible_triples':triples},indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='score_counts'},indent=2))
