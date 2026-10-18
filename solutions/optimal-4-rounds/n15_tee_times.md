# 15 players — optimal fairness schedule

Minimum distinct tee slots: **2**. Total spread: **45**. Four rounds; no repeated partners.

Player numbers are ordered by descending distinct tee-position count, with previous player ID breaking ties. Names follow roster order.

| Group | Tee time | Round 1 players | Round 2 players | Round 3 players | Round 4 players |
|---:|---|---|---|---|---|
| 1 | 10:00 | 10, 11, 12 | 5, 7, 9 | 1, 2, 3 | 4, 6, 8 |
| 2 | 10:07 | 3, 8, 9, 15 | 2, 4, 12, 15 | 4, 9, 11, 14 | 1, 7, 11, 15 |
| 3 | 10:14 | 2, 6, 7, 14 | 1, 8, 10, 14 | 7, 8, 12, 13 | 3, 5, 12, 14 |
| 4 | 10:21 | 1, 4, 5, 13 | 3, 6, 11, 13 | 5, 6, 10, 15 | 2, 9, 10, 13 |

| Player | Round 1 | Round 2 | Round 3 | Round 4 | Distinct slots | Three-player rounds | Four-player rounds |
|---:|---|---|---|---|---:|---:|---:|
| 1 | 10:21 | 10:14 | 10:00 | 10:07 | 4 | 1 | 3 |
| 2 | 10:14 | 10:07 | 10:00 | 10:21 | 4 | 1 | 3 |
| 3 | 10:07 | 10:21 | 10:00 | 10:14 | 4 | 1 | 3 |
| 4 | 10:21 | 10:07 | 10:07 | 10:00 | 3 | 1 | 3 |
| 5 | 10:21 | 10:00 | 10:21 | 10:14 | 3 | 1 | 3 |
| 6 | 10:14 | 10:21 | 10:21 | 10:00 | 3 | 1 | 3 |
| 7 | 10:14 | 10:00 | 10:14 | 10:07 | 3 | 1 | 3 |
| 8 | 10:07 | 10:14 | 10:14 | 10:00 | 3 | 1 | 3 |
| 9 | 10:07 | 10:00 | 10:07 | 10:21 | 3 | 1 | 3 |
| 10 | 10:00 | 10:14 | 10:21 | 10:21 | 3 | 1 | 3 |
| 11 | 10:00 | 10:21 | 10:07 | 10:07 | 3 | 1 | 3 |
| 12 | 10:00 | 10:07 | 10:14 | 10:14 | 3 | 1 | 3 |
| 13 | 10:21 | 10:21 | 10:14 | 10:21 | 2 | 0 | 4 |
| 14 | 10:14 | 10:14 | 10:07 | 10:14 | 2 | 0 | 4 |
| 15 | 10:07 | 10:07 | 10:21 | 10:07 | 2 | 0 | 4 |

Selected source: [runs/tertiary_fairness_20261019/four-round-n15.csv](../../runs/tertiary_fairness_20261019/four-round-n15.csv).
Original minimum/total optimality evidence: [runs/n15_to24_fair_sweep_20261002/n15/run.json](../../runs/n15_to24_fair_sweep_20261002/n15/run.json).
The original evidence proves the first two priorities; see [third-priority results and numbering audit](../../runs/tertiary_fairness_20261019/README.md).
