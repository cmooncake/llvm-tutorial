# 第 01 章：读写和验证 LLVM IR

预计用时：4–6 小时。先修：第 00 章。

## 学习目标

- 阅读 module、function、basic block、instruction 和 SSA value；
- 区分整数类型、指针类型与内存对象；
- 正确构造调用、分支和返回；
- 使用 parser 与 verifier 定位非法 IR。

## 1.1 最小函数

```llvm
define i32 @add(i32 %lhs, i32 %rhs) {
entry:
  %sum = add i32 %lhs, %rhs
  ret i32 %sum
}
```

`%sum` 是 SSA value，不是可反复赋值的变量。类型属于指令语义的一部分；`add i32` 与 `add i64` 是不同运算。

运行：

```sh
llvm-as add.ll -o add.bc
opt -passes=verify -disable-output add.bc
```

parser 主要检查文本是否能构成 IR；verifier 检查 CFG、类型、phi、支配关系等结构不变量。两者都通过仍不代表符合源语言语义。

## 1.2 基本块与终结指令

每个基本块必须以 terminator 结束，例如 `ret`、`br`、`switch` 或 `unreachable`。terminator 后不能再放普通指令。

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

注意 `abs(INT_MIN)` 的数学结果无法用 `i32` 表示。本例使用回绕结果；不能无条件给 `sub` 添加 `nsw`。

## 1.3 内存不是 SSA 名字

`alloca` 创建栈对象，`load` 读取，`store` 写入。下面的 `%slot` 是地址，`%value` 才是加载出的整数：

```llvm
%slot = alloca i32, align 4
store i32 42, ptr %slot, align 4
%value = load i32, ptr %slot, align 4
```

现代 LLVM 使用 opaque pointers，`ptr` 本身不编码 pointee type；load/store/GEP 的其他操作数承担类型信息。

## 引导实验

完成 `exercises/classify.ll` 中的 TODO，使函数返回：负数为 `-1`，零为 `0`，正数为 `1`。

```sh
llvm-as exercises/classify.ll -o classify.bc
opt -passes=verify -disable-output classify.bc
```

然后写一个 `main` 调用三次，并用退出码或外部 C harness 验证结果。

## 破坏性实验

复制一份正确 IR，依次制造并记录诊断：

1. 删除一个基本块 terminator；
2. 让 `ret i64` 返回给声明为 `i32` 的函数；
3. 为 phi 删除一个前驱 incoming；
4. 在某条路径使用并不支配该 use 的 value。

每次只引入一个错误，区分 parser error 与 verifier error。

## 独立挑战

实现 `clamp(x, low, high)`。自行规定 `low > high` 的行为并写在函数注释中。至少提供五个边界测试。

## 提交物与验收

- 完成的 `classify.ll`、`clamp.ll` 与测试 harness；
- 四个非法 IR 及对应诊断摘要；
- 所有合法 IR 通过 verifier；
- 能逐条解释每个 block 的前驱、后继和 terminator。

## 常见失败

- 把块标签写成 `%then`：定义标签时没有 `%`，引用时使用 `label %then`。
- phi 的 incoming block 不是真实 CFG 前驱：phi 描述的是控制流边，不是任意候选值。
- 比较结果当作 `i32`：`icmp` 返回 `i1`。
- 将宿主语言未定义行为误认为 LLVM 语义：必须检查具体指令和 flags。

