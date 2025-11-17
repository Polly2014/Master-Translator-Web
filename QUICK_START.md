# 🚀 快速开始指南 - Master Translator Web

## ⚡ 5 分钟启动

### 1️⃣ 安装依赖
```bash
cd Master-Translator-Web
pip install -r requirements.txt
```

### 2️⃣ 启动服务
```bash
python app.py
```

### 3️⃣ 打开浏览器
```
http://localhost:5001
```

就这么简单！🎉

---

## 🎯 基础使用

### 上传文件
1. 拖拽 Markdown 文件到上传区，或点击选择
2. 选择目标语言（24种可选）
3. 勾选"使用混合术语模式"（推荐）
4. 点击"开始翻译"

### 实时查看
- **日志面板**: 实时滚动显示翻译过程
- **进度面板**: 显示当前进度和统计
- **分块列表**: 查看文本分块情况

### 下载结果
翻译完成后，点击"下载翻译文件"按钮

---

## 🤖 切换 AI 模型

### 方法 1: 图形化工具（推荐新手）
```bash
python model_manager.py
```

查看所有模型和成本对比，然后：
```bash
python model_manager.py switch claude-sonnet-4
```

### 方法 2: 直接修改（最快）
打开 `app.py`，找到第 70 行：
```python
ACTIVE_MODEL = 'deepseek-free'  # 改成你想要的模型
```

可选值：
- `'deepseek-free'` - 免费（Demo 推荐）
- `'claude-sonnet-4'` - 最高质量
- `'gpt-4o'` - 平衡选择
- `'deepseek-v3'` - 高性价比

修改后重启服务器：
```bash
python app.py
```

---

## 💰 成本估算

### 使用工具估算
```bash
# 估算翻译 150K 字符的成本
python model_manager.py cost 150000 claude-sonnet-4
```

### 成本速查表
| 文件大小 | DeepSeek Free | DeepSeek V3 | GPT-4o | Claude |
|---------|---------------|-------------|--------|--------|
| 50K 字符 | $0.00 | $0.07 | $0.34 | $0.50 |
| 150K 字符 | $0.00 | $0.20 | $1.00 | $1.50 |
| 300K 字符 | $0.00 | $0.39 | $2.01 | $3.00 |

---

## 📚 查看术语库

### 方法 1: Web UI
翻译页面点击"查看术语库"按钮

### 方法 2: API 查询
```bash
curl http://localhost:5001/api/terminology
```

### 方法 3: 直接查看文件
```bash
cat terminology_curated.json
```

---

## 🔍 查看模型信息

### 当前模型信息
```bash
curl http://localhost:5001/api/model-info
```

### 所有可用模型
```bash
curl http://localhost:5001/api/models
```

### 使用工具查看
```bash
python model_manager.py
```

---

## 🧪 运行测试

### 测试混合术语模式
```bash
python test_hybrid_mode.py
```

### 测试模型 API
```bash
# 确保服务器正在运行
python app.py

# 新终端运行测试
python test_model_api.py
```

### 验证项目完整性
```bash
python check_project.py
```

---

## ⚙️ 常用配置

### 修改端口
`app.py` 最后一行：
```python
socketio.run(app, host='0.0.0.0', port=5001, debug=True)
```

改成你想要的端口（避免冲突）

### 修改超时时间
`app.py` 第 78 行：
```python
TIMEOUT = 3600  # 秒（1小时）
```

### 修改分块大小
`app.py` 第 77 行：
```python
CHUNK_TARGET_SIZE = 110000  # 字符
```

---

## 🎬 Demo 演示建议

### 准备阶段
1. ✅ 使用免费模型（`deepseek-free`）
2. ✅ 准备测试文件（3-5 章，~20K 字符）
3. ✅ 勾选混合术语模式
4. ✅ 测试完整流程 1-2 次

### 演示步骤
1. **展示上传** - 拖拽文件，强调简单易用
2. **展示配置** - 24 种语言，混合术语模式
3. **展示实时性** - 日志流、进度条、分块列表
4. **展示结果** - 下载文件，对比原文

