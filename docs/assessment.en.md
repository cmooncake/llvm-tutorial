# Assessment and Acceptance

[简体中文](assessment.md) | [English](assessment.en.md)

## Suggested Weights

| Component | Weight | Evidence |
|---|---:|---|
| Chapter laboratories | 30% | concepts, tests, timely feedback |
| M1–M4 milestones | 20% | integration, stable interfaces, risk management |
| Final implementation | 25% | correctness, completeness, architecture |
| Tests and diagnostics | 10% | positive/negative cases and regression protection |
| Design document and defense | 10% | explanation of IR, semantics, and ABI |
| Engineering collaboration | 5% | incremental commits, review, issue records |

## Final Project Rubric

**Correctness:** complete and consistent core semantics, verifier-clean IR, equivalent JIT/AOT behavior, and controlled failure for invalid input.

**Design:** clear lexer/parser/sema/codegen/execution boundaries, a source type system independent of LLVM, a minimal documented runtime ABI, and explicit error/lifetime handling.

**Evidence:** automated tests for every claimed feature, equivalence checks and data for optimization, documented limits, and a clean-build demonstration.

## Excellence Threshold

A project cannot receive the highest evaluation without automated end-to-end tests, robust malformed-input handling, verifier integration, an explanation of control-flow lowering, and a demonstration free of hidden machine-specific edits.

## Individual Assessment in Teams

For teams of two or three, each member identifies owned interfaces and tests, reviews another module, explains one cross-module data path, and submits a short retrospective including one corrected design error.

