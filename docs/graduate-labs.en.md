# Graduate MLIR Laboratories

[简体中文](graduate-labs.md) | [English](graduate-labs.en.md)

These labs connect LLVM foundations to multilevel IR. Run an example, change one semantic condition, and predict which stages change. They are reproducible CPU experiments, not GPU requirements or an implemented MiniLang MLIR backend.

## Setup and execution

After the foundational Ubuntu 24.04 setup, install matching-release MLIR tools:

```sh
sudo apt-get install mlir-22-tools
cmake -S . -B build -DTUTORIAL_ENABLE_MLIR=ON
cmake --build build --parallel 2
ctest --test-dir build -L mlir --output-on-failure
```

Reuse a build already configured with the correct LLVM_DIR; initial setup follows the [testing guide](testing.en.md). Missing or mismatched tools fail rather than skipping MLIR. Stage outputs live under separate suite directories in `build/mlir-artifacts/`, allowing parallel tests.

## Structured loops and control flow

The input is `chapters/16-progressive-lowering/test/sum.mlir`. The scf.for interval includes its lower bound and excludes its upper bound. Its carried accumulator is a value, not implicit mutable storage. The program sums 0 through 9, compares against 45 internally, and returns zero for success.

Before running, identify initialization, iteration arguments, and results. Locate the corresponding block arguments in cfg.mlir, then follow them through llvm-dialect.mlir and program.ll. Explain which structural facts become explicit branches, not merely which operations are renamed.

Reproduce the main conversions manually:

```sh
mlir-opt chapters/16-progressive-lowering/test/sum.mlir --convert-scf-to-cf -o cfg.mlir
mlir-opt cfg.mlir --convert-to-llvm --reconcile-unrealized-casts -o lowered.mlir
mlir-translate --mlir-to-llvmir lowered.mlir -o program.ll
opt -passes=verify -disable-output program.ll
lli program.ll
```

The automated test also checks behavior after O2. When changing bounds, step, or initial value, compute the answer independently first. Changing the expected constant to match an incorrect result is not a repair.

## Tensor values and buffer reuse

The input is `chapters/17-tensor-vector-gpu/test/value-semantics.mlir`. Tensor a contains four ones; b changes its zeroth element to two. The program then reads both a[0] and b[0], whose sum must be three. Assuming tensor.insert always permits destructive reuse can incorrectly produce four.

The pipeline performs One-Shot Bufferization and ownership-based deallocation, lowers Linalg to loops and SCF to CFG, then converts to LLVM. Inspect allocations, copies, and releases in buffers.mlir. Identify the use preventing unconditional reuse. A memcpy is not inherently a bad optimization result; ask whether it is necessary under the live-value requirements.

As an extension, remove the old-value read and compare copying. This changes observable requirements and the legal optimization space. Preserve both inputs; they are not interchangeable workloads for a direct speed comparison. Discuss loop-carried updates, function boundaries, and ownership beyond the fixed example's coverage.

## Invalid region results

The fixture `chapters/14-mlir-foundations/test/invalid-yield.mlir` deliberately yields index from a loop expecting i32. Predict the diagnosed operation, then run the test. Distinguish parsing errors, type invariants, and missing conversion patterns; they require different repairs.

Submit a different type/region counterexample with a diagnostic assertion. Any nonzero status is insufficient because missing tools and crashes also fail. The existing test checks error text and scf.yield, not full diagnostic locations.

## From laboratory to research

L5 assesses understanding of existing conversions. Research requires an increment, such as an operation verifier/conversion or two legal schedules compared for copying and runtime cost. Course reference implementations of custom dialect and Transform projects do not yet exist. These three tests do not complete chapters 14–18.

Sources are [Toy chapter 5](https://mlir.llvm.org/docs/Tutorials/Toy/Ch-5/), [chapter 6](https://mlir.llvm.org/docs/Tutorials/Toy/Ch-6/), and [Bufferization](https://mlir.llvm.org/docs/Bufferization/). All three suites passed locally with LLVM/MLIR 22.1.8 on WSL Ubuntu 24.04; the raw report is `build-validation/mlir-results.xml`. GPUs, Transform schedules, and custom dialects are outside that result.
