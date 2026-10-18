# 16 players — optimal fairness schedule

Minimum distinct tee slots: **2**. Total spread: **44**. Four rounds; no repeated partners. Group sizes: 4, 4, 4, 4.

Additional fairness rule: **P1–P12 each receive three distinct tee positions; P13–P16 each receive two**. Counts differ by at most one. Names are assigned in roster order.

| Group | Tee time | Round 1 players | Round 2 players | Round 3 players | Round 4 players |
|---:|---|---|---|---|---|
| 1 | 10:00 | 10, 11, 12, 16 | 3, 5, 15, 16 | 2, 5, 7, 12 | 2, 4, 8, 16 |
| 2 | 10:07 | 7, 8, 9, 15 | 2, 6, 9, 11 | 4, 11, 13, 15 | 1, 6, 12, 15 |
| 3 | 10:14 | 4, 5, 6, 14 | 1, 4, 7, 10 | 1, 9, 14, 16 | 3, 7, 11, 14 |
| 4 | 10:21 | 1, 2, 3, 13 | 8, 12, 13, 14 | 3, 6, 8, 10 | 5, 9, 10, 13 |

| Player | Round 1 | Round 2 | Round 3 | Round 4 | Distinct slots | Three-player rounds | Four-player rounds |
|---:|---|---|---|---|---:|---:|---:|
| 1 | 10:21 | 10:14 | 10:14 | 10:07 | 3 | 0 | 4 |
| 2 | 10:21 | 10:07 | 10:00 | 10:00 | 3 | 0 | 4 |
| 3 | 10:21 | 10:00 | 10:21 | 10:14 | 3 | 0 | 4 |
| 4 | 10:14 | 10:14 | 10:07 | 10:00 | 3 | 0 | 4 |
| 5 | 10:14 | 10:00 | 10:00 | 10:21 | 3 | 0 | 4 |
| 6 | 10:14 | 10:07 | 10:21 | 10:07 | 3 | 0 | 4 |
| 7 | 10:07 | 10:14 | 10:00 | 10:14 | 3 | 0 | 4 |
| 8 | 10:07 | 10:21 | 10:21 | 10:00 | 3 | 0 | 4 |
| 9 | 10:07 | 10:07 | 10:14 | 10:21 | 3 | 0 | 4 |
| 10 | 10:00 | 10:14 | 10:21 | 10:21 | 3 | 0 | 4 |
| 11 | 10:00 | 10:07 | 10:07 | 10:14 | 3 | 0 | 4 |
| 12 | 10:00 | 10:21 | 10:00 | 10:07 | 3 | 0 | 4 |
| 13 | 10:21 | 10:21 | 10:07 | 10:21 | 2 | 0 | 4 |
| 14 | 10:14 | 10:21 | 10:14 | 10:14 | 2 | 0 | 4 |
| 15 | 10:07 | 10:00 | 10:07 | 10:07 | 2 | 0 | 4 |
| 16 | 10:00 | 10:00 | 10:14 | 10:00 | 2 | 0 | 4 |

Selected source: [runs/n16_balanced_tee_positions_20261018/first-twelve-schedule.csv](../../runs/n16_balanced_tee_positions_20261018/first-twelve-schedule.csv).
[Balanced-position experiment and validation](../../runs/n16_balanced_tee_positions_20261018/README.md).
[Original optimality proof](../../runs/n15_to24_fair_sweep_20261002/n16/run.json): the new witness retains the same proven optimum (2,44).
The CSV is headerless: round, group, player IDs. Player IDs are placeholders; assigning names preserves validity and fairness scores.
