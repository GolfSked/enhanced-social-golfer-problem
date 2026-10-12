# Final 23-player five-round GroupMixer comparison — 12 October 2026

GroupMixer independently matched the proven ESGP optimum **(5,115)**. All23 players visit five distinct tee slots; fifteen players have four fours and eight have five. Zero repeated partners,165 unique pairs,88 unmet pairs. No reference schedule or ESGP hint was imported.

Scenario: one triple followed by five fours, five sessions. Repeat threshold1, squared penalty weight10000; distinct groups>=5 weight10000 plus the same target weight1; combined fours visits4..5 weight10000. These soft preferences were independently verified as strictly satisfied. Auto budget120seconds, four native lanes, with the current app's CP-SAT challenger/polish telemetry. The live completion screen reports93.9seconds; stored elapsed fields are raw telemetry rather than a controlled timing comparison.

Result: [b90e772b-c1d2-4637-9a2f-bb0a0f741e6d](https://groupmixer.app/app/results/b90e772b-c1d2-4637-9a2f-bb0a0f741e6d).

Evidence: configuration.json, result.json, completed.jpg, rotation.jpg, independently reconstructed groupmixer_n23.csv, audit.py and audit.json. Run `.venv/bin/python runs/groupmixer_n23_r5_final_20261012/audit.py` to reproduce validation. Earlier (4,107) comparison remains preserved in its original run directory.

Combined with the earlier17–19 matches and the six cases in ../groupmixer_missing_r5_20261012/, GroupMixer has now matched **all ten five-round optima for15–24 players**. All runs are complete. Proofs of ESGP optimality remain separate from finding matching schedules.
