# 19 players via deletion from 20 — completed

All 20 single-player deletions from the saved five-round 20-player schedule
were tested. Each resulting structure has exact group sizes 3,4,4,4,4 and
balanced fours participation. The ordering model permits every permutation
of the four four-player tee slots in each round; the triple is always first.
A common permutation of those slots preserves the score, so round one is
fixed without loss. Objective is 96 times minimum spread plus total spread.

Every deletion returned OPTIMAL with **(4,79)** and objective/bound 463.
Every saved witness passed independent schedule validation: 135 unique
pairs, zero repeated partners, 36 unmet pairs; fifteen players play four
fours and four play five fours. These are exact ordering optima for the
tested source structure, not a global n19 proof. No search is pending.
Source and script hashes, player mappings, all 20 solver logs and schedules,
and summary.json are retained. best_schedule.csv is a representative witness.

## A complete structural route

Any balanced 19-player/five-round schedule has 15 players appearing in one
triple and four players appearing in none. Its five triples are therefore
disjoint. Adding a twentieth player to each triple creates five rounds of
five fours and repeats no partner involving the new player. Existing pairs
are unchanged. Conversely, deleting any player from any valid 20-player
five-round schedule yields exactly this balanced 19-player participation.

Thus all feasible 19-player structures arise from valid 20-player structures
by deletion. The present experiment covers only one such source structure.
Generating structurally different 20-player designs and optimizing their
deletions is a justified next search; exhaustive structural coverage would
be needed to turn this route into a global proof. The source n20 tee-time
objective need not be optimized: its group membership is what matters here.
