# MLIR 研究生实验

[简体中文](graduate-labs.md) | [English](graduate-labs.en.md)

这组实验将 LLVM 基础连接到多层 IR。先运行给定例子，再修改其中一个语义条件，预测哪些转换阶段会变化。它们是 CPU 上可重复的实验，不要求 GPU，也不声称已经实现 MiniLang 的 MLIR 后端。

## 准备与运行

在已完成基础安装的 Ubuntu 24.04 中，安装同一发布线的 MLIR 工具：

```sh
sudo apt-get install mlir-22-tools
cmake -S . -B build -DTUTORIAL_ENABLE_MLIR=ON
cmake --build build --parallel 2
ctest --test-dir build -L mlir --output-on-failure
```

这里沿用已经选择正确 LLVM_DIR 的 build；首次配置仍按[测试指南](testing.md)。工具缺失或版本不一致时失败，不自动略过 MLIR。输出保存在 `build/mlir-artifacts/`，分 suite 存放，可以并行运行。

## 结构化循环与控制流

输入为 `chapters/16-progressive-lowering/test/sum.mlir`。`scf.for` 的区间是左闭右开，循环携带的 `%acc` 是一个值，不是隐式的可变内存。循环计算 0…9 的和，程序内部比较 45，返回 0 表示符合预期。

第一次运行前画出循环的初值、迭代参数和结果。在 `cfg.mlir` 中找出对应 block arguments；在 `llvm-dialect.mlir` 与 `program.ll` 中继续追踪它们。不要只观察操作名变化：回答每一阶段把哪些结构性事实变成了显式分支。

手工重现核心转换：

```sh
mlir-opt chapters/16-progressive-lowering/test/sum.mlir --convert-scf-to-cf -o cfg.mlir
mlir-opt cfg.mlir --convert-to-llvm --reconcile-unrealized-casts -o lowered.mlir
mlir-translate --mlir-to-llvmir lowered.mlir -o program.ll
opt -passes=verify -disable-output program.ll
lli program.ll
```

自动测试另行检查 O2 后的结果。改动上界、步长和初值时，先用独立数学计算写出预期值，再修改 IR。仅将比较常量改为实际错误结果不算修复。

## Tensor 值与 buffer 复用

输入为 `chapters/17-tensor-vector-gpu/test/value-semantics.mlir`。`%a` 的四个元素为 1；`%b` 由 `%a` 的第 0 项改为 2 得到。随后同时读取 `%a[0]` 和 `%b[0]`，正确和为 3。如果错误地认为 tensor.insert 总是可以原地修改同一个 buffer，就可能得到 4。

流水线先做 One-Shot Bufferization 和 ownership-based deallocation，再把 Linalg 降成循环、SCF 降成 CFG，最后转入 LLVM。查看 `buffers.mlir` 中的分配、复制和释放，说明哪个 use 阻止了无条件复用。不要以“出现了 memcpy”判断优化好坏；先问它在当前存活关系下是否必要。

拓展实验删去旧值读取，再比较复制行为；它改变了可观察需求，因此也改变了合法优化空间。记录两个输入，不把它们当成相同工作负载的直接速度对照。进一步讨论循环中的 tensor 更新、函数边界和 ownership，但这些不属于当前固定例子的覆盖范围。

## 非法 region 结果

`chapters/14-mlir-foundations/test/invalid-yield.mlir` 故意让声明返回 i32 的循环 yield index。预测报错所在 operation，再运行诊断测试。分析这是语法问题、类型不变量还是转换缺少 pattern；这三类错误需要不同修复。

学生提交一个不同的类型/region 反例并断言诊断。测试不能只接受任意非零退出码，因为工具缺失和进程崩溃也会失败。现有测试检查 `error:` 与 `scf.yield`，但还不是完整诊断位置测试。

## 从实验到研究

L5 要求理解这些现成转换。研究项目则必须实现一个明确的增量，例如为 operation 编写 verifier 与 conversion，或用两个合法 schedule 比较复制量与运行代价。自定义 dialect 与 Transform 工程尚未提供课程参考实现，不应把这三组测试称为第 14–18 章全部完成。

方法依据是 [Toy 第 5 章](https://mlir.llvm.org/docs/Tutorials/Toy/Ch-5/)、[第 6 章](https://mlir.llvm.org/docs/Tutorials/Toy/Ch-6/)与 [Bufferization 文档](https://mlir.llvm.org/docs/Bufferization/)。本地 LLVM/MLIR 22.1.8、WSL Ubuntu 24.04 实测三组均通过；原始报告在 `build-validation/mlir-results.xml`。GPU、Transform 和自定义 dialect 不在此结果范围内。
