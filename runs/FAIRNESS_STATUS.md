# Current fairness status — 3 October 2026

Rules: four rounds, unique partners, balanced three/four-player participation,
triples before fours, and tee times seven minutes apart from 10:00. Fairness
maximizes minimum individual distinct tee slots, then total distinct slots.
No average-start-time objective or player-specific restrictions apply.

| Players | Best minimum / total | Fairness optimality |
|---:|---|---|
| 15 | 2 / 45 | Proven by sweep OPTIMAL status |
| 16 | 2 / 44 | Proven by sweep OPTIMAL status |
| 17 | 3 / 63 | Proven by global bound and exhaustive score-64 repeat cases |
| 18 | 3 / 65 | Proven by exhaustive two-class canonical exclusion of every fairness improvement |
| 19 | 3 / 68 | Proven by counting bound, total-70 exclusion and complete canonical score-69 exclusion |
| 20 | 4 / 80 | Proven; four distinct slots for everyone |
| 21 | 4 / 84 | Proven; four distinct slots for everyone |
| 22 | 4 / 88 | Proven; four distinct slots for everyone |
| 23 | 4 / 92 | Proven; four distinct slots for everyone |
| 24 | 4 / 96 | Proven; four distinct slots for everyone |

Validated attaining schedules for every count are in
`runs/n15_to24_fair_sweep_20261002/nN/solution_nN_sol.csv`.

Proof references:

- Original sweep: `runs/n15_to24_fair_sweep_20261002/`.
- 17-player proof: `runs/n17_target64_repeat_cases_20261002/`.
- 18-player fair upper bound: `runs/n18_20261001_214154/fair/run.json`,
  weighted bound 286 with weight 73, hence total <=67 at minimum 3.
- 18-player complete optimality proof: `runs/n18_canonical_two_rounds_20261003/`.
  Every improvement has a round pair with diagonal trace zero or one; exhaustive
  intersection-matrix enumeration gives one symmetry class for each. Both
  classes are INFEASIBLE with minimum >=3 and total >=66 in both formulations.
  This also excludes minimum four. Integer times: 11.495 and 3.562 seconds;
  retained formulation: 17.214 and 6.041 seconds.
- 19-player total-70 proof: `runs/n19_round_pair_targets_20261002/A/`.
- 19-player complete canonical score-69 proof:
  `runs/n19_canonical_two_rounds_20261003/`; integer formulation INFEASIBLE
  in 0.863 seconds, independently confirmed by the retained formulation in
  13.143 seconds without additional round-pair strengthening.

Historical total-only scores remain separate: the older 17-, 18- and
19-player references score 64, 66 and 69 with minimum 2. Higher total alone
does not outrank the proven minimum-first fairness scores above.

The retained generator `cp_sat_caseB_v1_1.py` and original schedules remain
unchanged by these latest experiments. The experimental integer formulation
is separate. Existing changes and all audits remain uncommitted. No run is
pending from these experiments.

## Five-round results — 11 October 2026

For 16 players, minimum spread **2** and total spread **51** are globally
optimal. Every player meets all 15 others exactly once. An exhaustive
grid/transversal enumeration covers all structures and 27,648 canonical
tee orderings. The full v2 CP-SAT model independently returns OPTIMAL after
fixing the second round by valid player relabelling; objective and bound
both equal 181. See [proof and validated witnesses](n16_r5_ordering_20261011/README.md).
The separate unrestricted run was interrupted after about 80 seconds once
these proofs completed; its FEASIBLE status remains recorded accurately.

For **17 players over five rounds**, **(4,76) is globally optimal** under the
minimum-first fairness objective. The participation bound proves minimum
spread cannot exceed four, and a validated schedule attains (4,76).
Total 79 was excluded in both integer and Boolean formulations. The complete
canonical trace-zero target test for minimum >=4 and total 77–78 returned
**INFEASIBLE in 173.068413 seconds**, within its 1,200-second cap. This excludes
every remaining improvement. See [the completed target test](n17_r5_target77_1200s_20261011/README.md)
and [the symmetry proof and validated witnesses](n17_r5_ordering_20261011/README.md).

For **18 players over five rounds**, minimum spread **4 is proven optimal**.
Both the corrected integer optimization and independent GroupMixer run attain
**(4,72)**; all players visit four distinct tee slots. Both schedules validate
with120 unique pairs,33 unmet pairs, and balanced fours participation (twelve
players three fours, six four fours). Integer status FEASIBLE after1200.032273
seconds, upper bound84. Total remains unresolved in72–84. See
[integer run](n18_r5_integer_fair_1200s_20261011/README.md) and
[GroupMixer comparison](groupmixer_n18_r5_1200s_20261011/README.md).

