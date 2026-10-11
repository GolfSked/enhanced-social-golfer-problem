# GroupMixer independent 17-player / five-round test

Generated in the browser on 11 October 2026, in a separate scenario named
“ESGP 17 players — five rounds”. No ESGP schedule was imported or provided as a hint.

The independently validated saved result scores minimum spread 4, total spread 71.
Fourteen players visit four distinct tee slots; three visit all five. All 105
pair meetings are unique, leaving 31 unmet pairs. Eleven players play in fours
twice and six three times. Every round fills capacities 3,3,3,4,4 exactly.
Our existing best (4,76) remains better; this test does not prove total optimality.
The documented external upper bound remains 78.

## Configuration

Five rounds, full attendance, tee slots named 10:00,10:07,10:14,10:21,10:28.
Avoid Repeats: threshold 1, squared, weight 10000.
Group Visits: combined fours min 2/max 3, weight 10000;
distinct groups min 4, weight 10000; distinct groups min 5, weight 1.
The first two preferences and repeat penalty dominate all possible gains in
last preference. Given the separately proven maximum minimum spread of four,
this searches the same feasible minimum-four region and then maximizes total.
Preferences are soft; compliance was independently checked from assignments.
The remaining app penalty 14 equals 85 minus total spread 71. The app's one
unmet preference is the aspiration that everyone visit five different groups.

Auto coordinator with four parallel lanes and minimum/maximum budget both
60 seconds. The saved result reports 60423.33 ms; the completion page showed
about 60.6 seconds. No cross-solver speed claim is made. Native search and
CP-SAT challenger/polish lanes were visible in the live cockpit.

## Evidence

- configuration.json: pre-run saved settings and exact scenario.
- result.json: full inspected selected result, IDs and raw assignments.
- schedule.csv: assignments mapped to Player 1–17 and chronological slots,
  in the repository's round/group/member format (not a site CSV export).
- audit.json: independent esgp_v2.validate check of that schedule.
- rotation.jpg: screenshot of the app's matching spread summary.

Workspace ID: c7b799a8-49f4-4088-b798-fdb8bf488c73.
Result ID: 49780df9-1c6a-45e2-9f8f-5436e0e7de27 (Result 3).
The result is saved locally in the in-app browser. No public share link was created.
