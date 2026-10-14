# MiniLang 1.0 语言规范

[简体中文](language-spec.md) | [English](language-spec.en.md)

本页保留综合语言设计与语法背景。研究生版必做范围和语义歧义以 [MiniLang Scalar 契约](language-profile.md) 为准；数组属于需另行补全构造与 ABI 的扩展，不是已冻结的共同验收要求。

## 1. 词法

源文件使用 UTF-8。1.0 版只允许 ASCII 字母参与标识符：

```text
identifier := [A-Za-z_][A-Za-z0-9_]*
integer    := 0 | [1-9][0-9]*
comment    := // 到行尾
```

关键字：

```text
fn let var if else while return true false
i32 bool unit
```

空格、制表符和换行分隔 token。换行本身没有语义。每个 token 携带半开区间源码位置 `[begin, end)`。

## 2. 语法

以下为教学用 EBNF：

```text
program       := function* EOF ;
function      := "fn" IDENT "(" parameters? ")" ("->" type)? block ;
parameters    := parameter ("," parameter)* ;
parameter     := IDENT ":" type ;
type          := "i32" | "bool" | "unit" | "[" type ";" INTEGER "]" ;

block         := "{" statement* expression? "}" ;
statement     := let-decl | var-decl | while-stmt | return-stmt | expr-stmt ;
let-decl      := "let" IDENT (":" type)? "=" expression ";" ;
var-decl      := "var" IDENT (":" type)? "=" expression ";" ;
while-stmt    := "while" expression block ;
return-stmt   := "return" expression? ";" ;
expr-stmt     := expression ";" ;

expression    := assignment ;
assignment    := IDENT "=" assignment | logical-or ;
logical-or    := logical-and ("||" logical-and)* ;
logical-and   := equality ("&&" equality)* ;
equality      := comparison (("==" | "!=") comparison)* ;
comparison    := term (("<" | "<=" | ">" | ">=") term)* ;
term          := factor (("+" | "-") factor)* ;
factor        := unary (("*" | "/" | "%") unary)* ;
unary         := ("!" | "-") unary | call ;
call          := primary ("(" arguments? ")" | "[" expression "]")* ;
arguments     := expression ("," expression)* ;
primary       := INTEGER | "true" | "false" | IDENT
               | "(" expression ")" | if-expr | block ;
if-expr       := "if" expression block ("else" (if-expr | block))? ;
```

若函数省略返回类型，则返回 `unit`。块的最后一个无分号表达式是块值；没有尾表达式的块值为 `unit`。

## 3. 名字与作用域

- 顶层函数处于同一全局命名空间，允许调用文本位置靠后的函数；
- 参数和局部变量处于词法块作用域；
- 内层作用域可以遮蔽外层名字；
- 同一作用域重复定义是错误；
- 名字在初始化表达式完成之后才进入作用域；
- 赋值左侧必须解析为可变 `var`，不能是 `let`、参数或函数。

## 4. 类型规则

- 1.0 版不做隐式数值转换；
- 算术运算接收并返回 `i32`；
- 比较运算接收两个 `i32` 并返回 `bool`；
- `==`/`!=` 要求两侧同类型，1.0 版仅支持 `i32` 和 `bool`；
- `!`、`&&`、`||` 只接受 `bool`；
- `if` 条件和 `while` 条件必须是 `bool`；
- 有 `else` 的 `if` 两个分支类型必须一致；
- 无 `else` 的 `if` 类型为 `unit`，其 then 块也必须为 `unit`；
- 函数所有可达返回路径必须满足声明的返回类型；
- `unit` 不能用于算术、比较或数组元素。

声明类型可省略，此时从初始化表达式推导。课程不要求全局 Hindley–Milner 推导。

## 5. 求值语义

- 函数参数从左到右求值；
- 二元运算数从左到右求值；
- `&&` 和 `||` 短路；
- `if` 只求值被选择的分支；
- `while` 在每轮开始前求值条件；
- `i32` 使用二进制补码回绕语义；
- 除以零、余数除数为零和数组越界触发 runtime trap；
- `return` 立即离开当前函数。

LLVM codegen 必须与这些语义一致。例如，源语言规定回绕时，不应无依据地为整数运算添加 `nsw`。

## 6. 数组

- `[T; N]` 是固定长度值类型，`N` 必须是非负编译期整数；
- 1.0 核心语法暂不提供数组字面量，数组由标准库/runtime helper 构造；
- 索引类型为 `i32`；
- 每次索引都必须进行边界检查，除非后续优化能证明安全；
- 数组赋值采用值语义；实现可内部使用内存，但不能暴露别名差异。

## 7. 程序入口与退出

可执行程序必须定义：

```text
fn main() -> i32 { ... }
```

返回值成为进程退出码。JIT 测试也调用相同签名。

## 8. 标准 runtime 表面

核心课程只规定最小能力：

```text
print_i32(value: i32) -> unit
print_bool(value: bool) -> unit
trap(code: i32) -> unit
```

LLVM 层的 C ABI 名称、布尔表示、字符串表示和 calling convention 在后端阶段单独冻结。

## 9. 必需诊断类别

- `E0001` 非法字符
- `E1001` 语法错误
- `E2001` 未定义名字
- `E2002` 同作用域重复定义
- `E2003` 对不可变绑定赋值
- `E3001` 类型不匹配
- `E3002` 参数数量错误
- `E3003` 缺失返回
- `E3004` 非布尔条件

测试断言诊断编号、源码 span 和关键参数，不应依赖整段自然语言完全一致。

## 10. 示例

```text
fn sum_to(n: i32) -> i32 {
  var i = 0;
  var sum = 0;
  while i < n {
    sum = sum + i;
    i = i + 1;
  }
  return sum;
}

fn main() -> i32 {
  let answer = sum_to(10);
  print_i32(answer);
  return 0;
}
```

