# 教程完成路线

[简体中文](ROADMAP.md) | [English](ROADMAP.en.md)

状态分为“教学内容”“可执行资产”“运行验证”。教学内容包含中英文讲义、实验规格、提交要求与来源；可执行资产是 starter、参考实现和自动测试；运行验证要求在支持的 LLVM 环境实际执行。

| 模块 | 双语教学内容 | 可执行资产 | 运行验证 |
|---|---|---|---|
| 课程结构、评分与规范 | ✅ | 文档审计脚本 | ✅ 74 文件审计 |
| 00 工具链 | ✅ | 环境检查脚本 | ⏳ 缺本地 LLVM |
| 01–02 IR、SSA/CFG | ✅ | 练习与参考 IR | ⏳ 缺本地 LLVM |
| 03 C++ API | ✅ | 生成器与检查 | ⏳ 缺本地 LLVM/CMake |
| 04 Pass | ✅ | 插件与检查 | ⏳ 缺本地 LLVM/CMake |
| 05–07 前端 | ✅ | 实验接口待实现 | ❌ |
| 08–12 后端与工程化 | ✅ | 实验接口待实现 | ❌ |
| 13 Capstone | ✅ | starter/reference 待实现 | ❌ |
| 14–18 MLIR | ✅ | 实验接口待实现 | ❌ |

## 最近里程碑

### R1：LLVM 基础可运行

- 完成 00–04 的 starter、solution 和 lit/FileCheck 测试；
- 建立跨平台 CI；
- 记录 LLVM 21.1 与 22.1 的兼容差异。

### R2：MiniLang 前端

- lexer、Pratt parser、AST dump、resolver 与 type checker；
- 完整源码位置和诊断测试；
- 冻结语言规范 1.0。

### R3：MiniLang LLVM 后端

- codegen、runtime、JIT/AOT、优化与调试信息；
- 公开测试与教师参考实现；
- 完成学生版 starter 仓库。

### R4：MLIR 进阶后端

- Mini dialect、conversion pipeline 和差分测试；
- tensor/vector/bufferization 选修实验；
- Transform dialect 研究项目。

