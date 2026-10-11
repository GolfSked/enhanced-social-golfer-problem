# Version history

## v2.0 — 12 October 2026

- Configurable positive round counts, defaulting to four, with an interface for individual cases and ranges containing ten feasible player counts from the smallest feasible count. Infeasible counts are recorded; unresolved counts stop discovery or collection.
- Preserve the original v1.1 solver and move the curated four-round schedules to `solutions/optimal-4-rounds/`.
- Establish a minimum of nine players for three and four rounds, and fifteen for five rounds, under the prescribed group mix and balance rules.
- Complete the five-round 15–24 investigation, including global minimum-first fairness proofs of **(4,72) for 18 players** and **(4,79) for 19 players**. Preserve solver snapshots, unsuccessful searches, schedules, and audit evidence under `runs/`. See the [proof status](runs/FAIRNESS_STATUS.md) and [18-player proof](runs/n18_six_intersection_cases_20261012/PROOF.md).
- Add regression checks for model equivalence, schedule validation, and feasible-count range handling.

Thank you to **Guido of [GroupMixer](https://groupmixer.app/)** for adding **“Different selected groups visited”** to group counting during this work. It helped us express tee-slot diversity in GroupMixer and compare its schedules with our independently validated results. GroupMixer comparisons supported the investigation; the optimality proofs are documented separately in this repository.

## Earlier work

The retained v1.1 solver introduced optional minimum-first fairness, logically implied strengthening constraints, and repaired complete/partial CSV hint loading. The four-round 15–24 fairness results and curated schedules were committed before v2.0. See [historical run notes](HISTORICAL_RUNS.md) and the Git history for the original experiments and subsequent proof work.
