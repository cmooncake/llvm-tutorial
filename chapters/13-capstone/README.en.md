# Chapter 13: Course Project—The MiniLang Compiler

[简体中文](README.md) | [English](README.en.md)

> Graduate schedule: proposal in week 6, baseline in week 9, interim results in week 12, final package in week 16. The last 4–5 weeks focus on research and evaluation; chapter numbers are not teaching weeks.

The project turns individually functioning phases into a reproducible, tested, and explainable compiler product. The [project specification](../../docs/capstone.en.md) and [Scalar contract](../../docs/language-profile.en.md) define requirements; this chapter defines execution and review order.

## 13.1 Milestones

**M1 Proposal (week 6):** freeze the Scalar core and submit a question, hypothesis, minimal implementation, baseline, and risks. L3 assesses the front end separately.

**M2 Executable Baseline (week 9):** functions, bindings, control flow, and primitive types execute; every module passes the verifier. Include a baseline and at least one case that must not be transformed.

**M3 Interim Results (week 12):** submit the research increment, preliminary correctness results, raw measurements, and a reduced plan. Arrays and strings are not shared-core deliverables.

**M4 Final Package (week 16):** submit code, test matrix, reproduction steps, report, raw data, and individual contributions; complete the demonstration and defense.

Every milestone builds from a clean checkout, preserves existing tests, and includes a one-page architecture decision record. A small end-to-end slice is more valuable than many unintegrated partial modules.

## 13.2 Final Review

Review begins in a clean environment: follow the README, build, test, and compile an example. Each student explains IR containing control flow, the data path of one diagnostic, and one ABI decision.

The demonstration includes a successful program, static error, runtime trap, AST or IR dump, actual execution path, and data for the research increment. Identify external lli if used; a negative performance result is not automatically a failed project. Slides do not replace execution evidence.

## 13.3 Release Checklist

- language specification matches implementation;
- every public feature has automated tests;
- verifier and sanitizer/fuzz results are recorded;
- CLI, exit codes, and diagnostics are stable;
- runtime ABI is versioned;
- builds contain no personal absolute paths;
- Chinese and English user documentation agree; and
- known limitations are stated honestly.

## Submission

Submit source, tests, runtime, examples, language and ABI documents, architecture description, raw performance data, demo script, and individual or team retrospective. Reference-solution size is not a grading criterion; evidence and explanation are.

## References

- [Complete course-project specification](../../docs/capstone.en.md)
- [MiniLang Scalar teaching contract](../../docs/language-profile.en.md)
- [Research reports and reproduction](../../docs/project-report.en.md)

