# Version and Platform Policy

[简体中文](version-policy.md) | [English](version-policy.en.md)

## Supported Versions

- Primary: LLVM, Clang, and MLIR 22.1.x
- Compatibility: LLVM, Clang, and MLIR 21.1.x
- Language: C++20
- CMake: 3.20 or newer
- Recommended generator: Ninja

Tools, headers, and libraries from different LLVM major releases must not be mixed.

## Platforms

| Platform | Compiler | Support level |
|---|---|---|
| Ubuntu 24.04 x86-64 | Clang | primary CI |
| Windows 11 x86-64 | MSVC or ClangCL | primary desktop |
| macOS arm64 | AppleClang | best effort |

GPU hardware is not a core requirement. Students can generate, inspect, and lower GPU dialect and complete the CPU acceptance path.

## Version Record

Record `clang --version`, `llvm-config --version`, `opt --version`, `cmake --version`, and `ninja --version` before laboratories. When CMake finds the wrong installation, point `LLVM_DIR` at the intended `LLVMConfig.cmake` rather than combining global paths.

## Major-Version Upgrade

Use a separate branch, validate textual IR and tools, then C++ APIs and passes, and finally MLIR dialects and conversions. Record API changes under `docs/compatibility/llvm-N.md`. Change the primary version only after both supported lines pass.

## Official References

- [LLVM releases](https://github.com/llvm/llvm-project/releases)
- [Embedding LLVM with CMake](https://llvm.org/docs/CMake.html#embedding-llvm-in-your-project)
- [LLVM command guide](https://llvm.org/docs/CommandGuide/)
- [MLIR getting started](https://mlir.llvm.org/getting_started/)

