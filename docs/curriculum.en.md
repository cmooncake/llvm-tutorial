# Syllabus

[简体中文](curriculum.md) | [English](curriculum.en.md)

Each chapter follows a common structure: objectives, conceptual model, worked example, laboratory, independent exercise, and acceptance evidence. Lecture code explains a concept; submitted code passes automated tests and includes a short design note.

## Unit A: LLVM Foundations

**00 Course Overview and the LLVM Toolchain.** Separate Clang, IR, `opt`, `llc`, `lli`, object emission, and linking. Preserve intermediate artifacts and explain target triple and DataLayout.

**01 LLVM Intermediate Representation.** Write typed functions, branches, calls, memory operations, and invalid examples. Distinguish parser failures from verifier failures.

**02 Control Flow and SSA.** Construct CFGs, phi nodes, loops, and short-circuit operations. Compare memory form with mem2reg output.

**03 Constructing LLVM IR with C++.** Use Context, Module, IRBuilder, values, and ownership correctly. Generate and verify prior hand-written functions.

**04 Analysis and Transformation Passes.** Build a New Pass Manager plugin, preserve analyses correctly, and test both transformations and non-transformations.

## Unit B: Compiler Front End

**05 Lexical Analysis.** Produce located tokens, stable EOF behavior, and lexical diagnostics.

**06 Parsing and ASTs.** Implement recursive descent, Pratt expressions, deterministic AST dumps, and bounded recovery.

**07 Static Semantics and Type Checking.** Resolve names under lexical scope, enforce MiniLang typing rules, suppress cascades, and check return paths.

## Unit C: Back End and Engineering

**08 LLVM IR Code Generation.** Lower values, addresses, bindings, control flow, calls, and returns while preserving evaluation semantics.

**09 Data Layout and Calling Conventions.** Implement arrays and strings through target DataLayout, GEP, a documented runtime ABI, and conformance tests.

**10 JIT and Ahead-of-Time Compilation.** Share one module pipeline between ORCv2 LLJIT and object emission/linking; compare execution behavior.

**11 Optimization and Compiler Testing.** Build reproducible pipelines, layered tests, differential checks, fuzzing, and measured optimization experiments.

**12 Diagnostics and Debug Information.** Separate diagnostic data from rendering and add source-level debug metadata.

## Unit D: Course Project

**13 The MiniLang Compiler.** Complete M1 front-end freeze, M2 executable core, M3 runtime and aggregates, and M4 release candidate. Every milestone builds from a clean checkout and retains a working vertical slice.

## Unit E: Advanced MLIR Track

**14 MLIR Fundamentals.** Study operations, regions, blocks, dialects, verification, and `mlir-opt`.

**15 Defining an MLIR Dialect.** Define Mini operations with ODS, verifiers, interfaces, parsing, printing, and canonicalization.

**16 Dialect Conversion and Progressive Lowering.** Implement `Mini → Arith/SCF/Func → CF/MemRef/LLVM dialect → LLVM IR` as independently testable passes.

**17 Tensors, Vectorization, and Heterogeneous Code Generation.** Develop a Linalg/Tensor, Vector, Bufferization, and optional GPU pipeline.

**18 Transform Dialect and Optimization Scheduling.** Express replaceable schedules, validate failures and handle lifetimes, and conduct reproducible tuning.

## Teaching Rhythm

Use approximately 25% lecture, 15% guided code reading, 45% laboratory, and 15% design review. Every two chapters, hold an IR clinic in which students diagnose an unexplained verifier or semantic failure through types, CFG, dominance, and ABI.

