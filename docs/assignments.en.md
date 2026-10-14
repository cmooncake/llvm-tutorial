# Graduate Course Assignments

[简体中文](assignments.md) | [English](assignments.en.md)

Assignments develop one cumulative project, not one repository per chapter. L1–L5 contribute 40 course points; subdivisions below are already course points and are not weighted twice. Public tests provide feedback, complemented by independent cases and explanation. Before assigning work, check assets against [release readiness](release-readiness.en.md); do not claim an unavailable starter exists.

## L0 Environment and reproduction record

Complete in week 1, ungraded. Follow the [testing guide](testing.en.md), recording tool versions, eight foundational test results, and a staged compilation. Intentionally point LLVM_DIR at an invalid location and explain the failing phase. TAs check independent reproduction, not a screenshot.

## L1 Control flow and SSA

Due week 2, 6 points. Implement exercise IR for classify and sum_to, then add a function with short-circuited effects. State expected behavior before constructing the CFG and phi nodes. Submit IR, three boundary cases, one verifier counterexample, and at most two pages of reasoning.

Run classify/sum-to tests with `TUTORIAL_IR_SET=exercises`. Award 3 points for behavior, 2 for SSA/edge reasoning, and 1 for the counterexample. Renaming a reference answer is not a submission. With public references, assign an additional control-flow variant and publish its rules to everyone.

## L2 Analysis and optimization correctness

Due week 4, 10 points. Extend the pass project with deterministic opcode statistics and either integer `sub x, 0 → x` or safe local redundant-expression elimination. The latter covers pure integer expressions in one block, without memory operations; cross-block, load, and floating-point CSE are not minimum requirements.

The graduate analysis component also implements the backward-liveness worklist from Section 11.4, including phi edge uses. Submit diamond, loop, and unused-value results plus a termination argument. Do not use this analysis to delete instructions yet: liveness alone does not establish side-effect safety. Its implementation belongs to the two implementation/invalidation points below, and its derivation to the argument points; total weight is unchanged.

Submit the rule, preconditions, invalidation argument, at least four transformable cases and four non-transformable cases. Address flags, duplicate operands, multiple uses, dead instructions, unchanged functions, and vectors. Run verification, behavioral comparisons, and a fixed negative control for an incorrect transformation.

Award 4 points for correctness/boundaries, 2 for implementation/invalidation, 2 for tests, and 2 for reasoning/individual explanation. Rediscovering an existing pass is acceptable, but claiming its implementation as yours is not. The public passes suite checks the existing add-zero example, not your new rule.

## L3 Front end and semantic diagnostics

Due week 6, 8 points. Implement Scalar lexing, parsing, scope, type checking, and check. For every diagnostic, pair a valid/invalid input differing in one condition: nested shadowing versus same-scope duplication, for example. Track byte spans and test EOF, CRLF, comment endings, and the minimum integer.

Submit code, tests, an AST example, and diagnostic inventory. Award 2 points for lexing/parsing, 3 for names/types, 2 for spans/error paths, and 1 for module boundaries. Missing recovery can lose error-path credit; a crash is never a diagnostic. LLVM verification cannot replace source typing.

## L4 Executable compiler core

Due week 8, 8 points. Add emit-ir and run to L3, including output and traps under the [Scalar contract](language-profile.en.md). Demonstrate recursion, loops, short circuit, shadowing, explicit returns, and trailing values. Compare complete stdout, stderr, and exit status before/after optimization.

Award 4 points for source semantics, 2 for verification/ABI, and 2 for end-to-end/negative tests. External lli is acceptable here; embedded JIT/AOT is not counted again as base credit. Host crashes for language traps, exit-status comparisons of arbitrary i32 results, or a single zero-return main do not satisfy acceptance.

## L5 MLIR staged conversion and value semantics

Due week 11, 8 points. Run the SCF, bufferization, and invalid-yield tests in the [graduate labs](graduate-labs.en.md), retaining each stage. Extend summation to a parameterized function with two branches, zero-trip cases, and nonzero initial values. Design another tensor update retaining the old value and explain its copy requirements.

Submit input, pipeline commands, intermediate IR, output checks, and a legality table: allowed/forbidden dialects, type changes, preserved semantics, and failure conditions per stage. Award 3 points for executable lowering, 2 for tensor semantics/errors, 2 for stage contracts, and 1 for explanation. Calling upstream passes is the starting point, not an implementation of custom conversion; MLIR research teams must implement their own increment later.

## Submission and feedback

Each submission includes commit ID, build/test commands, expected results, limitations, and individual contributions. Exclude binaries, SDKs, and build trees. TAs grade in one environment, distinguishing build, semantic, and environment failures before applying the rubric.

The default allowance is three calendar late days per student across the semester, at most two per submission, excluding the final presentation. Instructors announce treatment beyond this allowance in week 1 rather than changing it retrospectively. Return feedback before the next assignment. Allow one revision explanation documenting diagnosis and repair while preserving original and revised submissions separately.

Official documentation, conceptual discussion, and AI assistance are allowed with disclosure of borrowed/generated code and its validation. Students may not submit unexplained code or fabricate measurements. Academic-integrity decisions require human review, not automatic generated-content detection. Individual defense checks understanding without replacing the public rubric.
