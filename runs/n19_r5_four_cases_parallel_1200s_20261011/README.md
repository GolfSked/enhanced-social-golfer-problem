# Four smaller complete cases: 19 players over five rounds

Each test requires minimum spread >=4 and total >=80. Four workers per case, seed101,
1,200-second cap per case. Two cases run concurrently, up to roughly 40 minutes for two waves.
No hints. Source snapshot, hashes, models, logs and completed results retained.

## Why four cases cover every improvement

Nineteen spreads of at least four sum to at least76. Total >=80 implies
at least four players with spread five. Select any four of them. Every
five-slot player visits the triple exactly once: balanced participation
allows at most one triple per player, and five distinct slots include tee0.
Each triple holds three people. The selected players' triple-appearance
counts are five integers in0..3 summing to4. Up to round order there are
exactly four patterns: (3,1,0,0,0), (2,2,0,0,0), (2,1,1,0,0), (1,1,1,1,0).
The runner independently enumerates these integer patterns and asserts this.

The selected four are witnesses, not necessarily all five-slot players.
More than four five-slot players remain allowed. Cases may overlap, which
does not harm exhaustive coverage. In any improving schedule, choose four
and reorder rounds to their sorted pattern before applying the normalized
20-player grid. Every such ordered schedule still normalizes with the deleted
player at(0,1). Round-zero tee labels may then be permuted commonly without
changing any spread or triple appearance. No prior sampling exclusions or
extra round symmetry restrictions are applied.

The model snapshots the complete normalized extension formulation. Its
coverage argument and positive control are recorded in
../n19_via20_complete_target80_1200s_20261011/README.md.
Selection implies spread five; selected AND tee0 indicators enforce each
pattern exactly. All other players retain their original freedom.

If all four cases are INFEASIBLE, (4,79) is globally optimal. A validated
witness improves the score. Any UNKNOWN case prevents an exclusion proof.
progress.json identifies the active case; results.json is updated after
each case; summary.json exists only after all four complete.


Supersedes the interrupted sequential batch; original files are preserved.

Case 2_2_0_0_0: UNKNOWN, 1200.015922 seconds.

Case 3_1_0_0_0: UNKNOWN, 1200.069870 seconds.

Case 2_1_1_0_0: UNKNOWN, 1200.012658 seconds.

Case 1_1_1_1_0: UNKNOWN, 1200.023039 seconds.

All four cases completed. UNKNOWN cases leave total optimality unresolved.
