#!/usr/bin/env python3
"""
验证 Demo 文件的字数和结构
"""

from pathlib import Path
import re

def count_words(text):
    """统计英文单词数"""
    # 移除 Markdown 标记
    text = re.sub(r'[#*`\-\[\]]', ' ', text)
    # 统计单词
    words = text.split()
    return len(words)

def count_paragraphs(text):
    """统计段落数"""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return len([p for p in paragraphs if not p.startswith('#')])

def count_chapters(text):
    """统计章节数"""
    return len(re.findall(r'^## CHAPTER', text, re.MULTILINE))

def analyze_demo_file(file_path):
    """分析 Demo 文件"""
    if not file_path.exists():
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {
        'file': file_path.name,
        'size': len(content),
        'words': count_words(content),
        'paragraphs': count_paragraphs(content),
        'chapters': count_chapters(content),
        'lines': len(content.split('\n'))
    }

def main():
    """主函数"""
    print("\n" + "="*70)
    print("📊 Demo 文件验证")
    print("="*70)
    
    demo_dir = Path(__file__).parent / 'demo_files'
    
    files = [
        demo_dir / 'Mustafa_Book_Quick_Demo.md',
        demo_dir / 'Mustafa_Book_Demo.md'
    ]
    
    results = []
    for file_path in files:
        result = analyze_demo_file(file_path)
        if result:
            results.append(result)
    
    if not results:
        print("\n❌ 未找到 Demo 文件")
        return
    
    # 显示结果
    print("\n📁 文件统计:")
    print("-" * 70)
    
    for result in results:
        print(f"\n📄 {result['file']}")
        print(f"   文件大小: {result['size']:,} bytes")
        print(f"   单词数: {result['words']:,} words")
        print(f"   段落数: {result['paragraphs']} paragraphs")
        print(f"   章节数: {result['chapters']} chapters")
        print(f"   行数: {result['lines']} lines")
        
        # 估算翻译时间
        if result['words'] < 200:
            time_est = "60-90 秒"
            speed = "⚡ 超快速"
        elif result['words'] < 1000:
            time_est = "3-5 分钟"
            speed = "🚀 快速"
        else:
            time_est = "10+ 分钟"
            speed = "📚 标准"
        
        print(f"   估算时间: {time_est}")
        print(f"   速度等级: {speed}")
    
    # 对比表格
    print("\n" + "="*70)
    print("📊 对比表格")
    print("="*70)
    print(f"\n{'文件':<30} {'单词':<10} {'章节':<8} {'时间'}")
    print("-" * 70)
    
    for result in results:
        name = result['file'].replace('Mustafa_Book_', '').replace('.md', '')
        words = f"{result['words']} words"
        chapters = f"{result['chapters']} 章"
        
        if result['words'] < 200:
            time = "60-90秒"
        elif result['words'] < 1000:
            time = "3-5分钟"
        else:
            time = "10+分钟"
        
        print(f"{name:<30} {words:<10} {chapters:<8} {time}")
    
    # 建议
    print("\n" + "="*70)
    print("💡 使用建议")
    print("="*70)
    
    for result in results:
        name = result['file']
        
        if 'Quick' in name:
            print(f"\n⚡ {name}")
            print("   适用场景: 超快速演示，初次展示，注意力有限")
            print("   优点: 60-90秒完成，即时反馈，观众不会分心")
        else:
            print(f"\n📚 {name}")
            print("   适用场景: 标准演示，功能展示，技术细节")
            print("   优点: 3-5分钟完成，多章节，展示分块能力")
    
    print("\n" + "="*70)
    print("✅ 验证完成！")
    print("="*70)
    
    # 快速启动命令
    print("\n🚀 快速启动:")
    print("   1. python app.py")
    print("   2. open http://localhost:5001")
    print("   3. 上传 demo_files/Mustafa_Book_Quick_Demo.md")
    print("   4. 选择中文，勾选混合术语模式")
    print("   5. 点击\"开始翻译\"")
    print("\n   60-90 秒后完成！🎉")
    print()

if __name__ == '__main__':
    main()
