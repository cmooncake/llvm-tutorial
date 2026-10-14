"""Black-box Scalar acceptance harness. Requires a student compiler, never skips it."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile


def invoke(command, timeout):
    return subprocess.run([str(item) for item in command], capture_output=True,
                          text=True, encoding="utf-8", timeout=timeout)


def check_result(result, code, stdout, stderr):
    actual = (result.returncode, result.stdout, result.stderr)
    expected = (code, stdout, stderr)
    if actual != expected:
        raise AssertionError(f"Expected {expected!r}, got {actual!r}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiler", required=True, type=Path)
    parser.add_argument("--stage", choices=["check", "run"], default="run")
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if not args.compiler.is_file():
        parser.error("--compiler must name an existing executable")
    compiler = args.compiler.resolve()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text(encoding="utf-8"))
    results = []
    with tempfile.TemporaryDirectory(prefix="minilang-acceptance-") as directory:
        for case in cases:
            path = Path(directory) / (case["name"] + ".ml")
            path.write_text(case["source"], encoding="utf-8")
            try:
                checked = invoke([compiler, "check", path], args.timeout)
                if "diagnostic" in case:
                    if checked.returncode != 1 or checked.stdout:
                        raise AssertionError(f"Expected source error 1 and empty stdout: {checked}")
                    location = rf"{case['line']}:{case['column']}" if "line" in case else r"[1-9]\d*:[1-9]\d*"
                    pattern = re.escape(str(path)) + ":" + location + ": error " + case["diagnostic"] + ":"
                    if not re.search(pattern, checked.stderr):
                        raise AssertionError(f"Missing diagnostic/location {pattern}: {checked.stderr}")
                else:
                    check_result(checked, 0, "", "")
                    if args.stage == "run":
                        executed = invoke([compiler, "run", path], args.timeout)
                        check_result(executed, case["exit"], case["stdout"], case.get("stderr", ""))
                results.append({"name": case["name"], "passed": True})
                print("PASS", case["name"])
            except (AssertionError, OSError, subprocess.TimeoutExpired) as error:
                results.append({"name": case["name"], "passed": False, "error": str(error)})
                print("FAIL", case["name"], str(error))
    report = {"stage": args.stage, "passed": sum(item["passed"] for item in results),
              "total": len(results), "cases": results}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{report['passed']}/{report['total']} passed ({args.stage})")
    raise SystemExit(0 if all(item["passed"] for item in results) else 1)


if __name__ == "__main__":
    main()
