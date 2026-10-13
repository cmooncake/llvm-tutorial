# Chapter 00: Course Overview and the LLVM Toolchain

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 2–4 hours. This chapter establishes a map of the toolchain before asking you to understand every line of LLVM IR.

## 0.1 Components of the LLVM Toolchain

LLVM is not one executable. Clang translates C and C++ into LLVM IR, `opt` analyzes and transforms IR, `llc` performs target code generation, `lli` executes bitcode, and assemblers and linkers complete the path to a native program.

Separating these stages gives failures a location. Instead of saying “the IDE build failed,” we can ask whether source translation, IR verification, optimization, code generation, or linking failed.

## 0.2 Environment and Version Consistency

Run `./tools/check-env.ps1` in PowerShell or `./tools/check-env.sh` in a Unix shell. Compare the major versions of Clang, `llvm-config`, `opt`, `llc`, and `lli`. Later C++ work also requires LLVM headers, libraries, and `LLVMConfig.cmake`; a standalone Clang driver is insufficient.

### Platform Notes

Ubuntu may use distribution or official LLVM packages. Windows may use a complete LLVM development installation with Visual Studio/ClangCL or work entirely inside WSL2. macOS requires a full LLVM package in addition to AppleClang. Do not mix Windows, WSL, and unrelated LLVM installations in one build tree.

## 0.3 Compilation Pipeline

Create:

```c
int answer(void) { return 6 * 7; }
int main(void) { return answer() == 42 ? 0 : 1; }
```

Then preserve each stage:

```sh
clang -O0 -Xclang -disable-O0-optnone -S -emit-llvm answer.c -o answer.ll
llvm-as answer.ll -o answer.bc
opt -passes='mem2reg,instcombine,simplifycfg' answer.bc -o answer.opt.bc
llvm-dis answer.opt.bc -o answer.opt.ll
```

Compare the two textual IR files. Look for stack traffic, constant folding, and simplified control flow. `-disable-O0-optnone` is an observation aid: without it, the front end may attach `optnone`, causing many optimization passes to skip the function.

## 0.4 Bitcode Execution and Native Code Generation

Execute bitcode with `lli answer.opt.bc`, then inspect the exit code. Generate and link native code with:

```sh
llc -filetype=obj answer.opt.bc -o answer.o
clang answer.o -o answer
```

The first path executes bitcode in the LLVM execution environment; the second creates an object file and delegates final linking to the platform toolchain. These become the JIT and AOT paths later in the course.

## 0.5 Target Triple and Data Layout

The target triple names an architecture, vendor, operating system, and environment. Data layout records pointer sizes and alignment rules. Small arithmetic examples may appear to work without them, but aggregates, GEP, and ABI boundaries depend on target layout. Obtain these values from the selected target rather than copying them from another machine.

## Laboratory 0: Compilation Stages and Target Dependence

Add local variables and a conditional to the C program. Generate IR at `-O0` and `-O2`, then assembly with `llc`. Annotate which source information disappears before IR, which structures optimization changes, where target instructions first appear, and which artifacts could be reused for another target.

The required evidence is an annotated pipeline diagram naming every tool, input, and output—not merely a transcript of successful commands.

## Diagnostic Notes

Missing `opt` usually means the complete tool suite is absent or not on `PATH`. No IR change may mean `optnone` or simply that the chosen pass has no legal work. Link failure should first be investigated through symbols, architecture, object format, and ABI rather than random IR type edits.

## Summary

Clang produces IR; `llvm-as` and `llvm-dis` convert between text and bitcode; `opt` analyzes and transforms; `lli` executes; `llc` generates target code; and a linker creates the program. Chapter 01 now examines the `.ll` level directly.

### Submission

- environment report;
- C source, unoptimized and optimized IR, and target assembly;
- annotated compilation pipeline; and
- answers to the observation questions.

## References

- [LLVM Command Guide](https://llvm.org/docs/CommandGuide/)
- [Building LLVM with CMake](https://llvm.org/docs/CMake.html)

