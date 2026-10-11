# Nonextendable 18-player/five-round improvement test

Target minimum >=4,total >=73. Strengthened Boolean model, ten workers,
seed101,1,200-second cap. No hint. Controls admit the fixed known(4,72)
schedule without the nonextendability condition and reject it with that
condition. Model, source hashes, logs and results are retained.

## Exact nonextendability condition

Create ten vertices, one per triple (two per round). Join the two triples
within each round. Also join triples that contain the same player in two
different rounds. Balanced participation means twelve players belong to
two triples each and six belong to one each. Pair uniqueness prevents
two triples from sharing more than one player.

This graph is bipartite if and only if the structure extends to20 players.
A two-colouring gives each new player one triple per round, and gives each
twice-in-triples player one appearance with each new player. No partners
repeat. Conversely, any extension to20 assigns the new players to opposite
triples each round and opposite ends of every shared-player edge, providing
a two-colouring. Deleting two players to obtain exact3,3,4,4,4 sizes requires
them to be separated every round, so there is no alternative extension type.

A finite undirected graph is nonbipartite exactly when it has an odd cycle.
The model existentially selects a simple directed circuit on the underlying
undirected edges, with unused vertices represented by self-loops. Its length
is3,5,7 or9. Every odd simple cycle is allowed; graph edges outside the chosen
cycle remain unrestricted. This describes exactly the nonextendable family.

At least one five-slot player exists in any target73 improvement. Relabel
that player18 and reorder rounds by their five tee slots; then relabel the
other players within round zero to the generic fixed first round. This
preserves graph bipartiteness and all objective/participation conditions.
The pinned five-slot-player symmetry therefore retains every improvement.

The extendable family is already proved bounded by(4,72) in
../n18_via20_ordering_20261011/README.md. Consequently INFEASIBLE here would
complete the global n18/R5 proof. UNKNOWN does not exclude an improvement.

Completed: UNKNOWN after 1200.042054 seconds. UNKNOWN leaves nonextendable improvements unresolved; best remains (4,72).
