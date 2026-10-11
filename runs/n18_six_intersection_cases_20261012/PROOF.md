# Global fairness optimum for 18 players over five rounds: (4,72)

Audited 12 October 2026. This is a computational proof for the repository's mixed-size model: two triples followed by three fours each round, unique partners, balanced participation, and lexicographic maximization of minimum individual distinct tee slots followed by total distinct slots.

## Coverage

The binary intersection matrix of any two rounds has row and column sums (3,3,4,4,4). Exhaustive enumeration gives 258 labelled matrices, in six size-preserving row/column permutation classes of sizes 6,72,36,36,72,36. The separate coverage audit explicitly transforms every labelled matrix to exactly one chosen representative.

Fixing a representative loses no full schedule: rename first-round groups within their size tiers, rename second-round groups within their tiers, and rename players within first-round groups by their second-round membership. Unique partners make those memberships distinct. The chosen representatives obey second-round first-appearance naming. Each remaining round can independently be named by first appearance within tiers, then the last three rounds sorted lexicographically. These are exactly the structural model's symmetry constraints.

## Exhausting the nonextendable family

Build a graph with ten vertices, one for each triple. Join the two triples in each round; also join two triples when they share a player. A schedule extends to a 20-player all-fours schedule exactly when this graph is bipartite. A proper colouring assigns the two added players to triples, once per round, without any repeated partner. Conversely any such extension supplies that colouring.

The original six searches use an odd-cycle circuit to select nonbipartite graphs. All six returned INFEASIBLE after excluding the complete assignment orbits of three previously found structures.

The audit replaces the circuit with a different condition: the five within-round edges force opposite colours, leaving sixteen colourings after fixing the first vertex's colour. Every one must have a monochromatic shared-player edge. All six cases again returned INFEASIBLE, taking at most 32.158373 solver seconds each.

All 1,896 excluded assignments were decoded and independently validated. Their orbit sets were regenerated from the saved source schedules. Exhaustive tee ordering, with the first round fixed by a common slot permutation and 12 choices in each remaining round, checks 20,736 assignments per structure. The three exact optima are (3,72), (3,68), and (3,72). Therefore no nonextendable schedule attains minimum spread four.

## Extendable family and conclusion

The previous complete 20-player catalogue contains ten structural classes, confirmed by a separate Boolean exclusion model. Every balanced two-player deletion is covered by the 228 recorded ordering problems in ../n18_via20_ordering_20261011/. All saved witnesses were revalidated and all OPTIMAL objective bounds checked; the best is (4,72).

Any 18-player schedule is either extendable or nonextendable, so these two families exhaust the model. Six players have four fours and one triple; they can visit at most three four-player slots and one triple slot, bounding the minimum spread by four. The extendable witness reaches four, and no schedule with that minimum exceeds total 72. Thus (4,72) is globally optimal under the stated fairness objective.

This is solver-backed computational evidence, not an independently checkable formal SAT certificate. It does not optimize the historical total-only objective or models allowing triples and fours to exchange tee-slot tiers.

Evidence: coverage.json, summary.json, audit.json, audit_coverage_ordering.json, audit_witnesses.json, configuration.json, and the saved source scripts and solver logs. The ordering and extendable-family audit depend on the previously recorded complete 20-player catalogue proof.
