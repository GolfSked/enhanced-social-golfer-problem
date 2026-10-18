# Third-priority fairness and best-first numbering — 19 October 2026

The solver now maximises minimum distinct tee positions, then total distinct positions, then minimises players receiving the minimum. No across-player maximum-gap constraint is imposed. Lower player numbers receive higher distinct-position counts; previous IDs break ties. This is a deterministic allocation convention, not a measure of early/late start fairness.

## Results and evidence

- **15 players, four rounds:** at (2,45), the saved distribution is 3×2 + 9×3 + 3×4. `n15_r4/result.json` records CP-SAT INFEASIBLE for any schedule with at most two players at the minimum. The canonical first round fixes only player relabelling symmetry. Thus three is optimal.
- **16 players, four rounds:** at (2,44), write x/y/z for counts receiving 2/3/4 positions. Then x+y+z=16 and 2x+3y+4z=44 imply x=z+4, so at least four players receive two. The adopted 4×2 + 12×3 schedule attains that bound.
- **16 players, five rounds:** the bounded CP-SAT attempt returned UNKNOWN at 120 seconds; that attempt proves nothing about infeasibility. Separately, `global_enumeration_n16_five.py` exhausts every structure and ordering, preserving ordered slots under player relabelling. All first-two-round intersections are singletons, fixing them as rows/columns. It enumerates all 24 transversals, all 24 partitions into four transversals, both compatible triples of partitions and all 24³ orderings: 27,648 cases. Permuting rounds 3–5 does not change any player’s distinct-position count. `global_result.json` proves the best tuple is (minimum 2, total 51, minimum-count 3), attained by 3×2 + 7×3 + 6×4. The published witness already attains this; only its numbering changes.
- **All other published cases:** either all players receive the optimum minimum, or only the minimum and minimum+1 counts are possible. The fixed total then determines the number at the minimum, leaving no third-priority freedom. Three-round counts are bounded by three; five-round 15-player counts are bounded by its four tee groups.

## Players receiving the minimum in the published schedules

| Players | Three rounds | Four rounds | Five rounds |
|---:|---:|---:|---:|
| 15 | 9 | 3 | 9 |
| 16 | 12 | 4 | 3 |
| 17 | 1 | 5 | 9 |
| 18 | 18 | 7 | 18 |
| 19 | 3 | 8 | 16 |
| 20 | 20 | 20 | 20 |
| 21 | 21 | 21 | 21 |
| 22 | 22 | 22 | 22 |
| 23 | 23 | 23 | 23 |
| 24 | 24 | 24 | 24 |

## Reproduction and provenance

Run `.venv/bin/python runs/tertiary_fairness_20261019/experiment.py` for the bounded exclusion checks, or `.venv/bin/python runs/tertiary_fairness_20261019/global_enumeration_n16_five.py` for the global five-round proof. `cp_sat_caseB_v2.py`, `esgp_v2.py` and `source-sha256.json` preserve the solver implementation used.

`four-round-player-mappings.json` maps the previously published IDs to current IDs. `four-round-n*.csv` are current curated witnesses. Three- and five-round source manifests record mappings from their original saved witnesses; source logs and historical schedules are unmodified. Regeneration builders preserve the numbering policy. No min/total score or underlying group structure was changed by renumbering.

The historic two-component fairness label (minimum,total) remains visible in the explorer for continuity. Its allocation summary supplies the full distribution, and new solver records additionally include `players_at_minimum`.
