# 前沿专题轨道

[简体中文](frontier-tracks.md) | [English](frontier-tracks.en.md)

研究生版已经将 MLIR 基础、逐层 lowering 与 CPU bufferization 纳入必修，见[公共实验](graduate-labs.md)。本页是进一步选题的目录；专题建议时长在第 12–16 周内安排，不是全部追加到学期末。

前沿专题的目标不是追逐新 API，而是让学生接触现代编译器的核心问题：如何保留高层语义、如何组合多级变换、如何面向异构硬件，以及如何使优化策略可验证、可搜索和可复现。

## 为什么在 LLVM IR 之后学习 MLIR

LLVM IR 非常适合低层、机器无关的优化与代码生成，但许多领域信息在降到指针、循环和基本块后难以恢复。MLIR 允许一个编译器同时持有多个抽象层级，通过 dialect 表达领域语义，再通过显式 conversion pipeline 逐步 lower。

教学顺序必须是：

```text
先理解 LLVM IR / SSA / CFG / ABI
                ↓
再理解 MLIR operation / region / dialect
                ↓
最后讨论多层 lowering 与异构优化
```

没有第一层，学生容易把 MLIR 当成另一种语法；没有第二层，学生无法判断一次 lowering 丢失了哪些信息。

## 轨道 A：MLIR 编译器工程（推荐）

适合所有完成核心课程且希望继续深入的学生，建议 3–4 周。

### A1：IR 结构与工具

- 阅读 generic/custom assembly form；
- 操作 operation、region、block argument 和 SSA use-def；
- 使用 `mlir-opt`、`-verify-each`、IR printing 与 pass pipeline；
- 对比 LLVM IR 基本块和 MLIR region 的表达能力。

### A2：Mini Dialect

- 用 ODS/TableGen 定义 operations；
- 为 shape、type 或属性添加 verifier；
- 用 trait/interface 暴露跨 operation 的公共语义；
- 编写 canonicalization 与 pattern rewrite。

### A3：Progressive Lowering

推荐链路：

```text
Mini AST
  ↓
Mini dialect             保留语言语义
  ↓
Arith + SCF + Func       结构化控制流与通用计算
  ↓
CF + MemRef + LLVM       显式控制流、内存与 ABI
  ↓
LLVM IR                  优化、目标代码、JIT/AOT
```

每个箭头都是独立 pass，每层都有 legality contract、verifier 和 fixture。学生需要记录每层保留与丢弃的信息。

### A4：Capstone 升级

保留原来的直接 LLVM 后端作为 oracle，通过随机或表驱动程序比较：

```text
同一 MiniLang 程序
 ├─ Direct LLVM backend ─┐
 └─ MLIR backend ────────┴─ 比较输出、退出码和诊断
```

这让“多层 IR 更优雅”的主张变成可测试的工程结论。

## 轨道 B：张量与异构编译

适合有体系结构、并行计算或机器学习基础的学生，建议 3–5 周。

### 核心问题

- tensor value 何时、为何变成 memref/buffer；
- loop、structured op 与 vector op 分别适合表达什么；
- tiling、fusion、vectorization 的合法性条件；
- host/device、address space 和异步执行边界；
- target-independent 与 target-specific dialect 如何分工。

### 建议项目

实现一个很小的 MiniTensor 子语言，支持 elementwise、matmul 与 reduction：

```text
MiniTensor → Linalg/Tensor → SCF/Vector → Bufferization
           → LLVM（CPU）或 GPU/NVVM/ROCDL（可选）
```

基础验收只依赖 CPU；GPU 路径作为加分项。报告至少比较两种 schedule，并解释性能差异是否来自计算量、局部性、向量化或数据搬运。

## 轨道 C：可编程优化与自动调优

适合研究型课程，建议 2–3 周。

- 使用 Transform dialect 将 transform IR 与 payload IR 分离；
- 表达 tiling、fusion、unrolling、vectorization 或 GPU mapping；
- 定义合法参数空间并批量运行 benchmark；
- 保存编译器版本、pipeline、硬件信息与原始数据；
- 分析性能波动，而不是只汇报最快数字。

关键讨论：Transform dialect 不是 pass infrastructure 或 rewrite pattern 的替代品；它更接近对复杂变换的编排与定向控制。

## 轨道 D：现代 LLVM 系统专题

这些题目适合作为一周研讨、论文报告或独立项目，不建议全部塞入主线。

| 专题 | 可回答的问题 | 建议产物 |
|---|---|---|
| ORC JIT / JITLink | 增量编译、符号解析、延迟物化如何工作 | 支持多模块和重定义的 REPL |
| ClangIR（CIR）案例 | 为什么 C/C++ 也需要位于 AST 与 LLVM IR 之间的高层 IR | 对一个 C 特性的 CIR/LLVM IR 对照报告 |
| Profile-guided optimization | 动态行为如何反馈给静态优化 | PGO 前后性能与代码布局实验 |
| Sanitizer 与 fuzzing | 如何系统发现编译器崩溃和 miscompile | parser/sema fuzz harness 与最小化样例 |
| 自动微分 | 高层 IR 如何表达并变换数学语义 | 对标量或张量函数生成梯度 |
| 稀疏与量化 | 数据表示如何改变优化与硬件映射 | 小型 sparse/quant pipeline 分析 |

CIR 目前应当作为架构案例研究，而不是课程稳定依赖；它非常适合说明“在 AST 和 LLVM IR 之间保留语言语义”的现实需求。

## 研究型项目的评价方式

前沿项目按以下证据评分：

1. **语义契约**：每一层 IR 的合法输入和保持条件是什么；
2. **可验证性**：verifier、差分测试、属性测试或数值误差界；
3. **可复现性**：固定版本、pipeline、数据集、硬件和随机种子；
4. **消融实验**：移除某个 pass 或改变某个 schedule 会怎样；
5. **限制说明**：哪些结论只对当前 workload 或目标成立。

## 官方学习入口

- [MLIR Tutorials](https://mlir.llvm.org/docs/Tutorials/)
- [Creating a Dialect](https://mlir.llvm.org/docs/Tutorials/CreatingADialect/)
- [Dialect Conversion](https://mlir.llvm.org/docs/DialectConversion/)
- [MLIR Pass Infrastructure](https://mlir.llvm.org/docs/PassManagement/)
- [Transform Dialect](https://mlir.llvm.org/docs/Dialects/Transform/)
- [GPU Dialect](https://mlir.llvm.org/docs/Dialects/GPU/)
- [LLVM ORCv2](https://llvm.org/docs/ORCv2.html)
- [ClangIR](https://llvm.github.io/clangir/)

