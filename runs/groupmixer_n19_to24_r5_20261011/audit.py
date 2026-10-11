import csv,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from esgp_v2 import validate,group_distribution
root=Path(__file__).resolve().parent
n=int(sys.argv[1]);case=root/f'n{n}';data=json.loads((case/'result.json').read_text())
groups=data['scenario']['groups'];rounds=data['scenario']['session_count']
assert rounds==5 and [g['capacity'] for g in groups]==group_distribution(n)
assert len(data['scenario']['people'])==n
slots={g['id']:i for i,g in enumerate(groups)};schedule=[[[] for g in groups] for r in range(rounds)]
for row in data['result']['solution']['assignments']:
 p=int(data['person_names'][row['person_id']].removeprefix('Player '));schedule[row['session_id']][slots[row['group_id']]].append(p)
try:
 result=validate(schedule,n,rounds);result['valid']=True
except AssertionError as error:
 result={'valid':False,'rejection_reason':str(error)}
result.update(result_id=data['base_result_id'],reported_elapsed_ms=data['result']['solution']['elapsed_time_ms'],app_cost=data['result']['solution']['total_cost'])
(case/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
if result['valid']:
 with (case/'schedule.csv').open('w',newline='') as f:
  writer=csv.writer(f)
  for r,gs in enumerate(schedule,1):
   for g,players in enumerate(gs,1):writer.writerow([r,g,*sorted(players)])
print(json.dumps(result))
