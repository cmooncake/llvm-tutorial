# MiniLang Starter

[简体中文](README.md) | [English](README.en.md)

This directory now provides a compilable C++20 CLI shell, not a compiler. It validates arguments/files and exits 78 for unimplemented stages. SourceManager, diagnostics, lexing, parsing, sema, and codegen remain to be implemented under the [Scalar contract](../../docs/language-profile.en.md).

```sh
cmake -S capstone/starter -B build-starter
cmake --build build-starter
python3 capstone/tests/run.py --compiler build-starter/minilang --stage check
```

All acceptance cases should fail on the initial shell. The shell has no LLVM dependency; add the SDK when implementing codegen. Compiling a shell is not evidence of compiler completeness.
