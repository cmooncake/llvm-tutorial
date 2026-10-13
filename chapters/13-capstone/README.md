# 第 13 章：课程项目——MiniLang 编译器

[简体中文](README.md) | [English](README.en.md)

> 建议周期：4–5 周。项目整合前十二章，不再引入新的核心语言特性。

课程项目的目标是把多个“分别能工作”的阶段变成一个可复现、可测试、可解释的编译器产品。完整要求以 [`docs/capstone.md`](../../docs/capstone.md) 为准，本章说明执行顺序与评审方式。

## 13.1 里程碑

**M1 Front-end Freeze**：语言规范、lexer、parser、AST、resolver、type checker 和诊断编号稳定。所有非法输入以诊断结束，不崩溃。

**M2 Executable Core**：函数、绑定、控制流和基础类型可通过至少一条执行路径运行，所有 IR 经 verifier。

**M3 Runtime and Aggregates**：数组、字符串、边界检查、runtime ABI 及 JIT/AOT 差分测试完成。

**M4 Release Candidate**：优化、测试矩阵、构建说明、示例、已知限制、性能报告和现场演示完成。

每个里程碑都要求从干净 checkout 构建，已有测试不回退，并提交一页以内的架构决策记录。功能较少但纵向可运行，优于大量尚未集成的半成品模块。

## 13.2 Final Review

评审从一个陌生环境开始：按照 README 构建，运行测试，再编译示例。学生需要现场解释一段含分支或循环的 IR、一次诊断的数据流和一个 ABI 决策。

演示必须包含成功程序、静态错误、runtime trap、IR 或 AST dump、JIT/AOT 路径及一项有数据的优化。幻灯片不能代替运行证据。

## 13.3 Release Checklist

- 语言规范与实现一致；
- 所有公开功能有自动测试；
- verifier、sanitizer/fuzz 结果已记录；
- CLI、退出码和诊断稳定；
- runtime ABI 版本化；
- 构建不依赖个人绝对路径；
- 中英文用户文档同步；
- 已知限制诚实列出。

## 提交要求

提交源码、测试、runtime、示例程序、语言与 ABI 文档、架构说明、性能原始数据、演示脚本和个人/团队复盘。参考实现的代码量不是评分标准；正确性证据和设计解释是。

## 参考资料

- [课程项目完整规格](../../docs/capstone.md)
- [MiniLang 1.0 语言规范](../../docs/language-spec.md)

