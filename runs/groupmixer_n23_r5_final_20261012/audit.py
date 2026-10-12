import csv,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from esgp_v2 import validate
root=Path(__file__).resolve().parent
data=json.loads((root/'result.json').read_text());result=data['result'];assert data['generation_status']=='completed' and result['complete']
scenario=result['input']['scenario'];assert scenario['session_count']==5 and len(scenario['people'])==23
assert [g['capacity'] for g in scenario['groups']]==[3,4,4,4,4,4]
groups=[g['id'] for g in scenario['groups']];schedule=[[[] for g in groups] for _ in range(5)]
for a in result['solution']['assignments']:schedule[a['session_id']][groups.index(a['group_id'])].append(int(a['person_id'].split('_')[-1]))
metrics=validate(schedule,23,5);assert (metrics['minimum_spread'],metrics['total_spread'])==(5,115)
with (root/'groupmixer_n23.csv').open('w',newline='') as f:
 w=csv.writer(f)
 for r,row in enumerate(schedule,1):
  for g,people in enumerate(row,1):w.writerow([r,g,*sorted(people)])
audit=dict(players=23,rounds=5,score=[5,115],matched=True,result_id=result['result_id'],metrics=metrics)
(root/'audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit,indent=2))
