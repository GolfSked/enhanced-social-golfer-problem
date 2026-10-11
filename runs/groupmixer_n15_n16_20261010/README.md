# GroupMixer 15- and 16-player verification — 2026-10-10

Both cases matched our proven optimum on the first Auto generation, without importing a schedule or hint.

| Players | Group capacities | Our optimum (minimum, total distinct tee slots) | GroupMixer | Unique pairs | Repeated pairs |
|---|---|---|---|---|---|
| 15 | 3,4,4,4 | (2,45) | (2,45) | 84 | 0 |
| 16 | 4,4,4,4 | (2,44) | (2,44) | 96 | 0 |

Each scenario has four rounds. Independent audits of assignments and exported roster CSVs confirm every player appears exactly once per round, exact group capacities, no repeated partners, and balanced fours participation. For 15 players, twelve players play three fours and three play four fours; for 16 players, everyone plays four fours.

Configuration: repeat threshold 1, squared penalty weight 10000; distinct visits to all tee groups minimum 2 at weight 10000, plus minimum 4 with linear weight 1 to maximize the total. The 15-player case also has combined fours visits minimum 3 and maximum 4 at weight 10000. Since our proofs exclude minimum 3, this models the benchmark optimum. The unmet all-four-slots aspiration shown by the app is not a benchmark violation.

The saved results report elapsed values of 2000ms (15) and 1000ms (16). These are app result timestamps, not a controlled runtime comparison.

Evidence: `n15_auto.json`, `n16_auto.json` contain inspected workspace/results; `groupmixer_n15.csv`, `groupmixer_n16.csv` preserve roster export preview text; `audit.json` records assignment audits; the two rotation JPGs capture app results. Reference optima are in `solutions/optimal/n15_tee_times.md` and `solutions/optimal/n16_tee_times.md`.

Result IDs: 15 — `cf8471c5-c6c9-4a99-931d-d55f74b127d3`; 16 — `6177e1fe-ab62-4efc-9967-5e9675f4fe3e`.
