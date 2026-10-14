# 构建与自动测试

[简体中文](testing.md) | [English](testing.en.md)

测试的作用是让你在修改代码后获得可重复的反馈，而不只是证明参考答案能运行。以下命令都从仓库根目录执行；Windows 用户在 WSL2 Ubuntu 24.04 终端执行。先阅读[版本政策](version-policy.md)。

## 安装与首次构建

在你准备用于课程的 Ubuntu 24.04 环境中执行：

```sh
# 会添加 LLVM apt 源并安装系统包；不是只读检查。
sudo bash tools/setup-ubuntu.sh
export PATH=/usr/lib/llvm-22/bin:$PATH
cmake -S . -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DTUTORIAL_ENABLE_MLIR=ON \
  -DCMAKE_C_COMPILER=/usr/lib/llvm-22/bin/clang \
  -DCMAKE_CXX_COMPILER=/usr/lib/llvm-22/bin/clang++ \
  -DLLVM_DIR=/usr/lib/llvm-22/lib/cmake/llvm
cmake --build build --parallel 2
ctest --test-dir build --output-on-failure
```

这里的 `LLVM_DIR` 指向 CMake 配置目录，不是 `bin` 或安装前缀。依赖不完整、版本错误会在配置或测试时失败，不会静默跳过。测试入口使用 `tests/run.py`，不依赖 pip 包或 lit；FileCheck 来自 LLVM 工具包。

想查看每条命令的输出，用 `ctest --test-dir build -V`；只调试 Pass，用 `ctest --test-dir build -R '^passes$' --output-on-failure`。CTest 失败日志位于 `build/Testing/Temporary/LastTest.log`。子进程限时 30 秒，每组测试限时 90 秒，避免错误循环使作业检查一直挂起。

## 公开测试覆盖了什么

| CTest 名称 | 检查 | 不应据此推断 |
|---|---|---|
| environment | SDK 中 8 个工具的精确版本与 CMake 包一致 | 所有系统工具都兼容 |
| toolchain | C → IR → bitcode → 优化 → lli，以及目标文件 → 链接 → 执行 | 任意目标平台均能链接 |
| classify | 71 个输入：正负零、i32 两端、固定种子随机样本；优化前后均检查 | 已穷举全部 i32 |
| sum-to | 42 个输入：空范围、循环边界、65537 时的有符号溢出、固定种子样本；优化前后均检查 | 大输入性能满足要求 |
| generator | FileCheck 检查乘加结构；5 组运行值，包括回绕 | 所有 IRBuilder 用法正确 |
| passes | 消除左右零、连续消除、保留非零/浮点/向量；检查指令计数；4 个整数函数优化前后运行对比 | 已形式化证明变换正确 |
| verifier | 缺少前驱项的 phi 必须失败，并包含对应诊断 | 任意非零退出码都算通过 |
| negative-controls | 两个固定的“只返回 0”错误实现必须被行为检查拒绝 | 学生完成练习后还应失败 |

驱动在 IR 内比较完整 i32 返回值，最后只用 0/1 作为进程退出码，避免 Linux 将返回值截断为 8 位造成误判。所有输入都用同一 SDK 验证；优化步骤使用 `-verify-each`。行为样本是回归防线，不是正确性证明。

## 学生练习与参考实现

默认测试 `solutions/`，这是检查教学资产自身的模式。学生修改 `exercises/` 后在独立构建目录配置：

```sh
cmake -S . -B build-student -G Ninja \
  -DLLVM_DIR=/usr/lib/llvm-22/lib/cmake/llvm \
  -DCMAKE_C_COMPILER=/usr/lib/llvm-22/bin/clang \
  -DCMAKE_CXX_COMPILER=/usr/lib/llvm-22/bin/clang++ \
  -DTUTORIAL_IR_SET=exercises
cmake --build build-student --parallel 2
ctest --test-dir build-student -R '^(classify|sum-to)$' --output-on-failure
```

仓库原始练习只返回 0，两个测试都应失败；不要把它们标为 skip 或 expected failure。完成作业后，应使用同一入口通过它们。这个选项仅切换第 01–02 章 IR，不能把第 03–04 章的参考代码伪装成学生 starter。

## CI 与验证边界

[GitHub Actions 配置](../.github/workflows/tests.yml) 在 Ubuntu 24.04 安装 LLVM 22，构建并运行参考测试，以及独立的固定错误样例。错误样例与学生作业分离，学生完成练习不应导致 CI 失败。它保存 JUnit 报告、工具版本、软件包清单和日志。CI 使用新配置的 apt 发布线，因此未来补丁更新仍可能暴露兼容问题。

研究生配置还运行 `mlir-scf`、`mlir-bufferization`、`mlir-diagnostic` 三组测试，组超时 120 秒；转换产物保存在 `build/mlir-artifacts/`，详见[公共实验](graduate-labs.md)。省略 MLIR 选项时仅运行基础 8 组。CI 已启用 MLIR，但尚未远程实跑。

完整 MiniLang 前后端仍未实现。[公开验收驱动](../capstone/tests/README.md)提供 29 个输入，不能把这些输入的存在计为参考编译器已通过。第 15、18 章等研究方向也没有完整可运行实现；不能宣称全课程测试通过。

### 本地执行记录：2026-10-13

- WSL2 Ubuntu 24.04.1，x86-64；LLVM/Clang 22.1.8；CMake 3.28.3；Python 3.12.3；Release 构建。
- 本次使用 Unix Makefiles 生成器；文档推荐的 Ninja 和远程 GitHub Actions 尚未实跑，不能把本地结果写成远程 CI 通过。
- 官方 LLVM 包解压到被 Git 忽略的 `build/sdk`，未安装系统软件包。由于是非标准前缀，配置额外指定了 SDK 的 `CMAKE_PREFIX_PATH`、运行时 `LD_LIBRARY_PATH` 和系统 zstd 共享库路径；正常 apt 安装不需要这套临时适配。安装脚本经过语法检查，但没有在本机以 sudo 执行。
- 编译生成器和插件成功；8/8 CTest 通过，总耗时 101.63 秒。
- 原始 `exercises/` 中的 `classify` 与 `sum_to` 另行执行，都因结果错误被拒绝，而不是工具缺失或解析错误。
- 双语文档审计通过，共 78 个 Markdown 文件；Python 驱动通过语法编译检查。

首次基础运行的原始报告在 `build-validation/results.xml`，不提交构建产物。实测同时修复了 LLVM 22 的 PassPlugin 头文件路径和独立构建配置。环境检查、静态审阅与实际执行是不同证据；本记录只对上述环境和现有样例负责。

### 研究生版复测：2026-10-13

同一环境追加同版 MLIR 工具并开启 MLIR 选项后，全量 **11/11 CTest 通过，154.18 秒**，其中 3 组 MLIR 共 56.45 秒。报告为 `build-validation/graduate-results.xml`，最新运行日志为 `build-validation/Testing/Temporary/LastTest.log`；各层 MLIR/LLVM 产物保留在该构建目录的 `mlir-artifacts/`。

CLI 外壳另行配置并成功构建，公开 `check` 验收以 0/29 拒绝其未实现阶段；这不是语言参考实现通过。C runtime 在 Clang 22 下以 `-Wall -Wextra -Werror -std=c11` 编译通过，尚非完整端到端 ABI 验证。测量工具完成双进程、两轮、零预热的功能冒烟测试，不据此给出性能结论。双语审计更新为 90 个 Markdown 文件，新增 Python 文件通过语法编译检查。远程 CI、Ninja 和干净镜像安装仍未实跑。
