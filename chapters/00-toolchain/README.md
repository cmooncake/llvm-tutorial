# 第 00 章：建立可复现的 LLVM 工具链

预计用时：2–4 小时。先修知识：命令行、C/C++ 基础。

## 学习目标

完成本章后，你应当能够：

- 区分 Clang、LLVM IR、优化器、代码生成器、解释/JIT 工具和链接器；
- 确认所有工具来自兼容的 LLVM 发布线；
- 从 C 源文件保存 `.ll`、`.bc`、汇编、目标文件和可执行文件；
- 解释 target triple 与 data layout 为什么不能随意复制。

## 0.1 工具链不是一个程序

本课程最常用的流水线是：

```text
hello.c
  │ clang -S -emit-llvm
  ▼
hello.ll
  │ llvm-as
  ▼
hello.bc
  │ opt
  ▼
hello.opt.bc
  │ llc -filetype=obj
  ▼
hello.o
  │ clang
  ▼
hello / hello.exe
```

`clang` 在这里既能作为 C 前端，也能作为链接驱动。`opt` 运行 IR 分析和变换；`llc` 负责从 LLVM IR 生成目标相关代码；`lli` 直接执行 bitcode，适合早期实验。

## 0.2 安装要求

课程版本见 `docs/version-policy.md`。安装必须同时包含开发 headers/libraries 与命令行工具；只有一个 `clang.exe` 不足以编译后面的 C++ API 实验。

### Ubuntu

使用发行版包或 LLVM 官方安装方式安装同一主版本的 Clang、LLVM 开发包、lld、CMake 和 Ninja。不同发行版的包名不同，安装后以版本检查为准。

### Windows

建议选择下列一种一致方案：

1. Visual Studio 2022 + LLVM 完整开发包 + CMake + Ninja；
2. LLVM/ClangCL + Ninja；
3. WSL2 Ubuntu，并完全在 WSL 文件系统中构建。

不要让 Windows LLVM、WSL LLVM 和 Visual Studio 自带组件在同一个 build tree 中混用。

### macOS

AppleClang 不等于完整 LLVM 开发包。除 Xcode Command Line Tools 外，还需要安装带 `opt`、`llc`、headers 和 CMake config 的 LLVM 包。

## 0.3 环境自检

在仓库根目录运行：

```powershell
./tools/check-env.ps1
```

或：

```sh
./tools/check-env.sh
```

所有 LLVM 工具的主版本必须一致。保存输出到实验报告。

## 0.4 第一条完整流水线

新建 `answer.c`：

```c
int answer(void) { return 6 * 7; }
int main(void) { return answer() == 42 ? 0 : 1; }
```

依次运行：

```sh
clang -O0 -Xclang -disable-O0-optnone -S -emit-llvm answer.c -o answer.ll
llvm-as answer.ll -o answer.bc
opt -passes='mem2reg,instcombine,simplifycfg' answer.bc -o answer.opt.bc
llvm-dis answer.opt.bc -o answer.opt.ll
lli answer.opt.bc
llc -filetype=obj answer.opt.bc -o answer.o
clang answer.o -o answer
```

PowerShell 使用 `$LASTEXITCODE` 查看上一条程序的退出码。Unix shell 使用 `echo $?`。

`-disable-O0-optnone` 只用于观察教学 pass。如果函数带 `optnone`，许多优化会按契约跳过它。

## 0.5 观察而不是猜测

比较 `answer.ll` 和 `answer.opt.ll`：

- 函数是否仍有 `alloca`、`load`、`store`；
- 常量表达式是否折叠；
- 文件顶部的 `target triple` 与 `target datalayout` 是什么；
- 函数和参数带有哪些 attributes。

不要删除 data layout 后宣称程序仍然可移植。它描述指针大小、对齐和整数布局，会影响 GEP、结构体和 ABI。

## 独立练习

1. 添加一个带局部变量和 `if` 的函数，分别用 `-O0` 与 `-O2` 生成 IR。
2. 用 `opt -passes='print<domtree>' -disable-output` 查看支配树。
3. 用 `llc -march=...` 尝试一个非宿主目标，只生成汇编，不要求链接。
4. 记录哪个阶段首次变成 target-specific，并说明依据。

## 提交物

- 环境版本记录；
- `answer.c`、未优化 IR、优化 IR 与目标汇编；
- 一页以内说明，回答 target triple、data layout、`optnone` 的作用。

## 验收

- `llvm-as` 接受手中的 `.ll`；
- `opt`、`lli` 和最终可执行文件成功；
- 能从任意中间产物继续流水线；
- 不依赖 IDE 中不可见的手工设置。

## 常见失败

- `opt: command not found`：安装的只是 Clang driver，不是完整 LLVM 工具集。
- CMake 找到错误 LLVM：删除 build tree，用正确的 `LLVM_DIR` 重新 configure。
- `optnone` 导致 pass 没变化：按本章命令禁用该属性，或从手写 IR 开始。
- Windows 目标文件无法链接：检查生成目标与链接器架构、运行库和 object format 是否一致。

