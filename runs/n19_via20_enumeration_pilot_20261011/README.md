# Resumable 20-minute structural enumeration pilot

**Completed with a global proof: n19/R5 optimum is (4,79).**

The pilot exhausted the normalized structures in9.856794 seconds, far inside
its1,200-second budget. Two new classes supplement the eight inherited ones.
The final generation returned INFEASIBLE in6.269440 seconds. The10 classes
cover exactly1,336 normalized assignments, with disjoint orbit sets.
All200 deletion orderings returned OPTIMAL. Independently reading every
saved witness and checking its recorded bound gives best score(4,79).

An independent Boolean membership/pair-indicator formulation excludes
all designs outside those1,336 assignments: INFEASIBLE in3.181106 seconds.
This differs from the integer round-pair AllDifferent generation model.
See boolean_exclusion.py/result/log and ordering_audit.json. crosscheck.py
additionally attempts raw solution enumeration without orbit exclusions;
its separate result records whether its120-second audit budget sufficed.
That supplementary raw enumeration stopped at120.003204 seconds with FEASIBLE:
1,030 of1,336 assignments were visited, with none outside the recorded list.
It is not an exhaustion proof. Exhaustion is established by the completed
integer exclusion and independent Boolean exclusion tests above. No run is
pending from this pilot or its audits.

All balanced n19/R5 schedules extend to a valid n20/R5 schedule by adding
one player to each of the five disjoint triples. Conversely any n20 deletion
is balanced. The exhaustive structural coverage and exact deletion ordering
therefore exclude every n19/R5 score above(4,79), not merely the sampled designs.
All previously UNKNOWN feasibility results remain historical evidence only.

Uses ten solver workers in one process. Each invocation has a 1,200-second
overall budget, checked between solves; a final ordering solve can overrun
by up to its 60-second cap. Every new structural class has all 20 deletions
optimized and independently validated. Eight previously tested classes
are inherited with their completed exact ordering evidence.

Unlike earlier sampling, each discovered class is excluded in every equivalent
normalized assignment. The first two rounds are the off-diagonal 5x5 grid;
within-round names use first occurrence. The remaining three assignment
vectors are lexicographically ordered, removing only round naming symmetry.
For each ordered pair of rounds and each of 120 row orders, missing cells
force column labels and unique player coordinates. Normalizing each remaining
round's group names and sorting its vector yields every model assignment
equivalent to the design. All of these assignments are forbidden together.
Thus subsequent feasible candidates belong to genuinely new classes.

The initial eight orbit sets are checked disjoint; each new candidate must
lie in its own orbit and have a previously unseen canonical form. No fairness
requirements restrict structure generation. All possible n19 structures
extend to n20, so complete n20 enumeration plus exact deletion ordering covers
every n19 possibility. Only a final generation INFEASIBLE proves enumeration
exhaustion. UNKNOWN does not exclude anything, and the pilot budget alone
cannot establish optimality.

checkpoint.json saves all excluded assignments and class ordering progress.
Rerunning run.py resumes from it with another 20-minute budget. Generation
logs and per-class source/deletion schedules are retained. summary.json and
session files are written at completion. Any improved witness is saved as
best_schedule.csv. No curated solution or earlier evidence is overwritten.

Session result: {"session": 1, "elapsed_seconds": 9.85679433302721, "new_classes_this_session": 2, "total_classes": 10, "best_score": [4, 79], "exhausted": true, "ordering_complete": true, "all_orderings_proven": true, "stop": "All normalized structures excluded"}
