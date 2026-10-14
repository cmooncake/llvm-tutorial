# Course Completion Roadmap

[简体中文](ROADMAP.md) | [English](ROADMAP.en.md)

Status is tracked separately for bilingual instructional content, executable assets, and validation. Chapters 00–18 have bilingual notes, specifications, submission requirements, and references; this does not imply a completed teaching pilot. [Release readiness](docs/release-readiness.en.md) is the authoritative list of semester-launch blockers.

| Area | Bilingual content | Executable assets | Validation |
|---|---|---|---|
| course structure, assessment, specifications | graduate bilingual plan | documentation audit | see audit record in testing guide |
| 00 toolchain | complete | environment scripts and pipeline test | passed on WSL Ubuntu / LLVM 22.1.8 |
| 01–02 IR and SSA/CFG | complete | exercises, reference IR, behavior tests | references passed; initial exercises rejected |
| 03 C++ API | complete | generator, structure and behavior tests | passed on LLVM 22.1.8 |
| 04 passes | complete | plugin, regression and behavior tests | passed on LLVM 22.1.8 |
| 05–07 front end | complete | implementation pending | not run |
| 08–12 back end and engineering | complete | implementation pending | not run |
| 13 course project | notes present | CLI shell, C runtime, 29 public inputs; full reference pending | shell builds and is rejected by acceptance; runtime compiles; full semantics unvalidated |
| 14, 16, 17 shared MLIR labs | notes present | SCF, bufferization, invalid diagnostic | 3 suites passed on MLIR 22.1.8 |
| 15, 18 and other MLIR specializations | notes present | custom dialect, Transform, and other implementations pending | not run |

## R1: Runnable LLVM Foundations

Existing chapter 00–04 implementations now use CTest/Python/FileCheck; chapters 01–02 can select exercise or reference IR. Ubuntu 24.04 / LLVM 22 CI is configured but has not run remotely. LLVM 21 and native Windows/macOS support are not promised. Separate chapter 03–04 student starters remain to be added. See the [testing guide](docs/testing.en.md) for execution evidence.

## R2: MiniLang Front End

Implement lexer, Pratt parser, AST dump, resolver, type checker, and diagnostics; independently validate the Scalar teaching contract.

## R3: MiniLang LLVM Back End

Implement code generation, Scalar runtime, reliable execution, optimization, public tests, and student starter distribution. Full JIT/AOT and debug information depend on the selected research direction.

## R4: MLIR Back End

Implement Mini dialect, conversion pipeline, direct-back-end differential tests, and Transform experiments. Extend the existing shared CPU bufferization lab with tensor/vector specializations.

