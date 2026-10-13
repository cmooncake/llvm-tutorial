# Chinese–English Maintenance Policy

[简体中文](translation-policy.md) | [English](translation-policy.en.md)

## File Naming

- Chinese: `README.md` or `name.md`
- English: `README.en.md` or `name.en.md`
- Each translated pair provides language-switch links at the top.
- Source code, tests, fixtures, and commands are maintained once and referenced by both versions.

## Synchronization

Chinese is currently the normative version. An English translation is prepared after the chapter structure stabilizes. Both versions retain the same section numbers, laboratory numbers, specification clauses, and link targets. Translation preserves the instructional argument and examples rather than replacing sentences word for word.

Changes to language semantics, the ABI, assignment requirements, observable test behavior, or grading rules must update both languages in one commit. Language-only copy edits may be committed independently but must not change technical meaning.

## Terminology

| Chinese | English |
|---|---|
| 中间表示 | intermediate representation (IR) |
| 基本块 | basic block |
| 静态单赋值形式 | static single assignment form (SSA) |
| 支配关系 | dominance |
| 终结指令 | terminator |
| 词法分析 | lexical analysis |
| 语法分析 | parsing / syntax analysis |
| 静态语义 | static semantics |
| 调用约定 | calling convention |
| 提前编译 | ahead-of-time compilation (AOT) |
| 逐层 Lowering | progressive lowering |

LLVM and MLIR class names, instruction names, command-line options, and dialect names retain their official spelling.

## Definition of Translation Complete

An English note is complete only when it:

1. corresponds to the same revision as the normative Chinese note;
2. has valid local links;
3. references the same code and commands as the Chinese note;
4. follows the terminology policy;
5. has received independent language or technical review; and
6. reads as instructional English rather than a sentence-by-sentence machine translation.

