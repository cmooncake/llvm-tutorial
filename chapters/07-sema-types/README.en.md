# Chapter 07: Static Semantics and Type Checking

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 7–10 hours. Prerequisites: Chapter 06 and the MiniLang typing rules.

Successful parsing proves only that a program has legal syntax. `x + true` forms a valid binary-expression node but violates MiniLang's type rules; `answer()` forms a call node but may refer to no declaration. Static semantics answers questions that syntax alone cannot.

## 7.1 Phase Separation

Keep name resolution and type checking distinct. First collect top-level function signatures so functions can call later declarations. Then resolve parameters and local bindings under lexical scope. Finally check expressions and control flow using resolved references.

Do not use LLVM types as the front-end type system. MiniLang `bool`, `unit`, array value semantics, and the error type belong to the source language and may later have several LLVM or runtime representations.

## 7.2 Scope and Name Resolution

A scope stack gives each block its own declaration map. Lookup proceeds from the innermost scope outward. Duplicate-definition checks inspect the current scope; shadowing occurs across different scopes.

An initializer is checked before its new name enters scope. In `let x = x;`, the right-hand `x` therefore resolves to an outer declaration or produces `E2001`. Distinguish `var`, `let`, parameters, and functions so assignment diagnostics are precise.

After resolution, a name expression refers to a stable declaration or symbol identifier. Code generation must not repeat string-based lookup.

## 7.3 Type Checking

A checking function returns either a semantic type or an error type. The error type suppresses cascades: after `unknown` has produced an undefined-name error, `unknown + true` should not generate several meaningless operator errors.

State local rules for each operator and construct. Addition consumes two `i32` values and produces `i32`; comparison consumes two `i32` values and produces `bool`; an `if` condition is `bool`, and an `if` with `else` has matching branch types.

Return checking considers reachable paths rather than merely counting `return` statements. A conservative definitely-returns analysis is sufficient for the core course: if every path cannot be proven to return, a non-`unit` function receives `E3003`.

## 7.4 Diagnostics as an Interface

Each diagnostic has a stable code, primary span, and structured arguments. Human-readable wording may improve over time; tests primarily assert the code, important arguments, and spans. Type mismatches report both actual and expected types and may use a secondary span for the original declaration.

Semantic analysis must tolerate error nodes created earlier. Recovery is a property of the complete front end, not just the parser.

## Laboratory 7: Resolver and Type Checker

Implement top-level signature collection, lexical scopes, shadowing, undefined-name and mutability checks, every MiniLang 1.0 expression rule, call checking, condition and branch checks, missing-return analysis, and a typed-AST or semantic dump.

Organize tests by diagnostic category. Each category includes a successful case, a direct failure, and a case that demonstrates cascade suppression.

### Design Question

For:

```text
let x = 1;
{
  let x = x + 1;
}
```

explain how each occurrence of `x` resolves. Explain why the point at which a declaration enters scope is a language rule rather than an accidental symbol-table behavior.

## Submission

- front-end Type representation and symbol model;
- resolver, type checker, and return-path analysis;
- typed-AST or semantic dump;
- tests for every required diagnostic code; and
- a concise static-semantics rule summary.

## Summary

Static semantics turns an AST that merely resembles a program into a representation with resolved references and consistent types. Chapter 08 accepts only semantically valid input, so code generation does not have to discover source-language errors while constructing IR.

## References

- [Stanford CS143: Semantic Analysis and Type Checking](https://web.stanford.edu/class/cs143/)
- [MIT 6.035: Semantic Analysis](https://ocw.mit.edu/courses/6-035-computer-language-engineering-spring-2010/pages/lecture-notes/)

