# 18 players, five rounds: interrupted Boolean fairness search

Configured for 1200 seconds, four workers, seed 101, original pilot hint. Stopped gracefully after 99.362 solver seconds when the user clarified parallel tests meant local integer programming plus GroupMixer. Run termination: **INTERRUPTED**. Raw CP-SAT status: **FEASIBLE**.

The persisted schedule independently validates at **(4,72)**: all 18 players visit four distinct tee slots; no repeated partners; 120 unique pairs and 33 unmet pairs. Twelve players play three fours, six play four fours.

Minimum spread four is globally optimal: the six players playing four fours can visit at most three distinct four-player slots and one triple slot. The total mathematical ceiling is 84 (twelve players at most five plus six at most four). Total 72 is not proven optimal and should not replace a stronger existing minimum-four witness if one exists. Raw objective bound 448 is weaker than this external bound.

Source snapshots, summary, solver log, persisted witness, audit and interruption metadata retained. No UNKNOWN or INFEASIBLE claim is made.
