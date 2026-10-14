# Advanced Topics Tracks

[简体中文](frontier-tracks.md) | [English](frontier-tracks.en.md)

The graduate course requires MLIR foundations, staged lowering, and CPU bufferization; see the [shared labs](graduate-labs.en.md). This page catalogs further research choices. Suggested specialization durations fit within weeks 12–16, not additional compulsory weeks after the semester.

Advanced units study how modern compilers retain high-level semantics, compose multi-level transformations, target heterogeneous hardware, and make optimization strategies verifiable and reproducible.

## Why MLIR Follows LLVM IR

Students first learn LLVM IR, SSA, CFGs, and ABI; then MLIR operations, regions, and dialects; finally progressive lowering and heterogeneous optimization. Without the first layer, MLIR looks like alternate syntax. Without the second, students cannot state what a lowering preserves or loses.

## Track A: MLIR Compiler Engineering

Study generic/custom assembly, operation and region structure, `mlir-opt`, ODS, verifiers, traits, interfaces, patterns, and the pipeline:

```text
Mini AST
  -> Mini dialect
  -> Arith + SCF + Func
  -> CF + MemRef + LLVM dialect
  -> LLVM IR
```

Every arrow is an independent pass with legality, verification, and fixtures. Retain the direct LLVM back end as an oracle for differential tests.

## Track B: Tensor and Heterogeneous Compilation

Study tensor versus buffer semantics, structured and vector operations, tiling/fusion/vectorization conditions, host-device boundaries, address spaces, and target-independent versus target-specific dialects. A MiniTensor project lowers elementwise, matmul, and reduction through Linalg/Tensor, SCF/Vector, Bufferization, and CPU LLVM; GPU is optional.

## Track C: Programmable Optimization and Tuning

Use Transform dialect to separate transform IR from payload IR. Define legal parameter spaces, run repeated benchmarks, preserve versions and raw data, and analyze variation. Transform dialect orchestrates passes and patterns rather than replacing them.

## Track D: Modern LLVM Systems

Seminar or independent projects may cover ORC/JITLink, ClangIR as a high-level C/C++ IR case study, PGO, sanitizer and fuzzing infrastructure, automatic differentiation, and sparse or quantized compilation. These are not all core dependencies.

## Research-Project Evaluation

Evaluate semantic contracts, verification or differential evidence, reproducibility, ablation, and honestly bounded conclusions. Feature count is secondary.

## Official Entry Points

- [MLIR Tutorials](https://mlir.llvm.org/docs/Tutorials/)
- [Creating a Dialect](https://mlir.llvm.org/docs/Tutorials/CreatingADialect/)
- [Dialect Conversion](https://mlir.llvm.org/docs/DialectConversion/)
- [Transform Dialect](https://mlir.llvm.org/docs/Dialects/Transform/)
- [GPU Dialect](https://mlir.llvm.org/docs/Dialects/GPU/)
- [LLVM ORCv2](https://llvm.org/docs/ORCv2.html)
- [ClangIR](https://llvm.github.io/clangir/)

