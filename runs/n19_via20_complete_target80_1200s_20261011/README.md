# Complete 19-player target via normalized 20-player extension

Target minimum four, total at least 80. Eight workers, seed101, 1,200 seconds.
Unlike the earlier sampling, this model does not exclude any structural
class. Logically implied total ceiling91 is included. A positive-control
solve admits the known (4,79) witness before the target80 test starts.

## Completeness of the normalization

In every balanced n19/R5 schedule, fifteen players play four fours and four
play five. The five triples are disjoint. Add player20 to each triple:
the result is a valid n20/R5 structure. Conversely every n20 deletion meets
the required n19 balance. Pairwise round intersection matrices are 5x5
zero/one matrices with row/column sums four, so missing cells form a matching.

Choose the first two rounds. Label their groups as rows and columns with
the missing matching on the diagonal. The deleted player occupies some
off-diagonal cell (a,b). A simultaneous row/column permutation maps a to0
and b to1. Every deletion is therefore represented by coordinate(0,1);
fixing it loses no structure. Players are then labelled by their unique
off-diagonal coordinates. Later group labels can freely be renamed to put
the deleted player's group at structural label0.

Tee-time labels are separate permutation variables for each round. The
deleted player's group must be tee0 (the resulting triple). First-round
four-tee labels can be fixed by a common permutation across all rounds,
which preserves every player's number of distinct tee times. Later tee
permutations remain free. There are no other structural restrictions.

AllDifferent pairwise-round membership codes exactly encode unique partners
in the 20-player extension. Exact capacities are four everywhere; first
two rounds have them by construction. The extension thus enforces balance
for the 19 retained players automatically.

INFEASIBLE proves (4,79) globally optimal. A feasible result is independently
validated and improves the best known score; UNKNOWN proves no exclusion.
The normalized baseline, positive-control result, source hashes, model,
solver log and completed result are retained.

Completed: UNKNOWN after 1200.087539 seconds. UNKNOWN leaves total unresolved; best remains (4,79).
