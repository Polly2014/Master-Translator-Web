# Terminology Database Feature Guide

## 🎯 Overview

The Terminology Database is a curated collection of important terms that ensures translation consistency across all chunks of a long document.

---

## 📚 What is the Terminology Database?

Located at: `./terminology_curated.json` (in project root)

The database contains three categories of terms:

### 1. 👤 **Proper Nouns** (专有名词)
- Person names: "Mustafa Suleyman", "Demis Hassabis"
- Company names: "DeepMind", "OpenAI", "Google"
- Place names: "Silicon Valley", "London"
- Book titles: Specific publication names

**Translation Rule**: Keep in original English, do not translate

### 2. 🔧 **Technical Terms** (技术术语)
- AI terminology: "artificial intelligence", "machine learning", "neural network"
- Technology concepts: "algorithm", "model", "training", "inference"
- Domain-specific: "GPT", "transformer", "attention mechanism"

**Translation Rule**: Translate consistently, optionally add English in parentheses on first occurrence

### 3. 💡 **Key Concepts** (关键概念)
- Important domain concepts: "containment", "proliferation"
- Specialized terms: "synthetic biology", "biotechnology"
- Core ideas that need consistent translation

**Translation Rule**: Maintain exact same translation throughout all chunks

---

## ✅ Using Terminology Database (Checked - Default)

### What Happens:
1. **System loads** `terminology_curated.json` at translation start
2. **Logs show**: "📚 已加载 X 个术语" (Loaded X terms)
3. **AI receives** the term list in its prompt
4. **Translation enforces** consistency rules

### Prompt Enhancement:
```
<key_terminology>
CRITICAL: These important terms appeared in earlier chunks.
Please maintain EXACTLY the same translation for consistency:

artificial intelligence, machine learning, GPT, Mustafa Suleyman, ...

- Keep proper nouns (names, companies) in original English
- Use consistent translation for technical terms throughout
- When translating these terms, match the usage from previous chunks
</key_terminology>
```

### Benefits:
- ✅ **Consistency**: "AI" always translates the same way
- ✅ **Professionalism**: Proper nouns stay in English
- ✅ **Accuracy**: Technical terms maintain precision
- ✅ **Readability**: Reader isn't confused by varying translations

### Example:
**With Terminology Database:**
```
Chapter 1: "artificial intelligence" → "人工智能"
Chapter 5: "artificial intelligence" → "人工智能" (consistent!)
Chapter 10: "Mustafa Suleyman" → "Mustafa Suleyman" (kept in English)
```

---

## ⬜ Not Using Terminology Database (Unchecked)

### What Happens:
1. **System skips** loading terminology file
2. **Logs show**: "ℹ️ 用户选择不使用术语数据库" (User chose not to use terminology)
3. **AI translates** based purely on context
4. **No consistency enforcement**

### Benefits:
- ✅ **More Natural**: AI can choose contextually appropriate translations
- ✅ **Flexibility**: Not constrained by predefined terms
- ✅ **Faster**: Slightly less prompt overhead

### Drawbacks:
- ❌ **Inconsistency**: Same term may translate differently
- ❌ **Confusion**: Reader may not recognize recurring concepts
- ❌ **Less Professional**: Proper nouns might be translated

### Example:
**Without Terminology Database:**
```
Chapter 1: "artificial intelligence" → "人工智能"
Chapter 5: "artificial intelligence" → "AI" (inconsistent)
Chapter 10: "Mustafa Suleyman" → "穆斯塔法·苏莱曼" (translated, less recognizable)
```

---

## 📊 Viewing Terminology Details

### How to View:
1. Click the **📚 icon** next to "Use Terminology Database" checkbox
2. Modal window opens showing:
   - **Statistics**: Total terms, category counts
   - **Proper Nouns**: Names, companies, places
   - **Technical Terms**: AI/tech terminology
   - **Key Concepts**: Domain-specific terms

### Modal Features:
- **Category Cards**: Each category shown separately
- **Term Pills**: Visual display of all terms
- **Counts**: Shows how many terms per category
- **Scrollable**: Handle large terminology lists
- **Close**: Click X or outside modal to close

---

## 🎯 When to Use Which Option?

### ✅ Use Terminology Database When:
- Translating **technical books** (AI, science, tech)
- Working with **proper nouns** that should stay in English
- Need **professional consistency** for publication
- Translating **series or related documents**
- Multiple translators working on same project

### ⬜ Don't Use Terminology Database When:
- Translating **creative writing** (fiction, poetry)
- Want **maximum naturalness** over consistency
- Source has **no technical terms**
- Experimenting with **different translation styles**
- Terminology file doesn't match your content

---

## 🔧 Technical Implementation

### Backend (`app.py`):
```python
# Load terminology if enabled
if task.use_terminology:
    terminology = load_terminology_db()
    if terminology:
        task.emit_log(f"📚 已加载 {len(terminology)} 个术语", 'success')
else:
    task.emit_log(f"ℹ️ 用户选择不使用术语数据库", 'info')
    terminology = None
```

### Frontend (`app.js`):
```javascript
// Send user preference to backend
const useTerminology = document.getElementById('useTerminology').checked;

fetch(`/api/translate/${currentTaskId}`, {
    method: 'POST',
    body: JSON.stringify({ use_terminology: useTerminology })
})
```

### API Endpoint:
```
GET /api/terminology
Returns: {
    "terminology": {
        "proper_nouns": [...],
        "technical_terms": [...],
        "key_concepts": [...]
    },
    "stats": {
        "total": 150,
        "categories": {...}
    }
}
```

---

## 📝 Best Practices

### For Demo:
1. **Show the modal** - Let audience see what's in the database
2. **Explain the difference** - Briefly mention consistency vs. naturalness
3. **Keep it checked** - Default is usually best for demos
4. **Point out logs** - Show when terms are loaded

### For Production:
1. **Curate your terminology** - Customize for your domain
2. **Update regularly** - Add new terms as you encounter them
3. **Category organization** - Keep terms well-organized
4. **Review translations** - Verify AI respects the terminology

---

## 🎬 Demo Script Addition

When showing this feature:

```
"Before we translate, notice this checkbox: 'Use Terminology Database'.

[Click the 📚 icon]

This opens our curated list of 150+ important terms - proper nouns like 
'Mustafa Suleyman', technical terms like 'artificial intelligence', and 
key concepts. 

When enabled, the AI ensures these terms are translated consistently 
across all 30 chapters. For example, 'artificial intelligence' will 
always be '人工智能', never switching to just 'AI' halfway through.

This is crucial for professional book translation where consistency 
equals credibility.

[Close modal, keep checkbox checked, continue demo]
"
```

---

## 🔍 Troubleshooting

### "Terminology database not found"
- Check `./terminology_curated.json` exists in project root
- Verify file path in `app.py` line ~220
- Ensure proper JSON format

### Modal doesn't open
- Check browser console for errors
- Verify `/api/terminology` endpoint works
- Test with: `curl http://localhost:5001/api/terminology`

### Terms not being respected
- Verify checkbox is checked
- Check logs for "已加载 X 个术语"
- Review AI prompt construction in `translate_chunk_web()`

---

**Feature Status**: ✅ Fully Implemented  
**Testing**: Ready for Demo  
**Documentation**: Complete
