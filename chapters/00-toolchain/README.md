# 第 00 章：课程概述与 LLVM 工具链

> 预计用时：2–4 小时。本章不要求你理解 LLVM IR 的每个符号，我们先建立一张不会迷路的地图。

## 0.1 LLVM 工具链的组成

第一次安装 LLVM 时，人们经常会问：“LLVM 的可执行文件是哪一个？”这个问题没有唯一答案。LLVM 更像一间工厂：前台接收 C/C++ 的是 Clang，车间里负责整理中间表示的是 `opt`，把中间表示翻译成机器代码的是 `llc`，旁边还有汇编器、链接器、调试器和 JIT 基础设施。

这会带来一个实际困难。程序编译失败时，如果我们只知道按一下 IDE 的 Build 按钮，就不知道错误发生在前端、优化、代码生成还是链接阶段。接下来先把这些阶段拆开，亲手保存每一步的产物。

本章结束时，你应该能回答这样一个问题：手里拿着一个 `.ll` 文件，怎样确认它合法、运行它、优化它，并最终得到操作系统能够启动的程序？

## 0.2 环境与版本一致性

本课程的主版本记录在 [`docs/version-policy.md`](../../docs/version-policy.md)。LLVM 的命令行工具和 C++ 库需要来自兼容的发布线。一个常见而隐蔽的问题是：`clang` 来自一套安装，`opt` 来自另一套安装，CMake 又找到了第三套 headers。前几章也许还能工作，等到编译 Pass 插件时才暴露 ABI 或 API 不一致。

在仓库根目录运行环境检查：

```powershell
./tools/check-env.ps1
```

在 Unix shell 中运行：

```sh
./tools/check-env.sh
```

不要看到一串绿色的 `[ok]` 就立刻关闭终端。把版本号放在一起看：`clang`、`llvm-config`、`opt`、`llc` 和 `lli` 的主版本是否一致？如果不一致，先解决环境问题。课程后面的 bug 已经足够有意思，不需要再混入工具链偶然性。

### 平台说明

Ubuntu 可以使用发行版软件包或 LLVM 官方安装方式；Windows 推荐使用完整 LLVM 开发包配合 Visual Studio 2022/ClangCL，也可以选择完全工作在 WSL2 中；macOS 除了 AppleClang，还需要包含 `opt`、`llc`、开发库和 CMake 配置的 LLVM 安装。

关键不是选择哪一种包管理器，而是满足两点：命令行工具齐全，以及后续 C++ 项目能找到 `LLVMConfig.cmake`。只装一个能编译 C++ 的 `clang` 还不够。

## 0.3 编译流水线

在临时目录中新建 `answer.c`：

```c
int answer(void) {
  return 6 * 7;
}

int main(void) {
  return answer() == 42 ? 0 : 1;
}
```

这是一个刻意无聊的程序。我们不想把注意力花在 C 语义上，而是想观察它在编译过程中怎样改变形态。

第一步，让 Clang 只做到 LLVM IR 为止：

```sh
clang -O0 -Xclang -disable-O0-optnone -S -emit-llvm answer.c -o answer.ll
```

打开 `answer.ll`。即使暂时看不懂全部内容，也请找到下面几样东西：`answer` 和 `main` 两个函数、若干带类型的运算、`ret` 返回指令，以及文件开头附近的 `target triple` 和 `target datalayout`。

这里的 `-O0` 让前端尽量保留容易观察的结构。`-disable-O0-optnone` 则避免 Clang 给函数加上阻止多数优化 Pass 运行的 `optnone` 属性。这是教学观察用的选择，不是日常编译程序的固定模板。

接下来把文本 IR 组装成 bitcode：

```sh
llvm-as answer.ll -o answer.bc
```

`.ll` 和 `.bc` 表达的是同一层信息，一个适合人阅读，一个适合工具紧凑处理。如果 `llvm-as` 拒绝文件，说明文本连 LLVM IR 的基本格式或类型要求都没有满足。

现在运行一个很短的优化流水线：

