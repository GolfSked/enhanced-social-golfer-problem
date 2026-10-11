# 18-player tee ordering via the complete 20-player catalogue

**Completed: the entire extendable family has optimum (4,72).**
All228 cases returned OPTIMAL in3.141691 seconds of batch elapsed time.
Every persisted witness validates, and every optimal bound matches its
minimum-first score. See audit.json and family_optimal_schedule.csv.
No case or run is pending. Global optimality remains unproven: structures
that do not extend to20 have not been excluded by this experiment.

Tests all228 balanced two-player deletions across the10 proven n20/R5
structural classes. Two concurrent cases, five workers each, seed101,
60-second cap per ordering problem. Each input and extracted witness is
independently validated. Sources, hashes, player mappings and solver logs
are retained. Existing evidence is preserved.

## Coverage and objective

Delete two players who never meet, so every round has two triples and three
fours. For balanced n18 participation, every remaining player must meet at
least one of the deleted players: then each plays three or four fours.
The union of their partner sets must therefore cover all18 retained players.
These necessary and sufficient tests select228 pairs across representative
classes. Every extendable n18 structure is represented by some deletion;
equivalent duplicates may remain and do not harm coverage.

Each round freely permutes its two triples within tee slots0..1 and three
fours within slots2..4. Fixing round-zero labels removes only a common slot
permutation, preserving distinct-slot scores. All other rounds are free.
Objective91 times minimum spread plus total is exactly minimum-first because
the total cannot exceed90. Balanced participation gives minimum ceiling4.

If all cases are OPTIMAL, the maximum proves the optimum for the entire
extendable family. It does not exclude n18 structures that cannot extend to
n20. Any improvement must still be independently validated. progress.json
records case completion; summary.json is written only when the batch ends.

Completed: {"completed": 228, "total_cases": 228, "elapsed_seconds": 3.141691291995812, "all_orderings_proven": true, "best_in_family": [4, 72], "best_known": [4, 72], "scope": "All balanced n18/R5 structures extendable to n20; not all n18 structures", "counts_by_class": {"0": 0, "1": 40, "2": 12, "3": 40, "4": 40, "5": 40, "6": 40, "7": 16, "8": 0, "9": 0}}