The subsequent n18/R5 complete feasibility target min>=4,total>=73 returned
UNKNOWN after1357.386375 solver seconds against a configured1200-second cap.
Both low-trace symmetry classes (60 seconds each) and the all-five-player
reduction (120 seconds) also returned UNKNOWN. These tests do not exclude
an improvement or tighten the72–84 total interval. See
[target and completion audit](n18_r5_target73_1200s_20261011/README.md).

The strengthened Boolean target min>=4,total>=73 with complete all-five-player
symmetry reduction also returned **UNKNOWN after1200.062642 seconds** (eight
workers, seed101). No improving witness or exclusion proof. The n18/R5 total
remains unresolved in72–84. See
[completed Boolean test](n18_r5_target73_boolean_1200s_20261011/README.md).

### Completed 19–24 player sweep

Each local run had a 120-second cap. Independent GroupMixer runs for 19 and
23 players also used 120-second budgets and improved the local witnesses.
Every saved schedule was independently validated for unique partners, exact
attendance and group sizes, and balanced three/four-player participation.

| Players | Best minimum spread | Best total spread | Proof status |
|---|---:|---:|---|
| 19 | 4 | 79 | Globally optimal; complete structural enumeration |
| 20 | 5 | 100 | Globally optimal |
| 21 | 5 | 105 | Globally optimal |
| 22 | 5 | 110 | Globally optimal |
| 23 | 5 | 115 | Globally optimal; targeted feasibility witness |
| 24 | 5 | 120 | Globally optimal |

The local 19-player result was (3,79); GroupMixer improved its minimum to four.
The local 23-player result was (4,106); GroupMixer improved its total to 107.
The subsequent minimum-five feasibility test found **(5,115)** in
**2.479319 seconds**, attaining the absolute ceiling. All 23 players visit
five distinct tee times, with 165 unique pairs and zero repeated partners;
15 players play four fours and eight play five fours. The independently
validated witness proves global optimality. See
[completed 23-player target test](n23_r5_min5_1200s_20261011/README.md).
All runs are complete. Remaining five-round proof gaps are 18 and19 players.
The complete 19-player target minimum >=4, total >=80 returned **UNKNOWN
after 1200.030140 seconds**. No improvement or exclusion proof was found;
the best remains (4,79), with total ceiling 91. See
[completed target test](n19_r5_target80_1200s_20261011/README.md).
All 20 single-player deletions from the saved n20/R5 source were subsequently
optimized over all tee orderings. Every structure has proven ordering optimum
(4,79). This excludes improvements within that source only, not globally.
Every valid balanced n19/R5 structure extends to n20 by adding a player to
its five disjoint triples, so other n20 structures provide a complete search
route. See [deletion experiment and structural argument](n19_via20_ordering_20261011/README.md).
The diverse-source batch generated 40 candidates, identifying seven new
structural classes. All 140 deletions were optimized exactly; none of these
classes permits minimum four. Best remains (4,79); bounded sampling is not
a global proof. All persisted schedules passed independent validation. See
[diverse-source experiment](n19_via20_diverse_20261011/README.md).
The complete normalized n20-extension target for n19 minimum >=4,total >=80
also returned **UNKNOWN after 1200.087539 seconds**. The positive control
reproduced (4,79), but no improvement or exclusion proof was found. Best
remains (4,79), total ceiling91. No run is pending. See
[completed normalized target](n19_via20_complete_target80_1200s_20261011/README.md).
The complete four-witness-pattern split also finished: 3+1, 2+2, 2+1+1,
and 1+1+1+1 each returned UNKNOWN at its 1,200-second cap. Two cases ran
concurrently with four workers each. No improvement or exclusion was found;
best remains (4,79), and all four cases remain mathematically unresolved.
Completed results agree with logs and source hashes match. Nothing is pending.
See [four-case batch](n19_r5_four_cases_parallel_1200s_20261011/README.md).

The subsequent resumable structural enumeration **proved (4,79) globally
optimal for n19/R5**. It found two additional n20/R5 classes, then excluded
all remaining normalized structures (INFEASIBLE in6.269440 seconds).
Ten exact structural classes cover1,336 normalized assignments. All200
single-player deletion ordering problems returned OPTIMAL; independently
read witnesses and optimal bounds agree, with maximum minimum-first score
(4,79). An independent Boolean formulation excluding those1,336 assignments
also returned INFEASIBLE in3.181106 seconds, confirming structural coverage.
Every balanced n19/R5 structure extends to n20 by adding a player to the
five disjoint triples, so this exhausts all possible n19 improvements.
Earlier UNKNOWN tests remain recorded above; they did not supply this proof.
**Only the18-player five-round total remains unresolved.** See
[enumeration proof and audits](n19_via20_enumeration_pilot_20261011/README.md).

