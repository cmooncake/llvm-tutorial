# 第 11 章：优化与编译器测试

[简体中文](README.md) | [English](README.en.md)

> 预计用时：6–9 小时。本章把“程序能运行”提升为“语义有证据，优化有数据”。

优化只在保持语言允许观察的行为时才正确。IR 变短不等于更快，benchmark 更快也不证明所有程序语义保持。课程将正确性测试和性能实验分开设计。

## 11.1 Pass Pipeline

通过 PassBuilder 构造标准 `O0`、`O1`、`O2` pipeline，并把目标机器分析信息传入。自定义 pass 插入点必须记录；学生应能用 `-print-pipeline-passes` 或等价日志复现实际 pipeline。

每次自定义变换后运行 verifier。对整数 overflow flags、poison、未定义行为、别名和副作用作保守处理；不能用 C/C++ 直觉替代 LLVM LangRef。

## 11.2 测试分层

单元测试覆盖 lexer、parser、sema 的局部规则；lit/FileCheck 回归测试检查 IR 与诊断的关键形状；端到端测试观察程序行为；差分测试比较 JIT/AOT 或优化前后；fuzzing 寻找崩溃、hang 和阶段不一致。

FileCheck 应断言重要关系而不是完整文本。诊断测试断言编号、span 和参数。任何曾经发生的 bug 都先写失败测试再修复。

## 11.3 性能实验

选择可解释的 microbenchmark，隔离 warm-up、JIT 时间、运行时间和链接时间。报告中给出硬件、系统、编译器版本、pipeline、样本数和统计方法。至少同时观察运行时间与代码尺寸或编译时间。

## 实验 11：优化等价性与基准

建立 `O0`/`O2` 差分 runner，并为一项自定义或标准优化设计 benchmark。加入随机生成的、受类型约束的小表达式程序，比较优化前后输出与 trap 行为。

故意注入一个不安全变换（仅在测试分支），证明测试能捕获它，再删除该变换。实验报告区分 correctness result 与 performance result。

## 提交要求

- 可打印和复现的优化 pipeline；
- 单元、回归、端到端和差分测试入口；
- 一个回归 bug 的最小测试；
- benchmark 原始数据与分析；
- 优化正确性说明。

## 参考资料

- [LLVM Testing Infrastructure Guide](https://llvm.org/docs/TestingGuide.html)
- [FileCheck](https://llvm.org/docs/CommandGuide/FileCheck.html)
- [Using the New Pass Manager](https://llvm.org/docs/NewPassManager.html)

