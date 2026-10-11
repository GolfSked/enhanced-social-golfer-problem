import json,hashlib,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from esgp_v2 import read_schedule,validate
base=Path('runs/v2_pilot_20261011')
count=0
for summary in base.glob('*/summary.json'):
 data=json.loads(summary.read_text())
 for name,digest in data['source_sha256'].items():
  assert hashlib.sha256((summary.parent/name).read_bytes()).hexdigest()==digest
 for result in data['discovery']+data['results']:
  if result['status'] in ('OPTIMAL','FEASIBLE'):
   directory=summary.parent/('discovery' if result in data['discovery'] else '')/f"n{result['players']}"
   metrics=validate(read_schedule(directory/'schedule.csv',result['players'],result['rounds']),result['players'],result['rounds'])
   for k,v in metrics.items():
    assert json.dumps(v,sort_keys=True)==json.dumps(result[k],sort_keys=True),(directory,k)
   count+=1
stop=json.loads((base/'unknown_stop_smoke/summary.json').read_text())
assert not stop['minimum_proven'] and not stop['results']
assert stop['discovery'][-1]['status']=='UNKNOWN'
old=subprocess.check_output(['/usr/bin/git','show','HEAD:cp_sat_caseB_v1_1.py'])
assert old==Path('cp_sat_caseB_v1_1.py').read_bytes()
(base/'final_audit.json').write_text(json.dumps({'validated_pilot_schedules':count,'snapshot_hashes_verified':True,'unknown_stops_discovery':True,'v1_1_unchanged':True},indent=2)+'\n')
print(f'PASS: {count} pilot schedules independently revalidated; hashes; UNKNOWN stop; v1.1 unchanged')
