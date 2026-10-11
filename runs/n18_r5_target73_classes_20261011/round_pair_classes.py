"""Enumerate low-trace first-two-round matrices relevant to minimum spread four."""
import itertools,json
from pathlib import Path
sizes=(3,3,4,4,4)
perms=[a+b for a in itertools.permutations(range(2)) for b in itertools.permutations(range(2,5))]
options=[[tuple(int(g in selected) for g in range(5)) for selected in itertools.combinations(range(5),size)] for size in sizes]
matrices=[]
for rows in itertools.product(*options):
 if all(sum(row[g] for row in rows)==sizes[g] for g in range(5)):
  matrices.append(rows)
def key(rows):
 candidates=[]
 for p in perms:
  a=tuple(tuple(rows[p[r]][p[c]] for c in range(5)) for r in range(5))
  candidates.extend((a,tuple(zip(*a))))
 return min(candidates)
reps=sorted({key(m) for m in matrices if sum(m[g][g] for g in range(5))<=1})
result={'sizes':sizes,'matrices':len(matrices),'low_trace_matrices':sum(sum(m[g][g] for g in range(5))<=1 for m in matrices),'representatives':reps,'classes':len(reps)}
Path(__file__).with_name('round_pair_classes.json').write_text(json.dumps(result,indent=2)+'\n')
print({k:v for k,v in result.items() if k!='representatives'})
