# Instructor Guide

[简体中文](teaching-guide.md) | [English](teaching-guide.en.md)

The [graduate plan](graduate-course.en.md) provides weekly activities, discussion questions, and instructor answers. This page covers maintenance and organization. The [Scalar contract](language-profile.en.md) defines acceptance semantics; [release readiness](release-readiness.en.md) records launch status.

## Freeze Before the Course

Freeze one LLVM major line, C++ and CMake requirements, MiniLang syntax and typing, the runtime ABI, platform support, and the boundary between starter and reference code. LLVM APIs evolve; every note identifies the supported course release.

## Starter Code

Provide CMake targets, test commands, SourceManager and basic diagnostics, a CLI skeleton, empty interfaces, smoke tests, and cross-platform build instructions. Do not provide parser control flow, core typing rules, control-flow lowering, or a complete JIT wrapper that can be renamed and submitted.

## Chapter Package

Each chapter ultimately contains lecture notes, starter code, public tests, instructor solutions in a restricted location, and fixtures. Notes state prerequisites, time, submission, acceptance, common failures, and extension questions.

## Risk Control

- By week 3, every student builds an LLVM-dependent project from a clean environment.
- Freeze the Scalar contract by week 6.
- Provide runtime ABI conformance tests by week 9.
- Preserve one end-to-end vertical slice at every milestone.
- Run the reference solution on every supported platform.
- Provide prebuilt LLVM or a container for constrained machines without hiding the toolchain model.
- Require shared MLIR foundations/CPU lowering; specialize in GPUs, full custom dialects, or Transform as appropriate. Common acceptance needs no GPU.

## Review Priorities

Review error-path safety, module boundaries, semantic rather than implementation-detail tests, IR typing/terminators/dominance/ABI, and the student's ability to justify design.

## Academic Integrity

Require decision records and failed experiments, use equivalent small semantic variants where appropriate, ask students to trace the effect of a live rule change, keep hidden tests within the public specification, and grade explanation and evolution rather than code alone.

## Advanced-Topic Boundary

A hands-on advanced topic must form a two-week closed loop, have verifier/test/measurement evidence, explain a limitation of the core design, and remain assessable without scarce hardware. CIR, quantization, sparse tensors, automatic differentiation, e-graphs, and accelerator back ends are appropriate reading or independent-project topics; MLIR fundamentals, custom dialects, and dialect conversion form the continuous laboratory sequence.

