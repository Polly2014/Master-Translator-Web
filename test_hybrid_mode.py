#!/usr/bin/env python3
"""
测试混合术语模式
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from app import load_terminology_db, extract_terminology_from_chunk

def test_hybrid_mode():
    print("=" * 60)
    print("🧪 Testing Hybrid Terminology Mode")
    print("=" * 60)
    print()
    
    # Step 1: 加载精选术语库
    print("📚 Step 1: Load Curated Database")
    curated_terms = load_terminology_db()
    
    if curated_terms:
        print(f"✅ Loaded {len(curated_terms)} curated terms")
        print(f"   Examples: {', '.join(curated_terms[:5])}...")
    else:
        print("⚠️  No curated database found, will use pure dynamic mode")
        curated_terms = []
    
    print()
    
    # Step 2: 模拟首块翻译
    print("📝 Step 2: Simulate First Chunk Translation")
    
    # 模拟源文本（英文）
    sample_source = """
    # INTRODUCTION
    
    This book explores the future of artificial intelligence and its impact on humanity.
    Written by Demis Hassabis and Shane Legg, two pioneers in the field of deep learning,
    it discusses breakthrough technologies like AlphaGo, AlphaFold, and neural architecture search.
    
    We will examine concepts such as meta-learning, few-shot learning, and transfer learning,
    as well as emerging fields like edge computing and quantum supremacy.
    
    The authors, both from Google DeepMind, share insights from years of research in
    reinforcement learning and computer vision.
    """
    
    # 模拟翻译文本（中文）
    sample_translation = """
    # 引言
    
    本书探讨人工智能的未来及其对人类的影响。
    由深度学习领域的两位先驱 Demis Hassabis 和 Shane Legg 撰写，
    讨论了 AlphaGo、AlphaFold 和神经架构搜索等突破性技术。
    
    我们将研究元学习、少样本学习和迁移学习等概念，
    以及边缘计算和量子霸权等新兴领域。
    
    两位作者均来自 Google DeepMind，分享了多年来在
    强化学习和计算机视觉方面的研究见解。
    """
    
    print(f"   Source length: {len(sample_source)} chars")
    print(f"   Translation length: {len(sample_translation)} chars")
    print()
    
    # Step 3: 动态提取术语
    print("🔍 Step 3: Extract New Terms from First Chunk")
    extracted_terms = extract_terminology_from_chunk(sample_translation, sample_source)
    
    print(f"✅ Extracted {len(extracted_terms)} terms:")
    for term in extracted_terms[:15]:  # 只显示前15个
        print(f"   - {term}")
    if len(extracted_terms) > 15:
        print(f"   ... and {len(extracted_terms) - 15} more")
    print()
    
    # Step 4: 合并术语
    print("🔄 Step 4: Merge Terms")
    
    # 过滤已存在的术语
    new_terms = [t for t in extracted_terms if t not in curated_terms]
    
    print(f"   Curated: {len(curated_terms)} terms")
    print(f"   Extracted: {len(extracted_terms)} terms")
    print(f"   New (not in curated): {len(new_terms)} terms")
    print()
    
    if new_terms:
        print(f"✨ New terms to be added:")
        for term in new_terms[:10]:
            print(f"   + {term}")
        if len(new_terms) > 10:
            print(f"   ... and {len(new_terms) - 10} more")
    else:
        print("✅ All extracted terms already in curated database!")
    
    print()
    
    # Step 5: 最终统计
    print("📊 Step 5: Final Statistics")
    final_terms = curated_terms + new_terms
    print(f"   Total terminology: {len(final_terms)} terms")
    print(f"   = {len(curated_terms)} curated + {len(new_terms)} extracted")
    print()
    
    # 结论
    print("=" * 60)
    print("✅ Hybrid Mode Test Complete!")
    print()
    print("Expected behavior in real translation:")
    print("1. Load 90 curated terms")
    print(f"2. Translate chunk 1 with curated terms")
    print(f"3. Extract ~{len(new_terms)} new terms from chunk 1")
    print(f"4. Use {len(final_terms)} total terms for chunks 2-30")
    print("=" * 60)

if __name__ == '__main__':
    test_hybrid_mode()
