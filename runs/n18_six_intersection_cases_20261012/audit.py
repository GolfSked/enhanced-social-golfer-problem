"""Audit witnesses and independently encode nonextendability by 16 colourings."""
from structural_snapshot import *
from concurrent.futures import ThreadPoolExecutor
coverage=json.loads((root/'coverage.json').read_text())
inherited=json.loads((root/'inherited_orbits.json').read_text())
previous=root.parent/'n18_nonextendable_enumeration_pilot_20261011'
checks=[]
for i,assignments in enumerate(inherited):
 schedule=read_schedule(previous/f'class_{i:04d}/source.csv',18,5)
 assert assignments==[list(x) for x in orbit(schedule)]
 for assignment in assignments:
  decoded=decode(assignment);assert not bipartite(decoded)
 result=json.loads((previous/f'class_{i:04d}/ordering/result.json').read_text())
 witness=read_schedule(previous/f'class_{i:04d}/ordering/schedule.csv',18,5)
 measured=validate(witness,18,5)
 assert (measured['minimum_spread'],measured['total_spread'])==(result['minimum_spread'],result['total_spread'])
 assert result['status']=='OPTIMAL' and result['objective_bound']==91*result['minimum_spread']+result['total_spread']
 checks.append(dict(class_id=i,validated_assignments=len(assignments),score=[result['minimum_spread'],result['total_spread']]))
write=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n')
write(root/'audit_witnesses.json',checks)

def audit(case):
 # Keep the independently justified normalization; replace the entire odd-cycle encoding.
 model,slots=build(odd=False)
 members={}
 for r in range(5):
  for g in range(2):
   for p in range(18):
    b=model.NewBoolVar(f'audit_member_{r}_{g}_{p}')
    model.Add(slots[r][p]==g).OnlyEnforceIf(b)
    model.Add(slots[r][p]!=g).OnlyEnforceIf(b.Not());members[r,g,p]=b
 edges={}
 for a,b in itertools.combinations(range(10),2):
  if a//2==b//2:continue
  joint=[]
  for p in range(18):
   v=model.NewBoolVar(f'audit_joint_{a}_{b}_{p}')
   model.AddMultiplicationEquality(v,[members[a//2,a%2,p],members[b//2,b%2,p]]);joint.append(v)
  edge=model.NewBoolVar(f'audit_edge_{a}_{b}');model.AddMaxEquality(edge,joint);edges[a,b]=edge
 # Matching edges force opposite colours within each round. Fix vertex0 colour0.
 # These sixteen colourings are all possible proper colourings of those five edges.
 for tail in itertools.product((0,1),repeat=4):
  bits=(0,)+tail;colors=[c for bit in bits for c in (bit,1-bit)]
  model.AddBoolOr([edge for (a,b),edge in edges.items() if colors[a]==colors[b]])
 for v,value in zip(slots[1],case['second_round']):model.Add(v==value)
 variables=[v for row in slots[1:] for v in row]
 for assignments in inherited:model.AddForbiddenAssignments(variables,assignments)
 assert not model.Validate()
 solver=cp_model.CpSolver();solver.parameters.num_search_workers=5;solver.parameters.max_time_in_seconds=1200
 status=solver.Solve(model)
 result=dict(case=case['case'],status=solver.StatusName(status),seconds=solver.WallTime(),independent_nonbipartite_encoding='all sixteen matching-compatible two-colourings rejected')
 write(root/f'audit_case_{case["case"]:02d}.json',result);print(json.dumps(result),flush=True)
 return result
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(audit,coverage))
 write(root/'audit.json',dict(witnesses=checks,cases=results,all_independent_cases_infeasible=all(x['status']=='INFEASIBLE' for x in results)))
