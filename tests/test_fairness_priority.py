"""Check the third priority against two attaining schedules and test numbering."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cp_sat_caseB_v2 import build_model
from esgp_v2 import number_best_first, read_schedule, validate
from ortools.sat.python import cp_model


class FairnessPriorityTests(unittest.TestCase):
    def fixed_score(self, path):
        schedule = read_schedule(path, 16, 4)
        audit = validate(schedule, 16, 4)
        canonical = [list(range(13 - 4*g, 17 - 4*g)) for g in range(4)]
        mapping = {old: new for group, target in zip(schedule[0], canonical)
                   for old, new in zip(sorted(group), target)}
        schedule = [[[mapping[p] for p in group] for group in rd] for rd in schedule]
        model, solver, membership, _, _ = build_model(16, fair_spread=True, time_limit=10)
        for r, groups in enumerate(schedule):
            for g, members in enumerate(groups):
                for p in range(1, 17):
                    model.Add(membership[r, g, p] == int(p in members))
        solver.parameters.log_search_progress = False
        self.assertEqual(solver.Solve(model), cp_model.OPTIMAL)
        expected = 17 * (65 * audit['minimum_spread'] + audit['total_spread']) - audit['players_at_minimum']
        self.assertEqual(solver.ObjectiveValue(), expected)
        return solver.ObjectiveValue()

    def test_fewer_at_minimum_wins_without_changing_earlier_scores(self):
        original = self.fixed_score(ROOT / 'runs/n16_balanced_tee_positions_20261018/source.csv')
        improved = self.fixed_score(ROOT / 'solutions/optimal-4-rounds/n16_sol.csv')
        self.assertEqual(improved - original, 2)

    def test_weights_preserve_lexicographic_priorities(self):
        metrics = [(m, t, c) for m in range(1, 5) for t in range(16, 65) for c in range(1, 17)]
        key = lambda x: (x[0], x[1], -x[2])
        score = lambda x: 17 * (65 * x[0] + x[1]) - x[2]
        self.assertEqual(sorted(metrics, key=key), sorted(metrics, key=score))

    def test_numbering_preserves_schedule_quality_and_is_idempotent(self):
        schedule = read_schedule(ROOT / 'runs/n16_balanced_tee_positions_20261018/source.csv', 16, 4)
        ranked, mapping = number_best_first(schedule, 16)
        self.assertEqual(validate(ranked, 16, 4), validate(schedule, 16, 4))
        self.assertEqual(sorted(mapping.values()), list(range(1, 17)))
        counts = [sum(any(p in rd[g] for rd in ranked) for g in range(4)) for p in range(1, 17)]
        self.assertEqual(counts, sorted(counts, reverse=True))
        self.assertEqual(number_best_first(ranked, 16)[0], ranked)


if __name__ == '__main__':
    unittest.main()
