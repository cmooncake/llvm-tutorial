# Chapter 06: Parsing and Abstract Syntax Trees

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 7–10 hours. Prerequisites: Chapter 05 and the MiniLang EBNF.

The lexer identifies tokens but does not explain how they form a program. The parser recognizes that structure and constructs an abstract syntax tree (AST) that retains semantically relevant information. Parentheses and semicolons guide parsing, but need not become AST nodes themselves.

## 6.1 Recursive Descent

MiniLang functions, blocks, declarations, and statements map naturally to recursive-descent functions such as `parseFunction`, `parseBlock`, and `parseStatement`.

Use one contract consistently: on success, a parser function consumes exactly the tokens belonging to its construct and returns a node; on failure, it emits a diagnostic and advances to a documented recovery point. Inconsistent consumption rules lead to duplicate diagnostics and infinite loops.

## 6.2 Expressions and Precedence

Left-recursive expression grammars cannot be transcribed directly into recursive descent. This course uses Pratt parsing. Prefix parselets handle literals, names, unary operators, and grouping; infix parselets use binding powers for binary operators, calls, and indexing.

`1 + 2 * 3` must produce `+(1, *(2, 3))`, while assignment in `a = b = 1` is right associative. Keep precedence in one language-level table and test it directly.

## 6.3 Responsibilities of the AST

The AST models the source language, not LLVM. Nodes carry source spans, node-specific fields, and ownership of children. They do not store `llvm::Value*` or `llvm::Type*`.

Separate declarations, statements, expressions, and type syntax. Written type syntax and a resolved semantic type are different objects: one records what the programmer wrote; the other records its meaning after resolution and inference.

Provide a deterministic AST dump. It is an observable parser interface rather than a pretty-printer; stable field order and indentation make structural tests useful.

## 6.4 Error Recovery

Stopping at the first missing semicolon hides independent errors. Continuing without a boundary creates cascades. Statement-level recovery can synchronize at `;`, `}`, or a declaration starter. Record the current token before recovery and ensure that recovery makes progress.

Parser diagnostics identify the actual token, an expected set, and a source span. Undefined names and type mismatches belong to static semantics, not parsing.

## Laboratory 6: MiniLang Parser and AST Dump

Implement the parser in three increments: functions and basic statements; Pratt expressions including calls and indexing; then control flow, block expressions, and statement-level recovery.

For each increment, write expected AST dumps before implementing the parser. Cover precedence, associativity, nested blocks, empty parameter lists, trailing expressions, missing delimiters, and two independent syntax errors in one file.

### Required Explanation

Compare:

```text
if a { b } else { c }
if a { b; } else { c; }
```

Explain why MiniLang's block-value rule eventually assigns different type information. The parser does not type-check, but the AST must preserve the distinction between a trailing expression and an expression statement.

## Submission

- AST nodes, ownership policy, and deterministic dump;
- recursive-descent and Pratt parsers;
- error recovery and negative tests;
- a precedence and associativity table; and
- the token-consumption contract for success and failure.

## Summary

Parsing recovers nested language structure from a linear token stream. A sound AST describes MiniLang instead of prematurely imitating LLVM IR. The next chapter builds scopes, resolves names, and checks types over this tree.

## References

- [LLVM Kaleidoscope: Parser and AST](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl02.html)
- [Stanford CS143: Parsing](https://web.stanford.edu/class/cs143/)

