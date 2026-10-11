# v2.0 — configurable rounds and ten-player-count benchmark ranges

The v2 solver accepts any positive round count, default four. Every player
appears once per round. Each unordered pair meets at most once. The group mix
maximises the number of fours, using zero to three triples to fill the remainder;
triples precede fours in the tee-time order. Counts that cannot form this mix
are inadmissible. Participation in fours differs by at most one across players.

Fairness is lexicographic: maximise the minimum number of distinct tee slots,
then their sum. For N players, R rounds and G groups, weight
`N * min(R, G) + 1` makes one unit of minimum spread outweigh every possible
change in total spread. Tee slot g starts at 10:00 + 7(g−1) minutes.

## Usage

```sh
.venv/bin/python esgp_v2.py --rounds 3 --out runs/my-three-round-range
.venv/bin/python esgp_v2.py --rounds 5 --out runs/my-five-round-range
.venv/bin/python esgp_v2.py --n 18 --out runs/my-four-round-case
.venv/bin/python esgp_v2.py --rounds 5 --n 15 --hint some_schedule.csv --out runs/my-hinted-case
```

Without `--n`, minimum discovery starts at three players and checks each count
in increasing order, up to `--max-players` (default 128, also the benchmark search bound). Necessary mathematical
conditions reject impossible counts before model construction. Remaining cases
are solved for feasibility. Discovery stops at UNKNOWN or MODEL_INVALID;
there is no claim of a minimum or benchmark range past an unresolved case.
Once a feasible minimum is proven, counts are optimised in ascending order
until ten feasible player counts have been collected, including the minimum.
INFEASIBLE counts are recorded but do not consume the quota. OPTIMAL and
FEASIBLE both count; optimality is not required to meet the quota. UNKNOWN or
MODEL_INVALID stops the benchmark with an incomplete range, preserving the
ordering rather than silently skipping an unresolved count. The summary records
`feasible_count` and `range_complete`; reaching `--max-players` can also leave
the range incomplete.

The default time limit is 60 CP-SAT seconds **per case**, excluding model
construction and validation. Discovery and optimisation of the first count
are separate solves. There is no guarantee a bounded search discovers a
minimum for every round count. `--time-limit`, `--workers` and `--seed` control
search. The output directory must not exist; prior results are never overwritten.

Each run saves its configuration, environment, model/runner source snapshots
and hashes, solver logs, status, objective and bound, and independently validated
CSV schedules. The validator checks exact attendance, capacities, pair uniqueness,
participation balance and spread. OPTIMAL in a discovery record means a
feasibility problem was solved; only OPTIMAL in a fairness record proves the
fairness objective. FEASIBLE is an incumbent, INFEASIBLE an exclusion, and
UNKNOWN is unresolved. CP-SAT OPTIMAL has no user-set gap tolerance here.

## Mathematical starting points

For three and four rounds, nine players are feasible in three triples, using
parallel classes of the affine plane of order three. Thus the automatic ranges
begin at **9**, with 10–14 infeasible under the prescribed mix and balance.
They continue beyond 18 until ten feasible counts have been found.
The existing four-round 15–24 collection is preserved as a historical proven
benchmark collection, not described as starting at the global minimum.

For five rounds, the minimum is **15**, and the first candidate range is **15–24**, extending if any count is infeasible. Remove one
player from the 16-player, five-round affine-plane construction. Each remaining
player participates in one triple and four fours and meets every other player.
These are feasibility constructions, not claims about optimal tee-time spread.

The mathematical exclusions used in the runner are necessary conditions:

1. Each player has `2R + f` distinct partners, where f is their fours count.
   The largest balanced count cannot exceed N−1.
2. With at least two rounds, every group in one round must split across
   distinct groups in another, so its size cannot exceed G.
3. If G=4, every four intersects every group in another round exactly once.
   With q fours per round, there are `C(R,2) * q²` four/four intersections.
   Balance independently implies `sum_p C(f_p,2)` such intersections.
   Any mismatch rules out the case.

No exclusion asserts that passing these conditions establishes feasibility.
The 15-player five-round construction and mathematical exclusions establish
minimality independently of search; pilot discovery also checks the model.

## Preservation and verification

`cp_sat_caseB_v1_1.py` remains unchanged. `cp_sat_caseB_v2.py` generalises its
model, and `esgp_v2.py` supplies the new interface. The curated schedules moved
to `solutions/optimal-4-rounds/`; all CSV and tee-time summary bytes are unchanged.
The validation index and current documentation point to the new directory.
Historical run snapshots retain their original paths/text as audit evidence.

Run `.venv/bin/python tests/check_v2.py` for four-round model equivalence,
validation of all ten curated schedules, fixed-schedule solver acceptance,
a five-round constructive example, and rejection of an invalid schedule.
The regression checks do not rerun expensive four-round optimality proofs;
identical model protos preserve their applicability.

GroupMixer supplies comparison schedules. Its outputs require independent
validation and scoring under these rules. This implementation does not fetch
GroupMixer results or treat its generic contact score as tee-time fairness.
Initial 10-second pilots are engineering checks; they are not comparable solver
performance benchmarks and may run concurrently on the same machine.

The initial pilot records used the earlier ten-consecutive-count policy and are
preserved unchanged. New runs use the ten-feasible-count policy. Run
`.venv/bin/python tests/test_v2_range.py` to check quota accounting, unresolved
counts and the search bound.
