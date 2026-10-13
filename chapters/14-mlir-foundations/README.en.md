# Chapter 14: MLIR Fundamentals

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 6–8 hours. Prerequisites: LLVM IR, SSA, passes, and MiniLang code generation.

LLVM IR serves low-level optimization and code generation well, but source or domain semantics are difficult to recover after lowering to pointers and loops. MLIR supports several abstraction levels in one infrastructure and explicit conversion between them.

## 14.1 Uniform IR Structure

The central unit is an operation with operands, results, attributes, regions, and successors. Regions contain blocks; blocks contain operations and may have block arguments. Functions, loops, and modules are operations.

SSA remains, while nested regions express scope and structured control flow directly. A dialect names and defines a family of operations, types, attributes, and interfaces.

The MLIR LLVM dialect is an MLIR dialect that models LLVM-like semantics. It is not an `llvm::Module`; translation is still required to produce LLVM IR.

## 14.2 Text, Verification, and Passes

Use `mlir-opt` to parse, verify, run pipelines, and inspect every level. Begin with generic operation form before custom assembly syntax. Verify at pass boundaries and use IR-before/after printing to localize conversion failures.

## Laboratory 14: Observing Multi-Level IR

Annotate a program containing `func`, `arith`, and `scf`, identifying operations, regions, block arguments, and uses. Run canonicalization, CSE, and structured-control-flow conversion and record what each level preserves or discards.

Create invalid type, terminator, and region examples and connect each verifier diagnostic to a dialect invariant.

## Submission

- annotated MLIR sample;
- reproducible pass pipeline;
- three verifier failures; and
- comparison of LLVM IR, the LLVM dialect, and higher-level dialects.

## References

- [MLIR Documentation and Tutorials](https://mlir.llvm.org/docs/)
- [MLIR Toy Tutorial](https://mlir.llvm.org/docs/Tutorials/Toy/)

