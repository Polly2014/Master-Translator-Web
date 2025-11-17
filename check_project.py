#!/usr/bin/env python3
"""
快速验证脚本 - 检查项目完整性
"""

import sys
from pathlib import Path
import json

def check_file(path, name, required=True):
    """检查文件是否存在"""
    if path.exists():
        size = path.stat().st_size
        print(f"✅ {name:30s} ({size:,} bytes)")
        return True
    else:
        status = "❌" if required else "⚠️ "
        print(f"{status} {name:30s} - NOT FOUND")
        return False

def check_directory(path, name, create=True):
    """检查目录是否存在"""
    if path.exists():
        print(f"✅ {name:30s} (directory)")
        return True
    elif create:
        path.mkdir(parents=True, exist_ok=True)
        print(f"🔧 {name:30s} - CREATED")
        return True
    else:
        print(f"❌ {name:30s} - NOT FOUND")
        return False

def validate_terminology():
    """验证术语库格式"""
    term_file = Path(__file__).parent / 'terminology_curated.json'
    
    if not term_file.exists():
        return False
    
    try:
        with open(term_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total = sum(len(v) for v in data.values() if isinstance(v, list))
        print(f"   📚 Total terms: {total}")
        
        for category, terms in data.items():
            if isinstance(terms, list):
                print(f"      - {category}: {len(terms)} terms")
        
        return True
    except Exception as e:
        print(f"   ❌ Invalid JSON: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 Master-Translator-Web Project Validation")
    print("=" * 60)
    print()
    
    # 获取项目根目录
    project_root = Path(__file__).parent
    print(f"📁 Project Root: {project_root.resolve()}")
    print()
    
    # 核心文件检查
    print("📄 Core Files:")
    all_ok = True
    all_ok &= check_file(project_root / 'app.py', 'app.py')
    all_ok &= check_file(project_root / 'requirements.txt', 'requirements.txt')
    all_ok &= check_file(project_root / 'terminology_curated.json', 'terminology_curated.json')
    print()
    
    # 术语库验证
    print("📚 Terminology Database:")
    validate_terminology()
    print()
    
    # 模板文件检查
    print("🎨 Templates:")
    all_ok &= check_file(project_root / 'templates' / 'index.html', 'templates/index.html')
    print()
    
    # 静态文件检查
    print("📦 Static Assets:")
    all_ok &= check_file(project_root / 'static' / 'js' / 'app.js', 'static/js/app.js')
    check_file(project_root / 'static' / 'css' / 'style.css', 'static/css/style.css', required=False)
    print()
    
    # 文档检查
    print("📖 Documentation:")
    check_file(project_root / 'README.md', 'README.md')
    check_file(project_root / 'DEMO_GUIDE.md', 'DEMO_GUIDE.md')
    check_file(project_root / 'TERMINOLOGY_GUIDE.md', 'TERMINOLOGY_GUIDE.md')
    check_file(project_root / 'PROJECT_STRUCTURE.md', 'PROJECT_STRUCTURE.md')
    print()
    
    # 运行时目录检查
    print("📂 Runtime Directories:")
    check_directory(project_root / 'uploads', 'uploads/', create=True)
    check_directory(project_root / 'outputs', 'outputs/', create=True)
    check_directory(project_root / 'venv', 'venv/', create=False)
    print()
    
    # 总结
    print("=" * 60)
    if all_ok:
        print("✅ All required files present!")
        print("🚀 Ready for demo. Run: python app.py")
        return 0
    else:
        print("❌ Some required files are missing!")
        print("⚠️  Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
