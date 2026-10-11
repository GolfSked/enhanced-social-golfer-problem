#!/usr/bin/env python3
"""Configurable-round solver and ten-count benchmark runner."""
import argparse
import csv
import hashlib
import itertools
import json
import math
import platform
import shutil
import time
from collections import Counter
from pathlib import Path

import ortools
from ortools.sat.python import cp_model
from cp_sat_caseB_v2 import build_model, group_distribution, load_hints_from_csv


def exclusion(n, rounds):
    """Necessary conditions only: None means unresolved, never feasible."""
    try:
        sizes = group_distribution(n)
    except ValueError as error:
        return str(error)
    groups, fours = len(sizes), sizes.count(4)
    low, extra = divmod(rounds * 4 * fours, n)
    if 2 * rounds + low + bool(extra) > n - 1:
        return "Balanced partner count exceeds the available distinct partners"
    if rounds >= 2 and max(sizes) > groups:
        return "A group cannot split across the next round without repeating a pair"
    if rounds >= 2 and groups == 4:
        # Each four intersects every group in another round exactly once.
        required = math.comb(rounds, 2) * fours * fours
        actual = (n - extra) * math.comb(low, 2) + extra * math.comb(low + 1, 2)
        if required != actual:
            return f"Four/four intersection count requires {required}, balance permits {actual}"
    return None


def validate(schedule, n, rounds):
    """Independent validation from extracted groups, not solver variables."""
    sizes = group_distribution(n)
    assert len(schedule) == rounds, "Wrong number of rounds"
    pairs = Counter()
    visits = {p: set() for p in range(1, n + 1)}
    fours = Counter({p: 0 for p in visits})
    for groups in schedule:
        assert [len(g) for g in groups] == sizes, "Wrong group capacities"
        assert sorted(p for g in groups for p in g) == list(visits), "Wrong attendance"
        for slot, members in enumerate(groups):
            pairs.update(itertools.combinations(sorted(members), 2))
            for p in members:
                visits[p].add(slot)
                fours[p] += len(members) == 4
    assert max(pairs.values(), default=0) <= 1, "Repeated partners"
    assert max(fours.values()) - min(fours.values()) <= 1, "Unbalanced fours participation"
    spread = [len(v) for v in visits.values()]
    return {"minimum_spread": min(spread), "total_spread": sum(spread),
            "spread_distribution": dict(sorted(Counter(spread).items())),
            "fours_distribution": dict(sorted(Counter(fours.values()).items())),
            "unique_pairs": len(pairs), "unmet_pairs": math.comb(n, 2) - len(pairs)}


def read_schedule(path, n, rounds):
    sizes = group_distribution(n)
    rows = {}
    with open(path, newline="") as source:
        for row in csv.reader(source):
            r, g, *members = map(int, row)
            assert (r, g) not in rows, "Duplicate round/group"
            rows[r, g] = members
    assert set(rows) == {(r, g) for r in range(1, rounds + 1)
                         for g in range(1, len(sizes) + 1)}, "Wrong round/group coverage"
    return [[rows[r, g] for g in range(1, len(sizes) + 1)]
            for r in range(1, rounds + 1)]


