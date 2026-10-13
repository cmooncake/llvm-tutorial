# 第 09 章：数据布局与调用约定

[简体中文](README.md) | [English](README.en.md)

> 预计用时：7–10 小时。本章处理“源语言的值如何存在机器内存中”。

前几章的整数和布尔值几乎不需要讨论物理布局。数组、字符串和跨语言调用会迫使编译器回答大小、对齐、字段偏移、地址空间、参数传递和符号命名等问题。这些决定共同构成 ABI 边界。

## 9.1 DataLayout

Module 的 DataLayout 来自目标机器，不应手写复制。使用 `DataLayout` 查询类型存储大小、ABI 对齐和 struct layout；不要用宿主 C++ 的 `sizeof` 推断目标布局，因为编译器可能交叉编译。

前端 Type 与 LLVM Type 仍然分离。类型 lowering 负责表示选择，DataLayout 负责回答该 LLVM 表示在目标上的布局。

## 9.2 GEP 与内存访问

`getelementptr` 只计算地址，不读取内存。第一个类型操作数描述被索引对象的布局，后续索引沿聚合层次计算偏移。opaque pointer 不携带 pointee type，这使正确的 GEP 类型参数更加重要。

只有在能够证明结果位于同一分配对象允许范围内时才使用 `inbounds`。它是优化器可依赖的语义承诺，不是性能提示。

## 9.3 Runtime ABI

在独立文档中冻结 runtime 表面：导出符号、C calling convention、整数宽度、布尔表示、数组/字符串结构、所有权、错误行为和平台可见性。用 C ABI 作为第一版边界可减少 C++ name mangling 与异常 ABI 复杂度。

对每个 runtime 函数同时维护 C 头文件和 LLVM declaration 测试。链接成功不证明签名正确；参数宽度或返回约定不一致可能只在特定平台失败。

## 实验 9：数组、字符串与 Runtime

实现固定长度数组的布局、索引和边界检查，再实现只读字符串 slice `{ptr, length}`。生成目标相关 DataLayout，使用 GEP 访问元素，并通过 runtime 提供打印与 trap。

编写 ABI conformance harness：由 C 调用生成函数，再由生成代码调用 C runtime。测试空数组、零长度字符串、首尾元素、越界、嵌套调用和 32/64 位指针假设。

## 提交要求

- 类型 lowering 与布局查询层；
- 版本化 runtime ABI 文档和 C 头文件；
- 聚合访问、边界检查和 trap；
- 双向 ABI conformance tests；
- 对所有 `inbounds` 使用的证明说明。

## 参考资料

- [LLVM Language Reference](https://llvm.org/docs/LangRef.html)
- [The Often Misunderstood GEP Instruction](https://llvm.org/docs/GetElementPtr.html)

