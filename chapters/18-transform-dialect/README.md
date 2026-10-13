# 第 18 章：Transform Dialect 与优化调度

[简体中文](README.md) | [English](README.en.md)

> 预计用时：6–9 小时。本章把“执行什么变换”从硬编码 pass pipeline 中分离出来。

Transform dialect 使用一段 transform IR 控制另一段 payload IR。Handle 指向 payload operation 的集合，transform operation 对其施加匹配、tiling、fusion、vectorization 或 mapping。它编排底层 transformation，但不替代 pass infrastructure 或 rewrite patterns。

## 18.1 失败与 Handle 生命周期

Transform operation 可以成功、可恢复失败或不可恢复失败。匹配不到目标与违反变换前置条件不是同一种失败。某些变换会消费 handle；继续使用已经失效的 handle 是错误，应启用相应检查并为失败路径写测试。

## 18.2 调度与调优

把 tile size、vector width 和 mapping 作为受约束参数空间。每次实验保存 payload、transform IR、编译器版本、目标、原始测量和正确性结果。最快的一次偶然运行不是结论。

## 实验 18：可替换的优化 Schedule

对第 17 章 matmul 编写至少两套 transform schedule。每套先运行正确性测试，再进行重复测量。加入一个不满足前置条件的 payload，验证 transform 产生预期失败而不是静默生成错误 IR。

报告分析哪一步改变局部性、并行度、向量化或数据移动，并进行至少一次消融：移除一个变换，观察正确性与性能。

## 提交要求

- payload 与两套 transform IR；
- handle/失败路径测试；
- 参数空间与实验驱动；
- 原始数据、统计和消融报告；
- transform 与普通 pass 职责边界说明。

## 参考资料

- [Transform Dialect](https://mlir.llvm.org/docs/Dialects/Transform/)
- [Transform Dialect Tutorial](https://mlir.llvm.org/docs/Tutorials/Transform/)

