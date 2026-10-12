# GroupMixer missing five-round comparisons — 12 October 2026

Requested cases: 15,16,20,21,22,24 players, five rounds each. Dedicated workspace: b793381d-a3ce-45f3-99ff-c7125f03f07d, titled ESGP untested five-round comparisons 15 16 20 21 22 24. Previous workspaces and their results are preserved. No ESGP schedule is imported or supplied as a starting point.

Auto generation uses a 120-second target with four native lanes. Scenario settings and raw result inputs are recorded per case. Repeated pairs carry squared penalty weight10000; balanced fours participation and the proven minimum distinct-slot target use weight10000; the largest possible distinct-slot target uses linear weight1 to reward total spread. These are soft preferences, so every output is independently checked for strict ESGP validity.

The browser now exposes CP-SAT challenger/polish telemetry during Auto runs; results characterize the current GroupMixer implementation rather than an isolated comparison of its older native optimizer. Reported stored timings may differ from live timing. Screenshots and raw metadata preserve that distinction.

Run `.venv/bin/python runs/groupmixer_missing_r5_20261012/audit.py` to independently validate saved complete assignments, write CSVs and update audit.json. The audit checks attendance, exact prescribed group mix, partner uniqueness, fours balance and distinct-slot scores.

Completion results will be appended after all six cases finish.

## Completed results

All six cases matched on their first generation with the verified configuration. No run remains pending.

| Players | Our optimum | GroupMixer | Unique pairs | Result |
|---|---|---|---|---|
| 15 | (3,51) | (3,51) | 105 | [a98fd27f-0dcb-47f0-bcb1-4cc94a8c60c8](https://groupmixer.app/app/results/a98fd27f-0dcb-47f0-bcb1-4cc94a8c60c8) |
| 16 | (2,51) | (2,51) | 120 | [93587579-bb82-4eaf-8371-be7548fe40e4](https://groupmixer.app/app/results/93587579-bb82-4eaf-8371-be7548fe40e4) |
| 20 | (5,100) | (5,100) | 150 | [7e01a9b0-ce0e-4d16-8269-9352820bae6c](https://groupmixer.app/app/results/7e01a9b0-ce0e-4d16-8269-9352820bae6c) |
| 21 | (5,105) | (5,105) | 135 | [de06b1b1-bae3-4fe5-b9fc-4ccd9ed6f320](https://groupmixer.app/app/results/de06b1b1-bae3-4fe5-b9fc-4ccd9ed6f320) |
| 22 | (5,110) | (5,110) | 150 | [c0dd834e-68eb-4d7b-a5db-a0905285f174](https://groupmixer.app/app/results/c0dd834e-68eb-4d7b-a5db-a0905285f174) |
| 24 | (5,120) | (5,120) | 180 | [890c569f-c8ba-40f6-a387-60af26d3fe1d](https://groupmixer.app/app/results/890c569f-c8ba-40f6-a387-60af26d3fe1d) |

Together with the previously validated 17–19 matches, GroupMixer has matched nine of the ten five-round 15–24 benchmark optima. The prior 23-player result remains (4,107), below the proven (5,115); it was not rerun in this batch.
