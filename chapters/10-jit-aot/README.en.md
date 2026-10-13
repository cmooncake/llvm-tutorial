# Chapter 10: JIT and Ahead-of-Time Compilation

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 7–10 hours. This chapter sends one LLVM module through two execution paths.

JIT compilation emits and resolves code in the current process, supporting REPLs, dynamic languages, and rapid feedback. Ahead-of-time compilation emits an object file for the system linker. Both paths share the front end, code generator, and most optimization; they must not become semantically different compilers.

## 10.1 ORCv2 and LLJIT

Begin with ORCv2 `LLJIT`: initialize the native target, create the JIT, install a current-process symbol generator, add a `ThreadSafeModule` to a JITDylib, look up `main`, and invoke it.

JIT resources have lifetimes. Adding a module transfers ownership; runtime symbols require deliberate exposure; and LLVM `Expected`/`Error` values must be propagated rather than hidden behind unconditional `cantFail`.

## 10.2 Object Emission and Linking

The AOT path uses a TargetMachine to set the triple and DataLayout, runs the code-generation pipeline into an object file, and invokes a compiler driver or linker with the runtime. Provide `--emit-ir`, `--emit-obj`, and `build`, and print a reproducible link command.

Do not use shell-string concatenation as a process API. Pass an argument array, preserve paths containing spaces, and inspect process exit status.

## Laboratory 10: Dual Execution Back Ends

Implement `minilang run` and `minilang build`. Execute the same programs through JIT and AOT and compare standard output, standard error, exit status, and trap category.

Cover calls, recursion, runtime symbols, name collisions, missing `main`, link failures, and repeated JIT sessions. When measuring compile time, separate front end, optimization, code generation, and linking.

## Submission

- ORCv2 `LLJIT` engine;
- object emission and robust link driver;
- JIT/AOT differential tests;
- explicit handling of every LLVM Error; and
- platform limitations and reproducible commands.

## References

- [ORC Design and Implementation](https://llvm.org/docs/ORCv2.html)
- [LLVM Kaleidoscope Tutorial](https://llvm.org/docs/tutorial/)

