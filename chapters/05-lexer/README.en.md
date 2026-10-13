# Chapter 05: Lexical Analysis

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 5–7 hours. Read the [MiniLang 1.0 lexical rules](../../docs/language-spec.md#1-词法) before starting.

A compiler initially receives a sequence of bytes, while a parser wants symbols such as identifier, integer, and left parenthesis. The lexer sits between these views. It reads source text from left to right, groups characters into tokens, and preserves the source extent of every token.

The important result of this chapter is not a long list of recognized punctuation. It is an input model that will continue to support diagnostics, recovery, and testing throughout the compiler.

## 5.1 Tokens and Lexemes

The source text `let answer = 42;` contains five tokens. The actual text occupied by a token is its lexeme; keyword, identifier, equals, integer, and semicolon are token kinds.

Do not force every property into the token-kind enumeration. A useful token contains at least a kind and source span. MiniLang checks decimal syntax and the `i32` range in the lexer, while retaining the source span so diagnostics can reproduce what the programmer wrote.

```cpp
struct Token {
  TokenKind kind;
  SourceSpan span;
  std::optional<std::int32_t> integerValue;
};
```

## 5.2 Source Locations and Spans

Line and column numbers are convenient for presentation but poor canonical coordinates. Byte offsets are easier to slice, order, and combine. Represent a location as a file identifier plus byte offset, and a span as the half-open interval `[begin, end)`. The SourceManager computes display lines and columns when needed.

UTF-8 distinguishes byte offsets, Unicode code points, and display columns. MiniLang 1.0 restricts identifiers to ASCII, but comments and diagnostic context may still contain UTF-8. The core implementation stores byte offsets and documents its display-column policy.

## 5.3 Longest Match and Lookahead

`<` and `<=` share a prefix. The lexer should prefer the longest legal token, commonly called maximal munch. A small interface with `peek()` and `advance()` makes this rule explicit.

Scan the complete identifier pattern before consulting the keyword table. Returning `if` as soon as those two characters appear would incorrectly split `ifdef`.

## 5.4 Whitespace, Comments, and End of File

Whitespace and `//` comments do not reach the parser, but they still update source positions. End of file is represented by a stable EOF token; repeated requests at EOF must not read past the buffer.

An invalid character must not cause an infinite loop. After reporting `E0001`, consume at least one input unit before resuming. A single compilation can then report several independent lexical errors.

## Laboratory 5: The MiniLang Lexer

Implement `Lexer::next()` for keywords, identifiers, decimal `i32` values, operators, punctuation, whitespace, line comments, EOF, invalid characters, integer overflow, and half-open source spans.

Tests must inspect more than token kinds. Cover lexeme slices, multiline locations, a comment at EOF, `<` versus `<=`, identifiers with keyword prefixes, oversized integers, consecutive invalid characters, and an empty file.

### Observation

Print tokens, offsets, lines, and columns for:

```text
let café = 1;
```

MiniLang 1.0 does not permit `é` in an identifier. Explain which UTF-8 bytes the diagnostic covers and where scanning resumes. Different user-interface policies are possible, but the internal rule must be consistent and tested.

## Design Review

Does the lexer own the source buffer? Does a token copy its lexeme or refer back to the SourceManager? Does a token remain valid after the source buffer is destroyed? These choices determine both lookup cost and object lifetime in the parser.

## Submission

- lexer, token, and SourceLocation/SourceSpan implementations;
- positive, negative, and boundary tests;
- a token-dump tool or compiler option; and
- a one-page note documenting UTF-8, integer-range, and recovery policies.

## Summary

Lexical analysis turns an unstructured character stream into a located token stream. The parser in the next chapter operates on tokens rather than characters. Source ranges will survive through every later compiler phase, so they must be designed now rather than retrofitted after parsing.

## References

- [LLVM Kaleidoscope: The Lexer](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)
- [Stanford CS143: Lexical Analysis](https://web.stanford.edu/class/cs143/)

