"""Complete feasibility test: 23 players, five distinct tee slots each."""
import csv, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from boolean_model_snapshot import build_model
from esgp_v2 import validate
from ortools.sat.python import cp_model

root = Path(__file__).resolve().parent
model, solver, X, sizes, rounds = build_model(
    23, rounds=5, fair_spread=True, strengthen=True,
    time_limit=1200, workers=8, seed=101)
assert sizes == [3,4,4,4,4,4]
# Five rounds and no repeated tee slot is exactly five distinct tee slots.
for p in range(1,24):
    for g in range(6):
        model.AddAtMostOne(X[r,g,p] for r in range(5))
model.ClearObjective()
assert not model.Validate(), model.Validate()
model.ExportToFile(str(root/'model.pbtxt'))
configuration = dict(players=23, rounds=5, sizes=sizes, minimum_target=5,
    total_target=115, seconds=1200, workers=8, seed=101, strengthen=True,
    hint=None, symmetry='Generic first-round player relabelling only',
    source_sha256={n:hashlib.sha256((root/n).read_bytes()).hexdigest()
        for n in ('run.py','boolean_model_snapshot.py')})
(root/'configuration.json').write_text(json.dumps(configuration,indent=2)+'\n')
solver.parameters.log_to_stdout=False
with (root/'solver.log').open('w') as log:
    solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
    status=solver.Solve(model)
result=dict(status=solver.StatusName(status), solver_seconds=solver.WallTime(),
    minimum_target=5,total_target=115,configured_seconds=1200)
if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    schedule=[[[p for p in range(1,24) if solver.Value(X[r,g,p])]
        for g in range(6)] for r in range(5)]
    result.update(validate(schedule,23,5))
    assert result['minimum_spread']==5 and result['total_spread']==115
    with (root/'schedule.csv').open('w',newline='') as f:
        writer=csv.writer(f)
        for r,groups in enumerate(schedule,1):
            for g,members in enumerate(groups,1):writer.writerow([r,g,*members])
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n')
meaning=('Minimum four proven optimal; total at minimum four remains unresolved.'
    if status==cp_model.INFEASIBLE else
    'Validated (5,115) attains the absolute ceiling: globally optimal.'
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else
    'UNKNOWN leaves minimum five unresolved; best known remains (4,107).')
with (root/'README.md').open('a') as f:
    f.write(f'\nCompleted: {solver.StatusName(status)} after {solver.WallTime():.6f} seconds. {meaning}\n')
print(json.dumps(result,indent=2),flush=True)
