# Version history

## Explorer v1.5.0 — 20 October 2026

- Combine colour, tee time and player names into compact vertical group rows with linked highlighting, and add a Next round button that cycles through rounds.
- Move name editing above the Latin squares, initially collapsed under the schedule-summary twisty. Keep the grid label at normal size and the remaining summary smaller.
- Open landing-page links in new tabs, retaining the homepage. All saved schedules, fairness scores and player numbers are unchanged.

## Solver refinement and explorer v1.4.0 — 19 October 2026

- Add a third lexicographic fairness priority: minimise players at the minimum after preserving the optimal minimum and total. Record the count and player-ID mapping in new solver outputs.
- Number all 30 published explorer schedules best-first and display each player range's distinct-position allocation. Preserve min/total scores and group structure up to relabelling.
- Prove the existing 15-player four-round minimum count of three and the 16-player five-round count of three cannot be improved at their optimal minimum/total scores. [Evidence](runs/tertiary_fairness_20261019/README.md).

## Explorer v1.3.0 — 18 October 2026

- Adopt the balanced 16-player, four-round witness: P1–P12 visit three distinct tee positions and P13–P16 visit two. This retains the proven fairness optimum (2,44), exact fours and no repeated pairs. Other schedules are unchanged. [Experiment and validation](runs/n16_balanced_tee_positions_20261018/README.md).

## v2.0 — 12 October 2026

- Configurable positive round counts, defaulting to four, with an interface for individual cases and ranges containing ten feasible player counts from the smallest feasible count. Infeasible counts are recorded; unresolved counts stop discovery or collection.
- Preserve the original v1.1 solver and move the curated four-round schedules to `solutions/optimal-4-rounds/`.
- Establish a minimum of nine players for three and four rounds, and fifteen for five rounds, under the prescribed group mix and balance rules.
- Complete the five-round 15–24 investigation, including global minimum-first fairness proofs of **(4,72) for 18 players** and **(4,79) for 19 players**. Preserve solver snapshots, unsuccessful searches, schedules, and audit evidence under `runs/`. See the [proof status](runs/FAIRNESS_STATUS.md) and [18-player proof](runs/n18_six_intersection_cases_20261012/PROOF.md).
- Independently validate GroupMixer matches for all ten five-round optima from 15 through 24 players, including the final 23-player (5,115) result. Preserve configurations, result data, CSV schedules and screenshots.
- Add regression checks for model equivalence, schedule validation, and feasible-count range handling.

Thank you to **Guido of [GroupMixer](https://groupmixer.app/)** for adding **“Different selected groups visited”** to group counting during this work. It helped us express tee-slot diversity in GroupMixer and compare its schedules with our independently validated results. GroupMixer comparisons supported the investigation; the optimality proofs are documented separately in this repository.

## Earlier work

The retained v1.1 solver introduced optional minimum-first fairness, logically implied strengthening constraints, and repaired complete/partial CSV hint loading. The four-round 15–24 fairness results and curated schedules were committed before v2.0. See [historical run notes](HISTORICAL_RUNS.md) and the Git history for the original experiments and subsequent proof work.
