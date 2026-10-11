import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from esgp_v2 import read_schedule,validate
root=Path(__file__).resolve().parent
checkpoint=json.loads((root/'checkpoint.json').read_text())
audited=0;best=(0,0)
for c in checkpoint['classes']:
 if c['inherited'] and c['id']==0:
  directory=root.parent/'n19_via20_ordering_20261011'
  source=read_schedule(directory/'source.csv',20,5)
  for removed in range(1,21):
   d=directory/('delete_%02d'%removed)
   metrics=validate(read_schedule(d/'schedule.csv',19,5),19,5)
   saved=json.loads((d/'result.json').read_text())
   assert saved['status']=='OPTIMAL'
   assert saved['objective_bound']==96*metrics['minimum_spread']+metrics['total_spread']
   best=max(best,(metrics['minimum_spread'],metrics['total_spread']));audited+=1
 elif c['inherited']:
  directory=Path(c['source']).parent
  validate(read_schedule(directory/'schedule.csv',20,5),20,5)
  for removed in range(1,21):
   d=directory/('delete_%02d'%removed)
   metrics=validate(read_schedule(d/'schedule.csv',19,5),19,5)
   saved=json.loads((d/'result.json').read_text())
   assert saved['status']=='OPTIMAL'
   assert saved['bound']==96*metrics['minimum_spread']+metrics['total_spread']
   best=max(best,(metrics['minimum_spread'],metrics['total_spread']));audited+=1
 else:
  directory=root/('class_%03d'%c['id'])
  validate(read_schedule(directory/'source.csv',20,5),20,5)
  for removed in range(1,21):
   d=directory/('delete_%02d'%removed)
   metrics=validate(read_schedule(d/'schedule.csv',19,5),19,5)
   saved=json.loads((d/'result.json').read_text())
   assert saved['status']=='OPTIMAL'
   assert saved['bound']==96*metrics['minimum_spread']+metrics['total_spread']
   best=max(best,(metrics['minimum_spread'],metrics['total_spread']));audited+=1

result=dict(audited_deletion_optima=audited,best_score=best)
(root/'ordering_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
