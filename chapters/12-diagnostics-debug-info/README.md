# 第 12 章：诊断与调试信息

[简体中文](README.md) | [English](README.en.md)

> 预计用时：6–9 小时。诊断面向编译期用户，调试信息面向运行期 debugger；两者都依赖可靠源码位置。

## 12.1 Diagnostic Engine

诊断对象包含严重级别、稳定编号、主 span、结构化参数和可选 secondary spans/notes。渲染器负责文件名、行列、源码摘录、caret 和颜色。把数据与呈现分开，测试可以稳定检查语义而不锁死终端样式。

CLI 对错误、警告和内部错误使用稳定退出码。普通用户输入错误不得打印 C++ stack trace；内部不变量失败则保留足够上下文，并提示如何保存最小复现。

## 12.2 LLVM Debug Information

LLVM debug info 用 metadata 描述源文件、compile unit、subprogram、类型、变量和指令位置。使用 `DIBuilder` 建立 module 级结构，为生成指令设置 `DebugLoc`，并在结束时 finalize。

调试信息映射源语言对象，而不是简单复制 LLVM IR。优化可能消除变量或重排代码；要求是尽可能保持准确关系，而不是承诺每个优化后的变量始终可修改。

当前 LLVM 默认 debug records 与旧 intrinsic 模型不能在同一 module 混用。课程使用目标版本推荐模型，并把版本差异记录在兼容文档中。

## 实验 12：诊断呈现与源级调试

先实现统一诊断渲染，覆盖单行、多行、tab、UTF-8 上下文、secondary note 和无源码文件的内部错误。再为函数和语句生成最小 debug info，使 debugger 能设置源码断点并显示调用栈。

分别在 `-O0 -g` 和 `-O2 -g` 下观察断点、单步和局部变量。报告优化造成的可观察差异，不把 debugger 行为差异误判为 codegen 语义错误。

## 提交要求

- 结构化 Diagnostic Engine 与文本渲染器；
- 稳定退出码和诊断测试；
- 最小完整 DIBuilder 集成；
- debugger 会话记录；
- 优化后调试限制说明。

## 参考资料

- [Source Level Debugging with LLVM](https://llvm.org/docs/SourceLevelDebugging.html)
- [LLVM Kaleidoscope: Debug Information](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl09.html)

