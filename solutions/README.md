# Optimal fairness schedules — 3 October 2026

Four rounds; unique partners; balanced three/four-player participation. Tee times start at 10:00, seven minutes apart, with three-player groups before four-player groups. Fairness first maximizes each player’s minimum number of distinct tee slots, then the sum across players. Every selected schedule was independently revalidated from its CSV. Average tee time is not an optimization objective.

| Players | Minimum distinct slots | Total spread | Schedule | Tee times | Proof |
|---:|---:|---:|---|---|---|
| 15 | 2 | 45 | [CSV](optimal-4-rounds/n15_sol.csv) | [Summary](optimal-4-rounds/n15_tee_times.md) | [Evidence](../runs/n15_to24_fair_sweep_20261002/n15/run.json) |
| 16 | 2 | 44 | [CSV](optimal-4-rounds/n16_sol.csv) | [Summary](optimal-4-rounds/n16_tee_times.md) | [Evidence](../runs/n15_to24_fair_sweep_20261002/n16/run.json) |
| 17 | 3 | 63 | [CSV](optimal-4-rounds/n17_sol.csv) | [Summary](optimal-4-rounds/n17_tee_times.md) | [Evidence](../runs/n17_target64_repeat_cases_20261002/README.md) |
| 18 | 3 | 65 | [CSV](optimal-4-rounds/n18_sol.csv) | [Summary](optimal-4-rounds/n18_tee_times.md) | [Evidence](../runs/n18_canonical_two_rounds_20261003/README.md) |
| 19 | 3 | 68 | [CSV](optimal-4-rounds/n19_sol.csv) | [Summary](optimal-4-rounds/n19_tee_times.md) | [Evidence](../runs/n19_canonical_two_rounds_20261003/README.md) |
| 20 | 4 | 80 | [CSV](optimal-4-rounds/n20_sol.csv) | [Summary](optimal-4-rounds/n20_tee_times.md) | [Evidence](../runs/n15_to24_fair_sweep_20261002/n20/run.json) |
| 21 | 4 | 84 | [CSV](optimal-4-rounds/n21_sol.csv) | [Summary](optimal-4-rounds/n21_tee_times.md) | [Evidence](../runs/n15_to24_fair_sweep_20261002/n21/run.json) |
| 22 | 4 | 88 | [CSV](optimal-4-rounds/n22_sol.csv) | [Summary](optimal-4-rounds/n22_tee_times.md) | [Evidence](../runs/n15_to24_fair_sweep_20261002/n22/run.json) |
| 23 | 4 | 92 | [CSV](optimal-4-rounds/n23_sol.csv) | [Summary](optimal-4-rounds/n23_tee_times.md) | [Evidence](../runs/n15_to24_fair_sweep_20261002/n23/run.json) |
| 24 | 4 | 96 | [CSV](optimal-4-rounds/n24_sol.csv) | [Summary](optimal-4-rounds/n24_tee_times.md) | [Evidence](../runs/n15_to24_fair_sweep_20261002/n24/run.json) |

The 15–16-player proofs come from solver OPTIMAL results; 17–19 use exhaustive infeasibility proofs plus validated attaining schedules; 20–24 attain the absolute maximum of four distinct slots per player. See [full proof status](../runs/FAIRNESS_STATUS.md).

Older schedules, logs and comparisons are preserved in [the dated archive](archive/2026-10-03/README.md). The historical 18-player total-only score 66 has minimum 2; the selected minimum-first fairness optimum is (3,65). Detailed experimental audits remain in `runs/`.

Run new experiments under `runs/` to keep this collection clean. Regeneration script: `scripts/organize_solutions.py` (one-time migration; refuses to overwrite an existing collection).
