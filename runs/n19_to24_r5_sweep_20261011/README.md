# Five-round sweep: 19–24 players (11 October 2026)

Six sequential local fairness runs, each capped at 120 solver seconds, four workers, seed 101, with the original ten-second pilot CSV as a hint. Prior records were preserved. Each saved CSV was independently validated for attendance, capacities, unique partners and balanced fours participation.

| Players | Pilot | Sweep | Status | Minimum ceiling | Total ceiling |
|---|---|---|---|---|---|
| 19 | (3, 76) | (3, 79) | FEASIBLE | 4 | 91 |
| 20 | (5, 100) | (5, 100) | OPTIMAL | 5 | 100 |
| 21 | (4, 91) | (5, 105) | OPTIMAL | 5 | 105 |
| 22 | (3, 96) | (5, 110) | OPTIMAL | 5 | 110 |
| 23 | (3, 101) | (4, 106) | FEASIBLE | 5 | 115 |
| 24 | (5, 120) | (5, 120) | OPTIMAL | 5 | 120 |

## Independent GroupMixer comparison

- n19: GroupMixer (4, 79), independently validated from its saved CSV. Best known (4, 79); minimum proven, total ceiling 91. This result is recorded separately from the local sweep.
- n23: GroupMixer (4, 107), independently validated from its saved CSV. Best known (4, 107); minimum unresolved, total ceiling 115. This result is recorded separately from the local sweep.

## Mathematical ceilings

If a player has f four-player appearances in five rounds, their distinct-slot spread cannot exceed min(5, min(f, number of four-player slots) + min(5-f, number of triple slots)). Balanced fours participation determines exactly how many players have each f. The minimum ceiling is the smallest required individual ceiling; the total ceiling sums all individual ceilings. These are upper bounds, not feasibility claims. Matching a ceiling proves that objective component optimal. OPTIMAL also proves the lexicographic solver objective.

See comparison.json for independent audits and raw solver bounds. Per-count run folders contain source snapshots, configurations, logs, schedules and solver results. No targeted exclusions were run.
