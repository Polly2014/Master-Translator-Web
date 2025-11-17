#!/usr/bin/env python3
"""
测试 LLM 输出清洗功能
"""

import re

def clean_llm_artifacts(text):
    """
    清理 LLM 输出中的推理过程、思考标签等无关内容
    """
    if not text:
        return text
    
    original_text = text
    
    # 1. 移除 <think>...</think> 标签及其内容（DeepSeek R1）
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # 2. 移除 <reasoning>...</reasoning> 标签及其内容
    text = re.sub(r'<reasoning>.*?</reasoning>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # 3. 移除 <thought>...</thought> 标签及其内容
    text = re.sub(r'<thought>.*?</thought>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # 4. 移除开头的推理说明（常见模式）
    # 先尝试匹配到分隔线
    if '---' in text or '___' in text:
        reasoning_with_divider = [
            r'^.*?(?:Here\'s my reasoning|Let me think|My thought process|Thinking process):.*?(?=\n+---)',
            r'^.*?(?:I will translate|Let me translate|Translation process):.*?(?=\n+---)',
        ]
        for pattern in reasoning_with_divider:
            match = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)
            if match:
                text = text[match.end():]
                # 移除开头的空白行和分隔线
                text = re.sub(r'^\s*\n+---+\s*\n+', '', text)
                break
    
    # 如果没有分隔线，匹配到双换行
    if text.startswith(('Here', 'Let me', 'I will', 'My thought', 'Thinking')):
        reasoning_patterns = [
            r'^.*?(?:Here\'s my reasoning|Let me think|My thought process|Thinking process):.*?(?=\n\n)',
            r'^.*?(?:I will translate|Let me translate|Translation process):.*?(?=\n\n)',
        ]
        for pattern in reasoning_patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
            break
    
    # 5. 如果有明确的 "Translation:" 标记，只保留其后的内容
    translation_markers = [
        r'^.*?Translation:\s*\n',
        r'^.*?翻译结果[：:]\s*\n',
        r'^.*?Translated text:\s*\n',
        r'^.*?Final translation:\s*\n',
    ]
    for marker in translation_markers:
        match = re.search(marker, text, flags=re.DOTALL | re.IGNORECASE)
        if match:
            text = text[match.end():]
            break
    
    # 6. 移除开头和结尾的大量空白
    text = text.strip()
    
    # 7. 移除开头的代码块标记（如果被包裹在 markdown 代码块中）
    text = re.sub(r'^```(?:markdown|md|text)?\s*\n', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\n```\s*$', '', text)
    
    # 8. 移除末尾的总结性评论（常见于某些模型）
    summary_patterns = [
        r'\n---+\s*\n.*?(?:Note|Summary|Explanation):.*$',
        r'\n\n---+\s*\n.*$',  # 分隔线后的所有内容
    ]
    for pattern in summary_patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # 最终清理
    text = text.strip()
    
    # 如果清理后内容为空或过短（可能误删），返回原文
    if len(text) < 50 and len(original_text) > 100:
        return original_text
    
    return text


# ============ 测试用例 ============

def test_think_tags():
    """测试 <think> 标签清理"""
    input_text = """<think>
这是一本关于人工智能的技术书籍。我需要注意以下几点：
1. 保持专业术语的准确性
2. 维护上下文的连贯性
</think>

# 即将到来的浪潮

几乎每个文化都有洪水神话。"""
    
    expected = """# 即将到来的浪潮

几乎每个文化都有洪水神话。"""
    
    result = clean_llm_artifacts(input_text)
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    print("✅ Test 1: <think> tags - PASSED")


def test_translation_marker():
    """测试 Translation: 标记清理"""
    input_text = """I will translate this text from English to Chinese.

Translation:

# 即将到来的浪潮

几乎每个文化都有洪水神话。"""
    
    expected = """# 即将到来的浪潮

几乎每个文化都有洪水神话。"""
    
    result = clean_llm_artifacts(input_text)
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    print("✅ Test 2: Translation marker - PASSED")


def test_reasoning_prefix():
    """测试推理前缀清理"""
    input_text = """Here's my reasoning:
This is a technical book about AI, so I need to maintain consistency...

---

# 即将到来的浪潮

几乎每个文化都有洪水神话。"""
    
    expected = """# 即将到来的浪潮

几乎每个文化都有洪水神话。"""
    
    result = clean_llm_artifacts(input_text)
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    print("✅ Test 3: Reasoning prefix - PASSED")


def test_markdown_code_block():
    """测试 Markdown 代码块清理"""
    input_text = """```markdown
# 即将到来的浪潮

几乎每个文化都有洪水神话。
```"""
    
    expected = """# 即将到来的浪潮

几乎每个文化都有洪水神话。"""
    
    result = clean_llm_artifacts(input_text)
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    print("✅ Test 4: Markdown code block - PASSED")


def test_summary_note():
    """测试末尾总结清理"""
    input_text = """# 即将到来的浪潮

几乎每个文化都有洪水神话。

---

Note: This translation maintains the formal tone and technical accuracy."""
    
    expected = """# 即将到来的浪潮

几乎每个文化都有洪水神话。"""
    
    result = clean_llm_artifacts(input_text)
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    print("✅ Test 5: Summary note - PASSED")


def test_clean_text():
    """测试干净文本（无需清理）"""
    input_text = """# 即将到来的浪潮

几乎每个文化都有洪水神话。

在古代印度教文本中，我们宇宙中的第一个人玛努被警告即将到来的洪水。"""
    
    result = clean_llm_artifacts(input_text)
    assert result == input_text, f"Expected:\n{input_text}\n\nGot:\n{result}"
    print("✅ Test 6: Clean text - PASSED")


def test_chinese_translation_marker():
    """测试中文翻译标记清理"""
    input_text = """分析完成。

翻译结果：

# 即将到来的浪潮

几乎每个文化都有洪水神话。"""
    
    expected = """# 即将到来的浪潮

几乎每个文化都有洪水神话。"""
    
    result = clean_llm_artifacts(input_text)
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    print("✅ Test 7: Chinese translation marker - PASSED")


def test_safety_mechanism():
    """测试安全机制（防止误删）"""
    input_text = "短内容"
    
    result = clean_llm_artifacts(input_text)
    assert result == input_text, f"Expected:\n{input_text}\n\nGot:\n{result}"
    print("✅ Test 8: Safety mechanism - PASSED")


def test_complex_case():
    """测试复杂情况（多种混合）"""
    input_text = """<think>
Let me analyze this carefully...
I need to maintain consistency with terminology.
</think>

Here's my reasoning:
This is chapter 1 of a technical book.

---

Translation:

```markdown
# 第一章：遏制是不可能的

## 浪潮

几乎每个文化都有洪水神话。
```"""
    
    expected = """# 第一章：遏制是不可能的

## 浪潮

几乎每个文化都有洪水神话。"""
    
    result = clean_llm_artifacts(input_text)
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    print("✅ Test 9: Complex case - PASSED")


# ============ 运行所有测试 ============

if __name__ == '__main__':
    print("\n🧪 Testing LLM Artifact Cleaning Function\n")
    print("=" * 60)
    
    try:
        test_think_tags()
        test_translation_marker()
        test_reasoning_prefix()
        test_markdown_code_block()
        test_summary_note()
        test_clean_text()
        test_chinese_translation_marker()
        test_safety_mechanism()
        test_complex_case()
        
        print("=" * 60)
        print("\n✅ All tests PASSED! (9/9)\n")
        
    except AssertionError as e:
        print("=" * 60)
        print(f"\n❌ Test FAILED:\n{e}\n")
        exit(1)
