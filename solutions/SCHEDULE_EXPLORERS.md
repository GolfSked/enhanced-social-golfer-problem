# Schedule explorers

Open `three-round-schedule-explorer.html`, `four-round-schedule-explorer.html`
or `five-round-schedule-explorer.html` in a browser. All contain schedules for 15–24 golfers and default
to 16 golfers, coloured by Round 1. Previously saved selections take precedence.

Use **Edit rounds** for course labels, first tee times and intervals, and
**Replace player numbers with names** for one name per line in player order.
These edits change presentation, not group memberships or tee-slot indices.

URL parameters:

- `players=Bran:Train:Chops:...` assigns names in player-number order. A roster
  of 15–24 names selects the corresponding schedule.
- Repeat `round=Course|HH:MM|interval` in round order. The interval is optional
  and defaults to seven minutes. Omitted rounds use 10:00 and seven minutes.
  Intervals must be whole minutes from 1 to 60. URL values override remembered
  values on reopening; use the editors to change them for the current session.
- The four-round explorer rejects more than four
  entries, the five-round explorer rejects more than five, and the three-round
  explorer rejects more than three.
- Encode spaces as `%20`, `&` in names as `%26`, and `#` as `%23`.
  Colons separate player names; pipes separate round fields, so avoid those
  separator characters inside names or course labels respectively.

Five-round example (append to the HTML filename):

```text
?round=8-November%20Moruya|11:35&round=9-November%20Narooma|10:00&round=10-November%20Catalina|11:26&round=11-November%20Moruya|11:00&round=12-November%20Catalina|10:30
```

The first two rounds define grid rows and columns. Later rounds appear as
partial squares A and B, plus C for five rounds. Empty cells do not represent
golfers and require no values. Completion to full Latin squares is not required.
The three-round explorer needs only partial square A.

Three-round CSV sources and solver-optimal fairness scores are recorded in
`three-round-explorer-sources.json`. The original pilot supplies 15–18 players;
`runs/three_round_explorer_20261017/` supplies new optimal solves for 19–24.
`scripts/build-three-round-explorer.py` independently validates every witness.

Five-round CSV provenance and independently recomputed scores are recorded in
`five-round-explorer-sources.json`. All ten witnesses pass attendance, prescribed
group mix, partner uniqueness, participation balance and expected fairness-score
checks in `scripts/build-five-round-explorer.py`. Proof evidence remains in the
run directories and `runs/FAIRNESS_STATUS.md`.

Run `node tests/check_explorer_url.cjs` from the repository root to check both
exports, URL settings, editor updates, all thirty three-round views and all
fifty five-round views. All explorers retain the project MIT licence and attribution.
