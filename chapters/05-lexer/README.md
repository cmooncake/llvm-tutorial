# 第 05 章：词法分析

[简体中文](README.md) | [English](README.en.md)

> 预计用时：5–7 小时。阅读前请先熟悉 [MiniLang 1.0 词法规则](../../docs/language-spec.md#1-词法)。

编译器首先接收的是字节序列，而 parser 希望看到的是诸如“标识符”“整数”“左括号”这样的符号。词法分析器位于两者之间：它从左到右读取源码，把字符组织成 token，同时保留每个 token 在源文件中的位置。

本章的重点不是识别几十种符号，而是建立一个以后不会妨碍诊断、错误恢复和测试的输入模型。

## 5.1 Token 与词素

在源码 `let answer = 42;` 中，`let`、`answer`、`=`、`42` 和 `;` 是五个 token。源码里实际出现的字符片段称为词素（lexeme）；“关键字”“标识符”“等号”“整数”“分号”是 token kind。

不要把所有信息都塞进枚举。一个实用的 token 至少包含 kind 和源码范围；整数的数值可以在 lexer 中解析，也可以保留词素交给后续阶段。MiniLang 选择在 lexer 中检查十进制格式和 `i32` 范围，但仍保存原始范围，以便诊断引用用户写下的文本。

```cpp
struct Token {
  TokenKind kind;
  SourceSpan span;
  std::optional<std::int32_t> integerValue;
};
```

## 5.2 SourceLocation 与 SourceSpan

行号和列号适合展示，却不适合作为内部唯一位置。文件偏移更适合切片、排序和组合范围。建议把位置表示为 `file-id + byte-offset`，把 span 表示为半开区间 `[begin, end)`；需要显示时再由 SourceManager 计算行列。

UTF-8 会让“字节偏移”“Unicode code point”和“屏幕列”出现差异。MiniLang 1.0 只允许 ASCII 标识符，但注释和诊断上下文仍可能包含 UTF-8。课程基础实现以字节偏移存储位置，展示列时明确说明采用的计数策略，不假装一个 byte 永远等于一个可见字符。

## 5.3 最长匹配与查看下一个字符

`<` 与 `<=` 共享前缀。lexer 应先判断是否能组成更长的合法 token，这通常称为 maximal munch。实现时需要 `peek()` 查看但不消费下一个字符，以及 `advance()` 消费当前字符并更新位置。

对标识符先扫描完整 `[A-Za-z_][A-Za-z0-9_]*`，再查关键字表。不要在看到 `if` 的两个字符后立即返回关键字，否则 `ifdef` 会被错误拆分。

## 5.4 空白、注释与文件结束

空白和 `//` 注释不进入 parser，但 lexer 必须正确更新位置。文件结束应当产生一个稳定的 EOF token；重复请求 EOF 不应越界或改变结果。

非法字符不能导致无限循环。报告 `E0001` 后，lexer 至少消费一个输入单位，再继续扫描。这样一次编译可以报告多个互不依赖的词法错误。

## 实验 5：MiniLang Lexer

实现 `Lexer::next()`，覆盖：

- 关键字、标识符和十进制 `i32`；
- 单字符和双字符运算符；
- 标点、空白和行注释；
- EOF、非法字符与整数越界；
- 每个 token 的半开源码范围。

测试不要只比较 kind 序列。至少检查一次词素切片、跨行位置、文件末尾注释、`<`/`<=`、关键字前缀标识符、超大整数、连续非法字符和空文件。

### 观察任务

为下面输入打印 token、offset、line 和 column：

```text
let café = 1;
```

根据 MiniLang 1.0，`é` 不属于合法标识符。解释诊断范围覆盖哪些 UTF-8 字节，以及下一枚 token 从哪里开始。这里没有唯一的用户界面答案，但内部位置规则必须一致并由测试固定。

## 设计检查

完成实现后回答：lexer 是否拥有源码缓冲区？token 的词素是复制字符串还是引用 SourceManager？如果源文件生命周期结束，token 是否仍安全？这些问题决定后续 parser 能否低成本查看文本，也决定对象生命周期是否清晰。

## 提交要求

- lexer、token、SourceLocation/SourceSpan 的实现；
- 正例、负例和边界测试；
- token dump 工具或编译器选项；
- 一页设计说明，记录 UTF-8、整数范围和错误恢复策略。

## 小结

词法分析把无结构字符流转换成带位置的 token 流。下一章的 parser 不再关心字符细节，而是根据 token 的排列构造抽象语法树。源码范围会贯穿整个编译器，因此本章的位置模型不能在 parser 开始后再临时补上。

## 参考资料

- [LLVM Kaleidoscope: The Lexer](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)
- [Stanford CS143: Lexical Analysis](https://web.stanford.edu/class/cs143/)

