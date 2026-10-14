# 第 16 章：Dialect Conversion 与逐层 Lowering

[简体中文](README.md) | [English](README.en.md)

> 预计用时：8–12 小时。目标是让每个 lowering 阶段可独立验证和测试。

Dialect Conversion 用 conversion target 声明哪些 operation/type 合法，用 rewrite patterns 替换非法结构，并在需要时由 TypeConverter 处理类型与 materialization。Partial conversion 允许未声明非法的结构留下；full conversion 要求目标范围全部合法化。

课程采用：

```text
Mini → Arith/SCF/Func → CF/MemRef/LLVM dialect → LLVM IR
```

每个箭头是独立 pass。不要用一个巨型 pattern 从高层直接跳到 LLVM dialect，否则中间语义、测试定位和复用能力都会丢失。

## 16.1 Legality 是阶段契约

对每个阶段先写一句可以自动检查的后置条件。例如 SCF-to-CF 后不再保留 `scf.for`；最终 LLVM 翻译前不应依赖尚未 lower 的领域 operation。输入能被 parser/verifier 接受，不意味着当前 conversion target 接受它。

设一个概念性 `mini.add` 需要变成 `arith.addi`。将 Mini 声明为 illegal，Arith 声明为 legal，再提供对应 rewrite。现在暂时移除 rewrite：转换应失败，而不是把未知 op 留到最终翻译才发现。若采用动态 legality，必须解释它检查的类型/属性条件，并给条件两侧的样例。

Partial conversion 不是“可以留下任何东西”：明确 illegal 的 operation 仍须被消除。Full conversion 则要求范围内所有 operation 合法化。选择哪一个取决于本阶段承诺，不是哪个更容易让测试变绿。相关机制见 [Dialect Conversion](https://mlir.llvm.org/docs/DialectConversion/)。

## 16.2 类型转换必须跨越边界

把一个高层值转换成机器表示时，不仅要替换产生该值的 operation，还要考虑函数参数/结果、块参数、分支操作数和调用点。例如概念性的 slice 若变为 pointer 与 length，一对多转换会改变这些位置的 arity；仅替换函数体内部类型无法完成转换。

Materialization 在尚未统一的表示之间搭桥，不是语义证明。若最终残留 `unrealized_conversion_cast`，应先检查生产者和消费者采用的表示是否一致；不能用文本删除 cast 来假装 pipeline 完整。每层保留 IR 后，教师可要求学生指出第一个不满足后置条件的边界，而不是反复更换 Pass 顺序。

## 16.3 公共实验与研究扩展

必修 L5 从标准 SCF/Arith/Func 出发，运行本章 [sum.mlir](test/sum.mlir)，保留 CF、LLVM dialect 和 LLVM IR，并比较优化前后行为。具体命令见[公共实验](../../docs/graduate-labs.md)。这个实验已运行，但它没有实现 Mini dialect，也没有验证一对多 TypeConverter。

下面的 Mini-to-LLVM 实验用于自定义 dialect 研究方向；它不是每位学生在 L5 期限内都要完成的第二套编译器。额外验收要求是缺失 pattern 的失败例、跨函数签名的类型转换和与直接后端的差分结果。

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

