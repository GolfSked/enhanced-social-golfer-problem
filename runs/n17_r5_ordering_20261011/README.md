# 17 players over five rounds — ordering and minimum-four tests

The input pilot score is minimum spread 3, total spread 70. Groups per round
are three triples followed by two fours. Eleven players participate in two
fours and six in three fours. Every valid schedule has 105 distinct met pairs
and 31 unmet pairs.

`ordering.py` exhaustively checks 12^4 = 20,736 orderings of the input grouping
structure. Each round permits 3! × 2! equal-size group permutations; a common
permutation of tee slots allows the first ordering to remain fixed. The best
score is (3,70). This is a fixed-structure result, not global optimality.

## A bound and a complete minimum-four case split

Players participating in three fours can use at most two distinct four-group
slots and two distinct triple slots. Therefore minimum spread cannot exceed
four. The absolute total-spread bound is 11×5 + 6×4 = 79.

If minimum spread is at least four, each player repeats at most one tee slot
across five rounds. Consequently the sum of same-slot intersections across
all ten unordered round pairs is at most 17. Some round pair must therefore
have diagonal trace at most one; if all ten traces were at least two, the sum
would be at least 20.

Pair uniqueness means its 5×5 intersection matrix is binary, with row and
column sums (3,3,3,4,4). `round_pair_classes.py` enumerates all 453 such matrices.
Exactly 23 have trace at most one, forming four classes under simultaneous
permutations of equal-size slots and transposition. Selecting the pair as the
first two rounds, applying these common tee-slot permutations, and globally
renaming players preserves feasibility and the objective.

`test_min4_classes.py` tests every representative, fixing its first two rounds
and requiring at least four distinct tee slots for every player. The last three
rounds remain free. Each case has a 60-second CP-SAT cap with one worker. Logs,
model exports and results are preserved. Global exclusion is established only
if **all four** are INFEASIBLE; UNKNOWN does not exclude a case. A feasible
witness establishes feasibility of minimum four, subject to independent
validation. These tests run alongside the unrestricted search, so timings are
not comparative benchmarks.

The unrestricted 1,200-second search is recorded separately in
`../n17_r5_full_1200s_20261011/`, using the ordering witness as a hint.

## Improved schedules and targeted upper-bound tests

`integer_model_snapshot.py` adapts the retained integer experiment to five
rounds without changing its constraints. `test_min4_integer.py` positively
cross-forces the original pilot, then tests all four minimum-four classes with
an implied constraint: at most one pair of rounds can have equal tee slots
for any player. For five rounds, that is equivalent to at least four distinct
slots. All four cases have validated minimum-four witnesses. Their OPTIMAL
statuses refer to feasibility, not optimality of total spread.

`improved_ordering.py` reorders the first integer witness and reaches (4,74).
The unrestricted search improves to **(4,76)**. `optimize_min4_integer.py`
independently reaches the same score in two classes; its 60-second class runs
are FEASIBLE, not global optimality proofs. Their raw bounds can exceed the
external mathematical bound of 79 and should not replace that bound.

`cross_validate.py` forces the integer model's (4,76) witness into the Boolean
model, obtaining OPTIMAL for that fixed schedule and checking its weighted
score 420. Repeating round one as round two is correctly rejected.

At minimum spread four, total >=77 allows at most 85−77 = 8 repeated-slot pairs,
so some pair of rounds has diagonal trace zero. Exactly one of the four
canonical classes has trace zero. Therefore the score-77, 78 and 79 target
tests need only that one representative, without restricting the last three
rounds. The per-player bound `distinct <= 5 - extra_four` is implied by
participation: extra_four is one exactly when a player participates in three
fours, limiting that player to four distinct tee slots.

- `target77_integer.py`: UNKNOWN after the configured 120-second search.
- `target79_integer.py`: **INFEASIBLE**. Combined with the absolute bound 79,
  this proves total spread **at most 78** when minimum spread is four.
- `target78_integer.py`: UNKNOWN. Configured for 60 seconds; actual solver
  wall time was about 197 seconds, retained in its result record.
- `target79_boolean.py`: **INFEASIBLE** in about eight seconds, independently
  confirming the total upper bound of 78. It adds only logically implied
  repeat and participation bounds to the canonical target.
- `target77_boolean.py`: tests totals 77–78, using the proven exclusion of 79.
  UNKNOWN after 120 seconds; the total optimum is unresolved.

The original unrestricted search was restarted after 257.136 solver seconds
with the stronger (4,76) schedule as its hint. The restarted run has a
943-second cap, preserving approximately the original 1,200-second search
budget; it is recorded in `../n17_r5_full_remaining_943s_20261011/`.
That restart completed its cap, retaining (4,76) with FEASIBLE status. Combined
unrestricted solver time is about 1,200 seconds. Its raw weighted upper bound
remains 423 (total 79 at minimum four); the independent exclusions tighten
that upper bound to total 78.

The Boolean minimum-four feasibility tests returned UNKNOWN. Their fourth
case was interrupted after about 18 seconds once the integer witnesses had
established feasibility. No exclusion is inferred from these UNKNOWN results.

Minimum spread **four is proven optimal** by the participation bound and
validated witnesses. Total spread **76 is attained**, and the optimum is at
most **78**. The total component remains unproven until scores 77 and 78 are
excluded or an attaining upper-bound witness is found. The audit and source
hashes are in `source_audit.json`. No curated optimal schedule is claimed for
this case while that gap remains.

## Subsequent completion: global optimality established

The longer [target-77 integer test](../n17_r5_target77_1200s_20261011/README.md)
returned **INFEASIBLE in 173.068413 solver seconds** under a 1,200-second cap.
It uses the same complete trace-zero reduction and the already proven upper
bound 78. Thus totals 77 and 78 are excluded globally at minimum four.
Together with the earlier exclusion of 79, the minimum-four upper bound and
validated attaining witness, this proves **(4,76) globally optimal**.
The earlier UNKNOWN results above remain historical records; their unresolved
status is superseded by this completed proof.
