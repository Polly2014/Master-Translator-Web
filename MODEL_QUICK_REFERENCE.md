# 🎯 模型切换速查卡

## 一键切换（最快）

打开 `app.py`，找到第 70 行左右：

```python
ACTIVE_MODEL = 'deepseek-free'  # ← 修改这里
```

改成你想要的模型：

| 想切换到 | 修改为 | 成本 |
|---------|--------|------|
| **免费模型** | `'deepseek-free'` | $0.00 ✨ |
| **最高质量** | `'claude-sonnet-4'` | $0.01/1K |
| **OpenAI** | `'gpt-4o'` | $0.0067/1K |
| **高性价比** | `'deepseek-v3'` | $0.0013/1K |

保存后重启服务器：
```bash
python app.py
```

---

## 使用工具（推荐）

```bash
# 查看所有模型和当前配置
python model_manager.py

# 切换到 Claude（生产环境）
python model_manager.py switch claude-sonnet-4

# 切换到免费模型（Demo）
python model_manager.py switch deepseek-free

# 估算成本（150K 字符）
python model_manager.py cost 150000 claude-sonnet-4
```

---

## API 查询

```bash
# 当前模型信息
curl http://localhost:5001/api/model-info

# 所有可用模型
curl http://localhost:5001/api/models
```

---

## 场景推荐

| 场景 | 推荐模型 | 原因 |
|------|---------|------|
| 🎬 **Hackathon Demo** | `deepseek-free` | 免费、够用 |
| 🧪 **开发测试** | `deepseek-free` | 无限测试 |
| 🚀 **生产（质量优先）** | `claude-sonnet-4` | 最高质量 |
| 💰 **生产（成本优先）** | `deepseek-v3` | 性价比高 |
| ⚡ **快速翻译** | `deepseek-v3` | 最快速度 |

---

## 成本对比（150K 字符）

```
DeepSeek Free:   $0.00   ← Demo 首选！
DeepSeek V3:     $0.20   ← 生产性价比
GPT-4o:          $1.00
Claude Sonnet 4: $1.50   ← 最高质量
```

---

## 当前配置（2025-11-17）

✅ **活跃模型**: `deepseek-free`  
📊 **质量**: Good (8.5/10)  
💰 **成本**: $0.00  
🚀 **速度**: Fast  
🎯 **适用**: Demo / 开发  

---

*快速参考 - 保存此文件以便查阅*
