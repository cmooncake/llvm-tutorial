# 最终项目：MiniLang 编译器

[简体中文](capstone.md) | [English](capstone.en.md)

## 项目目标

构造一个真实可用的小型编译器，而不是 LLVM API 的薄封装。最终命令行界面建议为：

```text
minilang check program.ml
minilang emit-ir program.ml -o program.ll
minilang run program.ml
minilang build program.ml -o program
```

共同核心以 [MiniLang Scalar 契约](language-profile.md) 为准；`check`、`emit-ir`、`run` 必做，`build` 是 AOT 扩展。研究生项目在可执行核心上增加一项可评估的优化或 MLIR 研究增量，不能仅提交功能清单。第 6 周提交 M1 提案，第 9 周 M2 可执行基线，第 12 周 M3 中期结果，第 16 周 M4 最终包；细则见[研究报告要求](project-report.md)。

## 核心语言（所有学生必做）

- 类型：`i32`、`bool`；`unit` 表示无值结果，不作为可存储变量类型；数组与字符串属于另行定义语义的扩展
- 声明：不可变 `let`、可变 `var`、函数定义
- 表达式：算术、比较、逻辑短路、函数调用
- 控制流：块、`if/else`、`while`、`return`
- 作用域：词法作用域与遮蔽；同一作用域禁止重复定义
- 错误：词法、语法、名字解析和类型错误均带源码 span
- 执行：至少一条可靠的运行路径；允许调用外部 `lli`，但不得将它表述为自行实现了 ORC JIT

## 建议架构

```text
CLI
 ├─ SourceManager + Diagnostics
 ├─ Lexer -> Tokens
 ├─ Parser -> AST
 ├─ Resolver + TypeChecker -> typed AST
 ├─ CodeGen -> LLVM Module
 ├─ OptimizationPipeline
 └─ JITEngine / ObjectEmitter -> Runtime
```

必须维持的边界：

- AST 不直接持有 `llvm::Value*`；
- 前端类型不直接等同于 `llvm::Type`；
- parser 不做依赖 LLVM 的类型检查；
- runtime ABI 有独立头文件与版本说明；
- codegen 的每个 public entry point 有成功/失败契约。

## 必做工程能力

1. **可复现构建**：记录 LLVM 兼容版本、生成器和构建命令。
2. **验证**：每个生成模块通过 verifier，错误不能留到 `llc` 才暴露。
3. **测试分层**：lexer/parser 单元测试、语义负向测试、IR 结构测试、端到端运行测试。
4. **诊断**：至少覆盖未定义名字、类型不匹配、参数数量错误、缺失返回和非法控制流。
5. **可观察性**：支持 dump tokens、AST、typed AST 与 LLVM IR。
6. **文档**：语言参考、架构说明、构建指南和限制清单。

## 测试金字塔

```text
少量：端到端程序（JIT/AOT 输出与退出码）
中量：语义与 IR/FileCheck 测试
大量：lexer、parser、类型规则的单元测试
```

不要只做 golden IR 全文比较，因为无关的命名和 LLVM 版本变化会制造脆弱测试。优先检查：行为、关键指令、控制流形状、诊断类别和源码位置。

## 研究增量与扩展

所有研究生项目须选一个问题，提供基线、正确性论证、反例和实验数据；以下是选题方向，不要求全部实现。数组、字符串、完整调试信息等工程扩展不得挤占共同 MLIR 实验与研究评价的时间。

- 自定义优化 Pass，并给出正确性论证与 benchmark
- 闭包及 capture lowering
- 泛型的单态化
- tracing GC 或引用计数运行时
- DWARF 调试信息与源级断点
- 增量/多模块编译
- WebAssembly 目标
- LSP 的 diagnostics、hover 与 go-to-definition
- 增加 MLIR 后端：定义 Mini dialect，并逐层 lower 到 LLVM dialect 与 LLVM IR
- 面向张量的 MiniTensor 子语言：通过 Linalg/Vector/Bufferization 建立 CPU pipeline
- 使用 Transform dialect 表达可替换的 tiling/vectorization 策略

扩展项的评分首先看边界设计、测试与证据，而不是代码行数。

### MLIR 版 Capstone 的额外约束

选择 MLIR 扩展时，不允许仅把 LLVM IR 文本包装成 MLIR。项目必须提供：

- 至少一个表达 MiniLang 语义的自定义 operation；
- 明确的 dialect legality 与 verifier；
- 至少两个可独立检查的 lowering 阶段；
- 一项 canonicalization 或 rewrite；
- 从 MLIR 翻译到最终 LLVM IR 的可运行链路；
- 与原有解释器或直接 LLVM 后端的差分测试。

## 建议仓库布局

```text
capstone/starter/
├── CMakeLists.txt
├── cmake/
├── include/minilang/
│   ├── Basic/          # source、diagnostic
│   ├── Lexer/
│   ├── AST/
│   ├── Sema/
│   ├── CodeGen/
│   └── Execution/
├── lib/                # 与 include 对称
├── tools/minilang/     # CLI
├── runtime/            # C ABI runtime
├── test/               # lit/FileCheck 集成测试
├── unittests/
├── examples/
└── docs/
```

## 演示要求

最终演示不是播放 slides，而是进行一次可重复的工程 walkthrough：

1. 编译并运行一个包含函数、循环和条件分支的 Scalar 程序；选做的聚合类型另行演示；
2. 展示一个类型错误及其源码定位；
3. 展示该程序的 AST 或 IR，并解释一个 phi 或内存操作；
4. 展示从源码到执行的真实链路，标明外部工具与自写组件的边界；
5. 用数据说明一项优化或工程取舍。

