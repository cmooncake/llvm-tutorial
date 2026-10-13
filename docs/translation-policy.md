# 中英文版本维护规范

[简体中文](translation-policy.md) | [English](translation-policy.en.md)

## 文件命名

- 中文：`README.md` 或 `name.md`
- 英文：`README.en.md` 或 `name.en.md`
- 每对文档顶部提供语言切换链接
- 代码、测试、fixture 和命令不复制，两个语言版本引用同一份文件

## 同步原则

中文目前是规范版本。章节结构稳定后再翻译英文，英文版必须保持相同的章节编号、实验编号、规范条款和链接目标。翻译不是逐字替换，应当保持原有教学推理、例子和语气。

改变语言语义、ABI、作业要求、测试行为或评分标准时，中英文必须在同一提交中更新。只改错别字或改善某一种语言表达时，可以单独提交，但不得改变技术含义。

## 术语表

| 中文 | English | 说明 |
|---|---|---|
| 中间表示 | intermediate representation (IR) | 首次出现给出英文缩写 |
| 基本块 | basic block | 不译为 code block |
| 静态单赋值形式 | static single assignment form (SSA) | 首次出现展开 |
| 支配关系 | dominance | 动词使用 dominate |
| 终结指令 | terminator | 不译为 final instruction |
| 词法分析 | lexical analysis | lexer 指实现组件 |
| 语法分析 | parsing / syntax analysis | parser 指实现组件 |
| 静态语义 | static semantics | 包含名字解析与类型检查 |
| 调用约定 | calling convention | 与 ABI 区分 |
| 提前编译 | ahead-of-time compilation (AOT) | 首次出现展开 |
| 逐层 Lowering | progressive lowering | 保留 lowering 作为领域术语 |

LLVM 与 MLIR 类名、指令名、命令行选项和 dialect 名称保留官方拼写。

## 翻译完成条件

一份英文讲义只有满足以下条件才标记为完成：

1. 内容与中文规范版本同一修订；
2. 所有本地链接有效；
3. 代码和命令与中文版本引用同一文件；
4. 术语符合本规范；
5. 由另一位编辑进行语言或技术校对；
6. 不含机器逐句翻译造成的生硬表达。

