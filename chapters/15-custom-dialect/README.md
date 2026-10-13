# 第 15 章：MLIR Dialect 定义

[简体中文](README.md) | [English](README.en.md)

> 预计用时：8–12 小时。本章为 MiniLang 定义一层保留源语言语义的 IR。

## 15.1 选择语义边界

不要为每个 AST 节点机械创建 operation。Dialect 应保留后续变换真正需要的语义，例如 MiniLang 函数、带静态长度的数组操作和可检查的 trap 行为；已经由通用 dialect 准确表达的整数算术可以直接复用 `arith`。

## 15.2 ODS、Verifier 与 Interfaces

使用 ODS/TableGen 定义 operation 名称、operands、results、attributes、regions 和 traits。声明式约束处理局部形状，C++ verifier 处理跨字段不变量。错误必须发在最相关 operation 上。

Traits 表达可复用性质，interfaces 表达跨 operation 的行为契约。Canonicalization 只做语义等价且趋向规范形的改写，测试其幂等性和不得改写案例。

## 实验 15：Mini Dialect

定义最小 `mini` dialect，包括函数/返回、数组长度或 bounds-check operation，以及至少一个保留 MiniLang 特有语义的 operation。实现 parser/printer、verifier、canonicalization 和 round-trip tests。

用非法文本直接构造 verifier 测试，避免只有 C++ builder 能生成 IR 而错误形状从未被检查。

## 提交要求

- ODS 定义与生成规则；
- dialect 注册、parser/printer 与 verifier；
- canonicalization 正负测试；
- dialect reference，说明每个 operation 的语义而非只列语法。

## 参考资料

- [Creating a Dialect](https://mlir.llvm.org/docs/Tutorials/CreatingADialect/)
- [MLIR Operation Definition Specification](https://mlir.llvm.org/docs/DefiningDialects/Operations/)

