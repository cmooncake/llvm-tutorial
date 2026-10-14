# LLVM and MLIR Compiler Engineering

[简体中文](README.md) | [English](README.en.md)

This graduate project course assumes C++, data structures, introductory compilers, and architecture, but no LLVM engineering experience. It emphasizes semantics-preserving optimization, multilevel IR, and reproducible research.

The course does not stop at reproducing Kaleidoscope. Students incrementally implement the complete toolchain for **MiniLang**, a small statically typed language:

```text
source -> lexer -> parser -> AST -> semantic analysis -> LLVM IR
       -> optimization -> JIT / object file -> linked program
```

The final result is a compiler that can be tested, inspected, debugged, demonstrated, and extended—not a collection of isolated API examples.

## Course Description

The first half studies LLVM IR, SSA, passes, and the MiniLang Scalar front/back ends. The second develops optimization correctness, MLIR conversion, bufferization, and empirical evaluation. Shared MLIR labs are required; custom dialects, Transform, GPU, and advanced JIT systems are research specializations.

Course organization and assessment guidance are provided in the [instructor guide](docs/teaching-guide.en.md) and [assessment rubric](docs/assessment.en.md).

## Prerequisites

- Proficiency in a systems programming language; the course uses C++20
- Data structures, recursion, graph traversal, and elementary automata
- Familiarity with the purpose of lexical analysis, parsing, and type checking
- Command-line development, CMake, Git, and unit testing

Prior experience with LLVM, SSA, object-file formats, or JIT compilation is not required.

## Schedule

The sixteen-week course has two 90-minute discussions and one 60-minute clinic weekly, plus an estimated 8–12 hours of independent work. See the [graduate teaching plan](docs/graduate-course.en.md) for weekly activities and checks.

| Unit | Weeks | Outcome |
|---|---:|---|
| A. LLVM foundations | 1–4 | Read, construct, verify, and execute LLVM IR |
| B. Executable compiler core | 5–8 | Front end, typing, LLVM lowering, runtime, execution |
| C. Optimization and MLIR | 9–11 | Correctness, staged lowering, CPU bufferization |
| D. Research project | 12–16 | Increment, baseline, ablation, reproduction, defense |
| E. Specialization | within 12–16 | Custom dialect, Transform, GPU, or modern JIT |

## Course Materials

- [Graduate teaching plan and weekly schedule](docs/graduate-course.en.md)
- [Assignments and scoring](docs/assignments.en.md)
- [MiniLang Scalar teaching contract](docs/language-profile.en.md)
- [Shared MLIR labs](docs/graduate-labs.en.md)
- [Research reports and experimental records](docs/project-report.en.md)
- [Release acceptance and remaining blockers](docs/release-readiness.en.md)

- [Syllabus](docs/curriculum.en.md)
- [Lecture notes and laboratories](chapters/README.en.md)
- [MiniLang 1.0 language specification](docs/language-spec.en.md)
- [Course project specification](docs/capstone.en.md)
- [Version and platform policy](docs/version-policy.en.md)
- [Building and automated tests](docs/testing.en.md)
- [LLVM tutorial versions and environment study](docs/environment-research.en.md)
- [Advanced topics and MLIR tracks](docs/frontier-tracks.en.md)
- [Chinese–English maintenance policy](docs/translation-policy.en.md)

Chinese remains normative for MiniLang 1.0. English documents mirror the same numbered requirements and share all source code and tests.

## Lecture Notes

| No. | Topic | Principal artifact |
|---:|---|---|
| 00 | Course Overview and the LLVM Toolchain | Compilation stages, tools, versions, and reproducible environments |
| 01 | LLVM Intermediate Representation | Types, values, basic blocks, instructions, and verification |
| 02 | Control Flow and Static Single Assignment Form | CFGs, dominance, and phi nodes |
| 03 | Constructing LLVM IR with the C++ API | Context, Module, IRBuilder, and the verifier |
| 04 | LLVM Analysis and Transformation Passes | New Pass Manager, invalidation, and plugins |
| 05 | Lexical Analysis | Tokens, source locations, and lexical diagnostics |
| 06 | Parsing and Abstract Syntax Trees | Pratt parsing, AST design, and error recovery |
| 07 | Static Semantics and Type Checking | Scope, name resolution, typing rules, and diagnostics |
| 08 | LLVM IR Code Generation | Expressions, local variables, control flow, and functions |
| 09 | Data Layout and Calling Conventions | Aggregate types, memory layout, ABI, and runtime interfaces |
| 10 | JIT and Ahead-of-Time Compilation | ORC JIT, object files, and linking |
| 11 | Optimization and Compiler Testing | Pass pipelines, differential testing, and benchmarking |
| 12 | Diagnostics and Debug Information | Source management, diagnostic presentation, and DWARF |
| 13 | Course Project: the MiniLang Compiler | Front end, back end, runtime, and toolchain integration |
| 14 | MLIR Fundamentals | Operations, regions, blocks, and dialects |
| 15 | Defining an MLIR Dialect | ODS, verifiers, traits, and canonicalization |
| 16 | Dialect Conversion and Progressive Lowering | Mini → SCF/Arith/Func → LLVM dialect |
| 17 | Tensors, Vectorization, and Heterogeneous Code Generation | Linalg, Vector, bufferization, and GPU |
| 18 | Transform Dialect and Optimization Scheduling | Programmable transformations and reproducible tuning |

## Laboratories and Assignments

Laboratories live beside their lecture notes. Executable tests cover chapters 00–04 and three shared MLIR CPU experiments; chapters 01–02 have separate exercise and reference IR. MiniLang has a CLI shell, runtime, and public case driver, but no complete reference compiler. See [release readiness](docs/release-readiness.en.md). Project milestones are proposal, executable baseline, interim results, and final package.

## Course Project

Students implement the [MiniLang Scalar core](docs/language-profile.en.md) and evaluate one optimization or MLIR research increment. Shared MLIR labs are required; a custom MLIR compiler back end is a specialization. This repository is a pilot candidate, not a validated turnkey semester release.

## References

Each chapter links directly to the relevant official LLVM or MLIR documentation. References supplement API and formal details; students should not have to assemble the main conceptual path from unrelated external sources.

## Learning Outcomes

By the end of the course, students should be able to:

- explain the types, basic blocks, SSA values, and control flow in generated IR;
- generate LLVM IR that passes the verifier for every valid source program;
- produce source-located diagnostics for invalid programs without crashing;
- execute the same semantic test suite through a JIT or AOT path;
- establish semantic correctness with tests and evaluate an optimization with data;
- state clearly where source-language semantics, LLVM IR, and the platform ABI meet.

