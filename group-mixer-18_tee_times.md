# 18 players — GroupMixer comparison schedule

Minimum distinct tee slots: **2**. Total spread: **66**. Four rounds; no repeated partners. Group sizes: 3, 3, 4, 4, 4.

| Group | Tee time | Round 1 players | Round 2 players | Round 3 players | Round 4 players |
|---:|---|---|---|---|---|
| 1 | 10:00 | 3, 8, 14 | 9, 11, 17 | 6, 13, 15 | 1, 4, 16 |
| 2 | 10:07 | 1, 13, 17 | 2, 7, 15 | 5, 10, 18 | 6, 12, 14 |
| 3 | 10:14 | 9, 10, 15, 16 | 1, 8, 12, 18 | 3, 4, 12, 17 | 2, 5, 9, 13 |
| 4 | 10:21 | 5, 7, 11, 12 | 4, 10, 13, 14 | 2, 8, 11, 16 | 3, 11, 15, 18 |
| 5 | 10:28 | 2, 4, 6, 18 | 3, 5, 6, 16 | 1, 7, 9, 14 | 7, 8, 10, 17 |

| Player | Round 1 | Round 2 | Round 3 | Round 4 | Distinct slots | Three-player rounds | Four-player rounds |
|---:|---|---|---|---|---:|---:|---:|
| 1 | 10:07 | 10:14 | 10:28 | 10:00 | 4 | 2 | 2 |
| 2 | 10:28 | 10:07 | 10:21 | 10:14 | 4 | 1 | 3 |
| 3 | 10:00 | 10:28 | 10:14 | 10:21 | 4 | 1 | 3 |
| 4 | 10:28 | 10:21 | 10:14 | 10:00 | 4 | 1 | 3 |
| 5 | 10:21 | 10:28 | 10:07 | 10:14 | 4 | 1 | 3 |
| 6 | 10:28 | 10:28 | 10:00 | 10:07 | 3 | 2 | 2 |
| 7 | 10:21 | 10:07 | 10:28 | 10:28 | 3 | 1 | 3 |
| 8 | 10:00 | 10:14 | 10:21 | 10:28 | 4 | 1 | 3 |
| 9 | 10:14 | 10:00 | 10:28 | 10:14 | 3 | 1 | 3 |
| 10 | 10:14 | 10:21 | 10:07 | 10:28 | 4 | 1 | 3 |
| 11 | 10:21 | 10:00 | 10:21 | 10:21 | 2 | 1 | 3 |
| 12 | 10:21 | 10:14 | 10:14 | 10:07 | 3 | 1 | 3 |
| 13 | 10:07 | 10:21 | 10:00 | 10:14 | 4 | 2 | 2 |
| 14 | 10:00 | 10:21 | 10:28 | 10:07 | 4 | 2 | 2 |
| 15 | 10:14 | 10:07 | 10:00 | 10:21 | 4 | 2 | 2 |
| 16 | 10:14 | 10:28 | 10:21 | 10:00 | 4 | 1 | 3 |
| 17 | 10:07 | 10:00 | 10:14 | 10:28 | 4 | 2 | 2 |
| 18 | 10:28 | 10:14 | 10:07 | 10:21 | 4 | 1 | 3 |

## Comparison with the fairness optimum

| Schedule | Minimum distinct slots | Total spread | 73 × minimum + total |
|---|---:|---:|---:|
| GroupMixer | 2 | 66 | 212 |
| [Fairness optimum](solutions/optimal/n18_tee_times.md) | 3 | 65 | 284 |

Distinct-slot distribution: 1 player(s) with 2 slots, 4 player(s) with 3 slots, 13 player(s) with 4 slots.
Players with minimum variety: 11.
Validated: all 18 players appear once in every round; exact group capacities; no repeated unordered pairs; six players have two foursome rounds and twelve have three. There are 96 distinct met pairs and 57 unmet pairs.

Source: [group-mixer-18.txt](group-mixer-18.txt). Player IDs, round order and tee-slot assignments are preserved.
Converted CSV: [group-mixer-18_sol.csv](group-mixer-18_sol.csv). Format matches the reference: headerless rows containing round, group, player IDs.
