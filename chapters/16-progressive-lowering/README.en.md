# Chapter 16: Dialect Conversion and Progressive Lowering

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 8–12 hours. Every lowering stage must be independently verifiable and testable.

Dialect Conversion uses a conversion target to declare legal operations and types, rewrite patterns to replace illegal structure, and a TypeConverter for types and materializations. Partial conversion permits operations not declared illegal to remain; full conversion requires complete legalization in scope.

The course pipeline is:

```text
Mini → Arith/SCF/Func → CF/MemRef/LLVM dialect → LLVM IR
```

Each arrow is a separate pass. A giant direct rewrite hides intermediate semantics, weakens tests, and prevents reuse.

## Laboratory 16: Mini-to-LLVM Pipeline

Implement legality, type conversion, and rewrites for Mini operations. Emit fixtures and verify after each stage. Include a missing-pattern failure that proves illegal operations are diagnosed.

Translate the final LLVM dialect module to LLVM IR and run the same programs as the direct Chapter 08 back end. When results differ, identify the first IR level where observable behavior diverges.

## Submission

- staged conversion passes;
- legality and TypeConverter specification;
- per-level IR tests and failure diagnostics; and
- differential results against the direct LLVM back end.

## References

- [MLIR Dialect Conversion](https://mlir.llvm.org/docs/DialectConversion/)
- [MLIR Pass Infrastructure](https://mlir.llvm.org/docs/PassManagement/)

