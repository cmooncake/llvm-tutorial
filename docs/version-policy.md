# 版本与平台政策

[简体中文](version-policy.md) | [English](version-policy.en.md)

## 支持版本

- **主教学版本：LLVM/Clang/MLIR 22.1.x**
- LLVM 21/23 暂不支持；此前的 21.1 兼容声明没有运行证据，现已撤回。
- C++：C++20
- CMake：3.20 或更高
- 推荐生成器：Ninja
- Python：3.10 或更高（测试仅依赖标准库）

apt 安装固定 22 发布线，不固定补丁和包修订。CI 记录精确软件包清单，但尚未发布冻结镜像，不能声称逐字节可复现。授课前应冻结通过测试的镜像摘要或软件包快照；升级必须重跑测试。LLVM headers、libraries 与工具应来自同一 SDK，测试检查补丁版本一致。

## 支持平台

| 平台 | 编译器 | 状态 |
|---|---|---|
| Ubuntu 24.04 x86-64 | Clang 22 | 教学基线与 CI 配置目标 |
| Windows + WSL2 Ubuntu 24.04 | WSL 内的 Clang 22 | 推荐的 Windows 学习方式 |
| 原生 Windows、macOS | 尚未确定 | 未验证，不承诺支持 |

选择依据见[环境调研](environment-research.md)，安装、覆盖范围与真实执行记录见[测试指南](testing.md)。有 CI 配置不代表远程 CI 已通过。本课程的环境选择不代表高校或 LLVM 官方统一推荐。

MLIR 公共实验使用同版 `mlir-22-tools`，已在 22.1.8 实测三个 CPU 实验；开启 `-DTUTORIAL_ENABLE_MLIR=ON` 后检查精确版本。自定义 dialect 开发需要同版 MLIR 开发库，或从同一个 llvm-project 发布 tag 构建 LLVM、Clang 与 MLIR；不能混用系统 LLVM 和 main 分支 MLIR。GPU、Transform 与自定义 dialect 的完整课程实现尚未验证。

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
6. 候选版本通过后，再更新主教学版本，不自动承诺双版本兼容。

## 官方依据

- [LLVM releases](https://github.com/llvm/llvm-project/releases)
- [Embedding LLVM with CMake](https://llvm.org/docs/CMake.html#embedding-llvm-in-your-project)
- [LLVM command guide](https://llvm.org/docs/CommandGuide/)
- [MLIR getting started](https://mlir.llvm.org/getting_started/)

