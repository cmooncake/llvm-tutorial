# Chapter 09: Data Layout and Calling Conventions

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 7–10 hours. This chapter asks how source-language values exist in machine memory.

Integers and booleans need little physical-layout discussion. Arrays, strings, and foreign calls require sizes, alignment, field offsets, address spaces, parameter passing, and symbol naming. Together these decisions form an ABI boundary.

## 9.1 DataLayout

Obtain the module DataLayout from the target machine rather than copying a string. Query storage sizes, ABI alignment, and structure layout through `DataLayout`. Host C++ `sizeof` cannot describe a cross-compilation target.

Front-end and LLVM types remain separate. Type lowering selects a representation; DataLayout describes that LLVM representation on the selected target.

## 9.2 GEP and Memory Access

`getelementptr` computes an address and does not access memory. Its leading type describes the indexed object layout; indices traverse aggregates. Opaque pointers do not carry pointee types, making the explicit GEP type essential.

Use `inbounds` only when the result is proven to satisfy the allocated-object rules. It is a semantic promise to the optimizer, not a performance hint.

## 9.3 Runtime ABI

Freeze exported symbols, C calling convention, integer widths, boolean representation, array and string layouts, ownership, failures, and visibility in a separate ABI document. A C ABI avoids C++ name mangling and exception-ABI complexity in the first implementation.

Maintain a C declaration and an LLVM declaration test for every runtime function. Successful linking does not prove ABI agreement; mismatched widths and returns may fail only on some targets.

## Laboratory 9: Arrays, Strings, and the Runtime

Implement fixed-length array layout, indexing, and bounds checks, followed by an immutable `{ptr, length}` string slice. Obtain target DataLayout, use GEP for elements, and call runtime print and trap functions.

Build a conformance harness in both directions: C calls generated functions, and generated code calls the C runtime. Cover empty aggregates, endpoints, out-of-bounds accesses, nested calls, and hidden 32/64-bit assumptions.

## Submission

- type-lowering and layout-query layer;
- versioned runtime ABI and C header;
- aggregate access, bounds checks, and traps;
- bidirectional ABI conformance tests; and
- justification for every `inbounds` use.

## References

- [LLVM Language Reference](https://llvm.org/docs/LangRef.html)
- [The Often Misunderstood GEP Instruction](https://llvm.org/docs/GetElementPtr.html)

