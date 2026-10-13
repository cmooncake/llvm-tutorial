# LLVM 大项目教程

这是一门面向“学过 C/C++、数据结构与基础编译原理，但没有 LLVM 工程经验”的项目制课程。

课程不以照抄 Kaleidoscope 为终点，而是让学生逐步构造一门小型静态类型语言 **MiniLang** 的完整工具链：

```text
源代码 -> Lexer -> Parser -> AST -> 语义分析 -> LLVM IR
       -> 优化 -> JIT / 目标文件 -> 链接运行
```

最终成果应是一项可以演示、测试、调试和扩展的工程，而不只是若干 API 示例。

## 课程组织原则

1. **先建立正确心智模型，再调用 LLVM API**：学生应能解释 IR、SSA、CFG、ABI 和数据布局，而不是只会拼 Builder 调用。
2. **每章只引入一个主要困难**：语言设计、编译原理、LLVM API 和工程工具不能同时陡增。
3. **练习可独立验收，成果可累积复用**：前半程的小实验用于隔离概念；后半程把成果迁移进 MiniLang。
4. **从第一天就强调可观察性**：打印 IR、验证 IR、保存中间产物、写负向测试和检查诊断信息。
5. **优化晚于正确性**：先有清晰的前端/中端边界和解释性测试，再做 Pass 与性能实验。
6. **基础主线稳定，高阶内容分轨**：所有学生完成核心编译器；GC、闭包、调试信息、自定义 Pass 等作为荣誉扩展。

## 建议先修知识

- 熟练使用一种系统语言（课程主线建议 C++20）
- 数据结构、递归、图遍历、基本自动机概念
- 了解词法分析、语法分析和类型检查的目的
- 能使用命令行、CMake、Git 和单元测试框架

不要求学生事先了解 LLVM、SSA、目标文件格式或 JIT。

## 推荐节奏

建议 14–16 周，每周一次讲授和一次实验：

| 阶段 | 周数 | 目标 |
|---|---:|---|
| A. LLVM 基础 | 1–4 | 能阅读、生成、验证和执行 LLVM IR |
| B. 编译器部件 | 5–8 | 独立完成 lexer、parser、AST、类型检查 |
| C. 后端与工程化 | 9–11 | 完成 IR lowering、运行时、JIT/AOT 和测试 |
| D. 最终项目 | 12–16 | 集成完整语言、优化、诊断、文档与演示 |
| E. 前沿专题（选修） | 额外 3–6 | MLIR、多层 lowering、异构编译与现代 JIT |

## 目录

```text
llvm-tutorial/
├── README.md                 # 课程入口
├── docs/
│   ├── curriculum.md         # 章节、练习和里程碑
│   ├── capstone.md           # 最终大项目规格
│   ├── assessment.md         # 评分与验收标准
│   └── teaching-guide.md     # 教师组织建议
├── chapters/                 # 各章讲义与独立实验（后续逐章填充）
├── capstone/
│   ├── starter/              # 发给学生的起始仓库
│   ├── tests/                # 公开测试与端到端样例
│   └── reference/            # 教师参考实现；不要下发
├── common/                   # 诊断、测试、CMake 等可复用设施
└── tools/                    # IR 检查、测试驱动、结果可视化脚本
```

## 章节地图

| 章 | 主题 | 核心产物 |
|---:|---|---|
| 00 | 环境与工具链 | 可复现构建、`llvm-config`/CMake、lit/FileCheck 入门 |
| 01 | IR 与执行模型 | 手写 IR，使用 verifier、`opt`、`lli` |
| 02 | SSA 与控制流 | CFG、phi、支配关系练习 |
| 03 | LLVM C++ API | 程序化生成并验证一个函数 |
| 04 | Pass 与分析 | 新 Pass Manager 下的分析/变换 Pass |
| 05 | 词法分析 | 带源码位置的 token 流 |
| 06 | 语法分析与 AST | 优先级表达式、错误恢复、AST dump |
| 07 | 名字解析与类型系统 | 作用域、符号表、类型检查与诊断 |
| 08 | AST 到 LLVM IR | 表达式、局部变量、分支、循环、函数 |
| 09 | 数据布局与 ABI | struct、array、指针、调用约定、运行时边界 |
| 10 | JIT、AOT 与链接 | ORC JIT、目标文件、系统链接器 |
| 11 | 优化与测试 | Pass pipeline、差分测试、性能基准 |
| 12 | 调试信息与工具体验 | 源码位置、诊断、可选 DWARF |
| 13 | 最终项目冲刺 | MiniLang 编译器与运行时集成 |
| 14 | MLIR 心智模型 | operation/region/block、dialect、ODS、`mlir-opt` |
| 15 | 自定义 Dialect | Mini dialect、verifier、canonicalization |
| 16 | 多层 Lowering | Mini → SCF/Arith/Func → LLVM dialect → LLVM IR |
| 17 | 张量与异构编译 | Tensor/Linalg/Vector、bufferization、GPU 映射 |
| 18 | 可编程优化 | Transform dialect、调优空间与可复现实验 |

详细安排见 [课程大纲](docs/curriculum.md)，最终项目见 [Capstone 规格](docs/capstone.md)，前沿专题的完整路线见 [前沿专题轨道](docs/frontier-tracks.md)。

课程实现以 [MiniLang 1.0 规范](docs/language-spec.md) 为语义依据，以 [版本政策](docs/version-policy.md) 为工具链依据。当前完成度与后续里程碑记录在 [ROADMAP](ROADMAP.md)。

所有正式讲义遵循 [教材写作规范](docs/writing-guide.md)：从真实问题出发，通过可观察实验逐步建立概念，而不是把 API 和任务清单堆给学生。

## 完成标准

学生最终应能：

- 解释生成 IR 中的类型、基本块、SSA 值和控制流；
- 对合法程序生成通过 LLVM verifier 的 IR；
- 对非法程序给出带源码位置、可理解且不崩溃的诊断；
- 以 JIT 或 AOT 方式运行同一套语言测试；
- 用测试证明语义正确，并用基准数据评价至少一项优化；
- 清楚陈述前端语义、LLVM IR 与平台 ABI 之间的边界。

