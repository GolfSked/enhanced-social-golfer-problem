# 16 players, five rounds — global fairness optimum (2,51)

Every round has four fours. Every player meets all other 15 players exactly
once. The minimum-first tee-slot objective has proven optimum **minimum spread
2, total spread 51**. Minimum spread three is impossible.

## Independent proofs

`ordering.py` exhausts all 24^4 = 331,776 tee orderings of the original pilot
structure, fixing the first round's ordering by a common permutation of slots.
It confirms the incumbent (2,51), but this step alone is not a global proof.
See `result.json` and `schedule.csv`.

`global_enumeration.py` covers every possible five-round structure and ordering:

1. Between any two rounds, each four can intersect each other four at most
   once. Both rounds have four groups, so every intersection contains exactly
   one player. Global player relabelling therefore makes the first two ordered
   rounds the rows and columns of a 4×4 grid, preserving all tee-slot scores.
2. Every group in a later round must be a transversal of that grid: one player
   from each row and column. There are 4! = 24 transversals.
3. An exact-cover recursion enumerates all 24 partitions into four transversals.
   Two partitions are compatible precisely when each pair of their groups
   intersects at most once. Only two unordered triples of partitions are
   pairwise compatible. These exhaust the possible remaining three rounds.
4. The order of these three rounds does not change the objective. Each has
   24 tee-slot orders, giving 2 × 24^3 = **27,648** cases. Every case is scored;
   the lexicographic maximum is **(2,51)**.

The canonical grid fixes the *ordered* first two rounds by player relabelling;
there is no omitted tee-time ordering restriction. No classification theorem
about affine planes is required. See `partitions.json`, `global_result.json`
and the independently validated witness `global_schedule.csv`.

`canonical_crosscheck.py` independently uses the full v2 membership/pair
CP-SAT model. Its first round is already canonical. Fixing the second round
as ordered columns is valid by renaming players within first-round groups.
All remaining membership decisions are free. A relabelled enumerated witness
is supplied as a hint. CP-SAT returns **OPTIMAL**, weighted objective and bound
both **181** (65 × 2 + 51), in under one second. See `canonical_result.json`,
`canonical_solver.log`, `canonical_model.pbtxt` and `canonical_schedule.csv`.

## Original unrestricted search

The separate `../n16_r5_full_1200s_20261011/` run was launched with a 1,200-second
cap and the optimal ordering of the pilot as a hint. Once the independent
proof and canonical CP-SAT cross-check succeeded, it was interrupted after
about 80 seconds to avoid redundant computation. Its own status remains
FEASIBLE, score (2,51), weighted bound 185; it is not the optimality proof.
Its configuration, original source snapshots, log and validated schedule are
preserved unchanged.

## Reproduce

From the repository root, using the pinned dependencies:

```sh
.venv/bin/python runs/n16_r5_ordering_20261011/ordering.py
.venv/bin/python runs/n16_r5_ordering_20261011/global_enumeration.py
.venv/bin/python runs/n16_r5_ordering_20261011/canonical_crosscheck.py
```

The scripts write their own output files in this experimental directory.
`source_audit.json` records script/model/validator hashes and environment.
