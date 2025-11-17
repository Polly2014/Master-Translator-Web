#!/usr/bin/env python3
"""
模型管理工具 - 快速查看和切换模型
"""

import json
from pathlib import Path

# 读取 app.py 中的模型配置
def show_models():
    """显示所有可用模型"""
    models = {
        'deepseek-free': {
            'name': 'tngtech/deepseek-r1t-chimera:free',
            'max_tokens': 16000,
            'cost_per_1k': 0.0,
            'description': '免费模型，适合 Demo 和开发测试',
            'speed': 'fast',
            'quality': 'good'
        },
        'claude-sonnet-4': {
            'name': 'anthropic/claude-sonnet-4',
            'max_tokens': 100000,
            'cost_per_1k': 0.01,
            'description': '最高质量，适合生产环境',
            'speed': 'medium',
            'quality': 'excellent'
        },
        'gpt-4o': {
            'name': 'openai/gpt-4o',
            'max_tokens': 100000,
            'cost_per_1k': 0.0067,
            'description': '平衡性能和成本',
            'speed': 'fast',
            'quality': 'excellent'
        },
        'deepseek-v3': {
            'name': 'deepseek/deepseek-chat',
            'max_tokens': 64000,
            'cost_per_1k': 0.0013,
            'description': '高性价比，适合大规模生产',
            'speed': 'very-fast',
            'quality': 'good'
        }
    }
    
    print("\n" + "="*80)
    print("🤖 可用 AI 模型列表")
    print("="*80)
    
    for key, config in models.items():
        print(f"\n📦 {key}")
        print(f"   名称: {config['name']}")
        print(f"   描述: {config['description']}")
        print(f"   最大 Tokens: {config['max_tokens']:,}")
        print(f"   成本: ${config['cost_per_1k']:.4f} / 1K chars")
        print(f"   速度: {config['speed']}")
        print(f"   质量: {config['quality']}")
    
    print("\n" + "="*80)


def get_current_model():
    """获取当前使用的模型"""
    app_file = Path(__file__).parent / 'app.py'
    
    if not app_file.exists():
        print("❌ 找不到 app.py")
        return None
    
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 ACTIVE_MODEL 配置
    import re
    match = re.search(r"ACTIVE_MODEL = ['\"]([^'\"]+)['\"]", content)
    
    if match:
        return match.group(1)
    return None


def switch_model(new_model):
    """切换模型"""
    valid_models = ['deepseek-free', 'claude-sonnet-4', 'gpt-4o', 'deepseek-v3']
    
    if new_model not in valid_models:
        print(f"❌ 无效的模型: {new_model}")
        print(f"✅ 有效模型: {', '.join(valid_models)}")
        return False
    
    app_file = Path(__file__).parent / 'app.py'
    
    if not app_file.exists():
        print("❌ 找不到 app.py")
        return False
    
    # 读取文件
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换 ACTIVE_MODEL
    import re
    new_content = re.sub(
        r"ACTIVE_MODEL = ['\"]([^'\"]+)['\"]",
        f"ACTIVE_MODEL = '{new_model}'",
        content
    )
    
    # 写回文件
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 已切换到模型: {new_model}")
    return True


def estimate_cost(chars, model_key):
    """估算翻译成本"""
    costs = {
        'deepseek-free': 0.0,
        'claude-sonnet-4': 0.01,
        'gpt-4o': 0.0067,
        'deepseek-v3': 0.0013
    }
    
    cost_per_1k = costs.get(model_key, 0)
    total_cost = (chars / 1000) * cost_per_1k
    
    return total_cost


def show_cost_comparison(chars):
    """显示成本对比"""
    print(f"\n翻译 {chars:,} 字符的成本对比:")
    print("-" * 60)
    
    models = {
        'deepseek-free': '免费版',
        'deepseek-v3': 'DeepSeek V3',
        'gpt-4o': 'GPT-4o',
        'claude-sonnet-4': 'Claude Sonnet 4'
    }
    
    for key, name in models.items():
        cost = estimate_cost(chars, key)
        if cost == 0:
            print(f"  {name:20s}: $0.00 (免费！) ✨")
        else:
            print(f"  {name:20s}: ${cost:.4f}")
    
    print("-" * 60)


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) == 1:
        # 显示当前模型和所有可用模型
        current = get_current_model()
        print(f"\n🎯 当前使用模型: {current}")
        show_models()
        
        # 显示成本对比（以 150K 字符为例）
        show_cost_comparison(150000)
        
        print("\n使用方法:")
        print("  查看所有模型: python model_manager.py")
        print("  切换模型: python model_manager.py switch <model-name>")
        print("  估算成本: python model_manager.py cost <字符数> <model-name>")
        print("\n示例:")
        print("  python model_manager.py switch deepseek-free")
        print("  python model_manager.py cost 150000 claude-sonnet-4")
        
    elif sys.argv[1] == 'switch' and len(sys.argv) == 3:
        # 切换模型
        new_model = sys.argv[2]
        if switch_model(new_model):
            print("\n⚠️  请重启服务器以应用更改:")
            print("  python app.py")
    
    elif sys.argv[1] == 'cost' and len(sys.argv) == 4:
        # 估算成本
        chars = int(sys.argv[2])
        model_key = sys.argv[3]
        cost = estimate_cost(chars, model_key)
        
        print(f"\n💰 成本估算:")
        print(f"  字符数: {chars:,}")
        print(f"  模型: {model_key}")
        print(f"  成本: ${cost:.4f}")
        
        if cost == 0:
            print("  🎉 这是免费模型！")
    
    else:
        print("❌ 无效的命令")
        print("\n使用方法:")
        print("  python model_manager.py")
        print("  python model_manager.py switch <model-name>")
        print("  python model_manager.py cost <字符数> <model-name>")


if __name__ == '__main__':
    main()
