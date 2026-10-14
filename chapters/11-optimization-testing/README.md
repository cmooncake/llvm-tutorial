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

## 11.4 数据流分析：先求事实，再做变换

研究生阶段不能把“调用一个 Pass”当成理解优化。先在不修改 IR 的情况下实现一个分析，写出信息如何沿 CFG 传播、汇合点如何合并，以及迭代为什么停止。

以非 SSA 三地址代码的活跃变量为例，`USE[B]` 是块内在首次定义前读到的变量，`DEF[B]` 是块内定义的变量。采用后向 may 分析：

```text
OUT[B] = union(IN[S] for S in successors(B))
IN[B]  = USE[B] union (OUT[B] - DEF[B])
```

从空集合开始；出口的 OUT 为空；只有 IN 改变时把前驱重新加入工作表。有限变量集合与单调增长保证终止，但一次反向遍历并不保证求得循环的定点。让学生记录每轮变化，而不是仅交最后一张集合表。

课堂例子使用一个 diamond：左分支定义 `x = a + 1`，右分支定义 `x = b + 1`，汇合块返回 `x`。汇合块 IN 为 `{x}`；两分支 IN 分别为 `{a}` 和 `{b}`。再加入循环回边，要求解释哪一次传播会重新访问已经处理过的块。

迁移到 SSA 时，不能把 phi 的所有操作数当作后继块的普通 USE。先从后继 IN 中减去其 phi 定义，再加入该前驱边选中的 phi 操作数，之后对各后继边取并集。否则会把另一条边的值错误地判为当前路径活跃。第一版分析可只打印结果；接入变换后再讨论分析失效。

## 11.5 优化合法性：循环不变量不是充分条件

考虑以下控制流，其中 `%d` 在循环外定义，但可能为零：

```llvm
entry:
  br i1 %take, label %work, label %exit
work:
  %q = sdiv i32 42, %d
  br label %exit
exit:
  %r = phi i32 [ 0, %entry ], [ %q, %work ]
  ret i32 %r
```

当 `%take=false, %d=0` 时，原函数返回 0。把除法移动到 entry 会在原本不执行它的路径上引入未定义行为；verifier 仍可能接受新 IR。把 work 放到一个可能零次执行的循环体里，会得到同一类 LICM 反例。不要通过运行含 UB 的错误版本来规定一个“必然崩溃”的测试结果，应检查不得移动的 IR 位置并说明语义反例。

为候选指令逐项说明：操作数是否在新位置可用；是否引入新的执行；是否可能 trap 或产生 UB；读到的内存是否会被循环内写操作改变；移动后是否仍支配所有使用。`load` 的地址不变不代表内容不变，未知调用也不能默认无副作用。学生版安全子集可以只移动无 flags 的整数 `add/sub/mul`，明确排除内存、除法、调用和浮点；不要将该子集命名为完整 LICM。

还需区分普通整数回绕、带 `nsw` 的 poison 和立即 UB。MiniLang Scalar 的回绕加法不能随意加 `nsw`；产生 poison 也不等于在该指令处必然 trap。具体规则以 [LLVM 22 LangRef](https://releases.llvm.org/22.1.0/docs/LangRef.html) 为准。

## 11.6 正确性证据的层次

提交一个变换时，先写前置条件与语义推导，再写最小正例、不得变换的反例和边界值，最后运行差分测试。随机样本扩大覆盖面，但不能把有限测试写成全称证明。

[Alive2](https://web.ist.utl.pt/nuno.lopes/pubs.php?id=alive2-pldi21)可作为专题中的补充工具。报告须区分验证成功、找到反例、超时和不支持；循环展开有界时，“未找到反例”不能被扩张为任意迭代次数的证明。课堂练习要求学生先手算一个反例，再讨论工具适用范围，避免把安装求解器当成本章主要工作。

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

