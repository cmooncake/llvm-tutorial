# 第 16 章：Dialect Conversion 与逐层 Lowering

[简体中文](README.md) | [English](README.en.md)

> 预计用时：8–12 小时。目标是让每个 lowering 阶段可独立验证和测试。

Dialect Conversion 用 conversion target 声明哪些 operation/type 合法，用 rewrite patterns 替换非法结构，并在需要时由 TypeConverter 处理类型与 materialization。Partial conversion 允许未声明非法的结构留下；full conversion 要求目标范围全部合法化。

课程采用：

```text
Mini → Arith/SCF/Func → CF/MemRef/LLVM dialect → LLVM IR
```

每个箭头是独立 pass。不要用一个巨型 pattern 从高层直接跳到 LLVM dialect，否则中间语义、测试定位和复用能力都会丢失。

## 实验 16：Mini-to-LLVM Pipeline

实现 Mini operation 的 legality、类型转换和 rewrite。每阶段输出 fixture 并运行 verifier；提供故意遗漏 pattern 的失败测试，确认 conversion 会报告仍然非法的 operation。

最终把 LLVM dialect 翻译为 LLVM IR，与第 08 章直接后端运行同一组程序。差异出现时先定位在哪一层首次产生不同的可观察结果。

## 提交要求

- 分阶段 conversion passes；
- legality 与 TypeConverter 说明；
- 各层 IR tests 和失败诊断；
- MLIR/直接 LLVM 后端差分结果。

## 参考资料

- [MLIR Dialect Conversion](https://mlir.llvm.org/docs/DialectConversion/)
- [MLIR Pass Infrastructure](https://mlir.llvm.org/docs/PassManagement/)

