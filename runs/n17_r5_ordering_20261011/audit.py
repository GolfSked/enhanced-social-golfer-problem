"""Validate persisted witnesses and preserve sources for this experiment."""
import hashlib,json,platform,shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import ortools
from esgp_v2 import read_schedule,validate
root=Path(__file__).resolve().parent
sources={}
for name in ('cp_sat_caseB_v2.py','esgp_v2.py','requirements.txt'):
 destination=root/'sources'/name;destination.parent.mkdir(exist_ok=True)
 shutil.copy2(Path(name),destination)
 sources[str(destination.relative_to(root))]=hashlib.sha256(destination.read_bytes()).hexdigest()
for source in root.glob('*.py'):
 sources[source.name]=hashlib.sha256(source.read_bytes()).hexdigest()
witnesses=[]
for source in root.rglob('*.csv'):
 metrics=validate(read_schedule(source,17,5),17,5)
 witnesses.append({'path':str(source.relative_to(root)),**metrics})
for folder in ('n17_r5_full_1200s_20261011','n17_r5_full_remaining_943s_20261011'):
 source=Path('runs')/folder/'n17/schedule.csv'
 if source.exists():
  metrics=validate(read_schedule(source,17,5),17,5)
  witnesses.append({'path':str(source),**metrics})
for folder in ('target79_integer','target79_boolean'):
 assert json.loads((root/folder/'result.json').read_text())['status']=='INFEASIBLE'
classes=json.loads((root/'round_pair_classes.json').read_text())
assert classes['matrices']==453 and classes['low_trace_matrices']==23 and classes['classes']==4
assert sum(sum(m[g][g] for g in range(5))==0 for m in classes['representatives'])==1
best=max(witnesses,key=lambda row:(row['minimum_spread'],row['total_spread']))
result={'sources_sha256':sources,'python':platform.python_version(),'ortools':ortools.__version__,
 'witnesses':witnesses,'best_witness':best,'minimum_spread_upper_bound':4,'total_upper_bound_at_minimum4':78,'target79_excluded_in_both_formulations':True,'case_enumeration_counts_verified':True}
(root/'source_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(f"PASS: {len(witnesses)} valid schedules; best ({best['minimum_spread']},{best['total_spread']}); score79 excluded twice")
