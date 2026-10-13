# Chapter 08: LLVM IR Code Generation

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 8–12 hours. Input to this phase has passed Chapter 07 static semantics.

Code generation is not a node-by-node substitution of AST syntax with similar-looking LLVM instructions. It implements lowering rules that preserve MiniLang evaluation semantics. Each rule states its input invariants, resulting IR shape, and failure behavior.

## 8.1 Code Generation Context

A session owns an `LLVMContext`, `Module`, `IRBuilder`, source-to-LLVM type mapping, current function, and lexical binding environment. AST nodes do not retain `llvm::Value*`; values are valid only within their module and context lifetime.

Create all function declarations before bodies to support recursion and forward calls. Run `verifyFunction` after each body and `verifyModule` after the module. Verification close to construction localizes failures.

## 8.2 Values, Addresses, and Bindings

Expressions produce values; assignable places produce addresses. Use distinct interfaces. An immutable `let` may bind an SSA value. A basic `var` implementation creates entry-block allocas and uses loads and stores, allowing mem2reg to promote them later.

Manage entry allocas independently of the builder's current control-flow insertion point. Restore shadowed bindings when leaving scope.

## 8.3 Control Flow

An `if` creates branch blocks and, when it yields a value, a phi in the merge block. A branch terminated by `return` neither jumps to the merge nor contributes a phi incoming edge.

A `while` normally has condition, body, and exit blocks. Short-circuit operators use control flow; generating the right operand unconditionally is incorrect.

MiniLang `i32` arithmetic wraps, so ordinary operations do not receive unjustified `nsw`. Division by zero and bounds failures are explicit checks that invoke the runtime trap.

## Laboratory 8: MiniLang Core Code Generation

Implement constants, parameters, arithmetic, comparisons, and calls; then bindings and assignment; then control flow and return; finally verifier integration and IR dumping. Keep the suite passing after every increment.

Tests combine behavior with selected structural checks. Do not snapshot entire IR with unstable temporary names. Verify short-circuit side effects, terminated blocks, scope restoration, and the absence of incorrect overflow flags.

## Submission

- explicit value/address generation interfaces;
- core MiniLang lowering;
- per-function and per-module verification;
- structural IR and end-to-end behavior tests; and
- a table of lowering rules.

## References

- [LLVM Kaleidoscope: Code Generation to LLVM IR](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl03.html)
- [LLVM Language Reference](https://llvm.org/docs/LangRef.html)

