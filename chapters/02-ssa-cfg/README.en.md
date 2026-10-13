# Chapter 02: Control Flow and Static Single Assignment Form

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 5–7 hours. Prerequisite: Chapter 01.

## Learning Objectives

Reason from CFG edges rather than source indentation, determine whether definitions dominate uses, place phi nodes at merges, relate memory form to SSA form, and lower loops and short-circuit operations.

## 2.1 Definitions, Uses, and Dominance

For every use, ask where its definition occurs, whether the definition dominates the use, whether a phi operand is available on its named incoming edge, and whether that edge is reachable. This model is more reliable than asking for the current value of a mutable source variable.

## 2.2 Control-Flow Merges and Phi Nodes

When an `if` produces different values on two paths, the merge block uses a phi with one pair per predecessor. Phi instructions conceptually select on incoming edges and appear before non-phi instructions in a block.

## 2.3 Loop-Carried Values

A loop-header phi receives an initial value from the preheader and an updated value from the backedge. A textual definition later in the file may be valid because it is available on that backedge. Draw the CFG before editing phi operands.

## 2.4 Short-Circuit Evaluation

`a && f()` must not call `f` when `a` is false. Lower it with conditional control flow and a merge phi. The same principle applies to `||` with reversed branching.

## Laboratory 2A: Loop Summation

Complete `exercises/sum-to.ll` for the sum over `[0, n)`, returning zero for nonpositive `n`, without memory. Verify it, print the dominator tree, and annotate the CFG and backedge.

## Laboratory 2B: Short-Circuit Side Effects

Implement `and_then(i1 %lhs)` around a side-effecting `probe`. A C harness with a counter must detect eager evaluation; checking only the returned boolean is insufficient.

## Laboratory 2C: Mem2Reg and SSA Construction

Write a loop using allocas, loads, and stores, then run `opt -passes=mem2reg`. Compare the inserted phi nodes and state the preconditions under which local allocas can be promoted.

## Programming Exercise: Iterative Fibonacci

Implement iterative Fibonacci using one loop and no memory. Specify behavior for negative input and test boundary values.

## Submission

- summation, short-circuit, memory/SSA comparison, and Fibonacci IR;
- CFGs or adjacency lists;
- verifier results; and
- an explanation connecting every phi incoming value to one CFG edge.

## References

- [LLVM Language Reference: Phi Instruction](https://llvm.org/docs/LangRef.html#phi-instruction)
- [LLVM Kaleidoscope: Control Flow](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl05.html)

