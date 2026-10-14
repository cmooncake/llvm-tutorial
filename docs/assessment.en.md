# Assessment and Acceptance

[简体中文](assessment.md) | [English](assessment.en.md)

## Suggested Weights

| Component | Weight | Evidence |
|---|---:|---|
| L1–L5 assignments | 40% | 6, 10, 8, 8, 8 points respectively |
| Four reading discussions | 10% | 2.5 each: claim, assumptions, refuting experiment |
| M1–M3 milestones | 15% | 5 each: question, baseline, interim evidence |
| M4 research artifact and report | 25% | correctness 8, design 5, evaluation 8, reproduction 4 |
| Individual defense and contribution | 10% | semantics/IR explanation 6, contribution evidence 4 |

These are the graduate course's authoritative weights, totaling 100%. L0 is ungraded; M4 is not counted again as a milestone. Do not award implementation, testing, or collaboration credit twice for the same evidence.

## Performance levels and feedback

For each subcriterion, justify full credit for complete independent evidence, roughly 70% for a sound core with missing boundaries, roughly 40% for reproducible partial work with key defects, and zero for no inspectable artifact. Do not grade code volume. Semantic errors affect correctness and dependent experimental claims, not unrelated sound theoretical work.

M1 awards 2 for the question, 2 for a measurable hypothesis/baseline, and 1 for scope/risk. M2 awards 3 for an executable baseline and 2 for negative cases/records. M3 awards 2 for correctness evidence, 2 for raw results, and 1 for plan revision. Rigorous negative results are valid; speedup magnitude is not a grading formula. Speedups without a valid baseline earn no evaluation credit.

Hidden inputs must trace to public Scalar rules; instructors publish semantic errata. Infrastructure failures receive a uniform rerun opportunity rather than a student penalty. Individual credit is not determined solely by commit counts or peer ratings.

## Final Project Rubric

**Correctness:** complete and consistent core semantics, verifier-clean IR, equivalent JIT/AOT behavior, and controlled failure for invalid input.

**Design:** clear lexer/parser/sema/codegen/execution boundaries, a source type system independent of LLVM, a minimal documented runtime ABI, and explicit error/lifetime handling.

**Evidence:** automated tests for every claimed feature, equivalence checks and data for optimization, documented limits, and a clean-build demonstration.

## Excellence Threshold

A project cannot receive the highest evaluation without automated end-to-end tests, robust malformed-input handling, verifier integration, an explanation of control-flow lowering, and a demonstration free of hidden machine-specific edits.

## Individual Assessment in Teams

For teams of two or three, each member identifies owned interfaces and tests, reviews another module, explains one cross-module data path, and submits a short retrospective including one corrected design error.

