# 第 01 章：LLVM 中间表示

> 预计用时：4–6 小时。请先完成第 00 章，并确认 `llvm-as`、`opt` 和 `lli` 可以使用。

上一章里，LLVM IR 是 Clang 生成的中间产物。这一章我们反过来：不写 C，也不依赖 Clang，而是直接写 IR。这样做不是为了把 `.ll` 当成日常编程语言，而是为了看清编译器后端真正接收的结构。

我们会遇到两个不同的问题。第一，文本能不能被 LLVM 读懂？第二，读懂以后，它是否满足 LLVM IR 的结构规则？`llvm-as` 和 verifier 分别帮助我们回答这两个问题。

## 1.1 函数、类型与 SSA 值

新建 `add.ll`：

```llvm
define i32 @add(i32 %lhs, i32 %rhs) {
entry:
  %sum = add i32 %lhs, %rhs
  ret i32 %sum
}
```

先运行：

```sh
llvm-as add.ll -o add.bc
opt -passes=verify -disable-output add.bc
```

如果两条命令都安静结束，这个函数至少在结构上是合法的。现在逐行看它做了什么。

第一行声明了一个名为 `add` 的函数。它接收两个 `i32`，也返回 `i32`。`entry:` 开始一个基本块。基本块可以先理解为“一定从头执行到末尾、中间不会跳出去的一串指令”。`add` 指令产生一个新值 `%sum`，最后 `ret` 返回它。

这里最需要调整的直觉是：`%sum` 不是一个可以反复赋值的变量。它是这一次加法的结果，并且只定义一次。这种写法来自 SSA——静态单赋值形式。下一章会系统讨论 SSA；此处先记住，每条产生结果的指令都在给一个新值命名。

### 检查点：返回类型

把 `ret i32 %sum` 改成 `ret i64 %sum`，先不要运行。你预计错误会出现在哪一步？再实际执行 `llvm-as`。记录工具的原始诊断，并用自己的话解释：是返回值本身错了，还是函数签名与返回指令之间不一致？

这个习惯很重要。先预测，再观察，最后修正自己的模型；不要把编译器课程变成不断复制命令和错误信息。

## 1.2 基本块与终结指令

只要程序出现条件，就不再是一条直线。下面的函数返回一个 `i32` 的绝对值：

```llvm
define i32 @abs(i32 %x) {
entry:
  %negative = icmp slt i32 %x, 0
  br i1 %negative, label %neg, label %done

neg:
  %flipped = sub i32 0, %x
  br label %done

done:
  %result = phi i32 [ %flipped, %neg ], [ %x, %entry ]
  ret i32 %result
}
```

`icmp slt` 做有符号小于比较，结果类型是 `i1`，也就是一个一位的真假值。随后 `br` 根据这个值选择 `%neg` 或 `%done`。注意每个块都以 `br` 或 `ret` 结束。这类决定“接下来去哪里”的指令叫 terminator；合法的基本块不能缺少 terminator，也不能在 terminator 后继续放普通指令。

控制流在 `%done` 汇合时出现了一个问题：结果有时来自 `%flipped`，有时直接来自 `%x`。`phi` 根据程序是沿哪条前驱边进入 `%done` 来选择值。方括号中的第二项不是随手写的标签，它必须对应 `%done` 的真实前驱块。

`abs` 还隐藏着一个很好的边界问题。最小的 `i32` 没有对应的正数可以继续放在 `i32` 中，因此这里会得到回绕结果。我们没有给 `sub` 添加 `nsw`。`nsw` 不是“请帮我检查溢出”，而是编译器可以依赖的无有符号溢出承诺；承诺不成立时，后续优化可能产生你意料之外的结果。

## 1.3 内存操作与 Opaque Pointer

看下面四行：

```llvm
%slot = alloca i32, align 4
store i32 42, ptr %slot, align 4
%value = load i32, ptr %slot, align 4
ret i32 %value
```

`%slot` 是一个地址，指向栈上的存储位置；`%value` 是从该位置读出的整数。虽然两者都以 `%` 开头，但类型和用途完全不同。`store` 本身不产生一个可命名的普通结果，它改变的是内存状态。

现代 LLVM IR 使用 opaque pointer，所以地址通常写作 `ptr`，而不是把 pointee type 编进指针类型。真正被读写的 `i32` 出现在 `load` 和 `store` 指令中。看到 `ptr` 时，不要猜它“天生指向什么”；要沿着产生和使用该指针的指令寻找证据。

## 实验 1：整数分类函数

打开 [`exercises/classify.ll`](exercises/classify.ll)。目标函数的行为是：输入小于零时返回 `-1`，等于零时返回 `0`，大于零时返回 `1`。

先在纸上画三个框，分别代表负数、零和正数路径，再考虑是否真的需要三个返回块。你可以使用两个比较和条件分支，但不得使用 `alloca`、`load` 或 `store`。完成后执行：

```sh
llvm-as exercises/classify.ll -o classify.bc
opt -passes=verify -disable-output classify.bc
```

仅仅通过 verifier 还不能证明分类行为正确。请再写一个 `main` 或 C harness，至少测试 `-1`、`0`、`1`、`INT_MIN` 和 `INT_MAX`。参考实现位于 `solutions/`，但应在自己的版本通过测试并能解释 CFG 后再查看。

## 1.4 Parser 与 Verifier

接下来不要急着写更多正确代码。复制一份已经通过验证的 IR，每次只制造一种错误：删除 terminator；让返回类型与函数签名不一致；删除一个 phi incoming；或者让某条路径使用一个在该路径上尚未定义的值。

对每次实验记录三件事：哪条命令首先报错，诊断指向哪里，以及真正被破坏的规则是什么。你会发现，有些问题在文本解析阶段就能发现，有些则要等 verifier 检查控制流、类型或支配关系。这个区别会在以后调试 codegen 时节省大量时间。

## 编程练习：Clamp 函数

实现 `clamp(x, low, high)`：当 `x < low` 时返回 `low`，当 `x > high` 时返回 `high`，否则返回 `x`。先在注释中规定 `low > high` 时的行为；规范不明确时，任何看似合理的实现都可能在测试阶段产生争议。

至少覆盖五种输入，并提交一张 CFG。验收时，你需要逐块说明其前驱、后继和 terminator，还要指出最终返回值在哪些路径上定义。

## 诊断说明

如果你把块定义写成 `%then:`，请区分“定义一个标签”和“引用一个标签”：定义时写 `then:`，分支目标写 `label %then`。

如果 verifier 报告 phi 的 incoming block 有问题，先画真实 CFG，不要只盯着 phi 文本。phi 描述的是进入当前块的边，而不是一组任意候选值。

如果比较结果和整数运算对不上，检查类型。`icmp` 返回 `i1`，不会因为操作数是 `i32` 就返回 `i32`。需要把布尔量变成整数时，应明确选择 `zext`、`sext` 或 `select`，并解释为什么。

## 小结

LLVM IR 的核心对象开始有了轮廓：函数由基本块组成，基本块由 terminator 封口，指令产生带类型的 SSA 值，分支形成 CFG，phi 在汇合点按前驱边选择值，而内存对象通过地址、load 和 store 明确出现。

下一章会把重点从“读懂几段 IR”转向“系统推导控制流”。届时我们会用支配关系判断一个值能否在某处使用，并亲手构造带回边的循环。

### 提交物

- 完成并测试的 `classify.ll`；
- `clamp.ll`、至少五个测试和 CFG；
- 四份单一错误的非法 IR，以及对首次失败阶段的解释。

