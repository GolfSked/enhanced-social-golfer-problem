from structural_snapshot import *
coverage=json.loads((root/'coverage.json').read_text())
representatives=[tuple(tuple(int(g in item['second_round'][sum(sizes[:r]):sum(sizes[:r+1])]) for g in range(5)) for r in range(5)) for item in coverage]
counts=[0]*6
for rows in itertools.product(*(itertools.combinations(range(5),s) for s in sizes)):
 if any(sum(g in row for row in rows)!=sizes[g] for g in range(5)):continue
 matrix=tuple(tuple(int(g in row) for g in range(5)) for row in rows)
 hits=set()
 for ro in orders:
  for co in orders:
   transformed=tuple(tuple(matrix[r][c] for c in co) for r in ro)
   for i,rep in enumerate(representatives):
    if transformed==rep:hits.add(i)
 assert len(hits)==1
 counts[hits.pop()]+=1
assert counts==[x['labelled_count'] for x in coverage]
previous=root.parent/'n18_nonextendable_enumeration_pilot_20261011';scores=[]
for i in range(3):
 schedule=read_schedule(previous/f'class_{i:04d}/source.csv',18,5)
 memberships=[[next(g for g,m in enumerate(row) if p in m) for p in range(1,19)] for row in schedule]
 best=(0,0)
 for tail in itertools.product(orders,repeat=4):
  positions=[memberships[0]]+[[perm[g] for g in memberships[r]] for r,perm in enumerate(tail,1)]
  spread=[len({positions[r][p] for r in range(5)}) for p in range(18)]
  best=max(best,(min(spread),sum(spread)))
 saved=json.loads((previous/f'class_{i:04d}/ordering/result.json').read_text())
 assert best==(saved['minimum_spread'],saved['total_spread'])
 scores.append(best)
validated=0;best=(0,0)
for resultpath in (root.parent/'n18_via20_ordering_20261011').glob('class_*/result.json'):
 result=json.loads(resultpath.read_text());metrics=validate(read_schedule(resultpath.parent/'schedule.csv',18,5),18,5)
 score=(metrics['minimum_spread'],metrics['total_spread'])
 assert score==(result['minimum_spread'],result['total_spread'])
 assert result['status']=='OPTIMAL' and result['objective_bound']==91*score[0]+score[1]
 best=max(best,score);validated+=1
assert validated==228 and best==(4,72)
report=dict(labelled_matrices=sum(counts),class_counts=counts,every_matrix_has_exactly_one_representative=True,brute_force_orderings_per_nonextendable_class=12**4,nonextendable_optima=scores,extendable_witnesses_revalidated=validated,extendable_best=best)
(root/'audit_coverage_ordering.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
