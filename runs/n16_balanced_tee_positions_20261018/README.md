# 16-player balanced tee-position experiment

A validated witness exists for exactly 12 players visiting three distinct tee positions and four players visiting two positions across four rounds.

Starting with the currently published four-round, 16-player schedule, swap tee positions 3 and 4 in rounds 2 and 4. All group memberships remain unchanged. Rounds 1 and 3 remain unchanged.

The four players with two positions are P2, P6, P12 and P15. Everyone else has three. Total spread remains 44; minimum remains 2. This retains the previously proved optimal minimum-first/total-second fairness score while additionally balancing distinct-position counts within one.

The independent validator confirms exact attendance, four groups of four each round, no repeated unordered player pair (96 unique pairs), and balanced fours participation. It also re-reads and validates the persisted CSV. This is a constructive feasibility proof, not a new global solver optimisation run.

Reproduce from the repository root:

```sh
.venv/bin/python runs/n16_balanced_tee_positions_20261018/experiment.py
```

`source.csv` freezes the published schedule used as input; `schedule.csv` is the reordered witness; `players.csv` lists individual positions; `result.json` records the audit and old-to-new slot mapping. The first witness occurs after 578 orderings tested.

`groupmixer-scenario.json` is an unexecuted GroupMixer API scenario using the saved distinct-group visit format: strongly penalise counts outside 2–3 and repeated pairs, and prefer at least three distinct positions. A successful target result has zero repeats, zero range violations and four units of the prefer-three penalty. Weighted preferences require independent result checking; this file does not establish a GroupMixer solve result.

The first-twelve variant was adopted in the four-round explorer and curated 16-player schedule in release 1.3.0. Other player counts and round counts are unchanged.

## First twelve players receive three positions

`first-twelve-schedule.csv` relabels the same witness so P1–P12 have three distinct positions and P13–P16 have two. `first-twelve-players.csv` records individual positions and `first-twelve-result.json` preserves the original-to-new player mapping and independent validation. This changes which placeholder receives each schedule; an existing named roster would therefore receive different assignments.
