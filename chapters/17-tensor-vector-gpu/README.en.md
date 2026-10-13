# Chapter 17: Tensors, Vectorization, and Heterogeneous Code Generation

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 8–12 hours. GPU hardware is not required for core assessment.

This chapter follows a computation from mathematical tensors to concrete memory and hardware operations. Bufferizing too early loses value semantics useful for fusion and tiling; bufferizing too late prevents explicit allocation, aliasing, and movement.

## 17.1 Tensor, Linalg, and Vector

A tensor is an SSA value rather than mutable storage. Linalg structured operations expose iteration spaces, indexing maps, and reductions. The Vector dialect represents retargetable multidimensional vector operations before target-specific lowering.

## 17.2 Bufferization

Bufferization converts tensor semantics to memref or buffer semantics. One-Shot Bufferize uses destination-passing style to choose reuse or allocation, minimizing allocation and copying without overwriting live data.

Document alias and ownership assumptions. Leaks, double frees, and hidden copies are correctness or performance failures.

## 17.3 GPU Boundaries

The GPU dialect models kernels, launches, thread and block identifiers, and address spaces before lowering to NVVM, ROCDL, or another target. Distinguish host/device modules, data movement, and execution. Core work verifies IR against a CPU reference; hardware execution is optional.

## Laboratory 17: MiniTensor Matrix Multiplication

Build a CPU pipeline for elementwise operations, reductions, and matrix multiplication: `Linalg/Tensor → tiled Linalg → Vector → Bufferization → LLVM`. Compare at least two tile/vector schedules and validate numerically against a reference.

An extension maps parallel loops to GPU blocks and threads, reporting kernel and transfer time separately.

## Submission

- reproducible pipeline and per-level fixtures;
- buffer ownership and aliasing explanation;
- numerical correctness tests;
- raw performance data and hardware description; and
- IR-only acceptance path without a GPU.

## References

- [Linalg Dialect](https://mlir.llvm.org/docs/Dialects/Linalg/)
- [Bufferization](https://mlir.llvm.org/docs/Bufferization/)
- [Vector Dialect](https://mlir.llvm.org/docs/Dialects/Vector/)
- [GPU Dialect](https://mlir.llvm.org/docs/Dialects/GPU/)

