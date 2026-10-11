"""Control-flow tests: gaps, unresolved counts and the explicit search bound."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from esgp_v2 import benchmark_range


class RangeTests(unittest.TestCase):
    def run_range(self, statuses, upper=128):
        summary = {"results": []}
        args = SimpleNamespace(max_players=upper, out=Path("unused"))
        def fake_solve(n, *_):
            return {"players": n, "status": statuses.get(n, "FEASIBLE")}
        with patch("esgp_v2.solve", side_effect=fake_solve):
            benchmark_range(9, args, summary, lambda: None)
        return summary

    def test_infeasible_counts_do_not_consume_quota(self):
        result = self.run_range({n: "INFEASIBLE" for n in range(10, 15)})
        self.assertEqual(result["feasible_count"], 10)
        self.assertTrue(result["range_complete"])
        self.assertEqual([r["players"] for r in result["results"]], list(range(9, 24)))

    def test_unknown_is_not_skipped(self):
        result = self.run_range({11: "UNKNOWN"})
        self.assertEqual(result["feasible_count"], 2)
        self.assertFalse(result["range_complete"])
        self.assertEqual(result["results"][-1]["players"], 11)

    def test_bound_leaves_range_incomplete(self):
        result = self.run_range({}, upper=12)
        self.assertEqual(result["feasible_count"], 4)
        self.assertFalse(result["range_complete"])
        self.assertIn("--max-players", result["stopped_reason"])


if __name__ == "__main__":
    unittest.main()
