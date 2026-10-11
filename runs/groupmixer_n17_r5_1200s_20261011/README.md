# GroupMixer 17 players / five rounds — 1,200-second comparison

The browser app independently matched our best validated score **(4,76)**.
It did not find 77 or 78 during the configured 1,200-second run. The global
minimum spread is already proven to be four; total optimum remains between
76 and the externally proven upper bound 78. This run adds no optimality proof.

## Validation

All five rounds fill chronological tee-slot capacities 3,3,3,4,4 exactly.
Attendance is complete, all 105 pair meetings are unique, and fours participation
is balanced: eleven players twice, six three times. Nine players visit four
slots and eight visit five, giving minimum four and total 76.
Both the checkpoint and final result pass the independent esgp_v2.validate audit.
The app's remaining preference penalty 9 equals 85 minus total spread 76.
The unmet preference is the aspiration that everyone visit all five groups.

## Settings and provenance

Same scenario and objective weights as the earlier 60-second test, which scored
(4,71). Only Auto's minimum and maximum total budgets changed from 60 to 1200.
Four parallel lanes; repeat avoidance threshold one, squared weight 10000;
combined fours visits min two/max three weight 10000; distinct slots min four
weight 10000; distinct slots min five weight one. These weighted preferences
prioritize benchmark compliance over possible gains in total spread.
No repository schedule was imported or used as a hint. The live UI showed a
random initial arrangement costing 560029, native attempts, a CP-SAT challenger
and a CP-SAT polish lane. Cost nine first appeared at the observed 186.8-second
progress check; this is a sampled observation, not an exact discovery timestamp.
Two best-so-far snapshots were saved during the run; the later snapshot was
opened and validated while the solver continued. Selecting the snapshot caused
the workspace inspection to report its completed status, but the solver cockpit
still visibly showed an active search; the live counter continued through
477.2, 600.5, 915.6, 1102.3 and 1164.3 seconds before final completion.

## Timing discrepancy

The final result and Runs page report **2000 ms**, despite the live search running
through the 1200-second budget. The Runs page records **time_limit_reached**.
A saved checkpoint reports 387443.33 ms, already far exceeding the final metadata.
Preserve the raw values; do not use the final 2-second figure as whole-run timing
or make a cross-solver speed comparison. The configured 1200-second budget is
verified in configuration.json. Final result retains that budget in its input.

## Artifacts

- configuration.json: verified pre-run scenario and settings.
- started.jpg: screenshot confirming search launched.
- prior_active_result.json: earlier (4,71) selected result during the running search.
- checkpoint.json / checkpoint_audit.json / checkpoint_schedule.csv: validated
  best-so-far snapshot, result 865c60cd-ad73-409c-b1b0-e37c42af99b4.
- completion_context.json / result.json: complete final result snapshot.
- result_audit.json / result_schedule.csv: final independent audit and schedule
  mapped to repository Player 1–17 / chronological slot format (not site CSV export).
- run_history.txt: DOM evidence of result history and stopping reason.
- rotation.jpg: final app spread summary.
- audit.py: rerunnable independent checks: `.venv/bin/python runs/groupmixer_n17_r5_1200s_20261011/audit.py result`.

Scenario: ESGP 17 players — five rounds.
Workspace: c7b799a8-49f4-4088-b798-fdb8bf488c73.
Final result: Result 6, 5bd7cc3d-a827-41b2-99ca-b1dff0611c74.
Saved locally in the in-app browser; no public share link created. Search finished.
