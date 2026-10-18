# 19 players — optimal fairness schedule

Minimum distinct tee slots: **3**. Total spread: **68**. Four rounds; no repeated partners.

Player numbers are ordered by descending distinct tee-position count, with previous player ID breaking ties. Names follow roster order.

| Group | Tee time | Round 1 players | Round 2 players | Round 3 players | Round 4 players |
|---:|---|---|---|---|---|
| 1 | 10:00 | 10, 11, 19 | 3, 9, 14 | 2, 13, 15 | 4, 7, 8 |
| 2 | 10:07 | 8, 9, 17, 18 | 2, 5, 7, 11 | 12, 14, 16, 18 | 1, 6, 10, 14 |
| 3 | 10:14 | 6, 7, 15, 16 | 1, 4, 15, 18 | 3, 5, 8, 10 | 2, 9, 16, 19 |
| 4 | 10:21 | 4, 5, 13, 14 | 6, 8, 12, 19 | 1, 7, 17, 19 | 3, 11, 13, 18 |
| 5 | 10:28 | 1, 2, 3, 12 | 10, 13, 16, 17 | 4, 6, 9, 11 | 5, 12, 15, 17 |

| Player | Round 1 | Round 2 | Round 3 | Round 4 | Distinct slots | Three-player rounds | Four-player rounds |
|---:|---|---|---|---|---:|---:|---:|
| 1 | 10:28 | 10:14 | 10:21 | 10:07 | 4 | 0 | 4 |
| 2 | 10:28 | 10:07 | 10:00 | 10:14 | 4 | 1 | 3 |
| 3 | 10:28 | 10:00 | 10:14 | 10:21 | 4 | 1 | 3 |
| 4 | 10:21 | 10:14 | 10:28 | 10:00 | 4 | 1 | 3 |
| 5 | 10:21 | 10:07 | 10:14 | 10:28 | 4 | 0 | 4 |
| 6 | 10:14 | 10:21 | 10:28 | 10:07 | 4 | 0 | 4 |
| 7 | 10:14 | 10:07 | 10:21 | 10:00 | 4 | 1 | 3 |
| 8 | 10:07 | 10:21 | 10:14 | 10:00 | 4 | 1 | 3 |
| 9 | 10:07 | 10:00 | 10:28 | 10:14 | 4 | 1 | 3 |
| 10 | 10:00 | 10:28 | 10:14 | 10:07 | 4 | 1 | 3 |
| 11 | 10:00 | 10:07 | 10:28 | 10:21 | 4 | 1 | 3 |
| 12 | 10:28 | 10:21 | 10:07 | 10:28 | 3 | 0 | 4 |
| 13 | 10:21 | 10:28 | 10:00 | 10:21 | 3 | 1 | 3 |
| 14 | 10:21 | 10:00 | 10:07 | 10:07 | 3 | 1 | 3 |
| 15 | 10:14 | 10:14 | 10:00 | 10:28 | 3 | 1 | 3 |
| 16 | 10:14 | 10:28 | 10:07 | 10:14 | 3 | 0 | 4 |
| 17 | 10:07 | 10:28 | 10:21 | 10:28 | 3 | 0 | 4 |
| 18 | 10:07 | 10:14 | 10:07 | 10:21 | 3 | 0 | 4 |
| 19 | 10:00 | 10:21 | 10:21 | 10:14 | 3 | 1 | 3 |

Selected source: [runs/tertiary_fairness_20261019/four-round-n19.csv](../../runs/tertiary_fairness_20261019/four-round-n19.csv).
Original minimum/total optimality evidence: [runs/n19_canonical_two_rounds_20261003/README.md](../../runs/n19_canonical_two_rounds_20261003/README.md).
The original evidence proves the first two priorities; see [third-priority results and numbering audit](../../runs/tertiary_fairness_20261019/README.md).
