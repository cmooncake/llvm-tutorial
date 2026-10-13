# Chapter 01: LLVM Intermediate Representation

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 4–6 hours. Complete Chapter 00 and verify that `llvm-as`, `opt`, and `lli` are available.

In Chapter 00, Clang produced IR. Here we write it directly, separating two questions: can LLVM parse the text, and does the parsed IR satisfy structural invariants?

## 1.1 Functions, Types, and SSA Values

```llvm
define i32 @add(i32 %lhs, i32 %rhs) {
entry:
  %sum = add i32 %lhs, %rhs
  ret i32 %sum
}
```

Assemble and verify it with `llvm-as add.ll -o add.bc` and `opt -passes=verify -disable-output add.bc`. `%sum` is a single-assignment value, not a mutable variable. The `i32` types are part of instruction semantics.

### Checkpoint: Return Types

Change the return instruction to `ret i64 %sum`. Predict which tool rejects it, run the command, and explain whether the returned value or the agreement with the function signature is wrong.

## 1.2 Basic Blocks and Terminators

A conditional function divides execution into basic blocks. Every block ends in a terminator such as `br` or `ret`, with no ordinary instruction afterward. At a merge, a phi chooses one incoming value for each predecessor edge. The incoming block labels must be actual CFG predecessors.

When implementing integer absolute value, remember that negating the minimum `i32` wraps. Do not attach `nsw` unless the source language proves signed overflow cannot occur; it is a semantic promise rather than an overflow check.

## 1.3 Memory Operations and Opaque Pointers

```llvm
%slot = alloca i32, align 4
store i32 42, ptr %slot, align 4
%value = load i32, ptr %slot, align 4
```

`%slot` is an address while `%value` is an integer. With opaque pointers, `ptr` does not encode a pointee type; load, store, GEP, and surrounding context carry the relevant type information.

## Laboratory 1: Integer Classification

Complete [`exercises/classify.ll`](exercises/classify.ll) so negative, zero, and positive inputs return -1, 0, and 1. Do not use memory. Verification proves structure, not behavior, so add a main function or C harness covering -1, 0, 1, `INT_MIN`, and `INT_MAX`.

## 1.4 Parser and Verifier

Starting from valid IR, introduce one fault at a time: remove a terminator, mismatch a return type, remove a phi incoming edge, and use a value that does not dominate its use. Record the first failing command, diagnostic, and violated invariant. Some errors are textual; others require verifier knowledge of types and CFG structure.

## Programming Exercise: Clamp

Implement `clamp(x, low, high)`, specifying behavior when `low > high` before coding. Provide five boundary tests and a CFG. During review, explain each block's predecessors, successors, terminator, and value definitions.

## Diagnostic Notes

Define a block as `then:` but refer to it as `label %then`. Diagnose phi failures by drawing the actual CFG. Remember that `icmp` returns `i1`; any conversion to an integer must be explicit and justified.

## Summary

Functions contain basic blocks; terminators form a CFG; typed instructions produce SSA values; phi nodes merge predecessor-edge values; and memory is explicit through addresses, loads, and stores. Chapter 02 develops dominance and loop reasoning systematically.

### Submission

- tested `classify.ll`;
- `clamp.ll`, tests, and CFG; and
- four single-fault invalid IR files with explanations.

## References

- [LLVM Language Reference Manual](https://llvm.org/docs/LangRef.html)
- [LLVM Command Guide](https://llvm.org/docs/CommandGuide/)

