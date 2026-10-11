import hashlib,json,platform,shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import ortools
from esgp_v2 import read_schedule,validate
root=Path(__file__).resolve().parent
sources={}
for name in ('cp_sat_caseB_v2.py','esgp_v2.py','requirements.txt'):
 source=Path(name)
 destination=root/'sources'/name
 destination.parent.mkdir(exist_ok=True)
 shutil.copy2(source,destination)
 sources[str(destination.relative_to(root))]=hashlib.sha256(destination.read_bytes()).hexdigest()
for name in ('ordering.py','global_enumeration.py','canonical_crosscheck.py','audit.py'):
 sources[name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
for name in ('schedule.csv','global_schedule.csv','canonical_schedule.csv'):
 metrics=validate(read_schedule(root/name,16,5),16,5)
 assert (metrics['minimum_spread'],metrics['total_spread'])==(2,51)
full=Path('runs/n16_r5_full_1200s_20261011/n16/schedule.csv')
assert validate(read_schedule(full,16,5),16,5)['total_spread']==51
proof=json.loads((root/'global_result.json').read_text())
assert sum(proof['score_counts'].values())==proof['orderings_checked']==27648
crosscheck=json.loads((root/'canonical_result.json').read_text())
assert crosscheck['status']=='OPTIMAL'
assert crosscheck['objective_value']==crosscheck['objective_bound']==181
(root/'source_audit.json').write_text(json.dumps({'sources_sha256':sources,'python':platform.python_version(),'ortools':ortools.__version__,'all_four_witnesses_valid':True,'enumeration_count_verified':True,'canonical_optimal_bound_verified':True},indent=2)+'\n')
print('PASS: four independent witnesses; complete enumeration counts; matching OPTIMAL bound; source snapshots saved')
