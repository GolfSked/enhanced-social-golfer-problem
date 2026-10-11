# Diverse 20-player structures for the 19-player problem

Completed 40 candidate generations in 21.827965 seconds, identifying seven
new structural classes distinct from the earlier 20-player source. All 20
deletions of each new representative were optimized: 140 exact ordering
optima. Best known globally remains **(4,79)**. No search is pending.

| New class | Representative candidate | Best deletion score |
|---|---:|---|
| 1 | 1 | (3,77) |
| 2 | 2 | (3,79) |
| 3 | 4 | (3,76) |
| 4 | 6 | (3,77) |
| 5 | 14 | (3,77) |
| 6 | 15 | (3,76) |
| 7 | 23 | (3,78) |

Every deletion returned OPTIMAL with matching objective and bound, so none
of these seven structural classes permits minimum spread four after deletion.
This excludes the sampled classes, not all possible 20-player structures.
Generation status OPTIMAL is feasibility status with no objective, not a
certificate of structural enumeration completeness. Sampling stops at 40.

## Model and structural equivalence

Twenty players occupy five fours in each of five rounds. Pairwise round
membership codes are AllDifferent, exactly expressing unique partners.
Any two rounds have a 5x5 intersection matrix of zeroes and ones with four
ones per row and column. Their missing cells form a matching. Relabelling
normalizes the first two rounds to the off-diagonal cells of a 5x5 grid
without losing any structure. Other rounds have group labels ordered by
first player occurrence. Each generated assignment is excluded before the
next solve; equivalent relabellings may still be generated.

Exact structural equivalence is checked separately. For each ordered round
pair and each of 120 orderings of its first-round groups, the missing matching
forces second-round group labels. Player coordinates are unique. Sorting
remaining group and round partitions removes residual naming. The minimum
encoding over all 2,400 choices is canonical under player, round and group
relabelling. Matching encodings are duplicates. Each new class was checked
under random player/round/group relabelling, preserving its encoding.

The deletion ordering model freely permutes fours each round, retaining the
triple as tee one. Fixing round-one four-slot labels removes only a common
permutation preserving score. Objective is 96 times minimum plus total.

## Audit and evidence

All 40 persisted source schedules and all 140 persisted deletion schedules
were independently read and validated. All ordering bounds match the scores.
Source and runner hashes, initial model export, generation and ordering logs,
canonical forms, mappings and witnesses remain saved. See summary.json,
candidates.json and audit.json.

The original class remains the only tested class permitting minimum four.
A useful next experiment is a complete normalized structural search with
the minimum-four deletion requirement included. It must retain all possible
positions of the deleted player in the normalized two-round grid. A bounded
UNKNOWN remains inconclusive; exhaustive exclusion could establish optimality.
