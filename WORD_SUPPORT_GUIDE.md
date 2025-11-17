# Word 文档支持功能说明

## 功能概述
Master Translator Web 现已支持 Word (.docx) 文档作为输入！

## 实现方式

### 1. 后端改动
- **依赖包**: 
  - `python-docx`: 解析 Word 文档结构
  - `markdownify`: 辅助格式转换（可选）

- **转换函数** (`convert_docx_to_markdown`):
  - 提取段落文本
  - 识别标题层级 (Heading 1-6 → # - ######)
  - 保留表格结构（转换为 Markdown 表格）
  - 清理多余空行

- **上传接口更新**:
  - 支持 `.md` 和 `.docx` 文件类型
  - 自动检测文件类型并转换
  - 保存转换后的 Markdown 版本 (`{task_id}_converted.md`)
  - 返回转换提示信息

- **分析接口更新**:
  - 优先使用转换后的 Markdown 文件
  - 兼容原始 Markdown 上传

### 2. 前端改动
- 文件输入框 `accept` 属性: `.md,.docx`
- 上传区提示文字更新，标注支持 Word 文档

### 3. 转换特性
**支持的元素**:
- ✅ 标题 (Heading 1-6)
- ✅ 普通段落
- ✅ 表格（自动转换为 Markdown 表格）
- ✅ 文本格式保留（段落结构）

**已知限制**:
- ❌ 图片不会被提取（会忽略）
- ❌ 复杂格式（文本框、形状）会丢失
- ❌ 页眉页脚不会被包含
- ❌ 批注和修订不会保留

### 4. 使用流程
1. 上传 Word 文档 (.docx)
2. 系统自动转换为 Markdown
3. 提示 "✅ Word 文档已自动转换为 Markdown"
4. 后续流程与 Markdown 相同（分析→翻译→下载）

## 安装依赖
```bash
pip install python-docx markdownify
# 或使用 requirements.txt
pip install -r requirements.txt
```

## 测试建议
1. 准备测试 Word 文档（包含标题、段落、表格）
2. 上传并检查转换效果
3. 预览转换后的 Markdown
4. 完成翻译验证完整流程

## 潜在改进
- 支持图片提取（保存到 static 并引用）
- 支持更多格式（PDF、TXT）
- 添加转换预览步骤（用户确认后再翻译）
- 支持格式选项（是否保留表格、列表等）

---
**更新时间**: 2025-01-17  
**版本**: v1.1 - Word 支持
