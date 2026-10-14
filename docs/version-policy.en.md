# Version and Platform Policy

[简体中文](version-policy.md) | [English](version-policy.en.md)

## Supported Versions

- Primary: LLVM, Clang, and MLIR 22.1.x
- LLVM 21/23 are not supported yet. The earlier LLVM 21.1 compatibility claim had no execution evidence and is withdrawn.
- Language: C++20
- CMake: 3.20 or newer
- Recommended generator: Ninja
- Python: 3.10 or newer (tests use only the standard library)

The apt setup pins release line 22, not its patch or package revision. CI records exact packages, but no frozen image is published yet; installation is not bit-for-bit reproducible. Before a semester, preserve a tested image digest or package snapshot. Every upgrade must pass the tests again. Tools, headers, and libraries must come from one SDK; tests check matching patch versions.

## Platforms

| Platform | Compiler | Support level |
|---|---|---|
| Ubuntu 24.04 x86-64 | Clang 22 | course baseline and configured CI target |
| Windows + WSL2 Ubuntu 24.04 | Clang 22 inside WSL | recommended Windows learning environment |
| Native Windows and macOS | not established | unverified; no support commitment |

See the [environment study](environment-research.en.md) for rationale and the [testing guide](testing.en.md) for installation, coverage, and execution evidence. A workflow file does not prove remote CI has passed. This is our course decision, not a shared recommendation from universities or LLVM.

The shared MLIR labs use matching `mlir-22-tools`; three CPU experiments have run on 22.1.8. Enable `-DTUTORIAL_ENABLE_MLIR=ON` for exact version checks. Custom dialect development requires matching MLIR development libraries, or LLVM, Clang, and MLIR built from one llvm-project release tag. Do not mix system LLVM with MLIR from main. Complete course implementations of GPU, Transform, and custom dialect specializations remain unvalidated.

GPU hardware is not a core requirement. Students can generate, inspect, and lower GPU dialect and complete the CPU acceptance path.

## Version Record

Record `clang --version`, `llvm-config --version`, `opt --version`, `cmake --version`, and `ninja --version` before laboratories. When CMake finds the wrong installation, point `LLVM_DIR` at the intended `LLVMConfig.cmake` rather than combining global paths.

## Major-Version Upgrade

Use a separate branch, validate textual IR and tools, then C++ APIs and passes, and finally MLIR dialects and conversions. Record API changes under `docs/compatibility/llvm-N.md`. Change the primary version only after the candidate passes; do not automatically promise two supported versions.

## Official References

- [LLVM releases](https://github.com/llvm/llvm-project/releases)
- [Embedding LLVM with CMake](https://llvm.org/docs/CMake.html#embedding-llvm-in-your-project)
- [LLVM command guide](https://llvm.org/docs/CommandGuide/)
- [MLIR getting started](https://mlir.llvm.org/getting_started/)

