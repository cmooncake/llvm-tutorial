# 教程完成路线

[简体中文](ROADMAP.md) | [English](ROADMAP.en.md)

状态分为“教学内容”“可执行资产”“运行验证”。教学内容包含中英文讲义、实验规格、提交要求与来源；可执行资产是 starter、参考实现和自动测试；运行验证要求在支持的 LLVM 环境实际执行。

正式开课的阻断项以[发布验收](docs/release-readiness.md)为准。下表的讲义状态只表示已有内容，不表示经过完整试教。

| 模块 | 双语教学内容 | 可执行资产 | 运行验证 |
|---|---|---|---|
| 课程结构、评分与规范 | ✅ 研究生双语教案 | 文档审计脚本 | 见测试指南中的审计记录 |
| 00 工具链 | ✅ | 环境脚本与流水线测试 | ✅ WSL Ubuntu / LLVM 22.1.8 |
| 01–02 IR、SSA/CFG | ✅ | 练习、参考 IR、行为测试 | ✅ 参考通过、初始练习被拒绝 |
| 03 C++ API | ✅ | 生成器、结构与行为测试 | ✅ LLVM 22.1.8 |
| 04 Pass | ✅ | 插件、回归与行为测试 | ✅ LLVM 22.1.8 |
| 05–07 前端 | ✅ | 实验接口待实现 | ❌ |
| 08–12 后端与工程化 | ✅ | 实验接口待实现 | ❌ |
| 13 Capstone | ✅ | CLI 外壳、C runtime、29 个公开输入；完整参考待实现 | 外壳可构建且被验收拒绝；runtime 编译通过；完整语义未验证 |
| 14、16、17 MLIR 公共实验 | ✅ | SCF、bufferization、错误诊断 | ✅ MLIR 22.1.8，3 组通过 |
| 15、18 与其他 MLIR 深化 | ✅ | 自定义 dialect、Transform 等待实现 | ❌ |

## 最近里程碑

### R1：LLVM 基础可运行

- 第 00–04 章现有实现已接入 CTest/Python/FileCheck；第 01–02 章可选择练习或参考 IR；
- 已添加 Ubuntu 24.04 / LLVM 22 CI 配置，远程运行结果待验证；
- 暂不承诺 LLVM 21 兼容或原生 Windows/macOS 支持；
- 后续补齐第 03–04 章独立学生 starter。运行证据见[测试指南](docs/testing.md)。

### R2：MiniLang 前端

- lexer、Pratt parser、AST dump、resolver 与 type checker；
- 完整源码位置和诊断测试；
- 按 Scalar 教学契约完成独立实现复核。

### R3：MiniLang LLVM 后端

- codegen、Scalar runtime、可靠执行路径与优化；完整 JIT/AOT 和调试信息按研究方向选做；
- 公开测试与教师参考实现；
- 完成学生版 starter 仓库。

### R4：MLIR 进阶后端

- Mini dialect、conversion pipeline 和差分测试；
- 在现有 CPU bufferization 公共实验上增加 tensor/vector 深化；
- Transform dialect 研究项目。

