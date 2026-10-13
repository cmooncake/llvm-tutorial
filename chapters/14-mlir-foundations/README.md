# 第 14 章：MLIR 基础

[简体中文](README.md) | [English](README.en.md)

> 预计用时：6–8 小时。先修：LLVM IR、SSA、Pass 与 MiniLang codegen。

LLVM IR 适合低层优化和代码生成，但源语言或领域语义一旦降成指针与循环，通常难以恢复。MLIR 允许编译器在同一基础设施中保留多个抽象层，并用显式转换逐步降低。

## 14.1 统一 IR 结构

MLIR 的核心是 operation。Operation 可以有 operands、results、attributes、regions 和 successors；region 包含 blocks，block 包含 operations 并可有 block arguments。函数、循环乃至一个完整 module 都以 operation 表示。

SSA 仍然存在，但 region 的嵌套使作用域和结构化控制流比 LLVM IR 更直接。Dialect 为一组 operations、types、attributes 和 interfaces 提供命名空间与语义。

MLIR 的 LLVM dialect 是 MLIR 中表达 LLVM 风格语义的 dialect，并不等同于最终 `llvm::Module`。还需要 translation 才得到 LLVM IR。

## 14.2 文本、验证与 Pass

使用 `mlir-opt` 解析、验证、运行 pass pipeline 和打印每一层 IR。先用 generic form 观察 operation 的完整结构，再阅读 custom assembly form。所有 pass 边界开启验证，并学习用 `-mlir-print-ir-before/after` 定位转换失败。

## 实验 14：观察多层 IR

阅读包含 `func`、`arith` 与 `scf` 的小程序，标注每个 operation、region、block argument 和 SSA use。运行 canonicalize、CSE 和结构化控制流转换，记录每层保留与丢失的信息。

将一个错误类型、错误 terminator 和错误 region 结构分别交给 verifier，解释诊断对应的 dialect invariant。

## 提交要求

- 注释过的 MLIR 样例；
- 可复现 pass pipeline；
- 三个 verifier 失败案例；
- LLVM IR、LLVM dialect 与高层 dialect 的对比说明。

## 参考资料

- [MLIR Language Reference and Tutorials](https://mlir.llvm.org/docs/)
- [MLIR Toy Tutorial](https://mlir.llvm.org/docs/Tutorials/Toy/)

