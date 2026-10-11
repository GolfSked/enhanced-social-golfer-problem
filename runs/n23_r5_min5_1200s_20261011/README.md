# 23 players over five rounds: minimum-five feasibility test

Target: every player visits five distinct tee slots, hence total 115. Exact
group sizes 3,4,4,4,4,4; no repeated partners; balanced fours participation
(15 players four fours, eight players five fours). Strengthened Boolean model,
eight workers, seed 101, 1,200-second cap. No schedule hint.

The generic fixed first round only relabels players and preserves all feasible
structures. AtMostOne per player and tee slot is equivalent to the target.
No additional symmetry restriction is used. A feasible witness attains the
global ceiling. INFEASIBLE excludes minimum five, but does not prove total 107
optimal at minimum four. UNKNOWN proves neither claim.

Completed: OPTIMAL after 2.479319 seconds. Validated (5,115) attains the absolute ceiling: globally optimal.
