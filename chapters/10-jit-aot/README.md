# 第 10 章：JIT 与提前编译

[简体中文](README.md) | [English](README.en.md)

> 预计用时：7–10 小时。本章让同一个 LLVM Module 进入两条执行路径。

JIT 在当前进程中编译并解析符号，适合 REPL、动态语言和快速反馈；提前编译（AOT）产生目标文件，再交给系统链接器形成可执行程序。两者应共享前端、codegen 和大部分优化流水线，而不是发展成两个语义不同的编译器。

## 10.1 ORCv2 与 LLJIT

课程使用 ORCv2 的 `LLJIT` 起步。为目标初始化 native target，创建 JIT，设置当前进程符号生成器，向 JITDylib 加入 `ThreadSafeModule`，再通过符号查找调用 `main`。

JIT 资源有生命周期。Module 加入后所有权发生转移；runtime 符号必须明确暴露；错误使用 LLVM `Expected`/`Error` 传播，不能被 `cantFail` 无条件吞掉。

## 10.2 目标文件与链接

AOT 路径由 TargetMachine 设置 triple 和 DataLayout，运行 codegen pipeline 写出 object file，然后通过编译器 driver 或显式链接器与 runtime 链接。课程工具应提供 `--emit-ir`、`--emit-obj` 与 `build`，并打印实际链接命令以便复现。

不要让 shell 字符串拼接成为跨平台接口。参数应作为数组传递给进程执行层，并正确处理带空格路径与退出码。

## 实验 10：双执行后端

实现 `minilang run` 与 `minilang build`。同一组程序分别经 JIT 和 AOT 运行，比较标准输出、标准错误、退出码和 trap 类别。

至少覆盖函数调用、递归、runtime 符号、全局名字冲突、无 `main`、链接失败和重复 JIT session。记录编译时间时区分前端、优化、codegen 与链接阶段。

## 提交要求

- ORCv2 `LLJIT` 执行引擎；
- 目标文件 emission 与可靠的链接驱动；
- JIT/AOT 差分测试；
- 所有 LLVM Error 的显式处理；
- 平台限制与可复现命令记录。

## 参考资料

- [ORC Design and Implementation](https://llvm.org/docs/ORCv2.html)
- [LLVM Kaleidoscope Tutorial](https://llvm.org/docs/tutorial/)