For n18/R5, all228 balanced two-player deletions across the complete n20
catalogue were optimized, two concurrent cases with five workers each.
All returned OPTIMAL; best is(4,72). Independent saved-witness validation
and bound audits confirm the **entire family extendable to n20 has optimum
(4,72)**. Batch elapsed3.141691 seconds. This is not a global n18 proof:
nonextendable structures remain to be considered. No run is pending. See
[complete extendable-family test](n18_via20_ordering_20261011/README.md).
The complementary nonextendable-family target min>=4,total>=73 returned
UNKNOWN after1200.042054 seconds (ten workers, seed101). The triple-graph
odd-cycle condition exactly describes nonextendability; fixed-baseline
positive/negative controls passed. No improvement or exclusion proof was
found. Best remains(4,72); only nonextendable improvements remain unresolved.
The result and final log agree. No run is pending. See
[completed nonextendable target](n18_r5_nonextendable_target73_1200s_20261011/README.md).
The nonextendable structural enumeration pilot completed its20-minute budget
in1200.083644 seconds, finding three classes. Their exact ordering optima
are(3,72),(3,68),(3,72); saved witnesses and optimal bounds validate. Remaining
structure-generation attempts returned UNKNOWN at successive60-second caps;
enumeration is not exhausted. Best remains(4,72). Checkpoints preserve all
three complete orbit exclusions. No run is pending. See
[nonextendable enumeration pilot](n18_nonextendable_enumeration_pilot_20261011/README.md).
The resumed uninterrupted generation search also returned UNKNOWN after
1200.234760 solver seconds (session elapsed1200.246411). No new class was
found; all three exclusions are preserved. Nonextendable enumeration remains
incomplete and best remains(4,72). No run or ordering is pending.
Explicit triangle and five-cycle enumeration cases both completed UNKNOWN:
triangle1200.387169 seconds; five-cycle1199.947616 seconds. Neither found a
new class or proved exhaustion. Best remains(4,72); no run is pending. See
[completed cycle cases](n18_oddcycles_3_5_parallel_1200s_20261011/README.md).
See [local sweep and comparison](n19_to24_r5_sweep_20261011/README.md) and
[independent GroupMixer audits](groupmixer_n19_to24_r5_20261011/README.md).

## 12 October 2026: n18/R5 globally proved

The six first-two-round intersection cases all returned INFEASIBLE after
excluding the three known nonextendable structural classes. Coverage was
independently checked over all 258 labelled matrices (six classes). A second
nonextendability encoding rejecting all sixteen possible graph colourings
also returned INFEASIBLE in all six cases. All 1,896 excluded assignments
validate; brute-force enumeration of 20,736 tee orderings per class confirms
optima (3,72), (3,68), (3,72). Revalidation of the 228 complete extendable-family
ordering witnesses and bounds confirms best (4,72).
Together these exhaust both families and **prove (4,72) globally optimal for
18 players over five rounds under the minimum-first fairness objective**.
The earlier UNKNOWN entries above record historical results and are superseded
by this proof. No case remains pending. See
[proof and audit](n18_six_intersection_cases_20261012/PROOF.md).

## 12 October 2026: remaining GroupMixer comparisons

The six previously untested five-round cases all matched our optima: n15(3,51), n16(2,51), n20(5,100), n21(5,105), n22(5,110), n24(5,120). All saved assignments independently validate under strict ESGP rules. Combined with the earlier n17–19 matches, nine of ten are matched. The earlier n23 GroupMixer result (4,107) remains below (5,115) and was not rerun. No run remains pending. See [comparison and evidence](groupmixer_missing_r5_20261012/README.md).

## 12 October 2026: all ten GroupMixer five-round matches complete

The final n23 rerun matched(5,115), independently validated: all23 players
visit five distinct slots, fifteen have four fours and eight have five,165
unique pairs and zero repeats. Live completion93.9seconds within120-second
budget; no ESGP schedule supplied. GroupMixer has now matched all ten
five-round15–24 optima. Earlier n23(4,107) remains historical evidence.
No run remains pending. See [final23-player comparison](groupmixer_n23_r5_final_20261012/README.md).
