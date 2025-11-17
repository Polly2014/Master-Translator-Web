#!/usr/bin/env python3
"""
快速测试模型配置 API
"""

import requests
import json

BASE_URL = 'http://localhost:5001'

def test_model_info():
    """测试获取当前模型信息"""
    print("\n" + "="*60)
    print("📊 测试 /api/model-info")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/api/model-info')
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                info = data['model_info']
                print(f"\n✅ 成功获取模型信息:")
                print(f"   活跃模型: {info['active_model']}")
                print(f"   模型名称: {info['model_name']}")
                print(f"   Max Tokens: {info['max_tokens']:,}")
                print(f"   Temperature: {info['temperature']}")
                print(f"   成本: ${info['cost_per_1k']:.4f}/1K chars")
                print(f"   描述: {info['description']}")
                print(f"   速度: {info['speed']}")
                print(f"   质量: {info['quality']}")
                return True
            else:
                print(f"\n❌ 失败: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"\n❌ HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到服务器")
        print("   请确保服务器正在运行: python app.py")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False


def test_models_list():
    """测试获取所有模型列表"""
    print("\n" + "="*60)
    print("📋 测试 /api/models")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/api/models')
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print(f"\n✅ 成功获取模型列表:")
                print(f"   当前活跃: {data['active_model']}")
                print(f"\n   可用模型:")
                
                for key, model in data['models'].items():
                    active = "← 当前" if key == data['active_model'] else ""
                    print(f"\n   📦 {key} {active}")
                    print(f"      名称: {model['name']}")
                    print(f"      描述: {model['description']}")
                    print(f"      成本: {model['cost']}")
                    print(f"      速度: {model['speed']}")
                    print(f"      质量: {model['quality']}")
                
                return True
            else:
                print(f"\n❌ 失败: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"\n❌ HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到服务器")
        print("   请确保服务器正在运行: python app.py")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False


def test_terminology():
    """测试术语库 API（确保未破坏现有功能）"""
    print("\n" + "="*60)
    print("📚 测试 /api/terminology (验证未破坏)")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/api/terminology')
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('terminology'):
                stats = data.get('stats', {})
                print(f"\n✅ 术语库正常:")
                print(f"   总术语数: {stats.get('total', 0)}")
                print(f"   模式: {data.get('mode', 'unknown')}")
                print(f"   描述: {data.get('description', '')}")
                return True
            else:
                print(f"\n⚠️  警告: 可能找不到术语库")
                return False
        else:
            print(f"\n❌ HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到服务器")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🧪 Master Translator Web - API 测试")
    print("="*60)
    
    results = []
    
    # 测试 1: 模型信息
    results.append(("Model Info", test_model_info()))
    
    # 测试 2: 模型列表
    results.append(("Models List", test_models_list()))
    
    # 测试 3: 术语库（验证未破坏）
    results.append(("Terminology", test_terminology()))
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status}  {name}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print(f"\n   通过: {passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n🎉 所有测试通过！模型配置系统工作正常。")
    else:
        print("\n⚠️  有测试失败，请检查服务器是否正在运行。")
        print("   启动命令: python app.py")
    
    print("\n" + "="*60)


if __name__ == '__main__':
    main()
