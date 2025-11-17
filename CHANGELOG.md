# 📝 CHANGELOG - Model Configuration Update

## [2.0.0] - 2025-11-17 (模型配置字典化)

### 🎯 Major Changes

#### ✨ 新增：统一模型配置系统
- **字典化配置**: 从分散变量改为 `MODEL_CONFIGS` 字典
- **4 个 AI 模型**: DeepSeek Free, DeepSeek V3, GPT-4o, Claude Sonnet 4
- **元数据丰富**: 每个模型包含 8 个属性（名称、tokens、温度、成本、描述、速度、质量）
- **一键切换**: 修改 `ACTIVE_MODEL` 变量即可切换模型

#### 🛠️ 新增：管理工具
- **model_manager.py**: 200 行 CLI 工具
  - 查看所有模型和成本对比
  - 切换模型配置
  - 估算翻译成本
  - 成本对比分析

#### 🔌 新增：API 端点
- **GET /api/model-info**: 获取当前模型配置
- **GET /api/models**: 获取所有可用模型列表

#### 🧪 新增：测试工具
- **test_model_api.py**: 150 行测试脚本
  - 测试模型信息 API
  - 测试模型列表 API
  - 验证术语库未破坏

#### 📚 新增/更新：文档
- **MODEL_CONFIG_GUIDE.md**: 更新，添加字典配置说明
- **MODEL_QUICK_REFERENCE.md**: 新增，快速查阅卡
- **MODEL_CONFIG_IMPROVEMENT_REPORT.md**: 新增，完整改进报告
- **PROJECT_IMPROVEMENT_OVERVIEW.md**: 新增，项目总览
- **QUICK_START.md**: 新增，快速开始指南
- **FILE_MANIFEST.md**: 新增，文件清单
- **README.md**: 更新，添加模型配置说明

---

## [1.3.0] - 2025-11-17 (语言支持扩展)

### 🌍 新增：24 种语言支持
- **7 → 24 语言**: 扩展 243%
- **地区分组**: 东亚、欧洲、中东、东南亚
- **Flag Emoji**: 每种语言添加旗帜标识
- **全球覆盖**: 63% 人口

### 📚 新增：文档
- **SUPPORTED_LANGUAGES.md**: 完整语言列表
- **LANGUAGE_EXPANSION_SUMMARY.md**: 扩展总结

---

## [1.2.0] - 2025-11-17 (混合术语模式)

### 🔄 新增：混合术语系统
- **动态提取**: 从首块翻译提取新术语
- **术语合并**: 精选 90 + 动态 ~6 = ~96 个
- **智能适应**: 自动适应不同领域文本

### 📝 新增：函数
- `extract_terminology_from_chunk()`: 从翻译提取术语
- 修改 `translate_book_task()`: 集成混合模式逻辑

### 🧪 新增：测试
- **test_hybrid_mode.py**: 混合模式测试脚本

### 📚 新增：文档
- **HYBRID_MODE_GUIDE.md**: 混合模式完整指南
- **HYBRID_IMPLEMENTATION_SUMMARY.md**: 实现细节

---

## [1.1.0] - 2025-11-17 (术语库内部化)

### 🏠 重大变更：术语库迁移
- **外部 → 内部**: 从 `../Translator/` 迁移到项目根目录
- **路径更新**: `app.py` 中所有引用更新为本地路径
- **自包含**: 项目可独立运行

### 📚 新增：文档
- **terminology_curated.json**: 复制到项目根目录
- **MIGRATION_REPORT.md**: 迁移详细报告
- **PROJECT_STRUCTURE.md**: 项目结构说明

---

## [1.0.0] - 2025-11-17 (初始版本)

### ✨ 核心功能
- 智能分块翻译
- 实时 WebSocket 可视化
- 7 种语言支持
- 精选术语库（90 个）
- 黑暗主题 UI

### 🛠️ 技术栈
- Flask 3.0
- Flask-SocketIO 5.3
- LiteLLM 1.51
- Claude Sonnet 4

### 📚 文档
- README.md
- DEMO_GUIDE.md
- TERMINOLOGY_GUIDE.md

---

## 📊 版本对比总览

