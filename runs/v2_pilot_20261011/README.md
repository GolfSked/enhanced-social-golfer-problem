# v2 configurable-round pilots — 11 October 2026

Initial engineering runs: 10 CP-SAT seconds per case, eight workers, seed 101.
Some runs overlapped, so timings are not a comparative performance benchmark.
No GroupMixer schedules were used as hints. Output schedules were validated
for attendance, exact capacities, unique partners, participation balance and fairness.

The minimum is proven only after every smaller admissible count is excluded.
Discovery OPTIMAL records are feasibility checks, not fairness proofs.

| Rounds | Proven minimum | Ten-count range |
|---:|---:|---|
| 3 | 9 | 9–18 |
| 4 | 9 | 9–18 |
| 5 | 15 | 15–24 |

Four rounds starts at nine in this general search. The earlier 15–24 collection
remains preserved in `solutions/optimal-4-rounds/`.

| Rounds | Players | Status | Minimum spread | Total spread |
|---:|---:|---|---:|---:|
| 3 | 9 | OPTIMAL | 2 | 18 |
| 3 | 10 | INFEASIBLE | — | — |
| 3 | 11 | INFEASIBLE | — | — |
| 3 | 12 | INFEASIBLE | — | — |
| 3 | 13 | INFEASIBLE | — | — |
| 3 | 14 | INFEASIBLE | — | — |
| 3 | 15 | OPTIMAL | 2 | 36 |
| 3 | 16 | OPTIMAL | 2 | 36 |
| 3 | 17 | OPTIMAL | 2 | 50 |
| 3 | 18 | OPTIMAL | 3 | 54 |
| 4 | 9 | OPTIMAL | 2 | 21 |
| 4 | 10 | INFEASIBLE | — | — |
| 4 | 11 | INFEASIBLE | — | — |
| 4 | 12 | INFEASIBLE | — | — |
| 4 | 13 | INFEASIBLE | — | — |
| 4 | 14 | INFEASIBLE | — | — |
| 4 | 15 | OPTIMAL | 2 | 45 |
| 4 | 16 | FEASIBLE | 2 | 44 |
| 4 | 17 | FEASIBLE | 3 | 63 |
| 4 | 18 | FEASIBLE | 3 | 65 |
| 5 | 15 | OPTIMAL | 3 | 51 |
| 5 | 16 | FEASIBLE | 2 | 51 |
| 5 | 17 | FEASIBLE | 3 | 70 |
| 5 | 18 | FEASIBLE | 3 | 73 |
| 5 | 19 | FEASIBLE | 3 | 76 |
| 5 | 20 | OPTIMAL | 5 | 100 |
| 5 | 21 | FEASIBLE | 4 | 91 |
| 5 | 22 | FEASIBLE | 3 | 96 |
| 5 | 23 | FEASIBLE | 3 | 101 |
| 5 | 24 | OPTIMAL | 5 | 120 |

The four-round pilot reaches the preserved 15–18 scores. Its FEASIBLE statuses
retain their original meaning; external historical proofs establish optimality
for those scores, while this short run alone does not. All ten original 15–24
models are identical in v1.1 and v2 and accept their original schedules; see
[regression checks](regression.json).

One- and two-round smoke tests are recorded in `one_round_smoke/` and
`two_round_smoke/`. Source snapshots, configuration and environment hashes
are in each summary. Logs and per-case results accompany the schedules.
`unknown_stop_smoke/` uses a deliberately tiny limit to verify that UNKNOWN
halts minimum discovery without claiming a minimum or producing a range.
The [final audit](final_audit.json) revalidates persisted schedules, snapshot
hashes, the UNKNOWN stop and the unchanged v1.1 source.

New five-round FEASIBLE scores are incumbents, not proven optimal.
No curated three-/five-round collection has been created from unproven results.

Subsequent work independently proved the five-round 16-player score (2,51)
globally optimal; see [the complete proof](../n16_r5_ordering_20261011/README.md).
The original pilot result and source snapshots above are preserved.

Subsequent five-round 17-player work improves (3,70) to **(4,76)**. Minimum four
is proven optimal, and total is bounded above by 78; see
[the audit and unresolved targets](../n17_r5_ordering_20261011/README.md).

The subsequent 1,200-second-cap canonical target-77 test completed with
INFEASIBLE in 173.068413 seconds, excluding totals 77–78. **The five-round
17-player result (4,76) is now globally proven optimal.** See
[the completed proof](../n17_r5_target77_1200s_20261011/README.md).
