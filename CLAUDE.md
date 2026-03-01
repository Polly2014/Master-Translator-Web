# CLAUDE.md — Master-Translator-Web

## Project Overview

**Master Translator Web** 是 Master-Translator 翻译系统的 **Web Demo 界面**，基于 Flask + Socket.IO 构建，提供实时文档翻译体验。

- **定位**: Hackathon / 苏州Demo 展示用 Web 界面
- **上游依赖**: 通过 CopilotX 远程代理 (`api.polly.wang`) 调用多种 LLM 模型
- **核心能力**: 文档上传 → 智能分块 → 多模型翻译 → 实时流式输出 → 结果预览/下载

## Commands

```bash
# 快速启动
cd Master-Translator-Web
source venv/bin/activate     # 或创建: python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py                # http://localhost:5001

# 一键启动脚本
bash start.sh

# 模型管理
python model_manager.py                    # 查看当前模型和所有可用模型
python model_manager.py switch gpt-4o      # 切换模型（需重启服务）

# 测试
python test_model_api.py                   # 测试 API 连通性
python test_hybrid_mode.py                 # 测试混合术语模式
python test_adaptive_chunking.py           # 测试自适应分块
```

## Architecture

```
Master-Translator-Web/
├── app.py                    # 🎯 Flask 主应用 (1064 行单文件)
│                             #    ├─ 翻译配置 (CopilotX API, 模型字典)
│                             #    ├─ 分块配置 (Demo/生产模式)
│                             #    ├─ 核心函数 (DOCX转换, 章节提取, 分块规划)
│                             #    ├─ 翻译引擎 (LiteLLM 流式调用)
│                             #    ├─ Flask 路由 (REST API)
│                             #    └─ WebSocket 事件 (Socket.IO)
│
├── model_manager.py          # 模型查看/切换 CLI 工具
├── terminology_curated.json  # 精选术语数据库 (proper_nouns + technical_terms)
│
├── templates/
│   └── index.html            # 前端单页 (Tailwind CSS + Socket.IO)
├── static/
│   └── js/app.js             # 前端交互逻辑 (文件上传, 进度, 预览)
│
├── demo_files/               # Demo 专用文件
│   ├── Mustafa_Book_Quick_Demo.md   # Ultra Quick (~20-30s, 3 chunks)
│   └── Mustafa_Book_Demo.md         # Standard (~3-5min)
│
├── uploads/                  # 上传文件 (runtime)
├── outputs/                  # 翻译结果 (runtime)
│
├── .env                      # 环境变量 (gitignored)
├── .env.example              # 环境变量模板
├── requirements.txt          # Python 依赖
├── start.sh                  # 快速启动脚本
└── venv/                     # Python 虚拟环境 (gitignored)
```

## API Reference

### REST Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | 主页 (index.html) |
| `POST` | `/api/upload` | 上传文件 (.md / .docx)，返回 task_id |
| `POST` | `/api/analyze/<task_id>` | 分析文件，规划分块 |
| `POST` | `/api/translate/<task_id>` | 启动翻译（后台线程） |
| `GET` | `/api/status/<task_id>` | 查询任务状态 |
| `GET` | `/api/download/<task_id>` | 下载翻译结果 .md |
| `GET` | `/api/preview/<task_id>` | 预览翻译结果 |
| `GET` | `/api/preview-source/<task_id>` | 预览源文件 |
| `GET` | `/api/preview-chunk/<task_id>/<chunk_id>` | 预览特定 chunk |
| `GET` | `/api/terminology` | 获取术语数据库 |
| `GET` | `/api/model-info` | 当前模型配置 |
| `GET` | `/api/models` | 所有可用模型列表 |

### WebSocket Events (Socket.IO)

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Client→Server | 建立连接 |
| `join` | Client→Server | 加入任务房间 `{task_id}` |
| `log` | Server→Client | 翻译日志 (info/success/error/warning/progress) |
| `progress` | Server→Client | 进度更新 (overall%, chunk%, current/total) |

