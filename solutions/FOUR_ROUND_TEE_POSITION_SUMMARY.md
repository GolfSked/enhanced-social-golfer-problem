# Four-round tee-position breakdown — 19 October 2026

Counts are the number of players receiving each number of distinct tee-time positions across four rounds, taken from the current explorer. A position means first, second, etc., rather than a clock time.

“Other players met” counts distinct playing partners across all four rounds, shown as minimum–maximum or one number when equal.

| Players | 1 position | 2 positions | 3 positions | 4 positions | Total spread | Average | Fairness (minimum, total) | Other players met |
|---:|---:|---:|---:|---:|---:|---:|---|---|
| 15 | 0 | 3 | 9 | 3 | 45 | 3.00 | (2, 45) | 11–12 |
| 16 | 0 | 4 | 12 | 0 | 44 | 2.75 | (2, 44) | 12 |
| 17 | 0 | 0 | 5 | 12 | 63 | 3.71 | (3, 63) | 9–10 |
| 18 | 0 | 0 | 7 | 11 | 65 | 3.61 | (3, 65) | 10–11 |
| 19 | 0 | 0 | 8 | 11 | 68 | 3.58 | (3, 68) | 11–12 |
| 20 | 0 | 0 | 0 | 20 | 80 | 4.00 | (4, 80) | 12 |
| 21 | 0 | 0 | 0 | 21 | 84 | 4.00 | (4, 84) | 10–11 |
| 22 | 0 | 0 | 0 | 22 | 88 | 4.00 | (4, 88) | 10–11 |
| 23 | 0 | 0 | 0 | 23 | 92 | 4.00 | (4, 92) | 11–12 |
| 24 | 0 | 0 | 0 | 24 | 96 | 4.00 | (4, 96) | 12 |

The 16-player schedule was updated in explorer v1.3.0: P1–P12 receive three positions and P13–P16 receive two. All other player-count distributions are unchanged; placeholder numbering is now best-first throughout.

The saved schedules maximise the minimum distinct-position count first, then total spread. These objectives do not in general impose a balanced distribution within one; the 16-player schedule additionally satisfies that rule.

Players are now numbered best-first in every published schedule. New solver runs minimise the count receiving the minimum after preserving optimal minimum and total. [Third-priority results](../runs/tertiary_fairness_20261019/README.md).
