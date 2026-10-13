# Chapter 04: LLVM Analysis and Transformation Passes

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 6–8 hours. Prerequisite: Chapter 03.

## Learning Objectives

Distinguish analyses, transformations, and instrumentation; understand function and module scope; preserve or invalidate analyses correctly; register a plugin through PassBuilder; and test both transformations and intentional non-transformations.

## 4.1 Analysis and Transformation

An analysis answers a question without changing IR. A transformation changes IR and may invalidate cached analysis results. `PreservedAnalyses` is the transformation's contract with analysis managers.

The chapter plugin provides `print-inst-count` and `remove-add-zero`. The latter is deliberately small enough to reason about replacement, erasure, iterator safety, and invalidation.

## 4.2 Build

Configure `chapters/04-passes` with an explicit `LLVM_DIR`, build the platform-specific plugin, and load it with `opt -load-pass-plugin`. The dynamic plugin must use an ABI-compatible LLVM build.

## 4.3 Correctness Conditions

Integer `x + 0 -> x` is valid, including in the presence of `nsw/nuw`, because replacement does not introduce overflow. Similar-looking rewrites require separate proof: floating-point zero involves signed zero, NaN, and fast-math; multiplication by zero interacts with poison; side-effecting or trapping instructions cannot be erased casually.

## 4.4 Testing

Use FileCheck for right zero, left zero, nonzero constants, and floating-point non-transformation. Verify output IR and avoid complete golden snapshots.

## Laboratory 4: Analysis Results and Invalidation

Implement instruction count as an `AnalysisInfoMixin` result and obtain it through `FunctionAnalysisManager::getResult`. Print before and after the transformation and explain when recomputation is required.

## Programming Exercise: Local IR Transformation

Implement unreachable-block removal, a stable opcode histogram, or integer `sub x, 0 -> x`. Submit a correctness argument covering preconditions, maintained semantics, poison and flags, and side effects.

## Submission

- loadable `opt` plugin;
- positive and negative tests;
- verifier after transformation;
- accurate PreservedAnalyses; and
- one-page correctness note.

## Diagnostic Notes

Check exported plugin information and pipeline names when `opt` cannot find a pass. Advance iterators before erasing instructions. Returning `all()` after a real change can cause stale analyses to be reused.

## References

- [Writing an LLVM Pass](https://llvm.org/docs/WritingAnLLVMNewPMPass.html)
- [Using the New Pass Manager](https://llvm.org/docs/NewPassManager.html)