## Configuration

### LLM API (CopilotX)

通过 CopilotX 远程代理调用 GitHub Copilot 模型，**所有模型免费**。

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `COPILOTX_BASE_URL` | `https://api.polly.wang` | CopilotX 代理地址 |
| `COPILOTX_API_KEY` | (见 .env) | 远程访问密钥 |

### 可用模型

| Key | 模型名 | 速度 | 质量 | 场景 |
|-----|--------|------|------|------|
| `gpt-4o` | gpt-4o | fast | excellent | **Demo 首选** |
| `claude-sonnet-4` | claude-sonnet-4 | medium | excellent | 翻译质量极佳 |
| `claude-sonnet-4.5` | claude-sonnet-4.5 | medium | excellent | 最新旗舰 |
| `o3-mini` | o3-mini | fast | excellent | 推理增强 |
| `gemini-2.0-flash` | gemini-2.0-flash | very-fast | good | 超快速度 |

切换模型: 修改 `app.py` 中 `ACTIVE_MODEL` 变量，或运行 `python model_manager.py switch <model>`。

### Demo 模式 vs 生产模式

| 参数 | Demo 模式 | 生产模式 |
|------|----------|----------|
| `CHUNK_TARGET_SIZE` | 800 chars | 110,000 chars |
| `CONTEXT_PARAGRAPHS` | 1 | 2 |
| `OVERLAP_CHECK_CHARS` | 100 | 200 |
| 适用场景 | 快速演示 (~20-30s) | 大文档翻译 |

切换: 修改 `app.py` 中 `DEMO_MODE = True/False`。

## Translation Pipeline

```
用户上传文件 (.md/.docx)
        │
        ▼
    [文件解析] ── .docx → Markdown 自动转换
        │
        ▼
    [章节提取] ── 识别 # / ## 标题结构
        │
        ▼
    [智能分块] ── 按章节 + 目标大小规划 chunks
        │
        ▼
    [逐块翻译] ── LiteLLM → CopilotX → LLM
        │           ├─ 流式输出 (SSE → Socket.IO)
        │           ├─ 术语一致性 (curated + dynamic)
        │           └─ 上下文延续 (前一块末尾段落)
        ▼
    [增量保存] ── 每块完成即保存
        │
        ▼
    [结果合并] ── 全文拼接 → .md 下载/预览
```

### 混合术语模式 (Hybrid)

1. **精选术语** (`terminology_curated.json`): 人名、技术术语、组织名等
2. **动态提取**: 翻译第 1 块后，自动从译文中提取新术语
3. **后续块**: 合并精选 + 动态术语，确保全文一致性

## Supported Languages

20+ 语言，覆盖东亚、欧洲、中东、东南亚语系。主要:
- 中文(简/繁)、日语、韩语
- 法语、德语、西班牙语、俄语
- 阿拉伯语、泰语、越南语

## Key Implementation Details

- **LLM 调用**: 使用 `litellm.completion()` 统一接口，`model="openai/{MODEL}"` + `api_base=COPILOTX_BASE_URL`
- **流式输出**: 翻译结果通过 Socket.IO 实时推送到前端
- **后台翻译**: `threading.Thread` 避免阻塞 Flask 主线程
- **文件格式**: 支持 `.md` 直接读取和 `.docx` 自动转换 (python-docx + markdownify)
- **前端**: Tailwind CSS 单页应用，Socket.IO 客户端，Marked.js 渲染 Markdown 预览

## Relationship to Other Projects

```
Master-Translator-MCP-Server/  (核心翻译引擎, 12 MCP tools)
        │
        ├── Master-Translator-Web/  ← 本项目 (Web Demo 界面)
        │       └── CopilotX (api.polly.wang) 提供 LLM API
        │
        ├── Code4Paper_v2/  (实验验证代码)
        ├── Paper/  (学术论文)
        └── Patent/  (专利申请)
```
