# LLVM 编译器构造

这是一门面向“学过 C/C++、数据结构与基础编译原理，但没有 LLVM 工程经验”的项目制课程。

课程不以照抄 Kaleidoscope 为终点，而是让学生逐步构造一门小型静态类型语言 **MiniLang** 的完整工具链：

```text
源代码 -> Lexer -> Parser -> AST -> 语义分析 -> LLVM IR
       -> 优化 -> JIT / 目标文件 -> 链接运行
```

最终成果应是一项可以演示、测试、调试和扩展的工程，而不只是若干 API 示例。

## 课程说明

课程同时包含编译器原理与工程实践。前半部分通过短实验学习 LLVM IR、SSA、控制流和 Pass；中段实现 MiniLang 的词法、语法和静态语义；后半部分完成代码生成、运行时、JIT/AOT、优化和测试。MLIR 与异构代码生成作为完成核心项目后的选修单元。

教学设计、授课节奏和评分建议见 [教师指南](docs/teaching-guide.md) 与 [评分标准](docs/assessment.md)。

## 先修要求

- 熟练使用一种系统语言（课程主线建议 C++20）
- 数据结构、递归、图遍历、基本自动机概念
- 了解词法分析、语法分析和类型检查的目的
- 能使用命令行、CMake、Git 和单元测试框架

不要求学生事先了解 LLVM、SSA、目标文件格式或 JIT。

## 课程安排

建议 14–16 周，每周一次讲授和一次实验：

| 阶段 | 周数 | 目标 |
|---|---:|---|
| A. LLVM 基础 | 1–4 | 能阅读、生成、验证和执行 LLVM IR |
| B. 编译器部件 | 5–8 | 独立完成 lexer、parser、AST、类型检查 |
| C. 后端与工程化 | 9–11 | 完成 IR lowering、运行时、JIT/AOT 和测试 |
| D. 最终项目 | 12–16 | 集成完整语言、优化、诊断、文档与演示 |
| E. 前沿专题（选修） | 额外 3–6 | MLIR、多层 lowering、异构编译与现代 JIT |

## 课程材料

- [课程大纲（Syllabus）](docs/curriculum.md)
- [Lecture Notes 与章节实验](chapters/README.md)
- [MiniLang 1.0 语言规范](docs/language-spec.md)
- [课程项目说明](docs/capstone.md)
- [版本与平台政策](docs/version-policy.md)
- [前沿专题与 MLIR 选修轨道](docs/frontier-tracks.md)

## 课程讲义（Lecture Notes）

| 章 | 主题 | 核心产物 |
|---:|---|---|
| 00 | 课程概述与 LLVM 工具链 | 编译阶段、工具、版本与可复现环境 |
| 01 | LLVM 中间表示 | 类型、值、基本块、指令与验证 |
| 02 | 控制流与静态单赋值形式 | CFG、支配关系与 phi 指令 |
| 03 | 使用 C++ API 构造 LLVM IR | Context、Module、IRBuilder 与 verifier |
| 04 | LLVM 分析与变换 Pass | New Pass Manager、分析失效与插件 |
| 05 | 词法分析 | token、源码位置与词法诊断 |
| 06 | 语法分析与抽象语法树 | Pratt parsing、AST 与错误恢复 |
| 07 | 静态语义与类型检查 | 作用域、名字解析、类型规则与诊断 |
| 08 | LLVM IR 代码生成 | 表达式、局部变量、控制流与函数 |
| 09 | 数据布局与调用约定 | 聚合类型、内存布局、ABI 与 runtime |
| 10 | JIT 与提前编译 | ORC JIT、目标文件与链接 |
| 11 | 优化与编译器测试 | Pass pipeline、差分测试与基准 |
| 12 | 诊断与调试信息 | SourceManager、诊断呈现与 DWARF |
| 13 | 课程项目：MiniLang 编译器 | 前端、后端、runtime 与工具链集成 |
| 14 | MLIR 基础 | operation、region、block 与 dialect |
| 15 | MLIR Dialect 定义 | ODS、verifier、trait 与 canonicalization |
| 16 | Dialect Conversion 与逐层 Lowering | Mini → SCF/Arith/Func → LLVM dialect |
| 17 | 张量、向量化与异构代码生成 | Linalg、Vector、bufferization 与 GPU |
| 18 | Transform Dialect 与优化调度 | 可编程变换、调优空间与实验复现 |

详细安排见 [课程大纲](docs/curriculum.md)，最终项目见 [Capstone 规格](docs/capstone.md)，前沿专题的完整路线见 [前沿专题轨道](docs/frontier-tracks.md)。

课程实现以 [MiniLang 1.0 规范](docs/language-spec.md) 为语义依据，以 [版本政策](docs/version-policy.md) 为工具链依据。当前完成度与后续里程碑记录在 [ROADMAP](ROADMAP.md)。

所有正式讲义遵循 [教材写作规范](docs/writing-guide.md)：从真实问题出发，通过可观察实验逐步建立概念，而不是把 API 和任务清单堆给学生。

## 实验与作业（Laboratories and Assignments）

实验与对应讲义放在同一个章节目录中。每个实验给出 starter、公开测试、提交要求和验收标准；参考解答与学生起始代码分离。课程项目分为前端、静态语义、代码生成和工具链集成四个里程碑。

## 课程项目（Course Project）

课程项目要求实现一门小型静态类型语言 MiniLang。语言行为以 [MiniLang 1.0 规范](docs/language-spec.md) 为准，接口、测试要求和演示方式见 [课程项目说明](docs/capstone.md)。MLIR 后端是进阶扩展，不替代核心 LLVM IR 后端。

## 参考资料（References）

每章列出直接相关的 LLVM/MLIR 官方文档。参考资料用于补充 API 与形式化细节，讲义本身应提供完成实验所需的概念路径，不要求学生从外部文档自行拼凑课程。

## 学习成果

学生最终应能：

- 解释生成 IR 中的类型、基本块、SSA 值和控制流；
- 对合法程序生成通过 LLVM verifier 的 IR；
- 对非法程序给出带源码位置、可理解且不崩溃的诊断；
- 以 JIT 或 AOT 方式运行同一套语言测试；
- 用测试证明语义正确，并用基准数据评价至少一项优化；
- 清楚陈述前端语义、LLVM IR 与平台 ABI 之间的边界。

