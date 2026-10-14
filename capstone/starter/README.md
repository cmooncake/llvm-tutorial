# MiniLang Starter

[简体中文](README.md) | [English](README.en.md)

本目录提供可编译的 C++20 命令行外壳，不是已经完成的编译器。它检查参数和输入文件，对尚未实现的阶段返回 78，不会将空实现报告为成功。SourceManager、Diagnostic、lexer、parser、sema 与 codegen 仍需实现；参考接口见 [Scalar 契约](../../docs/language-profile.md)。

```sh
cmake -S capstone/starter -B build-starter
cmake --build build-starter
python3 capstone/tests/run.py --compiler build-starter/minilang --stage check
```

原始 starter 的公开测试应全部失败。外壳本身不依赖 LLVM，学生增加 codegen 时再接入 SDK；不要将初始外壳测试结果计作编译器完成度。