### 话术建议
```
"这是一个智能分块翻译系统，核心特点是：

1. 智能分块 - 自动识别章节边界，保持结构完整
2. 混合术语 - 精选术语库 + 动态提取，自适应文本
3. 实时可视化 - WebSocket 推送，全程透明
4. 多语言支持 - 24 种语言，覆盖全球 63% 人口
5. 灵活模型 - 4 个 AI 模型可选，一键切换

现在我演示一下翻译一本英文书到中文..."
```

---

## 🐛 常见问题

### Q1: 服务器启动失败
**A**: 检查端口是否被占用
```bash
lsof -i :5001  # 查看端口占用
```

修改端口或杀死占用进程

### Q2: 翻译失败
**A**: 检查 API Key 是否有效
```python
# app.py 第 36 行
OPENROUTER_API_KEY = "sk-or-v1-..."
```

### Q3: 模型切换不生效
**A**: 确保重启了服务器
```bash
# Ctrl+C 停止服务器
python app.py  # 重新启动
```

### Q4: 术语库不显示
**A**: 检查文件是否存在
```bash
ls -la terminology_curated.json
```

### Q5: 成本估算不准
**A**: 实际成本取决于：
- 输入 token 数量（原文 + 术语 + prompt）
- 输出 token 数量（译文）
- 模型定价

工具估算基于输入字符，实际可能有 10-20% 误差

---

## 📖 推荐阅读

### 新手必读
1. [README.md](README.md) - 项目总览
2. [MODEL_QUICK_REFERENCE.md](MODEL_QUICK_REFERENCE.md) - 模型速查卡

### 进阶阅读
3. [MODEL_CONFIG_GUIDE.md](MODEL_CONFIG_GUIDE.md) - 完整配置指南
4. [HYBRID_MODE_GUIDE.md](HYBRID_MODE_GUIDE.md) - 混合术语详解
5. [SUPPORTED_LANGUAGES.md](SUPPORTED_LANGUAGES.md) - 语言支持详情

### 开发者阅读
6. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构
7. [HYBRID_IMPLEMENTATION_SUMMARY.md](HYBRID_IMPLEMENTATION_SUMMARY.md) - 实现细节
8. [PROJECT_IMPROVEMENT_OVERVIEW.md](PROJECT_IMPROVEMENT_OVERVIEW.md) - 改进历史

---

## 🎯 最佳实践

### Demo 场景
```python
ACTIVE_MODEL = 'deepseek-free'  # 免费
```
- 文件大小: < 50K 字符
- 使用混合术语模式
- 准备备用方案（Claude）

### 开发测试
```python
ACTIVE_MODEL = 'deepseek-free'  # 免费
```
- 随意实验
- 快速迭代

### 生产环境（质量优先）
```python
ACTIVE_MODEL = 'claude-sonnet-4'  # 最高质量
```
- 重要文档
- 专业翻译
- 可接受成本

### 生产环境（成本优先）
```python
ACTIVE_MODEL = 'deepseek-v3'  # 高性价比
```
- 大规模翻译
- 成本敏感
- 质量要求 Good 级别

---

## 🔧 故障排查

### 检查清单
- [ ] Python 3.13+ 安装
- [ ] 依赖包已安装（`requirements.txt`）
- [ ] API Key 有效
- [ ] 端口 5001 未被占用
- [ ] `terminology_curated.json` 存在
- [ ] `uploads/` 和 `outputs/` 目录可写

### 验证命令
```bash
# 检查 Python 版本
python --version

# 验证依赖
pip list | grep -E "Flask|LiteLLM|SocketIO"

# 验证文件
python check_project.py

# 测试 API
python test_model_api.py
```

---

## 📞 获取帮助

### 查看日志
服务器日志会显示详细错误信息

### 文档索引
- [所有文档列表](PROJECT_IMPROVEMENT_OVERVIEW.md#文档体系)

### 工具帮助
```bash
python model_manager.py --help
```

---

## 🎊 开始使用吧！

```bash
# 1. 安装
pip install -r requirements.txt

# 2. 启动
python app.py

# 3. 访问
open http://localhost:5001

# 4. 翻译！
```

**祝你翻译愉快！** 🚀✨

---

*快速开始指南 v2.0*  
*更新: 2025-11-17*
