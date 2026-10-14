# 课程大纲（Syllabus）

[简体中文](curriculum.md) | [English](curriculum.en.md)

本页是知识目录；实际周次、必修范围与评分以[研究生教案](graduate-course.md)和[作业说明](assignments.md)为准。第 09 章聚合类型、第 10 章双执行后端、第 12 章完整调试信息是深化材料，不是所有小组的共同验收门槛。

每章统一采用六段式结构：**学习目标 → 心智模型 → 最小示例 → 引导实验 → 独立挑战 → 验收测试**。讲义中的代码用于解释概念；学生提交的代码必须通过自动测试，并附一段设计说明。

## 阶段 A：LLVM 基础

### 第 00 章：课程概述与 LLVM 工具链

- 目标：理解 LLVM 是一组库与工具，而不是单一“编译器”。
- 内容：Clang、LLVM IR、`opt`、`llc`、`lli`、CMake、版本固定。
- 实验：把一个 C 函数编译到 IR、优化、生成汇编并链接执行。
- 验收：能保存每个中间产物；能解释 target triple 与 data layout 的来源。

### 第 01 章：LLVM 中间表示

- 目标：掌握强类型 IR、基本块、终结指令和 verifier。
- 实验：手写整数运算、函数调用与分支；故意制造三种非法 IR 并解释报错。
- 验收：程序输出正确；所有有效 IR 均通过验证；错误案例可重复。

### 第 02 章：控制流与静态单赋值形式

- 目标：从控制流而非源语言语法理解 SSA。
- 实验：实现 `abs`、循环求和和短路逻辑；绘制 CFG；手工放置 phi。
- 挑战：解释 mem2reg 前后的等价性。
- 验收：能够说明每个 phi incoming value 对应的前驱块。

### 第 03 章：使用 C++ API 构造 LLVM IR

- 目标：理解 Context、Module、Type、Value、IRBuilder 的所有权与生命周期。
- 实验：用 API 生成第 02 章的函数，打印并验证模块。
- 验收：禁止只比较输出字符串；同时检查 verifier 与运行结果。

### 第 04 章：LLVM 分析与变换 Pass

- 目标：区分 analysis、transformation 与 preserved analyses。
- 实验：编写指令计数分析；再写一个局部、可证明正确的变换。
- 验收：含正例、反例与“不得变换”案例；展示 Pass 前后 IR。

## 阶段 B：独立构造编译器前端

### 第 05 章：词法分析

- 目标：把字符流转换为可诊断的 token 流。
- 实验：标识符、数字、关键字、运算符、注释；记录 span。
- 验收：覆盖 Unicode/ASCII 策略、非法字符、文件末尾和注释边界。

### 第 06 章：语法分析与抽象语法树

- 目标：理解 precedence climbing 或 Pratt parsing，并设计稳定 AST。
- 实验：表达式、声明、块、if、while、函数；实现 AST dump。
- 验收：错误恢复后能继续报告后续错误；不得以崩溃代替诊断。

### 第 07 章：静态语义与类型检查

- 目标：把语法正确与语义正确分开。
- 实验：作用域、重复定义、未定义名字、函数签名、隐式/显式转换策略。
- 验收：每类错误有源码位置；类型检查不依赖 LLVM Type 充当前端类型系统。

## 阶段 C：Lowering 与工程化

### 第 08 章：LLVM IR 代码生成

- 目标：建立明确的 codegen contract。
- 实验：整数/布尔表达式、局部变量、if、while、函数与 return。
- 验收：每个函数即时验证；失败时打印最小相关 IR；作用域退出后绑定正确恢复。

### 第 09 章：数据布局与调用约定

- 目标：理解“语义上的类型”与“机器上的布局”不同。
- 实验：数组、结构体、字符串 slice；调用少量 C runtime 函数。
- 验收：边界条件、对齐和跨模块调用均有测试；不得硬编码宿主机指针宽度。

### 第 10 章：JIT 与提前编译

- 目标：让同一 Module 进入两条执行路径。
- 实验：ORC JIT 交互执行；输出 object file 并调用链接器生成可执行文件。
- 验收：同一组语义测试在 JIT 和 AOT 下结果一致。

### 第 11 章：优化与编译器测试

- 目标：用证据讨论优化，而不是只比较 IR 是否“更短”。
- 实验：配置标准 pipeline；为一个 MiniLang 特性设计 microbenchmark。
- 验收：优化前后语义一致；报告编译时间、运行时间与代码尺寸中至少两项。

