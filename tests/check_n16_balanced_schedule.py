"""Validate the adopted 16-player witness and its explorer representation."""
import csv
import hashlib
import html
import itertools
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'solutions/optimal-4-rounds/n16_sol.csv'
rounds = [[None] * 4 for _ in range(4)]
for r, g, *players in csv.reader(path.open()):
    r, g = int(r), int(g)
    assert rounds[r - 1][g - 1] is None
    rounds[r - 1][g - 1] = list(map(int, players))
visits = {p: [] for p in range(1, 17)}
pairs = Counter()
for groups in rounds:
    assert sorted(sum(groups, [])) == list(visits)
    for slot, players in enumerate(groups):
        assert len(players) == 4
        pairs.update(itertools.combinations(sorted(players), 2))
        for p in players:
            visits[p].append(slot)
assert len(pairs) == 96 and max(pairs.values()) == 1
assert all(len(set(slots)) == (3 if p <= 12 else 2) for p, slots in visits.items())
assert sum(len(set(slots)) for slots in visits.values()) == 44

source = (ROOT / 'web/explorer-sources/four-round.html').read_text()
export = (ROOT / 'solutions/four-round-schedule-explorer.html').read_text()
frame = html.unescape(re.search(r'data-srcdoc="([\s\S]*?)"></iframe>', export)[1])
for text in (source, frame):
    entry = json.loads(re.search(r'const data=(.*?);\nconst np=', text, re.S)[1])['16']
    assert entry['rounds'] == rounds
    assert entry['groups'] == {str(p): slots for p, slots in visits.items()}
    assert (entry['minimum'], entry['total']) == (2, 44)
    for row, first in zip(entry['grid'], rounds[0]):
        for player, second in zip(row, rounds[1]):
            assert set(first) & set(second) == {player}
records = json.loads((path.parent / 'validation.json').read_text())
record = next(r for r in records if r['players'] == 16)
assert record['sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
print('16-player four-round witness: 12×3 + 4×2; 96 unique pairs; CSV and explorer agree.')
