# Nonextendable mixed-size structural enumeration pilot

Twenty-minute budget per invocation, ten workers. Structures are generated
without tee-time fairness requirements, then independently ordered. Complete
orbit exclusions prevent revisiting structural classes. checkpoint.json and
per-class orbit files support continuation. The last ordering solve can
overrun the pilot budget by up to60seconds. Exhaustion requires final
generation INFEASIBLE; a budget stop or UNKNOWN does not prove coverage.

## Complete normalization for3,3,4,4,4 groups

Fix first-round group sizes and labels. Choose any second round. No pair
repeats, so members of each first-round group occupy distinct second-round
groups. Order members by their second-round group labels. Within each size
category, second-round labels can be renamed by first appearance: groups
first encountered in the same first-round group are ordered together. This
produces both ascending labels inside each first-round block and canonical
first appearance. Later rounds also rename triples and fours separately
by first appearance. Finally sort the last three membership vectors
lexicographically. These operations affect only player, group and round names.

Each design's exact orbit considers20ordered first/second-round choices and
12size-preserving row orders times12size-preserving column orders. It labels
players by first-row block and ascending second-column membership, retains
canonical second-round name order, canonicalizes remaining rounds, and sorts
their vectors. This covers every normalized model assignment equivalent to
that structure. All orbit assignments are forbidden. Candidate membership
in its computed orbit and canonical uniqueness are checked.

The structure model enforces exact capacities, one/two triple appearances
per player and AllDifferent pairwise-round codes (unique partners). An
existential odd cycle in the ten-triple graph selects exactly nonextendable
structures, as proved in ../n18_r5_nonextendable_target73_1200s_20261011/README.md.
Fixed known extendable input is a positive control without the odd-cycle
condition and a negative control with it. No five-slot-player pin is used.

Ordering freely permutes both triples and all three fours each round, fixing
only a common first-round slot permutation. The minimum-first objective is
91times minimum plus total. Every input and extracted schedule is validated.
The extendable family already has proved optimum(4,72). Exhausting this
nonextendable family with exact ordering optima would complete the global
proof; incomplete enumeration does not.

Session completed: {"session": 1, "elapsed_seconds": 1200.0836436249665, "new_classes_this_session": 3, "total_classes": 3, "best_known": [4, 72], "exhausted": false, "all_orderings_proven": true, "pending_orderings": 0}

Session2 resumes the three saved exclusions with one uninterrupted generation solve using the remaining1,200-second invocation budget, ten workers. Session1 runner and configuration are preserved separately. If a new structure appears, its ordering is solved and generation may continue within the remaining budget.

Session completed: {"session": 2, "elapsed_seconds": 1200.2464106249972, "new_classes_this_session": 0, "total_classes": 3, "best_known": [4, 72], "exhausted": false, "all_orderings_proven": true, "pending_orderings": 0}
