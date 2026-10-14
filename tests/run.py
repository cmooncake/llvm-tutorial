"""Public regression tests. Python stdlib only; CTest supplies SDK/target paths."""
import argparse
from pathlib import Path
import random
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


class CommandError(AssertionError):
    def __init__(self, command, result, expected):
        self.command = command
        self.result = result
        super().__init__(
            f"Command: {command}\nExpected exit {expected}, got {result.returncode}"
            f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")


def run(command, *, input=None, expected=0):
    result = subprocess.run([str(x) for x in command], input=input,
                            text=True, capture_output=True, timeout=30)
    if result.returncode != expected:
        raise CommandError(command, result, expected)
    return result


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def i32(value):
    return (value + 2**31) % 2**32 - 2**31


def harness(function, cases):
    """Compare full-width results in IR, not truncated process exit values."""
    lines = ["define i32 @main() {", "entry:"]
    for index, (args, expected) in enumerate(cases):
        operands = ", ".join(f"i32 {value}" for value in args)
        lines += [f"  %r{index} = call i32 @{function}({operands})",
                  f"  %ok{index} = icmp eq i32 %r{index}, {expected}"]
        if index:
            previous = "%ok0" if index == 1 else f"%all{index - 1}"
            lines += [f"  %all{index} = and i1 {previous}, %ok{index}"]
    last = "%ok0" if len(cases) == 1 else f"%all{len(cases) - 1}"
    lines += [f"  %failed = xor i1 {last}, true",
              "  %exit = zext i1 %failed to i32", "  ret i32 %exit", "}"]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("suite", choices=["environment", "toolchain", "classify",
                                         "sum-to", "generator", "passes", "verifier", "negative-controls"])
    parser.add_argument("--llvm-bin", required=True, type=Path)
    parser.add_argument("--llvm-version", required=True)
    parser.add_argument("--generator", required=True, type=Path)
    parser.add_argument("--plugin", required=True, type=Path)
    parser.add_argument("--ir-set", choices=["solutions", "exercises"], default="solutions")
    args = parser.parse_args()

    def tool(name):
        candidate = args.llvm_bin / name
        return candidate if candidate.exists() else candidate.with_suffix(".exe")

    with tempfile.TemporaryDirectory(prefix="llvm-tutorial-") as folder:
        tmp = Path(folder)

        def verify(path):
            run([tool("opt"), "-passes=verify", "-disable-output", path])

        def execute(ir, function, cases):
            module = tmp / "execution.ll"
            module.write_text(ir + "\n" + harness(function, cases), encoding="utf-8")
            verify(module)
            run([tool("lli"), module])
            optimized = tmp / "execution.opt.bc"
            run([tool("opt"), "-passes=default<O2>", "-verify-each", module, "-o", optimized])
            run([tool("lli"), optimized])

        if args.suite == "environment":
            wanted = re.match(r"\d+\.\d+\.\d+", args.llvm_version).group()
            for name in ["clang", "opt", "lli", "llc", "llvm-as", "llvm-dis", "llvm-link", "FileCheck"]:
                output = run([tool(name), "--version"]).stdout
                found = re.search(r"version\s+(\d+\.\d+\.\d+)", output, re.I)
                require(found and found.group(1) == wanted,
                        f"{tool(name)} does not match SDK {wanted}: {output}")
                print(f"{tool(name)}: {wanted}")
        elif args.suite == "toolchain":
            ir, bc, optimized = tmp / "answer.ll", tmp / "answer.bc", tmp / "answer.opt.bc"
            run([tool("clang"), "-O0", "-Xclang", "-disable-O0-optnone", "-S", "-emit-llvm",
                 ROOT / "tests/answer.c", "-o", ir])
            run([tool("llvm-as"), ir, "-o", bc])
            run([tool("opt"), "-passes=mem2reg,instcombine,simplifycfg", "-verify-each", bc, "-o", optimized])
            run([tool("llvm-dis"), optimized, "-o", tmp / "optimized.ll"])
            run([tool("lli"), optimized])
            obj, exe = tmp / "answer.o", tmp / "answer.exe"
            run([tool("llc"), "-filetype=obj", "-relocation-model=pic", optimized, "-o", obj])
            run([tool("clang"), obj, "-o", exe])
            run([exe])
        elif args.suite in ("classify", "sum-to"):
            chapter = "01-llvm-ir" if args.suite == "classify" else "02-ssa-cfg"
            source = ROOT / "chapters" / chapter / args.ir_set / f"{args.suite}.ll"
            rng = random.Random(20261013)
            if args.suite == "classify":
                values = [-2**31, -100, -1, 0, 1, 100, 2**31 - 1]
                values += [rng.randint(-2**31, 2**31 - 1) for _ in range(64)]
                cases = [([x], (x > 0) - (x < 0)) for x in values]
                function = "classify"
            else:
                # 65537 crosses signed i32 overflow; no nsw flag is permitted here.
                values = [-2**31, -1, 0, 1, 2, 3, 10, 100, 65536, 65537]
                values += [rng.randint(0, 1000) for _ in range(32)]
                cases = [([n], i32(n * (n - 1) // 2) if n > 0 else 0) for n in values]
                function = "sum_to"
            execute(source.read_text(encoding="utf-8"), function, cases)
            print(f"{source}: {len(cases)} cases, before and after O2")
        elif args.suite == "generator":
            ir = run([args.generator]).stdout
            run([tool("FileCheck"), ROOT / "chapters/03-cpp-api/test/mul-add.check"], input=ir)
            pairs = [(0, 0), (2, 3), (-7, 9), (-2**31, -1), (2**31 - 1, 2)]
            execute(ir, "mul_add", [([a, b], i32(a * b + 7)) for a, b in pairs])
        elif args.suite == "passes":
            source = ROOT / "chapters/04-passes/test/add-zero.ll"
            plugin = [tool("opt"), "-load-pass-plugin", args.plugin]
            transformed = run(plugin + ["-passes=remove-add-zero", "-verify-each", "-S", source, "-o", "-"]).stdout
            run([tool("FileCheck"), source], input=transformed)
            count = run(plugin + ["-passes=remove-add-zero,print-inst-count", "-disable-output", source]).stderr
            for function, total in [("right_zero", 1), ("left_zero", 1), ("nonzero", 2),
                                    ("float_zero", 2), ("chain", 1), ("vector_zero", 2)]:
                require(f"{function}: {total} instructions" in count, count)
            for function in ("right_zero", "left_zero", "nonzero", "chain"):
                values = [-2**31, -1, 0, 1, 2**31 - 1]
                cases = [([x], i32(x + 1) if function == "nonzero" else x) for x in values]
                execute(source.read_text(encoding="utf-8"), function, cases)
                execute(transformed, function, cases)
        elif args.suite == "negative-controls":
            ir = (ROOT / "tests/wrong-results.ll").read_text(encoding="utf-8")
            for function, cases in [("classify", [([1], 1)]), ("sum_to", [([3], 3)])]:
                try:
                    execute(ir, function, cases)
                except CommandError as error:
                    # A parser error, missing tool, or crash is not this expected failure.
                    require(Path(error.command[0]).stem == "lli" and error.result.returncode == 1,
                            str(error))
                else:
                    raise AssertionError(f"Incorrect {function} escaped the behavioral oracle")
        else:
            result = subprocess.run([str(tool("opt")), "-passes=verify", "-disable-output",
                                     str(ROOT / "tests/invalid-phi.ll")],
                                    text=True, capture_output=True, timeout=30)
            require(result.returncode != 0, "Verifier accepted invalid phi")
            require("PHINode should have one entry" in result.stderr,
                    f"Expected phi verifier diagnostic, not an unrelated failure:\n{result.stderr}")
    print(f"PASS: {args.suite}")


if __name__ == "__main__":
    main()