def solve(n, args, directory, fairness=True, hint=None):
    directory.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    result = {"players": n, "rounds": args.rounds, "objective": "minimum_then_total" if fairness else "feasibility"}
    reason = exclusion(n, args.rounds)
    if reason:
        result.update(status="INFEASIBLE", evidence="mathematical", reason=reason)
    else:
        model, solver, membership, sizes, rounds = build_model(
            n, time_limit=args.time_limit, seed=args.seed, workers=args.workers,
            fair_spread=fairness, strengthen=True, rounds=args.rounds)
        if hint:
            for key, value in load_hints_from_csv(hint, membership).items():
                model.AddHint(membership[key], value)
        solver.parameters.log_to_stdout = False
        with (directory / "solver.log").open("w") as log:
            solver.log_callback = lambda message: log.write(message + "\n")
            status = solver.Solve(model)
        result.update(status=solver.StatusName(status), evidence="CP-SAT",
                      solver_seconds=solver.WallTime())
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            schedule = [[[p for p in range(1, n + 1) if solver.Value(membership[r, g, p])]
                         for g in range(len(sizes))] for r in range(rounds)]
            result.update(validate(schedule, n, rounds))
            if fairness:
                result.update(objective_value=solver.ObjectiveValue(), objective_bound=solver.BestObjectiveBound())
            with (directory / "schedule.csv").open("w", newline="") as output:
                writer = csv.writer(output)
                for r, groups in enumerate(schedule, 1):
                    for g, members in enumerate(groups, 1):
                        writer.writerow([r, g, *members])
            # Validate the persisted representation as well.
            assert validate(read_schedule(directory / "schedule.csv", n, rounds), n, rounds) == validate(schedule, n, rounds)
    result["elapsed_seconds"] = time.monotonic() - started
    (directory / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"R{args.rounds} n{n}: {result['status']} "
          f"{(result.get('minimum_spread'), result.get('total_spread'))}", flush=True)
    return result


def benchmark_range(minimum, args, summary, save):
    """Collect ten feasible counts, including the minimum, without skipping UNKNOWN."""
    summary.update(feasible_count=0, range_complete=False)
    for players in range(minimum, args.max_players + 1):
        result = solve(players, args, args.out / f"n{players}")
        summary["results"].append(result)
        if result["status"] in ("OPTIMAL", "FEASIBLE"):
            summary["feasible_count"] += 1
            if summary["feasible_count"] == 10:
                summary["range_complete"] = True
                save()
                return
        elif result["status"] != "INFEASIBLE":
            summary["stopped_reason"] = f"Benchmark unresolved at n={players}; ten-feasible-count range incomplete"
            save()
            return
        save()
    summary["stopped_reason"] = "Fewer than ten feasible counts within --max-players"
    save()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rounds", type=int, default=4)
    parser.add_argument("--n", type=int, help="Solve one count; otherwise discover the minimum and benchmark ten feasible counts")
    parser.add_argument("--time-limit", type=float, default=60, help="CP-SAT seconds per case, excluding model construction")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=101)
    parser.add_argument("--max-players", type=int, default=128, help="Upper bound on minimum discovery and benchmark counts")
    parser.add_argument("--hint", type=Path, help="Complete or partial CSV hint, single-count mode only")
    parser.add_argument("--out", type=Path, required=True, help="New output directory; refuses to overwrite")
    args = parser.parse_args()
    if args.rounds < 1 or args.workers < 1 or args.time_limit <= 0 or args.max_players < 3:
        parser.error("Rounds/workers/time limit must be positive; max players must be at least three")
    if args.n is not None:
        try:
            group_distribution(args.n)
        except ValueError as error:
            parser.error(str(error))
    if args.hint and args.n is None:
        parser.error("--hint requires --n")
    args.out.mkdir(parents=True, exist_ok=False)
    sources = {}
    for name in ("cp_sat_caseB_v2.py", "esgp_v2.py", "requirements.txt"):
        path = Path(__file__).parent / name
        shutil.copy2(path, args.out / name)
        sources[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    summary = {"configuration": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
               "environment": {"python": platform.python_version(), "ortools": ortools.__version__,
                               "platform": platform.platform()}, "source_sha256": sources,
               "minimum_proven": False, "discovery": [], "results": []}
    def save():
        (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    save()
    if args.n is not None:
        summary["results"].append(solve(args.n, args, args.out / f"n{args.n}", hint=args.hint))
    else:
        for n in range(3, args.max_players + 1):
            result = solve(n, args, args.out / "discovery" / f"n{n}", fairness=False)
            summary["discovery"].append(result)
            save()
            if result["status"] in ("OPTIMAL", "FEASIBLE"):
                summary.update(minimum_players=n, minimum_proven=True)
                benchmark_range(n, args, summary, save)
                break
            if result["status"] != "INFEASIBLE":
                summary["stopped_reason"] = f"Minimum discovery unresolved at n={n}; no range claimed"
                break
        else:
            summary["stopped_reason"] = "No feasible minimum within --max-players"
    save()


if __name__ == "__main__":
    main()
