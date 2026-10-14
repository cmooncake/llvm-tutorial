"""CPU MLIR labs with stage artifacts and behavioral checks."""
import argparse
from pathlib import Path
import re
import subprocess
from run import ROOT, run, require


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("suite", choices=["scf", "bufferization", "diagnostic"])
    parser.add_argument("--llvm-bin", required=True, type=Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    tool = lambda name: args.llvm_bin / name
    for name in ["mlir-opt", "mlir-translate", "opt", "lli"]:
        version = run([tool(name), "--version"]).stdout
        require(re.search(r"version\s+" + re.escape(args.version) + r"\b", version, re.I),
                f"SDK mismatch: {name}: {version}")

    if args.suite == "diagnostic":
        result = subprocess.run([str(tool("mlir-opt")), str(ROOT / "chapters/14-mlir-foundations/test/invalid-yield.mlir")],
                                text=True, capture_output=True, timeout=30)
        require(result.returncode != 0 and "error:" in result.stderr and "scf.yield" in result.stderr,
                f"Expected yield type diagnostic: {result.stderr}")
        print("PASS: invalid scf.yield rejected")
        return

    fixture = "16-progressive-lowering/test/sum.mlir" if args.suite == "scf" else "17-tensor-vector-gpu/test/value-semantics.mlir"
    source = ROOT / "chapters" / fixture
    stages = []
    if args.suite == "bufferization":
        stages += [("buffers", ["--one-shot-bufferize=bufferize-function-boundaries",
                                 "--buffer-deallocation-pipeline"]),
                   ("loops", ["--convert-linalg-to-loops", "--expand-strided-metadata"])]
    stages += [("cfg", ["--convert-scf-to-cf"]),
               ("llvm-dialect", ["--convert-to-llvm", "--reconcile-unrealized-casts"])]
    for stage, passes in stages:
        target = args.output / f"{stage}.mlir"
        run([tool("mlir-opt"), source, "--verify-each", *passes, "-o", target])
        source = target
    ir = args.output / "program.ll"
    run([tool("mlir-translate"), "--mlir-to-llvmir", source, "-o", ir])
    run([tool("opt"), "-passes=verify", "-disable-output", ir])
    run([tool("lli"), ir])
    optimized = args.output / "program.opt.bc"
    run([tool("opt"), "-passes=default<O2>", "-verify-each", ir, "-o", optimized])
    run([tool("lli"), optimized])
    print(f"PASS: {args.suite}; inspected stages retained in {args.output}")


if __name__ == "__main__":
    main()
