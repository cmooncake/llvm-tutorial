# 第 03 章：使用 C++ API 构造 LLVM IR

预计用时：5–7 小时。先修：第 01–02 章、C++ RAII。

## 学习目标

- 理解 `LLVMContext`、`Module`、`Function`、`BasicBlock`、`Value` 与 `IRBuilder` 的关系；
- 管理对象生命周期而不保存悬空的 `Value*`；
- 以 API 构造与手写 IR 等价的函数；
- 在最靠近错误来源的位置运行 verifier。

## 3.1 核心对象模型

- `LLVMContext` 拥有 uniqued types、constants 等上下文状态；
- `Module` 是函数、全局量和 target 信息的容器；
- `Function` 包含 basic blocks；
- `BasicBlock` 包含 instructions；
- `Instruction` 同时通常也是一个 SSA `Value`；
- `IRBuilder` 维护 insertion point，帮助创建指令，但不替你保证源语言语义。

本章程序先创建 context，再创建引用该 context 的 module。module 销毁前 context 必须仍然存活。

## 3.2 构建

```sh
cmake -S chapters/03-cpp-api -B build/03-cpp-api \
  -G Ninja \
  -DLLVM_DIR=/path/to/lib/cmake/llvm
cmake --build build/03-cpp-api
```

Windows PowerShell 将续行符改为反引号，或写在一行。`LLVM_DIR` 必须指向与目标版本匹配的 `LLVMConfig.cmake` 所在目录。

运行：

```sh
build/03-cpp-api/ir-generator > generated.ll
opt -passes=verify -disable-output generated.ll
FileCheck chapters/03-cpp-api/test/mul-add.check --input-file=generated.ll
```

## 3.3 阅读实现

打开 `src/ir_generator.cpp`，按以下顺序追踪：

1. 构造函数类型；
2. 创建函数并命名参数；
3. 创建入口块；
4. 设置 builder insertion point；
5. 创建 `mul`、`add` 与 `ret`；
6. 验证 function 和 module；
7. 打印 IR。

注意：`verifyModule` 返回 `true` 表示发现错误，这与许多“成功返回 true”的 API 相反。

## 实验 3：生成整数分类函数

把第 01 章的 `classify` 参考 IR 用 C++ API 生成。要求：

- 不读取 `.ll` 文件；
- basic block 名称有语义；
- phi incoming block 与真实前驱一致；
- `verifyFunction` 失败时程序返回非零；
- 新增 FileCheck 检查控制流形状，但不锁死所有临时变量编号。

## 编程练习：生成循环求和函数

生成第 02 章的 `sum_to`，并实现一个小 helper：在向 block 添加 terminator 前检查它是否已经终结。思考 helper 应属于教学工具层还是 LLVM 本身。

## 复习题：对象生命周期

回答：

1. `IRBuilder` 被销毁后，已经插入 module 的指令是否仍存在？
2. 删除一条 instruction 后，之前保存的 `Value*` 能否继续使用？
3. 一个 context 中的 type 能否直接放入另一个 context 的 module？
4. 为什么 AST 不应该长期保存 `llvm::Value*`？

## 提交要求

- `classify` 和 `sum_to` 的 API 生成实现；
- FileCheck 测试；
- 所有 module 通过 verifier；
- CMake 输出显示使用受支持 LLVM 版本；
- 代码没有全局 context/module/builder。

## 诊断说明

- builder insertion point 仍在旧 block：每次开始生成 block 都明确设置插入点。
- block 已有 terminator 后继续插入：生成语句时传播“当前块已终结”状态。
- phi 提前添加错误 incoming：先保存控制流结束块，再添加 incoming。
- CMake 能找到 headers 却链接失败：headers 与 libraries 很可能来自不同 LLVM 安装。

