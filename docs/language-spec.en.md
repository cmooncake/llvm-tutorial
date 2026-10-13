# MiniLang 1.0 Language Specification

[简体中文](language-spec.md) | [English](language-spec.en.md)

This document is normative for the core course. Implementations may add extensions but must not silently alter the behavior defined here.

## 1. Lexical Structure

Source files are UTF-8. Version 1.0 permits only ASCII letters in identifiers:

```text
identifier := [A-Za-z_][A-Za-z0-9_]*
integer    := 0 | [1-9][0-9]*
comment    := // through end of line
```

Keywords are `fn let var if else while return true false i32 bool unit`. Whitespace separates tokens and has no other meaning. Every token carries a half-open source span `[begin, end)`.

## 2. Grammar

```text
program       := function* EOF ;
function      := "fn" IDENT "(" parameters? ")" ("->" type)? block ;
parameters    := parameter ("," parameter)* ;
parameter     := IDENT ":" type ;
type          := "i32" | "bool" | "unit" | "[" type ";" INTEGER "]" ;

block         := "{" statement* expression? "}" ;
statement     := let-decl | var-decl | while-stmt | return-stmt | expr-stmt ;
let-decl      := "let" IDENT (":" type)? "=" expression ";" ;
var-decl      := "var" IDENT (":" type)? "=" expression ";" ;
while-stmt    := "while" expression block ;
return-stmt   := "return" expression? ";" ;
expr-stmt     := expression ";" ;

expression    := assignment ;
assignment    := IDENT "=" assignment | logical-or ;
logical-or    := logical-and ("||" logical-and)* ;
logical-and   := equality ("&&" equality)* ;
equality      := comparison (("==" | "!=") comparison)* ;
comparison    := term (("<" | "<=" | ">" | ">=") term)* ;
term          := factor (("+" | "-") factor)* ;
factor        := unary (("*" | "/" | "%") unary)* ;
unary         := ("!" | "-") unary | call ;
call          := primary ("(" arguments? ")" | "[" expression "]")* ;
arguments     := expression ("," expression)* ;
primary       := INTEGER | "true" | "false" | IDENT
               | "(" expression ")" | if-expr | block ;
if-expr       := "if" expression block ("else" (if-expr | block))? ;
```

An omitted function return type is `unit`. The final expression without a semicolon is the value of a block; a block without a trailing expression has value `unit`.

## 3. Names and Scope

- Top-level functions share one global namespace and may call functions declared later in the file.
- Parameters and local bindings have lexical block scope.
- An inner scope may shadow an outer name.
- Repeating a definition in the same scope is an error.
- A new binding enters scope after its initializer has been checked.
- Assignment requires a mutable `var`; `let`, parameters, and functions are not assignable.

## 4. Typing Rules

- Version 1.0 performs no implicit numeric conversions.
- Arithmetic consumes and produces `i32`.
- Ordering comparisons consume two `i32` values and produce `bool`.
- Equality and inequality require equal types and support `i32` and `bool` in version 1.0.
- `!`, `&&`, and `||` require `bool`.
- `if` and `while` conditions are `bool`.
- The branches of an `if` with `else` have the same type.
- An `if` without `else` has type `unit`, and its then block must also have type `unit`.
- Every reachable return path satisfies the declared function result type.
- `unit` is not an arithmetic, comparison, or array-element type.

An omitted binding annotation is inferred from its initializer. The course does not require global Hindley–Milner inference.

## 5. Evaluation Semantics

- Function arguments and binary operands evaluate left to right.
- `&&` and `||` short-circuit.
- An `if` evaluates only the selected branch.
- A `while` evaluates its condition before each iteration.
- `i32` arithmetic has two's-complement wrapping behavior.
- Division by zero, remainder by zero, and array bounds violations invoke a runtime trap.
- `return` immediately exits the current function.

Code generation must preserve these rules. In particular, wrapping source arithmetic does not justify LLVM `nsw` flags.

## 6. Arrays

- `[T; N]` is a fixed-length value type; `N` is a nonnegative compile-time integer.
- Version 1.0 has no core array-literal syntax; standard or runtime helpers construct arrays.
- Array indices have type `i32`.
- Every index is bounds-checked unless an optimization proves safety.
- Array assignment has value semantics; internal memory representation must not expose aliasing differences.

## 7. Program Entry and Exit

An executable program defines:

```text
fn main() -> i32 { ... }
```

Its result becomes the process exit status. JIT tests call the same signature.

## 8. Core Runtime Surface

```text
print_i32(value: i32) -> unit
print_bool(value: bool) -> unit
trap(code: i32) -> unit
```

The C ABI names, boolean representation, string representation, and calling conventions are frozen separately during the back-end unit.

## 9. Required Diagnostics

- `E0001` invalid character
- `E1001` syntax error
- `E2001` undefined name
- `E2002` duplicate definition in one scope
- `E2003` assignment to an immutable binding
- `E3001` type mismatch
- `E3002` incorrect argument count
- `E3003` missing return
- `E3004` non-boolean condition

Tests assert diagnostic code, source span, and important structured arguments rather than complete natural-language wording.

## 10. Example

```text
fn sum_to(n: i32) -> i32 {
  var i = 0;
  var sum = 0;
  while i < n {
    sum = sum + i;
    i = i + 1;
  }
  return sum;
}

fn main() -> i32 {
  let answer = sum_to(10);
  print_i32(answer);
  return 0;
}
```

