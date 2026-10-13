# LLVM Compiler Construction

[简体中文](README.md) | [English](README.en.md)

This is a project-based course for students who have studied C or C++, data structures, and introductory compiler concepts, but have not yet built software with LLVM.

The course does not stop at reproducing Kaleidoscope. Students incrementally implement the complete toolchain for **MiniLang**, a small statically typed language:

```text
source -> lexer -> parser -> AST -> semantic analysis -> LLVM IR
       -> optimization -> JIT / object file -> linked program
```

The final result is a compiler that can be tested, inspected, debugged, demonstrated, and extended—not a collection of isolated API examples.

## Course Description

The course combines compiler principles with engineering practice. The first part uses focused laboratories to study LLVM IR, SSA, control flow, and passes. The middle part develops the MiniLang lexer, parser, and static semantics. The final part covers code generation, the runtime boundary, JIT and ahead-of-time compilation, optimization, and compiler testing. MLIR and heterogeneous code generation are optional units taken after the core project.

Course organization and assessment guidance are provided in the [instructor guide](docs/teaching-guide.en.md) and [assessment rubric](docs/assessment.en.md).

## Prerequisites

- Proficiency in a systems programming language; the course uses C++20
- Data structures, recursion, graph traversal, and elementary automata
- Familiarity with the purpose of lexical analysis, parsing, and type checking
- Command-line development, CMake, Git, and unit testing

Prior experience with LLVM, SSA, object-file formats, or JIT compilation is not required.

## Schedule

The core course is designed for 14–16 weeks, with one lecture and one laboratory per week.

| Unit | Weeks | Outcome |
|---|---:|---|
| A. LLVM foundations | 1–4 | Read, construct, verify, and execute LLVM IR |
| B. Compiler front end | 5–8 | Implement a lexer, parser, AST, and type checker |
| C. Back end and engineering | 9–11 | Implement lowering, runtime interfaces, JIT/AOT, and tests |
| D. Course project | 12–16 | Integrate the language, diagnostics, optimization, documentation, and demo |
| E. Advanced topics (optional) | 3–6 additional | MLIR, progressive lowering, heterogeneous compilation, and modern JITs |

## Course Materials

- [Syllabus](docs/curriculum.en.md)
- [Lecture notes and laboratories](chapters/README.en.md)
- [MiniLang 1.0 language specification](docs/language-spec.en.md)
- [Course project specification](docs/capstone.en.md)
- [Version and platform policy](docs/version-policy.en.md)
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

Laboratories live beside their corresponding lecture notes. Each laboratory provides starter material, public tests, submission requirements, and acceptance criteria. Reference solutions remain separate from student starter code. The course project has four milestones: front end, static semantics, code generation, and toolchain integration.

## Course Project

Students implement MiniLang, a small statically typed language. The MiniLang 1.0 specification defines observable language behavior; the project specification defines interfaces, tests, and the final demonstration. An MLIR back end is an advanced extension and does not replace the core LLVM IR back end.

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

