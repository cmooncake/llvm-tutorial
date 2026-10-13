# 第 17 章：张量、向量化与异构代码生成

[简体中文](README.md) | [English](README.en.md)

> 预计用时：8–12 小时。GPU 硬件不是基础验收条件。

本章研究一个计算如何从数学张量逐步变成具体内存和硬件操作。过早 bufferize 会失去适合 fusion/tiling 的值语义；过晚则无法表达分配、别名和数据移动。

## 17.1 Tensor、Linalg 与 Vector

Tensor 是 SSA 值，不表示可原地修改的内存。Linalg 以 structured operation 表达迭代空间、索引映射和 reduction。Vector dialect 表达可重定向的多维向量操作，随后再 lower 到目标相关指令。

## 17.2 Bufferization

Bufferization 把 tensor semantics 转换为 memref/buffer semantics。One-Shot Bufferize 利用 destination-passing style 决定复用或分配 buffer；目标是减少分配与复制，同时不覆盖仍然活跃的数据。

学生必须记录 alias/ownership 假设。内存泄漏、重复释放和隐藏复制都属于正确性或性能问题。

## 17.3 GPU 边界

GPU dialect 表达 kernel、launch、thread/block id 和 address space，再 lower 到 NVVM/ROCDL 等目标。区分 host 与 device module、数据移动与 kernel 执行。基础实验只检查 IR 与 CPU reference；有硬件时再执行 GPU 路径。

## 实验 17：MiniTensor Matmul

为 elementwise、reduction 和 matmul 建立 `Linalg/Tensor → tiled Linalg → Vector → Bufferization → LLVM` CPU pipeline。比较至少两组 tile/vector 参数，并用 reference implementation 做数值检查。

加分路径将并行循环映射到 GPU blocks/threads。报告分别计算 kernel 时间与数据传输时间。

## 提交要求

- 可复现 lowering pipeline 与每层 fixture；
- buffer ownership/alias 说明；
- 数值正确性测试；
- 原始性能数据和硬件描述；
- GPU 不可用时仍可完成的 IR 验收。

## 参考资料

- [Linalg Dialect](https://mlir.llvm.org/docs/Dialects/Linalg/)
- [Bufferization](https://mlir.llvm.org/docs/Bufferization/)
- [Vector Dialect](https://mlir.llvm.org/docs/Dialects/Vector/)
- [GPU Dialect](https://mlir.llvm.org/docs/Dialects/GPU/)

