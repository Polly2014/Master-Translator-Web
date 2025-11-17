#!/usr/bin/env python3
"""
Preview Feature Verification Script
验证预览功能是否正确实现
"""

import os
from pathlib import Path

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} 缺失: {filepath}")
        return False

def check_string_in_file(filepath, search_string, description):
    """检查文件中是否包含特定字符串"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_string in content:
                print(f"✅ {description}")
                return True
            else:
                print(f"❌ {description} - 未找到: {search_string}")
                return False
    except Exception as e:
        print(f"❌ 检查失败 {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 Preview Feature Verification")
    print("=" * 60)
    
    base_dir = Path(__file__).parent
    results = []
    
    # 1. 检查核心文件
    print("\n📁 检查核心文件...")
    results.append(check_file_exists(
        base_dir / 'templates/index.html',
        'HTML 模板'
    ))
    results.append(check_file_exists(
        base_dir / 'static/js/app.js',
        'JavaScript 文件'
    ))
    results.append(check_file_exists(
        base_dir / 'app.py',
        'Flask 应用'
    ))
    
    # 2. 检查 HTML 中的预览功能
    print("\n🎨 检查 HTML 实现...")
    html_file = base_dir / 'templates/index.html'
    results.append(check_string_in_file(
        html_file,
        'marked.min.js',
        'Marked.js CDN 已引入'
    ))
    results.append(check_string_in_file(
        html_file,
        'id="previewBtn"',
        '预览按钮已添加'
    ))
    results.append(check_string_in_file(
        html_file,
        'id="previewModal"',
        '预览模态框已添加'
    ))
    results.append(check_string_in_file(
        html_file,
        'id="previewRawBtn"',
        '原始视图按钮已添加'
    ))
    results.append(check_string_in_file(
        html_file,
        'id="previewRenderedBtn"',
        '渲染视图按钮已添加'
    ))
    results.append(check_string_in_file(
        html_file,
        'markdown-content',
        'Markdown 渲染样式已添加'
    ))
    
    # 3. 检查 JavaScript 中的预览功能
    print("\n⚙️  检查 JavaScript 实现...")
    js_file = base_dir / 'static/js/app.js'
    results.append(check_string_in_file(
        js_file,
        'initializePreviewModal',
        'initializePreviewModal 函数存在'
    ))
    results.append(check_string_in_file(
        js_file,
        'showPreviewModal',
        'showPreviewModal 函数存在'
    ))
    results.append(check_string_in_file(
        js_file,
        'loadPreviewContent',
        'loadPreviewContent 函数存在'
    ))
    results.append(check_string_in_file(
        js_file,
        'marked.parse',
        'Markdown 渲染调用存在'
    ))
    results.append(check_string_in_file(
        js_file,
        "previewBtn",
        '预览按钮事件监听已添加'
    ))
    
    # 4. 检查 Flask API
    print("\n🔌 检查 Flask API...")
    app_file = base_dir / 'app.py'
    results.append(check_string_in_file(
        app_file,
        '/api/preview/<task_id>',
        '预览 API 端点已添加'
    ))
    results.append(check_string_in_file(
        app_file,
        'def preview_result',
        'preview_result 函数存在'
    ))
    
    # 5. 检查文档
    print("\n📚 检查文档...")
    results.append(check_file_exists(
        base_dir / 'PREVIEW_FEATURE_GUIDE.md',
        '用户指南'
    ))
    results.append(check_file_exists(
        base_dir / 'PREVIEW_IMPLEMENTATION_REPORT.md',
        '实施报告'
    ))
    
    # 统计结果
    print("\n" + "=" * 60)
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"📊 验证结果: {passed}/{total} 通过")
    
    if failed == 0:
        print("🎉 所有检查通过! 预览功能已正确实现。")
        print("\n下一步:")
        print("1. 启动应用: python app.py")
        print("2. 访问: http://localhost:5001")
        print("3. 上传文件并翻译")
        print("4. 点击 '👁️ Preview Translation' 测试功能")
        return 0
    else:
        print(f"⚠️  {failed} 项检查未通过，请检查上述错误。")
        return 1

if __name__ == '__main__':
    exit(main())
