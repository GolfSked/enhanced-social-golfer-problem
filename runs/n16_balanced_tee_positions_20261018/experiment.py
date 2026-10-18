"""Search tee orders of the saved 16-player schedule; preserve all memberships."""
import csv
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from esgp_v2 import read_schedule, validate

directory = Path(__file__).resolve().parent
source = read_schedule(directory / 'source.csv', 16, 4)
validate(source, 16, 4)
permutations = list(itertools.permutations(range(4)))
tested = 0
for orders in itertools.product(permutations, repeat=3):
    # Mapping: old slot -> new slot. Fix round one by global slot symmetry.
    schedule = [[list(group) for group in source[0]]]
    for groups, order in zip(source[1:], orders):
        reordered = [None] * 4
        for old, new in enumerate(order):
            reordered[new] = list(groups[old])
        schedule.append(reordered)
    tested += 1
    visits = {p: [] for p in range(1, 17)}
    for groups in schedule:
        for slot, group in enumerate(groups, 1):
            for player in group:
                visits[player].append(slot)
    distribution = Counter(len(set(slots)) for slots in visits.values())
    if distribution != {2: 4, 3: 12}:
        continue
    audit = validate(schedule, 16, 4)
    assert audit['total_spread'] == 44 and audit['minimum_spread'] == 2
    for before, after in zip(source, schedule):
        assert {frozenset(g) for g in before} == {frozenset(g) for g in after}
    with (directory / 'schedule.csv').open('w', newline='') as output:
        writer = csv.writer(output, lineterminator="\n")
        for r, groups in enumerate(schedule, 1):
            for g, players in enumerate(groups, 1):
                writer.writerow([r, g, *players])
    persisted = read_schedule(directory / 'schedule.csv', 16, 4)
    assert validate(persisted, 16, 4) == audit
    with (directory / 'players.csv').open('w', newline='') as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(['player', 'round_1', 'round_2', 'round_3', 'round_4', 'distinct_positions'])
        for p, slots in visits.items():
            writer.writerow([p, *slots, len(set(slots))])
    result = dict(status='VALIDATED_WITNESS', players=16, rounds=4,
                  method='Permute tee order only; keep all group memberships',
                  orderings_tested_until_first_witness=tested,
                  old_to_new_slots_1based=[[1, 2, 3, 4]] +
                  [[v + 1 for v in order] for order in orders],
                  two_position_players=[p for p, slots in visits.items() if len(set(slots)) == 2],
                  validation=audit)
    (directory / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    break
else:
    raise SystemExit('No witness among these tee-order permutations; not a global infeasibility proof.')
