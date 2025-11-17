# Master Translator Web

🚀 **智能分块翻译系统 - Hackathon Demo 版**

一个基于 Flask + WebSocket 的实时翻译可视化平台，展示 AI 驱动的长文本智能分块翻译。

![Master Translator Web Screenshot](Snapshot.png)

## ✨ 核心特性

- 🧠 **智能分块** - 按章节边界自动分割超长文本（3级fallback策略）
- 🌍 **24种语言支持** - 覆盖全球63%人口，按地区分组展示
- 📊 **实时可视化** - WebSocket 推送翻译进度和日志流
- 🔄 **混合术语模式** - 精选术语库 + 首块动态提取（90+术语）
- 🎨 **炫酷界面** - 科技感黑暗主题 + 实时动画效果
- ⚡ **流式翻译** - 实时显示 AI 生成过程
- 👁️ **浏览器预览** - 双视图模式（原始/渲染），无需下载即可查看 ✨新功能
- 📄 **Word 文档支持** - 自动转换 .docx 为 Markdown ✨新功能

## 🎯 Demo 展示流程

1. **上传文件** - 拖拽或点击上传 Markdown (.md) 或 Word (.docx) 文件
2. **智能分析** - 自动识别章节结构并规划分块
3. **实时翻译** - 流式展示翻译进度和日志
4. **预览结果** - 浏览器内即时查看翻译（双视图模式） ✨新功能
5. **下载结果** - 一键下载完整翻译文件

一个基于 Flask + WebSocket 的实时翻译可视化平台，展示 AI 驱动的长文本智能分块翻译。

## ✨ 核心特性

- 🧠 **智能分块** - 按章节边界自动分割超长文本（3级fallback策略）
- 📊 **实时可视化** - WebSocket 推送翻译进度和日志流
- � **混合术语模式** - 精选术语库 + 首块动态提取（90+术语）
- 🎨 **炫酷界面** - 科技感黑暗主题 + 实时动画效果
- ⚡ **流式翻译** - 实时显示 AI 生成过程

## 🎯 Demo 展示流程

1. **上传文件** - 拖拽或点击上传 Markdown 文件
2. **智能分析** - 自动识别章节结构并规划分块
3. **实时翻译** - 流式展示翻译进度和日志
4. **下载结果** - 一键下载完整翻译文件

## 🛠️ 技术栈

- **后端**: Flask 3.0 + Flask-SocketIO 5.3 + LiteLLM 1.51
- **前端**: Tailwind CSS + Socket.IO Client + Vanilla JS
- **AI 模型**: 4个可选模型（字典化配置，一键切换）
  - DeepSeek R1T Chimera (免费，当前) ✨
  - Claude Sonnet 4 (最高质量)
  - GPT-4o (平衡选择)
  - DeepSeek V3 (高性价比)
- **实时通信**: WebSocket
- **Python**: 3.13+

## 🤖 AI 模型配置

系统采用**统一字典管理**，支持 4 个模型快速切换：

```python
# app.py 中的配置
ACTIVE_MODEL = 'deepseek-free'  # 修改这里切换模型
```

| 模型 | 成本/1K | 最佳用途 |
|------|---------|----------|
| deepseek-free | $0.00 ✨ | Demo/开发 |
| deepseek-v3 | $0.0013 | 生产性价比 |
| gpt-4o | $0.0067 | 平衡选择 |
| claude-sonnet-4 | $0.0100 | 最高质量 |

**管理工具**:
```bash
# 查看所有模型
python model_manager.py

# 切换模型
python model_manager.py switch claude-sonnet-4

# 估算成本
python model_manager.py cost 150000 claude-sonnet-4
```

详见：[MODEL_CONFIG_GUIDE.md](MODEL_CONFIG_GUIDE.md) | [快速参考](MODEL_QUICK_REFERENCE.md)

## 📦 快速启动

### 1. 安装依赖

```bash
cd Master-Translator-Web
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python app.py
```

### 3. 访问界面

打开浏览器访问: **http://localhost:5000**

## 📂 项目结构

```
Master-Translator-Web/
├── app.py                      # Flask 主应用
├── requirements.txt            # Python 依赖
├── terminology_curated.json    # 术语数据库（157个精选术语）
├── templates/
│   └── index.html             # 主页面
├── static/
│   └── js/
│       └── app.js             # 前端交互逻辑
├── uploads/                   # 上传文件目录
├── outputs/                   # 翻译结果目录
└── docs/
    ├── README.md              # 项目文档
    ├── DEMO_GUIDE.md          # Demo 演示指南
    └── TERMINOLOGY_GUIDE.md   # 术语库使用指南
```