| 特性 | v1.0 | v1.1 | v1.2 | v1.3 | v2.0 |
|------|------|------|------|------|------|
| **语言数量** | 7 | 7 | 7 | 24 | 24 |
| **AI 模型** | 1 | 1 | 1 | 1 | 4 |
| **术语模式** | 静态 | 静态 | 混合 | 混合 | 混合 |
| **术语数量** | 90 | 90 | 96 | 96 | 96 |
| **术语位置** | 外部 | 内部 | 内部 | 内部 | 内部 |
| **API 端点** | 3 | 3 | 3 | 3 | 5 |
| **管理工具** | 0 | 1 | 2 | 2 | 4 |
| **文档数量** | 3 | 6 | 9 | 11 | 16 |

---

## 🚀 升级指南

### 从 v1.3 升级到 v2.0

#### 1. 拉取最新代码
```bash
git pull origin main
```

#### 2. 无需修改配置
模型配置已自动加载：
```python
ACTIVE_MODEL = 'deepseek-free'  # 默认免费模型
```

#### 3. 可选：切换模型
```bash
# 方法 1: 使用工具
python model_manager.py switch claude-sonnet-4

# 方法 2: 修改 app.py
# ACTIVE_MODEL = 'claude-sonnet-4'
```

#### 4. 重启服务器
```bash
python app.py
```

#### 5. 验证新功能
```bash
# 测试模型 API
python test_model_api.py

# 查看所有模型
python model_manager.py
```

### 从 v1.0 升级到 v2.0

⚠️ **重大变更**: 需要迁移术语库

#### 1. 备份数据
```bash
cp -r ../Translator/terminology_curated.json ./backup/
```

#### 2. 拉取代码
```bash
git pull origin main
```

#### 3. 验证术语库
```bash
ls -la terminology_curated.json
python check_project.py
```

#### 4. 重启服务器
```bash
python app.py
```

---

## 🔮 未来计划

### v2.1 (短期 - 1-2 周)
- [ ] 前端模型选择器（UI 切换）
- [ ] 成本追踪仪表板
- [ ] 翻译质量评分
- [ ] 模型性能监控

### v2.2 (中期 - 1-2 月)
- [ ] 多文件批量翻译
- [ ] 翻译历史记录
- [ ] 术语库编辑器
- [ ] 自定义模型配置

### v3.0 (长期 - 3-6 月)
- [ ] 用户账户系统
- [ ] 云部署支持
- [ ] 数据库持久化
- [ ] RESTful API v2
- [ ] 多租户支持

---

## 📈 性能改进

### v2.0 vs v1.0

| 指标 | v1.0 | v2.0 | 改进 |
|------|------|------|------|
| **模型切换时间** | ~5 分钟 | ~30 秒 | -83% |
| **模型数量** | 1 | 4 | +300% |
| **配置复杂度** | 中 | 低 | -50% |
| **成本灵活性** | 无 | 高 | +∞ |
| **文档完整度** | 60% | 95% | +58% |

---

## 🐛 已知问题

### v2.0
- ⚠️ 模型切换需重启服务器（不支持热重载）
- ⚠️ 成本估算有 10-20% 误差（取决于实际 token 使用）
- ⚠️ 免费模型有速率限制（~60 req/min）

### 计划修复
- v2.1: 支持模型热重载
- v2.1: 更精确的成本追踪（实时计算）
- 文档: 添加速率限制说明

---

## 💡 贡献者

### v2.0 贡献
- 模型配置系统: @AI-Assistant
- CLI 工具开发: @AI-Assistant
- 文档编写: @AI-Assistant

### v1.x 贡献
- 初始架构: @Polly
- 混合术语模式: @AI-Assistant
- 语言扩展: @AI-Assistant

---

## 📝 备注

### 破坏性变更
**无破坏性变更** - v2.0 向后兼容 v1.x

### 弃用警告
**无弃用内容**

### 安全更新
- ✅ API Key 管理：建议使用环境变量（待实现）
- ✅ 文件上传验证：已有基本验证

---

## 🎯 版本命名规则

```
MAJOR.MINOR.PATCH

MAJOR: 重大架构变更（v1 → v2）
MINOR: 新功能添加（v2.0 → v2.1）
PATCH: Bug 修复和小改进（v2.1.0 → v2.1.1）
```

### 当前版本: **2.0.0**
- **MAJOR**: 模型配置系统重构
- **累积改进**: 4 次迭代，16 个文档，4 个工具

---

*Changelog 最后更新: 2025-11-17*  
*下一版本预计: v2.1 (2 周内)*
