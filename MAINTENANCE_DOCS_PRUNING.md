## 文档与脚本精简说明 (2025-11-17)

本次清理目标：删除所有一次性 Bug 修复报告、阶段性总结、已废弃功能脚本，保留核心使用/配置/结构类文档，使仓库更轻、入口更清晰，方便 Hackathon Demo 与后续迭代。

### 保留策略
保留下列类别：
1. 使用与快速上手：`README.md`, `QUICK_START.md`
2. 关键特性与配置：`TERMINOLOGY_GUIDE.md`, `HYBRID_MODE_GUIDE.md`, `MODEL_CONFIG_GUIDE.md`, `FILE_CHUNK_PREVIEW_GUIDE.md`, `PREVIEW_FEATURE_GUIDE.md`
3. 项目结构与参考：`PROJECT_STRUCTURE.md`, `SUPPORTED_LANGUAGES.md`, `MODEL_QUICK_REFERENCE.md`, `UPLOAD_TROUBLESHOOTING.md`
4. 术语数据：`terminology_curated.json`
5. 测试与校验：`test_adaptive_chunking.py`, `test_hybrid_mode.py`, `test_model_api.py`, `verify_demo_files.py`, `verify_preview_feature.py`

### 已删除文件列表
以下文件为阶段性成果、临时优化笔记或已废弃功能相关，不再保留：
```
CHINESE_LOGS_ENGLISH_REPORT.md
DEMO_CHUNKING_FIX.md
DEMO_FILES_GUIDE.md
DEMO_MODE_REMOVAL_GUIDE.md
DEMO_OPTIMIZATION_GUIDE.md
DEMO_OPTIMIZATION_SUMMARY.md
DOC_INDEX.md
FILE_MANIFEST.md
HYBRID_IMPLEMENTATION_SUMMARY.md
LANGUAGE_EXPANSION_SUMMARY.md
LLM_ARTIFACT_CLEANING.md
LOG_IMPROVEMENT_SUMMARY.md
MIGRATION_REPORT.md
MODEL_CONFIG_COMPLETION_SUMMARY.md
MODEL_CONFIG_IMPROVEMENT_REPORT.md
PREVIEW_COMPLETION_CHECKLIST.md
PREVIEW_DEMO_GUIDE.md
PREVIEW_IMPLEMENTATION_REPORT.md
PREVIEW_SUMMARY.md
PREVIEW_UI_GUIDE.md
PROJECT_COMPLETION_REPORT.md
PROJECT_IMPROVEMENT_OVERVIEW.md
TRANSLATION_COMPLETE_FIX.md
test_cleaning.py
fix_chinese_logs.py
```

### 删除原因分类
| 分类 | 代表文件 | 删除原因 |
| ---- | -------- | -------- |
| 一次性修复报告 | CHINESE_LOGS_ENGLISH_REPORT.md, TRANSLATION_COMPLETE_FIX.md | 对应问题已直接在代码实现，报告仅历史参考 |
| Demo 调参与阶段总结 | DEMO_* / PREVIEW_* / MODEL_CONFIG_* / LOG_IMPROVEMENT_* | 内容已融入最终实现与核心指南，保留重复信息会增加维护成本 |
| 架构或里程碑总结 | PROJECT_COMPLETION_REPORT.md, PROJECT_IMPROVEMENT_OVERVIEW.md, MIGRATION_REPORT.md | 归档价值低于维护成本，可在仓库提交历史查看 |
| 实验/临时索引 | DOC_INDEX.md, FILE_MANIFEST.md | 信息与实际文件清单不同步风险高 |
| 已废弃功能 | LLM_ARTIFACT_CLEANING.md, test_cleaning.py | 推理清洗功能已移除，不再需要 |
| 临时脚本 | fix_chinese_logs.py | 中文日志翻译已内置无需额外脚本 |

### 后续建议
1. 新增文档统一进入 docs 分类前先评估“是否面向最终用户”——否则放在 Issue 或 PR 描述中即可。
2. 若再次需要里程碑总结，建议写入单一 `PROJECT_HISTORY.md`，分章节记录，避免大量散落的 *_SUMMARY.md。
3. 若恢复推理清洗功能，再新增 `ARTIFACT_CLEANING_GUIDE.md`，与实现同步。
4. 建议定期 (每季度) 回顾 docs 目录，移除超过 2 个月未更新且无直接用户价值的文件。

### 验证
清理前已确认：
* 删除脚本未被 `app.py` 或测试引用。
* 删除文档不影响启动、上传、分析、翻译主流程。

### 快速核对脚本与测试仍可用
保留测试文件：
* `test_adaptive_chunking.py`
* `test_hybrid_mode.py`
* `test_model_api.py`
* `verify_demo_files.py`
* `verify_preview_feature.py`

如需回滚，可通过 git 历史恢复上述删除文件。

---
文档精简完成，后续新增请遵循“面向用户 / 持续价值 / 不重复”三原则。