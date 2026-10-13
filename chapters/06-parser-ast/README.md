# 第 06 章：语法分析与抽象语法树

[简体中文](README.md) | [English](README.en.md)

> 预计用时：7–10 小时。先修：第 05 章与 MiniLang EBNF。

lexer 告诉我们输入中出现了哪些 token，却不说明它们怎样组成程序。Parser 的工作是识别结构，并构造只保留语义相关信息的抽象语法树（AST）。括号、分号等 token 可能帮助识别结构，但不一定需要成为 AST 节点。

## 6.1 从递归下降开始

MiniLang 的函数、块、声明和语句可以直接按语法规则写成递归下降函数。函数名应表达它解析的非终结符，例如 `parseFunction`、`parseBlock` 和 `parseStatement`。

每个函数都遵守相同契约：成功时消费恰好属于该结构的 token 并返回节点；失败时报告诊断，并把 token 流推进到约定的恢复点。若有些函数失败后消费 token、有些不消费，调用者很快会陷入重复诊断或死循环。

## 6.2 表达式与优先级

表达式左递归不适合直接写成递归下降。课程采用 Pratt parser：prefix parselet 处理字面量、名字、一元运算和括号；infix parselet 根据 binding power 处理二元运算、调用与索引。

`1 + 2 * 3` 必须形成 `+(1, *(2, 3))`，而 `a = b = 1` 的赋值是右结合。优先级表属于语言规范的一部分，应集中定义并直接测试，不要散落在多个 `switch` 中。

## 6.3 AST 的职责

AST 表达源语言结构，不表达 LLVM 实现。节点包含源码 span、节点特有字段和对子节点的所有权；它们不应保存 `llvm::Value*` 或 `llvm::Type*`。

建议区分 declaration、statement、expression 与 type syntax。语法中的类型写法和语义分析后的类型不是同一个对象：前者保留用户写了什么，后者表示解析、别名展开或推导后的含义。

为 AST 提供确定性的 dump。它不是漂亮打印器，而是 parser 的第一种可观察输出；字段顺序和缩进稳定后，测试可以检查结构而不过度依赖内存地址。

## 6.4 错误恢复

遇到缺失的 `;` 时立即终止整个编译器，会让后续错误被遮蔽；无边界地继续解析又容易产生大量级联诊断。语句级恢复可以跳到 `;`、`}` 或新的声明起点。恢复前记录当前 token 位置，恢复后必须确认输入已经前进。

诊断应指出实际 token、期望集合和相关源码范围。Parser 不负责判断名字是否定义或类型是否匹配，那些属于下一章的静态语义。

## 实验 6：MiniLang Parser 与 AST Dump

分三步实现：

1. 函数、参数、块、声明和 return；
2. Pratt 表达式，包括调用、索引、一元与二元运算；
3. `if`、`while`、块表达式和语句级恢复。

每一步都先写 AST dump 的预期结构，再实现 parser。至少测试优先级、结合性、嵌套块、空参数列表、尾表达式、缺失分隔符和一次输入中的两个独立语法错误。

### 必须解释的案例

比较：

```text
if a { b } else { c }
if a { b; } else { c; }
```

根据 MiniLang 的块值规则，解释两个表达式的类型信息为何最终不同。Parser 此时不做类型检查，但 AST 必须保留尾表达式与表达式语句的区别。

## 提交要求

- AST 节点、所有权策略与稳定 dump；
- 递归下降和 Pratt parser；
- 错误恢复及负向测试；
- 一张优先级/结合性表；
- 说明 parser 成功与失败时的 token 消费契约。

## 小结

Parser 把 token 的线性序列恢复为嵌套语言结构。一个合格 AST 应忠实表达 MiniLang，而不是提前变成 LLVM IR 的影子。下一章将在 AST 上建立作用域、解析名字并检查类型。

## 参考资料

- [LLVM Kaleidoscope: Parser and AST](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl02.html)
- [Stanford CS143: Parsing](https://web.stanford.edu/class/cs143/)

