# Chapter 15: Defining an MLIR Dialect

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 8–12 hours. This chapter defines an IR level that retains MiniLang semantics.

## 15.1 Choosing a Semantic Boundary

Do not create one operation mechanically for every AST node. Preserve semantics needed by later transformations, such as MiniLang functions, statically sized array operations, or checked traps. Reuse `arith` where it already models integer arithmetic exactly.

## 15.2 ODS, Verifiers, and Interfaces

Use ODS/TableGen for operation names, operands, results, attributes, regions, and traits. Declarative constraints cover local shape; C++ verifiers enforce cross-field invariants and emit diagnostics on the relevant operation.

Traits express reusable properties and interfaces express behavioral contracts across operations. Canonicalization applies semantics-preserving moves toward a normal form; test idempotence and cases that must remain unchanged.

## Laboratory 15: The Mini Dialect

Define a minimal `mini` dialect with function/return, an array-length or bounds-check operation, and at least one operation preserving MiniLang-specific semantics. Implement parsing, printing, verification, canonicalization, and round-trip tests.

Construct invalid textual IR for verifier tests rather than testing only builder-generated valid operations.

## Submission

- ODS definitions and generation rules;
- dialect registration, parser/printer, and verifier;
- positive and negative canonicalization tests; and
- a semantic dialect reference.

## References

- [Creating a Dialect](https://mlir.llvm.org/docs/Tutorials/CreatingADialect/)
- [MLIR Operation Definition Specification](https://mlir.llvm.org/docs/DefiningDialects/Operations/)

