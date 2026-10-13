# Chapter 18: Transform Dialect and Optimization Scheduling

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 6–9 hours. This chapter separates what to transform from a hard-coded pass pipeline.

Transform dialect uses transform IR to control payload IR. Handles refer to sets of payload operations, and transform operations apply matching, tiling, fusion, vectorization, or mapping. It orchestrates underlying transformations; it does not replace pass infrastructure or rewrite patterns.

## 18.1 Failure and Handle Lifetime

A transform may succeed, fail recoverably, or fail irrecoverably. No match and a violated transformation precondition are different failures. Some transforms consume handles; later use of an invalidated handle is erroneous and should be checked and tested.

## 18.2 Scheduling and Tuning

Treat tile sizes, vector widths, and mappings as a constrained parameter space. Preserve payload IR, transform IR, compiler version, target, raw measurements, and correctness result for every experiment. A single fastest run is not evidence.

## Laboratory 18: Replaceable Optimization Schedules

Write at least two transform schedules for the Chapter 17 matrix multiplication. Run correctness before repeated measurement. Include a payload that violates a precondition and verify a controlled failure rather than silently incorrect IR.

Explain effects on locality, parallelism, vectorization, or movement. Perform an ablation by removing one transform and observing correctness and performance.

## Submission

- payload and two transform IR schedules;
- handle-lifetime and failure tests;
- parameter space and experiment driver;
- raw data, statistics, and ablation report; and
- explanation of transform versus ordinary pass responsibilities.

## References

- [Transform Dialect](https://mlir.llvm.org/docs/Dialects/Transform/)
- [Transform Dialect Tutorial](https://mlir.llvm.org/docs/Tutorials/Transform/)

