"""Complete feasibility test: 19 players, minimum four and total at least 80."""
import csv, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from boolean_model_snapshot import build_model
from esgp_v2 import validate
from ortools.sat.python import cp_model

root = Path(__file__).resolve().parent
model, solver, X, sizes, rounds = build_model(
    19, rounds=5, fair_spread=True, strengthen=True,
    time_limit=1200, workers=8, seed=101)
assert sizes == [3,4,4,4,4]
distinct = [model.GetIntVarFromProtoIndex(i) for i,v in enumerate(model.Proto().variables) if v.name.startswith("distinct_pos_")]
assert len(distinct)==19
for v in distinct: model.Add(v>=4)
model.Add(sum(distinct)>=80)
model.Add(sum(distinct)<=91)
model.ClearObjective()
assert not model.Validate(), model.Validate()
model.ExportToFile(str(root/'model.pbtxt'))
configuration = dict(players=19, rounds=5, sizes=sizes, minimum_target=4,
    total_target=80, seconds=1200, workers=8, seed=101, strengthen=True,
    hint=None, symmetry='Generic first-round player relabelling only',
    source_sha256={n:hashlib.sha256((root/n).read_bytes()).hexdigest()
        for n in ('run.py','boolean_model_snapshot.py')})
(root/'configuration.json').write_text(json.dumps(configuration,indent=2)+'\n')
solver.parameters.log_to_stdout=False
with (root/'solver.log').open('w') as log:
    solver.log_callback=lambda msg:(log.write(msg+'\n'),log.flush())
    status=solver.Solve(model)
result=dict(status=solver.StatusName(status), solver_seconds=solver.WallTime(),
    minimum_target=4,total_target=80,configured_seconds=1200)
if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    schedule=[[[p for p in range(1,20) if solver.Value(X[r,g,p])]
        for g in range(5)] for r in range(5)]
    result.update(validate(schedule,19,5))
    assert result['minimum_spread']>=4 and result['total_spread']>=80
    with (root/'schedule.csv').open('w',newline='') as f:
        writer=csv.writer(f)
        for r,groups in enumerate(schedule,1):
            for g,members in enumerate(groups,1):writer.writerow([r,g,*members])
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n')
meaning=("(4,79) globally optimal: all improvements excluded." if status==cp_model.INFEASIBLE else "Validated improvement found; total optimality not established by feasibility status." if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else "UNKNOWN leaves improvement unresolved; best known remains (4,79).")
with (root/'README.md').open('a') as f:
    f.write(f'\nCompleted: {solver.StatusName(status)} after {solver.WallTime():.6f} seconds. {meaning}\n')
print(json.dumps(result,indent=2),flush=True)
