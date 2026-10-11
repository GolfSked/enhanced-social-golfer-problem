# GroupMixer 20–24-player verification, 11 October 2026

All five cases matched our proven optimum on the first Auto generation for that configuration. No reference schedules were imported. A single new workspace was reused sequentially; its final title is ESGP 20–24-player benchmark sweep. Earlier screenshots retain the initial 20-player title; the saved JSON contains the exact scenario and result input for each case.

| Players | Capacities | Minimum distinct slots | Total distinct slots | Unique pairs | Repeated pairs | Fours rounds distribution |
|---|---|---|---|---|---|---|
| 20 | 4,4,4,4,4 | 4 | 80 | 120 | 0 | 20 players × 4 |
| 21 | 3,3,3,4,4,4 | 4 | 84 | 108 | 0 | 15 × 2; 6 × 3 |
| 22 | 3,3,4,4,4,4 | 4 | 88 | 120 | 0 | 2 × 2; 20 × 3 |
| 23 | 3,4,4,4,4,4 | 4 | 92 | 132 | 0 | 12 × 3; 11 × 4 |
| 24 | 4,4,4,4,4,4 | 4 | 96 | 144 | 0 | 24 × 4 |

Every case has four rounds. An independent assignment audit confirmed exact capacities, every player present exactly once per round, no repeated pair, four distinct groups per player and balanced fours participation. Official roster CSV previews were saved and checked for exact membership agreement with those assignments.

Configuration: Avoid Repeats threshold 1, squared penalty, weight 10000; distinct visits to all groups minimum 4, linear penalty, weight 1. Combined visits to the fours groups have bounds 2–3 for 21/22 and 3–4 for 23 at weight 10000. For 24, the combined rule was updated to all groups, exactly 4 (redundant with four rounds). For 20, all groups are fours without an additional size rule. These are configured preferences, whose strict satisfaction was independently verified. Since four distinct slots is the absolute upper bound in four rounds, achieving it for everyone proves the rotation optimum directly.

Evidence: `nNN_auto.json` saves browser workspace inspection, result input, assignments and telemetry; `groupmixer_nNN.csv` preserves the official roster preview; `audited_nNN.csv` was reconstructed from inspected assignments for comparison; `audit.json` holds independent counts; `nNN_rotation.jpg` captures the app result. Our reference schedules and proof records are linked from `solutions/optimal/n20_tee_times.md` through `n24_tee_times.md`.

Reported elapsed times were 27, 222, 150, 142 and 317 milliseconds respectively. These are app telemetry values, not a controlled runtime comparison. Group names are generic slot labels; relabelling them as tee times preserves all benchmark scores.
