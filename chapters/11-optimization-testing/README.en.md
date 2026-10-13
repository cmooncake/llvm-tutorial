# Chapter 11: Optimization and Compiler Testing

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 6–9 hours. This chapter replaces “it runs” with evidence for semantics and measurements for optimization.

An optimization is correct only when it preserves every behavior observable under the language specification. Shorter IR is not necessarily faster, and a faster benchmark does not prove semantic equivalence for all programs. Correctness testing and performance experiments therefore remain separate.

## 11.1 Pass Pipelines

Use PassBuilder for standard `O0`, `O1`, and `O2` pipelines with target analysis information. Record custom extension points and expose the effective pipeline in logs.

Run the verifier after custom transformations. Treat overflow flags, poison, undefined behavior, aliasing, and side effects conservatively; C or C++ intuition does not replace the LLVM Language Reference.

## 11.2 Test Layers

Unit tests cover local lexer, parser, and semantic rules. lit/FileCheck regression tests inspect important IR and diagnostic structure. End-to-end tests observe program behavior. Differential tests compare JIT against AOT or optimized against unoptimized execution. Fuzzing searches for crashes, hangs, and phase disagreement.

FileCheck asserts important relationships rather than complete output. Diagnostic tests assert codes, spans, and parameters. Every regression first receives a failing test.

## 11.3 Performance Experiments

Use interpretable microbenchmarks and separate warm-up, JIT time, execution time, and linking. Report hardware, operating system, compiler version, pipeline, sample count, and statistical method. Observe at least two of run time, code size, and compile time.

## Laboratory 11: Optimization Equivalence and Benchmarking

Build an `O0`/`O2` differential runner and benchmark one standard or custom optimization. Generate small well-typed random expression programs and compare output and traps before and after optimization.

Temporarily inject one unsound transformation on an experiment branch, demonstrate that the suite detects it, and then remove it. Keep correctness conclusions separate from performance conclusions.

## Submission

- reproducible and printable pass pipelines;
- unit, regression, end-to-end, and differential test entry points;
- a minimized regression test;
- raw benchmark data and analysis; and
- an optimization correctness argument.

## References

- [LLVM Testing Infrastructure Guide](https://llvm.org/docs/TestingGuide.html)
- [FileCheck](https://llvm.org/docs/CommandGuide/FileCheck.html)
- [Using the New Pass Manager](https://llvm.org/docs/NewPassManager.html)

