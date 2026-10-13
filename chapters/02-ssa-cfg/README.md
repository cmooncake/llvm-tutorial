# 第 02 章：控制流与静态单赋值形式

[简体中文](README.md) | [English](README.en.md)

预计用时：5–7 小时。先修：第 01 章。

## 学习目标

- 从 CFG 而不是源代码缩进理解控制流；
- 判断 definition 是否支配 use；
- 在 merge point 正确放置 phi；
- 理解 memory form 与 SSA form 的关系；
- 正确 lower 短路逻辑和循环。

## 2.1 定义、使用与支配关系

看到一个 SSA use 时，依次问：

1. 它的 definition 在哪里？
2. definition 是否支配 use？
3. 如果 use 是 phi operand，它是否在对应 incoming edge 上可用？
4. 该路径是否真的能够到达？

这四个问题比“变量现在是什么值”更适合分析 LLVM IR。

## 2.2 控制流汇合与 Phi 指令

源程序：

```text
let y = if condition { 10 } else { 20 };
```

两条路径产生两个不同 SSA value，merge block 使用 phi 选择：

```llvm
then:
  br label %merge
else:
  br label %merge
merge:
  %y = phi i32 [ 10, %then ], [ 20, %else ]
```

phi 在概念上发生于进入块的边上，并且必须集中在块的开头。

## 2.3 循环携带值

```llvm
loop:
  %i = phi i32 [ 0, %entry ], [ %next, %body ]
  %keep_going = icmp slt i32 %i, %n
  br i1 %keep_going, label %body, label %exit
body:
  %next = add i32 %i, 1
  br label %loop
```

`%i` 的第二个 incoming value 来自回边。虽然 `%next` 在文本上位于 phi 之后，但它在 `%body -> %loop` 这条边上已经可用。

## 2.4 短路求值

`a && f()` 不能无条件调用 `f` 再做 `and`。正确 lowering 必须只在 `a` 为真时求值右侧，并在 merge block 用 phi 合并 `false` 与右侧结果。`||` 同理但方向相反。

## 实验 2A：循环求和

完成 `exercises/sum-to.ll`，实现 `[0, n)` 求和；当 `n <= 0` 时返回 0。限制：不得使用 `alloca`。

运行：

```sh
opt -passes=verify -disable-output exercises/sum-to.ll
opt -passes='print<domtree>' -disable-output exercises/sum-to.ll
```

画出 CFG，标注 dominator tree 和回边。

## 实验 2B：短路求值与副作用

声明：

```llvm
declare i1 @probe()
```

实现 `and_then(i1 %lhs)`，仅在 `%lhs` 为真时调用 `probe`。用一个带计数器的 C harness 证明短路发生，而不是只检查返回值。

## 实验 2C：Mem2Reg 与 SSA 构造

先用 `alloca/load/store` 写循环，再运行：

```sh
opt -passes='mem2reg' -S memory-form.ll -o ssa-form.ll
```

比较 phi 的位置，并回答 mem2reg 需要哪些前提。它不是任意内存优化器，通常提升入口块中、使用方式足够简单的局部 alloca。

## 编程练习：迭代 Fibonacci

实现迭代 Fibonacci：

```text
fib(0) = 0
fib(1) = 1
fib(n) = fib(n-1) + fib(n-2), n >= 2
```

要求只使用一个循环，不使用内存。为 `n < 0` 自行规定行为并记录。

## 提交要求

- `sum-to.ll`、短路实验、memory/SSA 对照和 Fibonacci；
- 每个函数的 CFG 图或文字邻接表；
- verifier 全部通过；
- harness 能检测错误的 eager evaluation；
- 能解释每个 phi incoming 与具体 CFG edge 的对应关系。

## 参考资料

- [LLVM Language Reference: Phi Instruction](https://llvm.org/docs/LangRef.html#phi-instruction)
- [LLVM Kaleidoscope: Control Flow](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl05.html)