## 🎨 界面预览

```
┌─────────────────────────────────────────────────────────┐
│           Master Translator - 智能分块翻译系统           │
├──────────┬─────────────────────────────┬────────────────┤
│          │                             │                │
│  上传区  │      实时日志流（滚动）      │   进度面板    │
│  配置区  │    📊 INFO ℹ️ SUCCESS ✅    │   统计信息    │
│  分块列表│    ⚠️  WARN ❌ ERROR        │   下载区      │
│          │                             │                │
└──────────┴─────────────────────────────┴────────────────┘
```

## 🚀 Hackathon Demo 要点

### 展示亮点

1. **视觉冲击** - 黑暗科技风 + 实时动画
2. **智能分块** - 自动识别章节边界（展示算法能力）
3. **实时推送** - WebSocket 流式日志（展示技术实力）
4. **用户体验** - 拖拽上传 + 进度可视化

### Demo 脚本建议

```
1. 打开界面 → "这是我们的智能翻译平台"
2. 拖拽上传 → "支持超大文件，自动分析章节结构"
3. 点击分析 → "看，系统识别了X个章节，智能分成Y块"
4. 开始翻译 → "实时展示 AI 翻译过程，每一条日志都是真实的"
5. 展示进度 → "双层进度条，可以看到整体和当前块的进度"
6. 完成下载 → "翻译完成，一键下载结果"
```

## 🔧 配置说明

### API Key

在 `app.py` 中配置 OpenRouter API Key:

```python
# 使用环境变量方式（推荐）
export OPENROUTER_API_KEY="sk-or-v1-xxxxxxxx"

# 或在项目根目录创建 .env （参考 .env.example）
# OPENROUTER_API_KEY=sk-or-v1-xxxxxxxx

# 代码中不再硬编码：app.py 会从 os.environ 读取 OPENROUTER_API_KEY
```

### 支持的语言

- 日语 (Japanese)
- 俄语 (Russian)
- 阿拉伯语 (Arabic)
- 印地语 (Hindi)
- 法语 (French)
- 西班牙语 (Spanish)
- 德语 (German)

### 分块参数

```python
CHUNK_TARGET_SIZE = 110000      # 每块目标大小（字符）
CONTEXT_PARAGRAPHS = 2          # 上下文段落数
OVERLAP_CHECK_CHARS = 200       # 重叠检查字符数
```

## 📊 性能指标

- **文件大小**: 支持最大 50MB
- **翻译速度**: ~100-500 chars/s（取决于模型）
- **实时延迟**: <100ms（WebSocket）
- **并发支持**: 单任务（Demo 版）

## 📚 完整文档

### 核心功能
- 📖 [预览功能使用指南](PREVIEW_FEATURE_GUIDE.md) - 浏览器内预览翻译结果 ✨新功能
- 📊 [Demo 文件指南](DEMO_FILES_GUIDE.md) - 快速演示文件使用说明
- 🔧 [术语功能指南](TERMINOLOGY_GUIDE.md) - 术语数据库使用详解

### 模型配置
- 🤖 [模型配置指南](MODEL_CONFIG_GUIDE.md) - 完整的模型管理文档
- ⚡ [模型快速参考](MODEL_QUICK_REFERENCE.md) - 一键切换模型指南
- 📈 [模型配置改进报告](MODEL_CONFIG_IMPROVEMENT_REPORT.md) - 技术实现细节

### 技术报告
- 🎯 [预览功能实施报告](PREVIEW_IMPLEMENTATION_REPORT.md) - 完整技术架构
- 🎬 [预览功能演示指南](PREVIEW_DEMO_GUIDE.md) - 演示脚本和培训建议
- 📝 [预览功能完成总结](PREVIEW_SUMMARY.md) - 项目总结和验收

### 验证工具
- ✅ [Demo 文件验证](verify_demo_files.py) - Demo 文件验证脚本
- 🔍 [预览功能验证](verify_preview_feature.py) - 预览功能验证脚本（18项检查）

## 🎯 TODO (生产版)

- [ ] 多任务并发处理
- [ ] 用户认证系统
- [ ] 历史记录管理
- [ ] 暂停/继续功能
- [ ] 成本估算
- [ ] 多文件批处理

## 📝 注意事项

1. **Demo 版限制** - 单任务处理，重启服务会丢失任务
2. **API 成本** - 使用 Claude Sonnet 4，注意 API 费用
3. **文件存储** - uploads/ 和 outputs/ 目录需要定期清理

## 🙏 致谢

基于 `script_v3_chunked.py` 的核心翻译逻辑改造而成。

---

**Made with ❤️ for Hackathon Demo** 🚀
