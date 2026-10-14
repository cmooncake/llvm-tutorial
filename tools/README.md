# Course Tools

[简体中文](README.md) | [English](README.en.md)

课程工具覆盖环境与文档审计，并为 IR 验证、测试运行、CFG 导出和 benchmark 汇总保留稳定 CLI 边界。工具不能替学生完成核心编译器逻辑。

```powershell
./tools/check-env.ps1
./tools/audit-docs.ps1
```

`audit-docs.ps1` 检查中英文配对、语言导航、本地链接和重复标题。

`setup-ubuntu.sh` 在 Ubuntu 24.04 中添加 LLVM 22 apt 源并安装开发工具，需显式用 sudo 执行。它会修改系统包，不是环境检查器。完整构建、CTest 命令和测试覆盖范围见[测试指南](../docs/testing.md)。

`measure.py` 比较两个确定性可执行程序的完整进程耗时，保存原始样本、二进制哈希、顺序与离散程度，并检查输出一致性。它不隔离进程启动、JIT 或 kernel 时间，也不自动给出统计显著性；用法与报告边界见[研究报告](../docs/project-report.md)。MLIR 实验入口与逐层产物见[公共实验](../docs/graduate-labs.md)。

