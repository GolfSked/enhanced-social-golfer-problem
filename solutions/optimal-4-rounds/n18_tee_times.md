# 18 players — optimal fairness schedule

Minimum distinct tee slots: **3**. Total spread: **65**. Four rounds; no repeated partners.

Player numbers are ordered by descending distinct tee-position count, with previous player ID breaking ties. Names follow roster order.

| Group | Tee time | Round 1 players | Round 2 players | Round 3 players | Round 4 players |
|---:|---|---|---|---|---|
| 1 | 10:00 | 16, 17, 18 | 4, 8, 11 | 5, 10, 12 | 7, 9, 14 |
| 2 | 10:07 | 9, 10, 11 | 2, 3, 6 | 7, 13, 15 | 1, 4, 5 |
| 3 | 10:14 | 5, 6, 7, 8 | 9, 12, 15, 16 | 1, 3, 11, 17 | 2, 10, 15, 17 |
| 4 | 10:21 | 3, 4, 14, 15 | 1, 7, 10, 18 | 2, 8, 14, 16 | 6, 11, 13, 16 |
| 5 | 10:28 | 1, 2, 12, 13 | 5, 13, 14, 17 | 4, 6, 9, 18 | 3, 8, 12, 18 |

| Player | Round 1 | Round 2 | Round 3 | Round 4 | Distinct slots | Three-player rounds | Four-player rounds |
|---:|---|---|---|---|---:|---:|---:|
| 1 | 10:28 | 10:21 | 10:14 | 10:07 | 4 | 1 | 3 |
| 2 | 10:28 | 10:07 | 10:21 | 10:14 | 4 | 1 | 3 |
| 3 | 10:21 | 10:07 | 10:14 | 10:28 | 4 | 1 | 3 |
| 4 | 10:21 | 10:00 | 10:28 | 10:07 | 4 | 2 | 2 |
| 5 | 10:14 | 10:28 | 10:00 | 10:07 | 4 | 2 | 2 |
| 6 | 10:14 | 10:07 | 10:28 | 10:21 | 4 | 1 | 3 |
| 7 | 10:14 | 10:21 | 10:07 | 10:00 | 4 | 2 | 2 |
| 8 | 10:14 | 10:00 | 10:21 | 10:28 | 4 | 1 | 3 |
| 9 | 10:07 | 10:14 | 10:28 | 10:00 | 4 | 2 | 2 |
| 10 | 10:07 | 10:21 | 10:00 | 10:14 | 4 | 2 | 2 |
| 11 | 10:07 | 10:00 | 10:14 | 10:21 | 4 | 2 | 2 |
| 12 | 10:28 | 10:14 | 10:00 | 10:28 | 3 | 1 | 3 |
| 13 | 10:28 | 10:28 | 10:07 | 10:21 | 3 | 1 | 3 |
| 14 | 10:21 | 10:28 | 10:21 | 10:00 | 3 | 1 | 3 |
| 15 | 10:21 | 10:14 | 10:07 | 10:14 | 3 | 1 | 3 |
| 16 | 10:00 | 10:14 | 10:21 | 10:21 | 3 | 1 | 3 |
| 17 | 10:00 | 10:28 | 10:14 | 10:14 | 3 | 1 | 3 |
| 18 | 10:00 | 10:21 | 10:28 | 10:28 | 3 | 1 | 3 |

Selected source: [runs/tertiary_fairness_20261019/four-round-n18.csv](../../runs/tertiary_fairness_20261019/four-round-n18.csv).
Original minimum/total optimality evidence: [runs/n18_canonical_two_rounds_20261003/README.md](../../runs/n18_canonical_two_rounds_20261003/README.md).
The original evidence proves the first two priorities; see [third-priority results and numbering audit](../../runs/tertiary_fairness_20261019/README.md).
