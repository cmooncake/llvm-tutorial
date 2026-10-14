# Capstone Tests

[简体中文](README.md) | [English](README.en.md)

`cases.json` 提供 29 个公开 Scalar 输入与预期结果；`run.py` 调用学生编译器的 `check`/`run`，检查输出、退出码、诊断编号和部分精确位置。编译器缺失直接报错，不跳过测试。

```sh
python3 capstone/tests/run.py --compiler /absolute/path/minilang --stage check --report build/frontend.json
python3 capstone/tests/run.py --compiler /absolute/path/minilang --stage run --report build/acceptance.json
```

check 模式只验前端，不能代替运行验证。run 模式先检查所有输入，再运行合法程序；每次调用限时 15 秒，失败汇总后返回 1。它尚未自动验证 emit-ir、JIT/AOT 差分和全部 span，不能用 29/29 代替完整语言 conformance。

Scalar 的运行时实现位于 `../runtime/`，代码生成器通过 C ABI 调用它。当前没有完整参考编译器，公开程序的端到端预期仍需在参考实现和独立实现上交叉验证；这是正式开课前的阻断项。隐藏测试只隐藏输入，不新增语义规则。

