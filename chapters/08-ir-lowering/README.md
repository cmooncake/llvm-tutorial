# 第 08 章：LLVM IR 代码生成

[简体中文](README.md) | [English](README.en.md)

> 预计用时：8–12 小时。输入必须已经通过第 07 章的静态语义检查。

代码生成不是把 AST 节点逐个翻译成“看起来相近”的 LLVM 指令，而是实现一组保持 MiniLang 求值语义的 lowering 规则。每条规则都应说明输入的不变量、产生的 IR 形状和失败方式。

## 8.1 CodeGen Context

一个 codegen session 拥有 `LLVMContext`、`Module`、`IRBuilder`、前端类型到 LLVM 类型的映射，以及当前函数和词法绑定环境。AST 不保存 `llvm::Value*`；Value 只在当前 module/session 的生命周期内有效。

每个函数先创建声明，再生成函数体，以支持递归和前向调用。函数完成后立即运行 `verifyFunction`，module 完成后运行 `verifyModule`。越靠近产生错误的位置验证，诊断越容易定位。

## 8.2 值、地址与绑定

表达式生成“值”，可赋值位置生成“地址”。不要用一个含糊的 `codegen()` 同时表达两者。`let` 可直接绑定 SSA value；`var` 的基础实现可在入口块创建 `alloca`，读写使用 `load/store`，随后由 mem2reg 提升。

入口块 alloca 的插入位置应独立管理，不能跟随当前控制流 block 的 builder 插入点。作用域退出时恢复被遮蔽的绑定。

## 8.3 控制流

`if` 表达式为两个分支建立 block，并在需要产生值时于 merge block 创建 phi。若某分支以 `return` 终结，它不会跳到 merge，也不能作为 phi incoming。

`while` 通常包含 condition、body 和 exit blocks。短路 `&&`/`||` 必须用控制流实现，不能无条件生成右侧表达式再做位运算。

MiniLang 的 `i32` 是回绕整数，因此普通加减乘不添加 `nsw`。除零和数组越界按照语言规范显式检查并调用 runtime trap。

## 实验 8：MiniLang Core CodeGen

按下列顺序实现并在每一步保持测试通过：

1. 常量、参数、算术、比较与函数调用；
2. `let`、`var`、赋值与块作用域；
3. `if`、短路逻辑、`while` 与 `return`；
4. verifier、IR dump 和阶段化错误报告。

测试同时检查行为和少量关键结构。不要全文锁定 IR 临时变量编号。至少验证短路右侧不会执行、已终结 block 不再插入指令、遮蔽退出后恢复外层绑定，以及回绕语义不携带错误 flags。

## 提交要求

- 明确的 value/address codegen 接口；
- 核心 MiniLang lowering；
- 每函数和每 module 验证；
- IR 结构测试与端到端行为测试；
- 一份 lowering rule 表。

## 参考资料

- [LLVM Kaleidoscope: Code Generation to LLVM IR](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl03.html)
- [LLVM Language Reference](https://llvm.org/docs/LangRef.html)

