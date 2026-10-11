"""Audit captured GroupMixer assignments using the repository's independent validator."""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from esgp_v2 import validate

DIRECTORY = Path(__file__).resolve().parent

def audit(name):
    data = json.loads((DIRECTORY / f'{name}.json').read_text())
    groups = data['scenario']['groups']
    rounds = data['scenario']['session_count']
    assert rounds == 5 and [g['capacity'] for g in groups] == [3, 3, 4, 4, 4]
    slots = {g['id']: i for i, g in enumerate(groups)}
    schedule = [[[] for _ in groups] for _ in range(rounds)]
    assignments = data['result']['solution']['assignments']
    assert len(assignments) == 90
    for row in assignments:
        player = int(data['person_names'][row['person_id']].removeprefix('Player '))
        schedule[row['session_id']][slots[row['group_id']]].append(player)
    result = validate(schedule, 18, rounds)
    assert data['result']['solution']['total_cost'] == 90 - result['total_spread']
    result['result_id'] = data['base_result_id']
    result['reported_elapsed_ms'] = data['result']['solution']['elapsed_time_ms']
    (DIRECTORY / f'{name}_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    with (DIRECTORY / f'{name}_schedule.csv').open('w', newline='') as target:
        writer = csv.writer(target)
        for r, gs in enumerate(schedule, 1):
            for g, players in enumerate(gs, 1):
                writer.writerow([r, g, *sorted(players)])
    print(json.dumps(result))

if __name__ == '__main__':
    audit(sys.argv[1] if len(sys.argv) > 1 else 'result')
