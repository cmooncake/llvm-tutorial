# Chapter 12: Diagnostics and Debug Information

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 6–9 hours. Compile-time diagnostics and runtime debugger information serve different users, but both depend on reliable source locations.

## 12.1 Diagnostic Engine

A diagnostic contains severity, stable code, primary span, structured arguments, and optional secondary spans or notes. A renderer supplies filenames, line and column display, source excerpts, carets, and color. Separating data from presentation keeps semantic tests stable without freezing terminal styling.

The CLI has stable exit codes for user errors, warnings, and internal failures. Invalid source input must not print a C++ stack trace. Internal invariant failures retain reproduction context.

## 12.2 LLVM Debug Information

LLVM debug metadata describes source files, compile units, subprograms, types, variables, and instruction locations. Use `DIBuilder` for module structure, assign `DebugLoc` during generation, and finalize before emission.

Debug information maps source-language objects rather than mirroring IR. Optimization may remove variables and reorder code; the goal is an accurate relationship where possible, not a promise that every optimized variable remains editable.

Current LLVM debug records and the legacy intrinsic model must not be mixed in one module. Use the model recommended by the supported release and document version differences.

## Laboratory 12: Diagnostic Presentation and Source Debugging

First implement rendering for single-line and multiline spans, tabs, UTF-8 context, secondary notes, and internal errors without source text. Then emit enough debug information for source breakpoints and call stacks.

Compare `-O0 -g` with `-O2 -g`. Record differences in stepping and variable availability without confusing debugger presentation with code-generation semantics.

## Submission

- structured diagnostic engine and renderer;
- stable exit codes and diagnostic tests;
- minimal complete DIBuilder integration;
- recorded debugger session; and
- documented optimized-debugging limitations.

## References

- [Source Level Debugging with LLVM](https://llvm.org/docs/SourceLevelDebugging.html)
- [LLVM Kaleidoscope: Debug Information](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl09.html)

