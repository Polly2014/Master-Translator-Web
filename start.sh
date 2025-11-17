#!/bin/bash

echo "=================================================="
echo "🚀 Master Translator Web - 快速启动"
echo "=================================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python"
    exit 1
fi

echo "✅ Python3 已安装"

# 检查依赖
echo ""
echo "📦 检查依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  依赖未安装，正在安装..."
    pip3 install -r requirements.txt
else
    echo "✅ 依赖已安装"
fi

# 创建必要目录
mkdir -p uploads outputs
echo "✅ 目录已创建"

# 启动服务
echo ""
echo "=================================================="
echo "🎯 启动服务器..."
echo "=================================================="
echo ""
echo "📡 访问地址: http://localhost:5000"
echo "🔧 按 Ctrl+C 停止服务"
echo ""

python3 app.py
