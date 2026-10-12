"""Validate GroupMixer assignments independently under ESGP five-round rules."""
import csv,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from esgp_v2 import validate
root=Path(__file__).resolve().parent
expected={15:(3,51),16:(2,51),20:(5,100),21:(5,105),22:(5,110),24:(5,120)}
results=[]
for n,target in expected.items():
 path=root/f'n{n}_result.json'
 if not path.exists():continue
 data=json.loads(path.read_text())
 if isinstance(data,str):data=json.loads(data)
 result=data['result'];assert result and result['complete']
 scenario=result['input']['scenario'];groups=[g['id'] for g in scenario['groups']]
 assert scenario['session_count']==5 and len(scenario['people'])==n
 assert [g['capacity'] for g in scenario['groups']]==sorted(g['capacity'] for g in scenario['groups'])
 schedule=[[[] for g in groups] for r in range(5)]
 for item in result['solution']['assignments']:
  schedule[item['session_id']][groups.index(item['group_id'])].append(int(item['person_id'].split('_')[-1]))
 metrics=validate(schedule,n,5);score=(metrics['minimum_spread'],metrics['total_spread'])
 with (root/f'groupmixer_n{n}.csv').open('w',newline='') as f:
  w=csv.writer(f)
  for r,row in enumerate(schedule,1):
   for g,members in enumerate(row,1):w.writerow([r,g,*sorted(members)])
 results.append(dict(players=n,rounds=5,expected=target,score=score,matched=score==target,result_id=result['result_id'],metrics=metrics))
(root/'audit.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
