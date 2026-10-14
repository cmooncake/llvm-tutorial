# MiniLang Scalar Teaching Contract

[简体中文](language-profile.md) | [English](language-profile.en.md)

The common graduate acceptance profile is MiniLang Scalar 1.0. This contract takes precedence over unresolved array/string requirements in the older comprehensive specification. Aggregate types require a separately approved extension. Teams can therefore compare optimizations and backends on shared scalar semantics without implementing an expanding language simultaneously.

## Syntax and values

Use the [language specification](language-spec.en.md) for functions, parameters, declarations, blocks, expressions, `if`, `while`, and `return`, but restrict `type` to `i32 | bool | unit`. Arrays, indexing, and strings are excluded. `unit` is a function result or the type of a valueless expression, never a parameter, local binding type, or stored value. Functions are not first-class; a call target must be a top-level function name not shadowed by a local binding.

Addition, subtraction, multiplication, and unary negation operate modulo 2³², interpreted as signed i32. Ordinary decimal literals range from 0 through 2147483647. The only additional form is directly written `-2147483648`; do not first convert its positive magnitude to a signed host integer. Reject `2147483648`, larger literals, and leading-zero forms such as `01`. Keep magnitude/text in tokens and validate when constructing unary expressions, rather than depending on host overflow.

Division truncates toward zero; a remainder has the dividend's sign. Define `INT_MIN / -1` as `INT_MIN` and `INT_MIN % -1` as zero. Handle this pair before emitting LLVM `sdiv/srem`, rather than generating an undefined operation. A zero divisor produces T1. Ordering is signed; logical operators accept only bool.

## Scope and control flow

Parameters and the outer function block share one scope. Duplicate parameters and locals repeating parameter names produce E2002. Nested blocks may shadow; check an initializer in the old environment before adding its binding. `let` and parameters are immutable; `var` is assignable. Top-level and built-in functions cannot be redefined. Locals may shadow function names but those local values cannot then be called.

Assignment expressions have type unit. Evaluate arguments and binary operands left to right; preserve short circuit for `&&`, `||`, and `if`. Conditions require bool; while has type unit.

Track reachability separately from expression type. A final expression without a semicolon supplies the result on normal function exit. Explicit return has no edge to subsequent statements. A non-fallthrough if branch contributes no merge value; if both branches fall through, their types must match. Without else, a normally completing then branch must yield unit.

Every reachable normal exit from a non-unit function supplies a result. Conservatively assume a while may execute zero times; infinite-loop proofs are not required. Continue name/type checking unreachable statements, but do not generate artificial merge edges. The core has no break, continue, exceptions, or implicit conversion.

## Output and runtime interface

| Source call | Observable behavior | LLVM/C boundary |
|---|---|---|
| `print_i32(i32) -> unit` | Signed decimal integer followed by LF | `void ml_print_i32(int32_t)` |
| `print_bool(bool) -> unit` | `true` or `false` followed by LF | `void ml_print_bool(int32_t)` with 0/1 only |
| `trap(i32) -> unit` | stderr `trap N` plus LF; immediate exit 70 | Non-returning `void ml_trap(int32_t)` |

Division/remainder by zero calls `ml_trap(1)`. Do not implement language traps by relying on SIGFPE, SIGILL, or platform signal numbers. Use i1 internally and zero-extend to i32 at the runtime boundary. Unit results use LLVM void. Obtain layout from target configuration, not a copied example. A small C runtime may be shared; source calls still undergo type checking.

Entry is parameterless `fn main() -> i32`. Process exit status is the low 8 bits of its result. Compare arbitrary i32 values through `print_i32`, not exit status. Optimization preserves stdout, stderr, normal termination, and traps.

## CLI and diagnostics

Required commands are `minilang check file.ml`, `minilang emit-ir file.ml -o file.ll`, and `minilang run file.ml`. Run may use external lli, but the report must not call this a custom ORC JIT. AOT build or embedded ORC is a project extension. Successful checking/emission exits 0, source errors 1, CLI misuse 2, language traps 70. Failed emission must not leave a new output that appears successful.

Diagnostics use `path:line:column: error Edddd: message`. Locations count UTF-8 bytes from one; spans are half-open source-byte intervals. CRLF is one newline; a tab is one byte column, not expanded display width. Tests match code/location, not translated message wording. The first error is stable; recovery cannot loop without consuming input.

Retain E0001/E1001/E2001–E2003/E3001–E3004. Add E0002 for invalid integer magnitude/form, E3005 for calling a non-function, and E4001 for a missing or incorrectly typed main. Check/emit-ir permit library sources without main; run/build require it. Diagnose core semantic errors before backend generation.

Public location assertions use these anchors: E0001 at the illegal character, E2001 at the first byte of the undefined identifier, E2003 at the assignment's left-hand identifier, and E3004 at the condition expression's first byte. Other diagnostics still need valid source locations, but the public driver does not fix their exact columns. Publish anchor rules before adding hidden location tests.

## Authority and changes

These are language-design decisions, not LLVM defaults. [LLVM 22.1 LangRef](https://releases.llvm.org/22.1.0/docs/LangRef.html) governs emitted IR, especially division, poison, and overflow flags. Freeze this contract in week 6. Later errata require executable examples and synchronized translations, tests, and grading notes. Hidden tests cannot introduce syntax.
