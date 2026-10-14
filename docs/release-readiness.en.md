# Course Release Acceptance

[简体中文](release-readiness.md) | [English](release-readiness.en.md)

This repository is a graduate-course pilot candidate, not a teaching-validated release. The design now uses sixteen weeks, a Scalar core, and optimization/MLIR. Semester-wide delivery still depends on the code, grading, and pilot gates below. This is the authoritative status index: an existing chapter is not an accepted lab.

## Available materials

| Material | Status and evidence |
|---|---|
| Bilingual teaching plan | Weekly schedule, outcomes, formative questions, assignment contracts, rubric, research report, scope |
| LLVM foundations | Generator/plugin build; eight suites passed on LLVM 22.1.8 |
| Shared MLIR labs | SCF lowering, tensor value semantics, invalid yield; three suites passed with matching MLIR |
| Capstone start | Compilable CLI shell and C runtime; no compiler implementation in the shell |
| Scalar public acceptance | Twenty-nine inputs and black-box runner; not passed by a complete reference compiler yet |
| Measurement utility | Output equality, warmup, randomized order, raw samples; measures full process time only |
| CI | Configured; remote execution, frozen image, and release tag remain pending |

## Launch blockers

| Gate | Acceptance condition | Current state |
|---|---|---|
| G1 Language/interface | Consistent Scalar semantics, diagnostics, CLI, ABI, translations | Contract written; independent implementation review needed |
| G2 Reference compiler | Complete L3/L4, all public cases pass, emit-ir and boundary checks added | Incomplete |
| G3 Student distribution | Clean build, stable interfaces, no false-positive starter, explicit public/instructor boundary | Shell exists; complete shared infrastructure pending |
| G4 Research assets | One complete reference vertical slice for each offered specialization | Local LLVM pass and standard MLIR pipeline available; custom dialect/Transform pending |
| G5 Grading calibration | Two graders score identical examples; resolve disagreements; trace hidden tests to rules | Not piloted |
| G6 Reproducible release | Clean image, dependencies, CI, tag, and student instructions agree | Not frozen |
| G7 Student pilot | Target students attempt labs; record time, barriers, TA intervention; revise workload | Not conducted |

Do not label the whole package a mature turnkey course before G1–G3 and G5–G7 pass. Satisfy G4 for the specializations actually offered; one semester need not offer GPU, JIT, tensors, and custom dialects simultaneously.

## Units suitable for a pilot

LLVM IR/SSA, C++ APIs, local passes, and the three CPU MLIR labs can be piloted now. With public references, assess explanations and modified conditions rather than assuming solutions are hidden. Front-end/compiler assignments still need instructor reference implementation; a student's first submission is not an unaudited standard answer.

## Maintenance and errata

Language changes include old/new behavior and a minimal program, then update contracts, translations, public cases, and grading together. Toolchain upgrades rerun foundational/MLIR tests and all source-semantic cases. Preserve a semester version instead of automatically tracking main during teaching.

Test count is not maturity. More test names, skips, empty-shell compilation, or upstream check-mlir results do not establish course compiler correctness. Explicit remaining scope is more useful for preparation than an unsupported completion label.
