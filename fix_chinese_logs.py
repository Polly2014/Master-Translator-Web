#!/usr/bin/env python3
"""
批量替换 app.py 中的中文日志为英文
"""

import re

# 定义所有需要替换的中文日志对照表
replacements = [
    # translate_chunk_web 函数
    (r'开始翻译块', 'Starting chunk'),
    (r'输入大小:', 'Input size:'),
    (r'字符', 'characters'),
    (r'Demo 模式：使用小块快速展示', 'Demo mode: Using small chunks for quick demonstration'),
    (r'使用 \{len\(terminology\)\} 个术语保持一致性', r'Using {len(terminology)} terms for consistency'),
    (r'📚 使用', r'📚 Using'),
    (r'个术语保持一致性', r'terms for consistency'),
    
    # 进度日志
    (r'正在接收翻译\.\.\.', 'Receiving translation...'),
    (r'块 ', r'Chunk '),
    (r' 完成:', r' completed:'),
    (r'翻译失败:', r'translation failed:'),
    
    # translate_book_task 函数
    (r'开始翻译任务', 'Starting translation task'),
    (r'文件:', 'File:'),
    (r'目标语言:', 'Target language:'),
    (r'已加载精选术语库:', r'Loaded curated terminology:'),
    (r'个术语', r'terms'),
    (r'混合模式：将在首块翻译后动态提取新术语', 'Hybrid mode: Will extract new terms dynamically after first chunk'),
    (r'术语数据库未找到，将使用纯动态提取模式', 'Terminology database not found, will use pure dynamic extraction mode'),
    (r'用户选择不使用术语数据库', 'User chose not to use terminology database'),
    
    # 术语提取
    (r'正在从首块提取新术语\.\.\.', 'Extracting new terms from first chunk...'),
    (r'提取到', r'Extracted'),
    (r'个新术语（总计:', r'new terms (total:'),
    (r'个新术语（Total:', r'new terms (total:'),
    (r'）', r')'),
    (r'新增:', 'New:'),
    (r'示例:', 'Sample:'),
    (r'首块术语已全部覆盖，无需补充', 'First chunk terms already covered, no supplement needed'),
    
    # 保存和完成
    (r'已保存进度', 'Progress saved'),
    (r'翻译完成！', 'Translation completed!'),
    (r'总计:', 'Total:'),
    (r'用时:', 'Time elapsed:'),
    (r'秒', 'seconds'),
    (r'翻译失败:', 'Translation failed:'),
    
    # WebSocket 日志（控制台输出）
    (r'客户端已连接', 'Client connected'),
    (r'客户端已断开', 'Client disconnected'),
    (r'客户端加入房间:', 'Client joined room:'),
]

def fix_chinese_logs(input_file, output_file):
    """替换文件中的中文日志"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 应用所有替换
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 替换完成！")
    print(f"📝 输入文件: {input_file}")
    print(f"📝 输出文件: {output_file}")
    print(f"🔍 共应用 {len(replacements)} 个替换规则")

if __name__ == '__main__':
    input_file = 'app.py'
    output_file = 'app.py'  # 直接覆盖原文件
    
    # 可以先备份
    import shutil
    backup_file = 'app.py.backup'
    shutil.copy(input_file, backup_file)
    print(f"💾 已创建备份: {backup_file}")
    
    fix_chinese_logs(input_file, output_file)
    print("\n✨ 所有中文日志已替换为英文！")
    print("🔄 如果需要恢复，运行: cp app.py.backup app.py")