```sh
opt -passes='mem2reg,instcombine,simplifycfg' answer.bc -o answer.opt.bc
llvm-dis answer.opt.bc -o answer.opt.ll
```

把 `answer.ll` 与 `answer.opt.ll` 并排打开。先不要查每个 Pass 的文档，凭观察回答：局部内存读写是否减少？`6 * 7` 是否还保留为乘法？控制流是否变短？我们在下一章才系统学习 IR；此处重要的是形成习惯——运行编译器以后，总要知道自己准备观察什么。

## 0.4 Bitcode 执行与本地代码生成

bitcode 可以直接交给 `lli`：

```sh
lli answer.opt.bc
```

这个程序没有打印内容，它用退出码报告成功。在 PowerShell 中查看 `$LASTEXITCODE`，在常见 Unix shell 中查看 `$?`。结果应为 0。

也可以把它编译为目标文件，再由系统链接器生成可执行文件：

```sh
llc -filetype=obj answer.opt.bc -o answer.o
clang answer.o -o answer
```

运行生成的 `answer`（Windows 上通常是 `answer.exe`），再次检查退出码。到这里，我们已经走完两条路径：一条由 `lli` 直接执行 bitcode；另一条经过目标代码和系统链接器。后面的 MiniLang 编译器会重新遇到这两个选择，分别演化为 JIT 和 AOT 模式。

## 0.5 Target Triple 与 Data Layout

回到最初的 `answer.ll`。`target triple` 大致说明目标架构、厂商、操作系统和环境；`target datalayout` 描述指针宽度、整数和向量对齐等布局规则。

初学者有时会从网上复制一段 IR，发现删掉这两行也能在自己的机器上运行，于是认为它们可有可无。这个结论只在非常小、几乎不接触内存布局的例子里看起来成立。一旦出现结构体、数组、指针运算或跨语言调用，布局就是语义的一部分。课程后面生成 Module 时，应从目标机器配置得到它们，而不是复制某台电脑上的字符串。

## 实验 0：编译阶段与目标相关性

给 `answer.c` 增加一个带局部变量和 `if` 的函数，然后分别用 `-O0` 和 `-O2` 生成 LLVM IR。继续生成目标汇编：

```sh
llc answer.opt.bc -o answer.s
```

比较 C、LLVM IR 和汇编三份文件，并在实验记录中回答：

1. 哪些信息在进入 LLVM IR 前已经消失？
2. 哪些结构在优化后发生变化，但程序行为不变？
3. 哪个阶段第一次出现明确的目标机器指令？
4. 如果换一个 target，哪些文件理论上可以复用？

完成练习的证据不是“命令都运行了”，而是一张由你标注的流水线图，图上写明每个输入、输出和负责的工具。

## 诊断说明

如果系统找不到 `opt`，通常意味着只安装了 Clang driver，没有完整工具集，或者 LLVM 的 `bin` 目录不在当前 shell 的 `PATH` 中。

如果优化前后毫无变化，先检查函数是否带 `optnone`，再检查你选择的代码是否真的给该 Pass 留下了工作。Pass 没有改变 IR 不等于 Pass 没运行。

如果目标文件无法链接，先比较生成目标和链接器所期待的架构与 object format。Windows 环境还要留意 MSVC/MinGW 运行库边界。不要一上来就在 LLVM IR 中随机修改类型；链接错误通常发生得更晚，它需要从符号、目标格式和 ABI 的角度分析。

## 小结

我们还没有正式学习 LLVM IR，但已经建立了后续排错需要的坐标系：Clang 产生 IR，`llvm-as` 与 `llvm-dis` 在文本和 bitcode 之间转换，`opt` 分析或改变 IR，`lli` 可以直接执行，`llc` 生成目标代码，最后由链接器组成程序。

下一章会停留在 `.ll` 这一层。我们将不再把它当作中间黑盒，而是自己写出第一个合法函数，并故意写坏几次，看看 parser 和 verifier 分别能发现什么。

### 提交物

- 环境检查输出；
- `answer.c`、优化前后的 IR、目标汇编；
- 带工具、输入和输出的流水线图；
- 上述四个观察问题的简短回答。

