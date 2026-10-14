# Chapter 16: Dialect Conversion and Progressive Lowering

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 8–12 hours. Every lowering stage must be independently verifiable and testable.

Dialect Conversion uses a conversion target to declare legal operations and types, rewrite patterns to replace illegal structure, and a TypeConverter for types and materializations. Partial conversion permits operations not declared illegal to remain; full conversion requires complete legalization in scope.

The course pipeline is:

```text
Mini → Arith/SCF/Func → CF/MemRef/LLVM dialect → LLVM IR
```

Each arrow is a separate pass. A giant direct rewrite hides intermediate semantics, weakens tests, and prevents reuse.

## 16.1 Legality as a Stage Contract

Write an automatically checkable postcondition for each stage: no `scf.for` after SCF-to-CF, and no unlowered domain operations before LLVM translation. Passing a parser/verifier does not establish conversion legality.

For a conceptual `mini.add` to `arith.addi` rewrite, mark Mini illegal and Arith legal. Remove the pattern and require conversion failure. For dynamic legality, explain the type/attribute predicate and test both sides.

Partial conversion must still eliminate explicitly illegal operations; it is not permission to retain anything. Full conversion requires legalization throughout its scope. Choose according to the stage contract, not convenience. See [Dialect Conversion](https://mlir.llvm.org/docs/DialectConversion/).

## 16.2 Type Conversion Across Boundaries

A representation change affects producers, function signatures, block arguments, branches, and calls. A conceptual slice becoming pointer plus length changes arity at each boundary; changing only body operations is insufficient.

Materialization bridges representations; it does not prove semantics. A remaining `unrealized_conversion_cast` calls for checking producer/consumer agreement, not deleting text. Retained stage IR lets students locate the first broken contract rather than shuffle passes blindly.

## 16.3 Shared Lab and Research Extension

Required L5 starts with standard SCF/Arith/Func and this chapter's [sum.mlir](test/sum.mlir). Retain CF, LLVM dialect, and LLVM IR; compare behavior before and after optimization using the [shared-lab commands](../../docs/graduate-labs.en.md). This tested experiment does not implement Mini or validate a one-to-many TypeConverter.

The following Mini-to-LLVM laboratory is a custom-dialect research specialization, not a second compiler everyone must finish by L5. Additional evidence includes a missing-pattern failure, signature conversion across functions, and differential results against the direct back end.

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

