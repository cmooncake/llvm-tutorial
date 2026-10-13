# Chapter 13: Course Project—The MiniLang Compiler

[简体中文](README.md) | [English](README.en.md)

> Recommended duration: 4–5 weeks. The project integrates Chapters 00–12 and introduces no new core language features.

The project turns individually functioning phases into a reproducible, tested, and explainable compiler product. [`docs/capstone.md`](../../docs/capstone.md) is normative; this chapter defines execution and review order.

## 13.1 Milestones

**M1 Front-end Freeze:** specification, lexer, parser, AST, resolver, type checker, and diagnostic codes are stable. Invalid input produces diagnostics without crashing.

**M2 Executable Core:** functions, bindings, control flow, and primitive types run through at least one execution path; every module passes the verifier.

**M3 Runtime and Aggregates:** arrays, strings, bounds checks, runtime ABI, and JIT/AOT differential tests are complete.

**M4 Release Candidate:** optimization, test matrix, build guide, examples, known limitations, performance report, and live demonstration are complete.

Every milestone builds from a clean checkout, preserves existing tests, and includes a one-page architecture decision record. A small end-to-end slice is more valuable than many unintegrated partial modules.

## 13.2 Final Review

Review begins in a clean environment: follow the README, build, test, and compile an example. Each student explains IR containing control flow, the data path of one diagnostic, and one ABI decision.

The demonstration includes a successful program, static error, runtime trap, AST or IR dump, JIT/AOT path, and one optimization supported by data. Slides do not replace execution evidence.

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
- [MiniLang 1.0 language specification](../../docs/language-spec.en.md)

