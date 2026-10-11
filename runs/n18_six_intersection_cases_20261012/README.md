# Six intersection classes: 18 players, five rounds

Each case has a 1,200-second budget, including structural generation and ordering. Two cases run concurrently, with five CP-SAT workers each. Ordering uses up to 60 seconds and can finish slightly after the case deadline.

Unique partners imply a binary intersection matrix between two rounds. Its row and column sums are (3,3,4,4,4). Exhaustive enumeration produces 258 labelled matrices and six equivalence classes under permutations of the two triples and three fours on each axis. coverage.json records all six class sizes and representatives.

Representatives satisfy the existing first-appearance group normalization. Within each first-round group, players are ordered by their second-round group. Thus fixing these two rounds preserves a representative of every possible structure. The remaining three rounds retain their lexicographic symmetry breaking. Cases may overlap in full structural classes because a structure has multiple choices of its first two rounds.

An odd cycle in the ten-vertex triple graph selects precisely structures that cannot extend to 20 players. The previous three structural classes are excluded using their complete normalized assignment orbits. Each new structure is independently validated and its tee-time ordering optimized. UNKNOWN leaves a case open; INFEASIBLE exhausts its remaining structures. Only exhaustion of all cases together with exact ordering results could settle the whole nonextendable family.

No global optimality claim is made by launching this experiment. The current best score remains (4,72).
