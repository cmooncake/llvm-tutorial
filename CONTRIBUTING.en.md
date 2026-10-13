# Contributing

[简体中文](CONTRIBUTING.md) | [English](CONTRIBUTING.en.md)

## Definition of Complete

A chapter is complete only when objectives, prerequisites, duration, and submission are explicit; commands are validated on a supported platform; starter code omits core answers; solutions pass public tests; positive, negative, and boundary cases exist; failure modes teach diagnosis; APIs match supported LLVM versions; and a clean checkout reproduces the work.

Student-facing notes follow `docs/writing-guide.en.md`. Bilingual work follows `docs/translation-policy.en.md`; specification, assignment, behavior, and grading changes update both languages together.

## Commit Types

Use `docs:`, `feat:`, `test:`, `build:`, and `fix:`. Keep large unrelated chapter rewrites in separate commits so notes and reference implementation remain traceable.

## Code

Use C++20 and two-space indentation. Public interfaces live under `include/`, implementations under `lib/`. Ordinary compilation failures do not use exceptions. Diagnostics carry phase, code, and source location. Generated LLVM IR is verified before optimization or execution.

## Changing MiniLang

Update both language specifications, parser/sema/codegen tests, an end-to-end example, the runtime ABI when affected, and an architecture decision record.

