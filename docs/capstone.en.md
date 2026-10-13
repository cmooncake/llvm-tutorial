# Course Project: The MiniLang Compiler

[简体中文](capstone.md) | [English](capstone.en.md)

## Objective

Build a usable small compiler rather than a thin wrapper around LLVM APIs. The suggested CLI is:

```text
minilang check program.ml
minilang emit-ir program.ml -o program.ll
minilang run program.ml
minilang build program.ml -o program
```

The first course offering freezes syntax and semantics so students solve compiler problems rather than simultaneously designing a language.

## Required Language

- `i32`, `bool`, `unit`, fixed-element arrays, and string slices
- immutable `let`, mutable `var`, and function definitions
- arithmetic, comparison, short-circuit logic, and calls
- blocks, `if/else`, `while`, and `return`
- lexical scope, shadowing, and same-scope duplicate rejection
- located lexical, syntax, resolution, and type errors
- at least one of JIT or AOT; excellent projects share code generation across both

## Architecture

```text
CLI
 ├─ SourceManager + Diagnostics
 ├─ Lexer -> Tokens
 ├─ Parser -> AST
 ├─ Resolver + TypeChecker -> typed AST
 ├─ CodeGen -> LLVM Module
 ├─ OptimizationPipeline
 └─ JITEngine / ObjectEmitter -> Runtime
```

The AST does not own `llvm::Value*`; front-end types are not aliases for `llvm::Type`; parsing does not perform LLVM-dependent type checking; the runtime ABI has a separate versioned document; and every public code-generation entry point has a success/failure contract.

## Engineering Requirements

1. Reproducible build with LLVM line, generator, and commands recorded.
2. Verification of every generated function/module before optimization or execution.
3. Lexer/parser unit tests, semantic negative tests, structural IR tests, and end-to-end execution tests.
4. Located diagnostics for undefined names, mismatched types, arity, missing returns, and invalid control flow.
5. Token, AST, typed-AST, and LLVM IR dumps.
6. Language reference, architecture, build guide, and known limitations.

## Test Pyramid

Use many front-end unit tests, a moderate number of semantic and IR regression tests, and a smaller set of full JIT/AOT programs. Avoid complete golden IR snapshots; assert behavior, key instructions, CFG shape, diagnostic codes, and spans.

## Advanced Extensions

Possible extensions include a custom optimization, closures, monomorphized generics, tracing GC or reference counting, DWARF, modules, WebAssembly, LSP support, an MLIR Mini dialect, a MiniTensor/Linalg pipeline, or Transform dialect schedules. Grade boundaries, tests, and evidence before feature count.

### Additional MLIR Requirements

An MLIR project defines at least one semantic Mini operation, verifier and legality contracts, two independently inspectable lowering stages, a canonicalization/rewrite, translation to runnable LLVM IR, and differential tests against the direct back end or an interpreter.

## Demonstration

Build and run a program with calls, loops, arrays, and strings; show a located type error; explain a phi or memory operation in AST/IR output; show a JIT or AOT artifact path; and justify one optimization or engineering decision with data.

