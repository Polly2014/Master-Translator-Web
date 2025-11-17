#!/usr/bin/env python3
"""
测试自适应分块功能
"""

# 模拟配置
CHUNK_TARGET_SIZE = 110000

def plan_chunks_test(content_len):
    """测试分块规划"""
    
    # 自适应分块大小
    chunk_size = CHUNK_TARGET_SIZE
    
    if content_len < 30000:
        chunk_size = max(2000, content_len // 3)
        print(f"📊 小文件模式: {content_len:,} 字符 → 块大小 {chunk_size:,}")
    elif content_len < 60000:
        chunk_size = max(15000, content_len // 2)
        print(f"📊 中等文件模式: {content_len:,} 字符 → 块大小 {chunk_size:,}")
    else:
        print(f"📊 大文件模式: {content_len:,} 字符 → 块大小 {chunk_size:,}")
    
    # 计算分块数量
    num_chunks = max(1, (content_len + chunk_size - 1) // chunk_size)
    avg_chunk_size = content_len / num_chunks
    
    print(f"   → 预计分成 {num_chunks} 块，平均每块 {avg_chunk_size:,.0f} 字符")
    print()
    
    return num_chunks

print("=" * 60)
print("🧪 自适应分块测试")
print("=" * 60)
print()

# 测试不同大小的文件
test_cases = [
    ("Mustafa_Book_Demo.md", 6874),
    ("Quick Demo", 5000),
    ("Standard Demo", 15000),
    ("Medium Book", 45000),
    ("Full Book Chapter", 80000),
    ("Large Book", 150000),
]

for name, size in test_cases:
    print(f"📄 {name}")
    plan_chunks_test(size)

print("=" * 60)
print("✅ 测试完成")
print("=" * 60)
print()
print("💡 规则说明:")
print("   • 文件 < 30K: 分成约 3 块（块大小 = 文件大小 / 3）")
print("   • 文件 30K-60K: 分成约 2 块（块大小 = 文件大小 / 2）")
print("   • 文件 > 60K: 使用标准块大小 110K")
print()
print("🎯 目标: 小文件也能展示完整的分块翻译和术语提取流程")
