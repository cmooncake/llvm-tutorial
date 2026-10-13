# Course Completion Roadmap

[简体中文](ROADMAP.md) | [English](ROADMAP.en.md)

Status is tracked separately for bilingual instructional content, executable assets, and validation. All 00–18 chapters now have Chinese and English notes, laboratory specifications, submission requirements, and references. Chapters 00–04 have initial shared IR/C++ assets; Chapters 05–18 still require the starter/reference implementation and executable tests described by their notes.

| Area | Bilingual content | Executable assets | Validation |
|---|---|---|---|
| course structure, assessment, specifications | complete | documentation audit | 74 files audited |
| 00 toolchain | complete | environment scripts | waiting for local LLVM |
| 01–02 IR and SSA/CFG | complete | exercises and reference IR | waiting for local LLVM |
| 03 C++ API | complete | generator and check | waiting for LLVM/CMake |
| 04 passes | complete | plugin and check | waiting for LLVM/CMake |
| 05–07 front end | complete | implementation pending | not run |
| 08–12 back end and engineering | complete | implementation pending | not run |
| 13 course project | complete | starter/reference pending | not run |
| 14–18 MLIR | complete | implementation pending | not run |

## R1: Runnable LLVM Foundations

Complete and validate 00–04 starter, solution, lit/FileCheck, cross-platform CI, and LLVM 21.1/22.1 compatibility notes.

## R2: MiniLang Front End

Implement lexer, Pratt parser, AST dump, resolver, type checker, diagnostics, and freeze MiniLang 1.0.

## R3: MiniLang LLVM Back End

Implement code generation, runtime, JIT/AOT, optimization, debug information, public tests, and student starter distribution.

## R4: MLIR Back End

Implement Mini dialect, conversion pipeline, direct-back-end differential tests, tensor/vector/bufferization laboratories, and Transform dialect experiments.

