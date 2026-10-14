# LLVM 教程的版本与实验环境

[简体中文](environment-research.md) | [English](environment-research.en.md)

调研日期：2026-10-13。下表区分来源明确写出的要求与本课程自己的选择。未给版本号的课程，不根据开课年份猜测版本。

## 上游材料对比

| 材料 | 版本和环境证据 | 对本课程的启示 |
|---|---|---|
| [Kaleidoscope 22.1.0](https://releases.llvm.org/22.1.0/docs/tutorial/index.html) | 有发布版本对应的教程；[在线版](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/)不是冻结版本 | API 与 release 文档配套；小型教程的工程简化不是最终项目架构 |
| [llvm-tutor](https://github.com/banach-space/llvm-tutor#development-environment) | 本次打开的 README 写 LLVM 23、C++17、CMake ≥ 3.20，自述测试于 Ubuntu 23.04 / macOS 11.7；采用 lit/FileCheck | 借鉴独立插件、测试与 CI，不照搬滚动更新的环境；上游自述不等于我们的验证 |
| [CMU 15-411 Spring 2024 Lab 6](https://www.cs.cmu.edu/~janh/courses/411/24/labs/lab6llvm.pdf) | 指向 Andrew Linux 机器，要求 LLVM 与原生后端、回归测试和报告；该作业未指定 LLVM 主版本 | 学习稳定的编译器接口和实验评估，不编造“CMU 使用 LLVM N” |
| [Cornell CS 6120 Spring 2025 Lesson 7](https://www.cs.cornell.edu/courses/cs6120/2025sp/lesson/7/) | 要求 LLVM/CMake；给出 Homebrew 示例，提醒不用 Xcode 内置 LLVM；未固定版本 | 区分系统编译器与完整 SDK；旧视频命令应对照修订后的文字 |
| [MLIR Getting Started](https://mlir.llvm.org/getting_started/) / [Toy](https://mlir.llvm.org/docs/Tutorials/Toy/) | 从 llvm-project 构建 MLIR，启用 examples、assertions，运行 `check-mlir`；网页命令未 checkout 固定 release | 为学生补上固定 tag；基础阶段不要求编译整个 LLVM/MLIR |

搜索摘要曾返回 llvm-tutor 的 LLVM 22 信息，直接打开 README 却返回 23。搜索结果不能充当版本锁定文件。表中的学期、发布版本页面有固定上下文；main 分支和在线文档仍会变化。

## 课程环境的选择

课程需要同一套可重现的环境，不是最大的版本号。LLVM 22.1 有发布文档，[apt.llvm.org](https://apt.llvm.org/) 提供 Noble 的 `llvm-toolchain-noble-22` 仓库。Ubuntu 24.04 能用于 Linux、WSL2 与 GitHub Actions，减少课堂中 ABI、动态库、链接器和 shell 差异。

基础阶段安装开发包，让学生把时间用在 IR 和 Pass 上。修改 LLVM、开启 assertions 或构建课程 dialect 时再进入源码构建。这是教学取舍，不是说其他平台不适合 LLVM。

安装脚本采用带 `signed-by` 的独立 apt 源并检查签名密钥指纹，不照搬旧教程的全局 `apt-key`。固定发布线并不等于固定补丁；开课前冻结镜像的要求见[版本政策](version-policy.md)。

## MLIR 选修的源码环境

以下是固定 tag 的准备方案，不是已经通过的课程 MLIR 实验。在独立目录中运行，需先安装 Git、CMake、Ninja、C++ 工具链与 Python；基础环境不需要 CUDA：

```sh
git clone --depth 1 --branch llvmorg-22.1.0 https://github.com/llvm/llvm-project.git
cmake -S llvm-project/llvm -B llvm-project/build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_PROJECTS="clang;mlir" \
  -DLLVM_TARGETS_TO_BUILD=Native \
  -DLLVM_BUILD_EXAMPLES=ON \
  -DLLVM_ENABLE_ASSERTIONS=ON
cmake --build llvm-project/build --target check-mlir --parallel 2
```

这个 tag 是明确版本示例，不是“最新补丁”的声明。需要其他 Clang/LLVM 工具时继续构建相关 targets 或完整构建。`check-mlir` 检查上游 MLIR，不代表尚未实现的 Mini dialect 已通过。GPU 章节再引入 NVPTX/AMDGPU、驱动和运行时；并发度根据可用内存选择。

## 自动测试的组织

[LLVM Testing Guide](https://llvm.org/docs/TestingGuide.html) 区分回归测试、单元测试和 test suite；[FileCheck](https://llvm.org/docs/CommandGuide/FileCheck.html) 适合匹配 IR 结构。本仓库当前采用 CTest 调度、Python 标准库驱动、FileCheck 检查，无需额外安装 lit。等 MiniLang/MLIR 有较多 `RUN:` 文件后再引入统一 lit 配置，不能把没有执行器的指令当作自动测试。

IR 文本检查不能代替行为检查。现有测试还用 `lli` 执行函数，在优化前后检查预期结果，并要求非法 IR 被 verifier 拒绝。具体覆盖范围见[测试指南](testing.md)。
