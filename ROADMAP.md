# 教程完成路线

状态含义：`设计`表示只有课程设计，`讲义`表示内容可阅读，`实验`表示有 starter/测试，`验证`表示已在支持版本执行通过。

英文版状态：课程首页已完成；其余讲义将在中文内容稳定后逐章翻译。翻译一致性要求见 `docs/translation-policy.md`。

| 模块 | 讲义 | 实验 | 验证 |
|---|---|---|---|
| 课程结构与评分 | ✅ | 不适用 | ✅ 文档检查 |
| 版本与环境政策 | ✅ | ⏳ | ⏳ |
| MiniLang 语言规范 | ✅ | ⏳ | ⏳ |
| 00 工具链 | ✅ | ⏳ | ⏳ |
| 01 LLVM IR | ✅ | ✅ | ⏳ 缺本地 LLVM |
| 02 SSA/CFG | ✅ | ✅ | ⏳ 缺本地 LLVM |
| 03 LLVM C++ API | ✅ | ✅ | ⏳ 缺本地 LLVM |
| 04 Pass | ✅ | ✅ | ⏳ 缺本地 LLVM |
| 05–07 前端 | 设计 | ❌ | ❌ |
| 08–12 后端与工程化 | 设计 | ❌ | ❌ |
| 13 Capstone | 规格 | ❌ | ❌ |
| 14–18 MLIR | 设计 | ❌ | ❌ |

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

