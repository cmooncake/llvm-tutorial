# Chapter 03: Constructing LLVM IR with the C++ API

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 5–7 hours. Prerequisites: Chapters 01–02 and C++ RAII.

## Learning Objectives

Understand the relationship among `LLVMContext`, `Module`, `Function`, `BasicBlock`, `Value`, and `IRBuilder`; manage lifetime without retaining dangling values; construct IR equivalent to hand-written examples; and verify close to the point of construction.

## 3.1 Core Object Model

The context owns uniqued types and constants; a module owns functions and globals; functions own basic blocks; blocks own instructions; and instructions commonly produce SSA values. IRBuilder maintains an insertion point but does not establish source-language correctness.

The context outlives every module and value that refers to it. Destroying a builder does not destroy inserted instructions, while erasing an instruction invalidates pointers to that instruction.

## 3.2 Build

Configure `chapters/03-cpp-api` with Ninja and an explicit `LLVM_DIR`, then build `ir-generator`. The CMake output must report a supported LLVM version and the intended `LLVMConfig.cmake`.

Run the generator into `generated.ll`, verify with `opt -passes=verify`, and check structure with `test/mul-add.check`. `verifyModule` returns true when it finds an error, an API detail worth handling explicitly.

## 3.3 Reading the Implementation

Trace creation of the function type, function arguments, entry block, insertion point, arithmetic instructions, return, verification, and module printing. Every step corresponds to an element previously written by hand.

## Laboratory 3: Generate the Classification Function

Generate Chapter 01 `classify` with the C++ API. Use semantic block names, correct phi predecessors, nonzero failure status on verifier error, and FileCheck patterns that do not freeze temporary numbering.

## Programming Exercise: Generate Loop Summation

Generate Chapter 02 `sum_to`. Add a helper that prevents adding a second terminator and explain whether that helper belongs to course infrastructure or LLVM itself.

## Review Questions: Object Lifetime

Explain builder destruction, erased instruction pointers, cross-context types, and why an AST must not retain `llvm::Value*`.

## Submission

- API generators for classification and summation;
- FileCheck tests;
- verifier integration; and
- no global context, module, or builder.

## Diagnostic Notes

Reset the insertion point for each block, never insert after a terminator, save the actual end block for phi incoming edges, and suspect mixed LLVM installations when compilation succeeds but linking fails.

## References

- [Embedding LLVM in a Project with CMake](https://llvm.org/docs/CMake.html#embedding-llvm-in-your-project)
- [LLVM Kaleidoscope: Code Generation](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl03.html)

