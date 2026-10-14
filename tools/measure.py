"""Measure deterministic executables; includes process startup, not kernel-only time."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import random
import statistics
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--arg", action="append", default=[])
    parser.add_argument("--runs", type=int, default=20)
    parser.add_argument("--warmups", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--seed", type=int, default=20261013)
    parser.add_argument("--context", required=True, help="Record commit, LLVM version, flags, and workload")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.runs < 2 or args.warmups < 0 or args.timeout <= 0:
        parser.error("need runs >= 2, warmups >= 0, timeout > 0")
    commands = {name: [str(getattr(args, name).resolve()), *args.arg] for name in ["baseline", "candidate"]}

    def execute(name):
        start = time.perf_counter_ns()
        result = subprocess.run(commands[name], capture_output=True, timeout=args.timeout)
        elapsed = time.perf_counter_ns() - start
        if result.returncode != 0:
            raise RuntimeError(f"{name} failed: {result.returncode}; {result.stderr!r}")
        return elapsed, (result.stdout, result.stderr)

    _, expected = execute("baseline")
    samples = []
    rng = random.Random(args.seed)
    for iteration in range(args.warmups + args.runs):
        order = ["baseline", "candidate"]
        rng.shuffle(order)
        for name in order:
            elapsed, output = execute(name)
            if output != expected:
                raise RuntimeError(f"Output mismatch in {name}; correctness failure, not a timing sample")
            if iteration >= args.warmups:
                samples.append({"pair": iteration - args.warmups, "configuration": name,
                                "order": order.index(name), "nanoseconds": elapsed})
    summary = {}
    for name in commands:
        times = [row["nanoseconds"] for row in samples if row["configuration"] == name]
        median = statistics.median(times)
        summary[name] = {"median_ns": median, "min_ns": min(times), "max_ns": max(times),
                         "mad_ns": statistics.median(abs(value - median) for value in times)}
    report = {"measurement": "end-to-end process time including startup; not statistical significance",
              "system": platform.platform(), "machine": platform.machine(), "processor": platform.processor(),
              "context": args.context, "commands": commands, "seed": args.seed,
              "warmups": args.warmups, "runs": args.runs,
              "executable_sha256": {name: hashlib.sha256(Path(command[0]).read_bytes()).hexdigest()
                                     for name, command in commands.items()},
              "stdout_sha256": hashlib.sha256(expected[0]).hexdigest(),
              "stderr_sha256": hashlib.sha256(expected[1]).hexdigest(),
              "summary": summary, "samples": samples,
              "ratio_of_medians": summary["baseline"]["median_ns"] / summary["candidate"]["median_ns"]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {len(samples)} timings to {args.output}; inspect raw samples before drawing conclusions.")


if __name__ == "__main__":
    main()
