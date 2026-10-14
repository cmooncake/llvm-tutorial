# Building and Automated Tests

[简体中文](testing.md) | [English](testing.en.md)

Graduate revalidation on 2026-10-13: in the same WSL Ubuntu 24.04.1 / LLVM 22.1.8 environment described below, matching MLIR tools and the enabled MLIR option produced **11/11 passing CTest suites in 154.18 seconds**, including three MLIR suites in 56.45 seconds. Evidence is in `build-validation/graduate-results.xml`, the latest `Testing/Temporary/LastTest.log`, and `mlir-artifacts/` under that build directory; generated artifacts are not committed.

The CLI shell separately configured and built; check-mode acceptance correctly rejected all 29 unimplemented cases. The C runtime compiled with Clang 22 and `-Wall -Wextra -Werror -std=c11`, not a complete end-to-end ABI validation. The measurement utility passed a two-round, zero-warmup process smoke test; this supports no performance conclusion. The updated bilingual audit covers 90 Markdown files, and new Python files passed syntax compilation. Remote CI, Ninja, and clean-image installation remain unrun. The eight-suite record below is the earlier foundation-only run, not the latest total.

Tests provide repeatable feedback after edits, not just evidence that reference answers once ran. Run commands from the repository root; Windows users should use WSL2 Ubuntu 24.04. Read the [version policy](version-policy.en.md) first.

## Installation and first build

In the Ubuntu 24.04 environment you intend to use for the course:

```sh
# Adds an LLVM apt source and installs system packages; not a read-only check.
sudo bash tools/setup-ubuntu.sh
export PATH=/usr/lib/llvm-22/bin:$PATH
cmake -S . -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DTUTORIAL_ENABLE_MLIR=ON \
  -DCMAKE_C_COMPILER=/usr/lib/llvm-22/bin/clang \
  -DCMAKE_CXX_COMPILER=/usr/lib/llvm-22/bin/clang++ \
  -DLLVM_DIR=/usr/lib/llvm-22/lib/cmake/llvm
cmake --build build --parallel 2
ctest --test-dir build --output-on-failure
```

`LLVM_DIR` is the CMake configuration directory, not `bin` or the installation prefix. Missing dependencies and incorrect versions fail configuration or tests rather than silently skipping them. The `tests/run.py` driver uses no pip packages or lit; FileCheck comes from the LLVM tools package.

Use `ctest --test-dir build -V` for verbose output, or `ctest --test-dir build -R '^passes$' --output-on-failure` to debug passes. Failure logs are in `build/Testing/Temporary/LastTest.log`. Each subprocess has a 30-second limit and each suite a 90-second limit, so a broken loop cannot hang grading indefinitely.

## Public test coverage

| CTest name | Checks | Does not establish |
|---|---|---|
| environment | Exact versions of 8 SDK tools match the CMake package | Compatibility of every system tool |
| toolchain | C → IR → bitcode → optimization → lli; object generation, linking, execution | Linking on arbitrary targets |
| classify | 71 inputs: signs, zero, i32 extremes, seeded random samples; before/after optimization | Exhaustive i32 coverage |
| sum-to | 42 inputs: empty range, loop boundaries, signed overflow at 65537, seeded samples; before/after optimization | Performance on huge inputs |
| generator | FileCheck multiplication/addition structure; 5 execution cases including wrapping | Correctness of all IRBuilder usage |
| passes | Remove left/right zero and chains; retain nonzero/float/vector adds; count instructions; execute 4 integer functions before/after transformation | A formal correctness proof |
| verifier | Incomplete phi must fail with its specific diagnostic | That any nonzero exit is acceptable |
| negative-controls | Two fixed return-zero implementations must fail behavioral checks | That completed student exercises should still fail |

The driver compares full i32 values inside IR, then returns only 0/1 as the process status. This avoids false positives from Linux truncating exit codes to 8 bits. Inputs use one SDK for verification; optimization uses `-verify-each`. These regression cases are not a proof of correctness.

## Student exercises and reference implementations

The default uses `solutions/`, validating the teaching assets themselves. After editing `exercises/`, students configure a separate tree:

```sh
cmake -S . -B build-student -G Ninja \
  -DLLVM_DIR=/usr/lib/llvm-22/lib/cmake/llvm \
  -DCMAKE_C_COMPILER=/usr/lib/llvm-22/bin/clang \
  -DCMAKE_CXX_COMPILER=/usr/lib/llvm-22/bin/clang++ \
  -DTUTORIAL_IR_SET=exercises
cmake --build build-student --parallel 2
ctest --test-dir build-student -R '^(classify|sum-to)$' --output-on-failure
```

The original exercises return 0, so both tests must fail. Do not mark them skipped or expected failures. Once the work is complete, the same entry point should pass. This option only selects chapter 01–02 IR; it does not turn chapter 03–04 reference code into student starters.

## CI and validation boundaries

The [GitHub Actions workflow](../.github/workflows/tests.yml) installs LLVM 22 on Ubuntu 24.04 and tests references plus independent fixed faulty examples. Negative controls are separate from student work, so completing an exercise cannot make CI fail. It saves JUnit results, tool versions, package versions, and logs. The apt release line can receive future patches that expose compatibility issues.

The graduate configuration also runs `mlir-scf`, `mlir-bufferization`, and `mlir-diagnostic`, with a 120-second suite timeout. Intermediate artifacts are retained in `build/mlir-artifacts/`; see the [shared labs](graduate-labs.en.md). Omitting the MLIR option selects the eight foundation suites. CI now enables MLIR but has not run remotely.

The complete MiniLang front/back ends remain unimplemented. The [public acceptance driver](../capstone/tests/README.en.md) supplies 29 inputs, not evidence of a passing reference compiler. Research specializations including Chapters 15 and 18 also lack complete runnable implementations; the entire course cannot be declared tested.

### Local execution record: 2026-10-13

- WSL2 Ubuntu 24.04.1, x86-64; LLVM/Clang 22.1.8; CMake 3.28.3; Python 3.12.3; Release build.
- This run used Unix Makefiles. The recommended Ninja generator and remote GitHub Actions have not been run; local results are not remote CI results.
- Official LLVM packages were unpacked under Git-ignored `build/sdk`, without installing system packages. The nonstandard prefix required SDK `CMAKE_PREFIX_PATH`, runtime `LD_LIBRARY_PATH`, and an explicit system zstd shared-library path; normal apt installation does not need these temporary adaptations. The installer was syntax-checked, not executed with sudo locally.
- The generator and plugin compiled successfully; all 8 CTest suites passed in 101.63 seconds.
- Original `exercises/` implementations of `classify` and `sum_to` were also run and rejected for incorrect results, not missing tools or parse failures.
- Bilingual documentation audit passed for 78 Markdown files; the Python driver passed syntax compilation.

Raw local evidence is in `build-validation/results.xml` and `build-validation/Testing/Temporary/LastTest.log`; build products are not committed. Actual compilation also exposed and fixed the LLVM 22 PassPlugin header path and standalone build configuration. Environment checks, static review, and execution are distinct evidence; this record covers only the stated environment and existing examples.
