# 17 players — optimal fairness schedule

Minimum distinct tee slots: **3**. Total spread: **63**. Four rounds; no repeated partners.

Player numbers are ordered by descending distinct tee-position count, with previous player ID breaking ties. Names follow roster order.

| Group | Tee time | Round 1 players | Round 2 players | Round 3 players | Round 4 players |
|---:|---|---|---|---|---|
| 1 | 10:00 | 11, 12, 17 | 6, 9, 10 | 2, 5, 17 | 3, 13, 15 |
| 2 | 10:07 | 10, 15, 16 | 4, 11, 14 | 1, 3, 8 | 5, 7, 14 |
| 3 | 10:14 | 7, 8, 9 | 2, 3, 16 | 4, 10, 13 | 1, 6, 12 |
| 4 | 10:21 | 3, 4, 5, 6 | 1, 7, 15, 17 | 9, 12, 14, 15 | 2, 8, 10, 11 |
| 5 | 10:28 | 1, 2, 13, 14 | 5, 8, 12, 13 | 6, 7, 11, 16 | 4, 9, 16, 17 |

| Player | Round 1 | Round 2 | Round 3 | Round 4 | Distinct slots | Three-player rounds | Four-player rounds |
|---:|---|---|---|---|---:|---:|---:|
| 1 | 10:28 | 10:21 | 10:07 | 10:14 | 4 | 2 | 2 |
| 2 | 10:28 | 10:14 | 10:00 | 10:21 | 4 | 2 | 2 |
| 3 | 10:21 | 10:14 | 10:07 | 10:00 | 4 | 3 | 1 |
| 4 | 10:21 | 10:07 | 10:14 | 10:28 | 4 | 2 | 2 |
| 5 | 10:21 | 10:28 | 10:00 | 10:07 | 4 | 2 | 2 |
| 6 | 10:21 | 10:00 | 10:28 | 10:14 | 4 | 2 | 2 |
| 7 | 10:14 | 10:21 | 10:28 | 10:07 | 4 | 2 | 2 |
| 8 | 10:14 | 10:28 | 10:07 | 10:21 | 4 | 2 | 2 |
| 9 | 10:14 | 10:00 | 10:21 | 10:28 | 4 | 2 | 2 |
| 10 | 10:07 | 10:00 | 10:14 | 10:21 | 4 | 3 | 1 |
| 11 | 10:00 | 10:07 | 10:28 | 10:21 | 4 | 2 | 2 |
| 12 | 10:00 | 10:28 | 10:21 | 10:14 | 4 | 2 | 2 |
| 13 | 10:28 | 10:28 | 10:14 | 10:00 | 3 | 2 | 2 |
| 14 | 10:28 | 10:07 | 10:21 | 10:07 | 3 | 2 | 2 |
| 15 | 10:07 | 10:21 | 10:21 | 10:00 | 3 | 2 | 2 |
| 16 | 10:07 | 10:14 | 10:28 | 10:28 | 3 | 2 | 2 |
| 17 | 10:00 | 10:21 | 10:00 | 10:28 | 3 | 2 | 2 |

Selected source: [runs/tertiary_fairness_20261019/four-round-n17.csv](../../runs/tertiary_fairness_20261019/four-round-n17.csv).
Original minimum/total optimality evidence: [runs/n17_target64_repeat_cases_20261002/README.md](../../runs/n17_target64_repeat_cases_20261002/README.md).
The original evidence proves the first two priorities; see [third-priority results and numbering audit](../../runs/tertiary_fairness_20261019/README.md).
