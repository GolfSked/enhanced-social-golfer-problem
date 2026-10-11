# Explicit triangle and five-cycle structural cases

Two concurrent cases, five workers each,1,200-second overall budget per case.
Each new structural class is ordered independently; the last ordering solve
can overrun by up to its60-second cap. The three previously checked class
orbits are excluded in both cases. These exclusions and source snapshots
are saved locally; earlier evidence is preserved.

The full normalized mixed-size structure model is retained. Instead of a
general AddCircuit condition, this model explicitly lists all undirected
simple cycles of the requested length on ten triple vertices:120triangles
and3,024five-cycles. Each cycle has its smallest vertex first and one of
its two directions selected, removing only rotation/direction duplicates.
A witness Boolean implies every required edge, and at least one witness
must hold. No fixed vertex/round placement is imposed: every placement
relative to the five round pairs is allowed, avoiding an unsafe symmetry
restriction. Other graph edges remain unrestricted.

Finding a requested odd cycle implies nonextendability. Cases may overlap;
each case keeps its own class exclusions. They cover all structures with
at least one triangle or five-cycle, not necessarily every nonextendable
structure. Seven/nine-cycle-only structures need separate treatment unless
a mathematical exclusion is established. Structure generation has no
tee-time fairness target; extracted schedules are validated and their
requested cycle is independently verified before exact ordering.

Per-case checkpoints, orbit exclusions, models, logs and schedules are
saved. Final per-case summary.json and batch summary.json record completion.
Only generation INFEASIBLE establishes exhaustion of a length family.
UNKNOWN and time-budget stops establish no exclusion.

Completed length case: {"cycle_length": 5, "completed": true, "elapsed_seconds": 1200.0366041670204, "new_classes": 0, "best_known": [4, 72], "exhausted": false, "all_orderings_proven": true, "attempts": [{"status": "UNKNOWN", "seconds": 1199.9476160000002}]}

Completed length case: {"cycle_length": 3, "completed": true, "elapsed_seconds": 1200.4791207499802, "new_classes": 0, "best_known": [4, 72], "exhausted": false, "all_orderings_proven": true, "attempts": [{"status": "UNKNOWN", "seconds": 1200.387169}]}