### 第 12 章：诊断与调试信息

- 目标：把编译器做成别人能使用的工具。
- 实验：统一 diagnostic engine、源码摘录、caret、阶段化日志；调试信息为进阶任务。
- 验收：CLI 退出码稳定；错误消息可测试但不过度依赖完整文案。

## 阶段 D：最终项目

### 第 13 章：课程项目——MiniLang 编译器

建议拆成四个里程碑：

1. **M1 提案（第 6 周）**：研究问题、假设、基线和风险；冻结 Scalar 核心。
2. **M2 可执行基线（第 9 周）**：可运行核心、基线与不得变换的例子。
3. **M3 中期结果（第 12 周）**：研究增量、正确性结果、原始数据和缩减计划。
4. **M4 最终包（第 16 周）**：代码、复现步骤、报告、个人贡献与答辩。

每个里程碑必须保持主分支可构建、已有测试不回退，并提交一页以内的工程决策记录。

## 阶段 E：MLIR 公共基础与研究专题

第 14 章基础、第 16 章标准 dialect lowering 和第 17 章 CPU bufferization 是必修公共实验；自定义 dialect、Transform、GPU 等按研究方向选择。下面各章列出完整知识范围，不表示所有实验都必交。

本阶段不取代 LLVM IR 基础，而是在学生已经能解释 SSA、CFG、data layout 和 lowering 后，引入多层 IR。推荐以 MiniLang 的第二条后端为载体：保留既有直接 LLVM IR 后端，再增加 MLIR 后端，以差分测试比较两条路径的语义。

### 第 14 章：MLIR 基础

- 目标：理解为什么单一低层 IR 难以长期保存领域语义。
- 内容：operation、region、block、value、attribute、type、trait、interface 与 dialect。
- 实验：用通用形式和自定义形式读写同一段 MLIR；用 `mlir-opt` 运行 parser、verifier 和 pass pipeline。
- 验收：能区分 LLVM IR、MLIR LLVM dialect 和最终 LLVM IR，避免把三者混为一谈。

### 第 15 章：MLIR Dialect 定义

- 目标：把语言语义表达为可验证、可变换的中高层 IR。
- 内容：ODS/TableGen、custom type、operation verifier、rewrite pattern、canonicalization。
- 实验：定义 `mini.func`、常量、算术、控制流或数组操作；实现至少一条局部规范化规则。
- 验收：畸形 IR 被 verifier 拒绝；rewrite 有正例、反例和幂等性测试。

### 第 16 章：Dialect Conversion 与逐层 Lowering

- 目标：把“大爆炸式 codegen”改造为多个保持语义的转换阶段。
- 内容：conversion target、legal/illegal op、rewrite pattern、type converter、materialization。
- 实验：构造 `Mini → Arith/SCF/Func → CF/LLVM dialect → LLVM IR` pipeline。
- 验收：每一层都可打印、验证和单独测试；最终结果与直接 LLVM IR 后端通过差分测试。

### 第 17 章：张量、向量化与异构代码生成

- 目标：理解抽象数据结构如何逐步映射为内存和硬件执行模型。
- 内容：tensor 与 memref 的差异、structured ops、vectorization、one-shot bufferization、GPU dialect。
- 实验：为矩阵或 stencil 小程序建立逐层 lowering；GPU 环境不足时以 IR 结构和 CPU 路径验收。
- 验收：解释 buffer ownership、address space 和 host/device 边界；不得把硬件可用性作为必需前提。

### 第 18 章：Transform Dialect 与优化调度

- 目标：将“要优化什么”与“如何实现底层变换”分离。
- 实验：对一个 Linalg kernel 表达 tiling、fusion、vectorization 或 mapping 策略，并记录失败条件。
- 验收：同一 payload 在至少两套 transform schedule 下保持语义一致，并用数据比较结果。

完整的选修组合、项目题目与风险控制见 `docs/frontier-tracks.md`。

## 建议教学节奏

- 讲授 25%：只覆盖下一次实验必需的概念。
- 代码阅读 15%：阅读小而完整的参考片段和真实 IR。
- 实验 45%：以自动测试为反馈主渠道。
- 设计复盘 15%：让学生解释错误方案为何失败。

每两章安排一次“IR 诊所”：学生携带一段无法解释或无法验证的 IR，课堂共同从 CFG、类型、支配关系和 ABI 四个角度诊断。

