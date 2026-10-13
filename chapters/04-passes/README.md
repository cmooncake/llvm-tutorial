# 第 04 章：LLVM 分析与变换 Pass

[简体中文](README.md) | [English](README.en.md)

预计用时：6–8 小时。先修：第 03 章。

## 学习目标

- 区分 analysis pass、transformation pass 与 instrumentation；
- 理解 function/module pass 的作用域；
- 正确声明 preserved analyses；
- 通过 PassBuilder pipeline parser 把插件接入 `opt`；
- 为变换编写“应变换”和“不得变换”测试。

## 4.1 分析与变换

分析回答问题而不改变 IR，例如指令数量、循环信息或支配树。变换修改 IR，例如删除冗余运算。变换之后，之前缓存的分析结果可能失效；`PreservedAnalyses` 就是变换对分析管理器作出的契约。

本章插件注册两个 function pass：

- `print-inst-count`：输出每个函数的指令数；
- `remove-add-zero`：将整数 `x + 0` 或 `0 + x` 替换为 `x`。

第二个 pass 很小，但足以讨论 use replacement、instruction deletion、迭代器安全和分析失效。

## 4.2 构建

```sh
cmake -S chapters/04-passes -B build/04-passes \
  -G Ninja \
  -DLLVM_DIR=/path/to/lib/cmake/llvm
cmake --build build/04-passes
```

插件文件名因平台而异。以下用 `$PLUGIN` 表示生成的动态库：

```sh
opt -load-pass-plugin "$PLUGIN" \
  -passes='remove-add-zero,print-inst-count' \
  -S test/add-zero.ll
```

## 4.3 变换的正确性条件

`x + 0 -> x` 对整数 `add` 成立，也不受 `nsw/nuw` 影响，因为替换不会新增溢出行为。下列相似变换不能未经论证直接照搬：

- 浮点 `x + 0.0 -> x`：涉及 signed zero、NaN 和 fast-math flags；
- `x * 0 -> 0`：对 poison/undef 的传播必须小心；
- 删除有副作用或可能 trap 的指令；
- 改写后违反 dominance 或 type 约束。

## 4.4 测试

```sh
opt -load-pass-plugin "$PLUGIN" \
  -passes=remove-add-zero -S test/add-zero.ll \
  | FileCheck test/add-zero.ll
```

测试文件同时包含：

- 右侧为零，应变换；
- 左侧为零，应变换；
- 常数非零，不得变换；
- 浮点加零，不得变换。

不要用完整 IR golden file 锁死无关格式。

## 实验 4：分析结果与失效

把 instruction count 提取为真正的 `AnalysisInfoMixin` 分析，并让 printer 通过 `FunctionAnalysisManager::getResult` 获取结果。然后在 `remove-add-zero` 前后打印数量，解释为什么结果需要失效或重新计算。

## 编程练习：局部 IR 变换

任选一个实现：

1. 删除无 predecessor 且不是 entry 的不可达 block；
2. 统计每个函数的 opcode histogram，并以稳定顺序输出；
3. 实现只针对整数的 `sub x, 0 -> x`，与 add-zero 共享 matcher。

要求写出 correctness argument：前置条件、保持的语义、可能受 poison/flags/side effects 影响的部分。

## 提交要求

- 可由 `opt` 加载的插件；
- 至少四个正向和四个负向检查；
- 变换后自动运行 verifier；
- `PreservedAnalyses` 与实际修改相符；
- 一页 correctness note。

## 诊断说明

- 插件能编译但 `opt` 找不到 pass：检查导出的 `llvmGetPassPluginInfo` 和 pipeline 名称。
- Windows DLL 加载失败：工具与插件必须使用 ABI 兼容的 LLVM 构建配置。
- erase 后继续使用旧 iterator/value：先递增 iterator，替换 uses 后再 erase。
- 无论是否修改都返回 `all()`：这会让下游错误复用已经失效的分析。

## 参考资料

- [Writing an LLVM Pass](https://llvm.org/docs/WritingAnLLVMNewPMPass.html)
- [Using the New Pass Manager](https://llvm.org/docs/NewPassManager.html)

