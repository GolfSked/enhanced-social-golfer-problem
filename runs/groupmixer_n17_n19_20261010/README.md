# GroupMixer 17- and 19-player app comparison — 10 October 2026

Both cases were configured and generated in the GroupMixer browser app using
placeholder Player names. No reference schedule was imported or supplied as a hint.

| Case | GroupMixer minimum / total | Proven ESGP optimum | Unique pairs | Repeated pairs |
|---|---|---|---|---|
| 17 | 3 / 63 | 3 / 63 | 84 | 0 |
| 19 | 3 / 68 | 3 / 68 | 108 | 0 |

Independent audits of both exported CSV previews passed coverage, exact ordered
capacities, pair uniqueness, balanced four-player participation and objective
values. The 17-player distribution is five players with three distinct slots and
twelve with four; two players have one four-player round and fifteen have two.
The 19-player distribution is eight players with three distinct slots and eleven
with four; twelve players have three four-player rounds and seven have four.

## Configuration and interpretation

Four rounds, full attendance, capacities summing to the player count, with all
three-player groups named as the earliest tee times. Group order in the app is
different from chronological order; names establish the intended tee slots.
Total capacity equals attendance, so every group is filled exactly.

GroupMixer represents size participation and distinct-group targets as weighted
preferences. Combined visits to four-player groups target 1–2 for 17 players and
3–4 for 19 players, weight 10000. Distinct visits to all groups target minimum 3,
weight 10000, plus minimum 4, weight 1. Avoid Repeats uses threshold 1, squared
penalty and weight 10000. Thus any single violation of the benchmark rules costs
more than every possible gain in total variety. Within the feasible minimum-3
region, the remaining linear penalty is 4n minus total distinct slots. Our
separate proofs exclude minimum 4, so this models the same optimum for these
cases. Strict compliance is established by the independent schedule audit.
The 17-player case also retains the default Maximize Contacts objective at weight
1, which is constant on benchmark-feasible schedules.

The app shows one unmet preference because minimum 4 for everyone is an
unattainable aspiration. Its remaining cost is 5 for n17 and 8 for n19, exactly
the unavoidable deficit from four distinct tee times per player.

## Runs and timing limits

The first Auto generation for n17 attained (3,63). The saved result reports
1000 ms solver elapsed time. The first Auto generation for n19 attained (3,67)
and reports 2000 ms. A fresh n19 generation with a manual 60-second budget
produced a new saved result attaining (3,68). Its selected result reports 1000 ms,
which is not the wall-clock duration of the full 60-second generation workflow.
These values must not be treated as a controlled cross-solver speed comparison.
The app retained the older active result after the longer generation; the new
best result was opened from Saved results and audited separately.

## Evidence

- `groupmixer_n17.csv`, `groupmixer_n19.csv`: unchanged CSV export-preview text.
- `n17_auto.json`: full inspected workspace and selected result.
- `n19_auto_first.json`: initial (3,67) workspace/result snapshot.
- `n19_auto_60s.json`: selected optimal result after the 60-second generation.
- `audit.json`: independent assignment-based audit summaries.
- `n17_rotation.jpg`, `n19_rotation.jpg`: app rotation pages confirming scores.

Both scenarios remain saved locally in the in-app browser under names
“ESGP 17-player tee-time benchmark” and “ESGP 19-player tee-time benchmark”.
No public share link was created.
