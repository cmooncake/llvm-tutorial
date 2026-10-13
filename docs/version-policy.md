# 版本与平台政策

## 支持版本

- **主教学版本：LLVM/Clang/MLIR 22.1.x**
- **兼容版本：LLVM/Clang/MLIR 21.1.x**
- C++：C++20
- CMake：3.20 或更高
- 推荐生成器：Ninja

课程只保证同一 LLVM 发布线内的最新修订版。不要混用不同大版本的 LLVM headers、libraries 与命令行工具。

## 支持平台

| 平台 | 编译器 | 状态 |
|---|---|---|
| Ubuntu 24.04 x86-64 | Clang | 主 CI 平台 |
| Windows 11 x86-64 | MSVC 或 ClangCL | 主桌面平台 |
| macOS arm64 | AppleClang | 尽力支持 |

GPU 专题不属于核心平台门槛。没有受支持 GPU 时，学生仍可生成、检查和 lower GPU dialect，并以 CPU pipeline 完成基础验收。

## 版本检查

开始实验前记录：

```text
clang --version
llvm-config --version
opt --version
cmake --version
ninja --version
```

版本不一致时，优先通过 `LLVM_DIR` 指向目标安装的 `LLVMConfig.cmake`，而不是调整全局 `PATH` 猜测性地混合工具链。

## 升级策略

升级 LLVM 主版本时：

1. 创建独立升级分支；
2. 先运行 IR 文本与命令行实验；
3. 再编译 C++ API 和 Pass；
4. 最后升级 MLIR dialect 与 conversion；
5. 把 API 变化记录到 `docs/compatibility/llvm-N.md`；
6. 两条支持线并行通过后，再更新主教学版本。

## 官方依据

- [LLVM releases](https://github.com/llvm/llvm-project/releases)
- [Embedding LLVM with CMake](https://llvm.org/docs/CMake.html#embedding-llvm-in-your-project)
- [LLVM command guide](https://llvm.org/docs/CommandGuide/)
- [MLIR getting started](https://mlir.llvm.org/getting_started/)

