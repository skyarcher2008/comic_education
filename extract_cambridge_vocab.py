#!/usr/bin/env python3
"""
从cambridge_english.py提取所有词汇，生成统一的词汇表用于prompt
"""

from cambridge_english import VOCABULARY, EnglishLevel

def extract_all_vocabulary():
    """提取所有级别的词汇，生成统一列表"""
    all_words = set()
    
    # 合并所有级别的词汇
    for level, words in VOCABULARY.items():
        all_words.update(words)
    
    # 排序并返回
    return sorted(list(all_words))

def generate_vocabulary_string():
    """生成用于prompt的词汇字符串"""
    words = extract_all_vocabulary()
    
    # 每行10个单词，格式化输出
    lines = []
    for i in range(0, len(words), 10):
        line_words = words[i:i+10]
        lines.append(", ".join(line_words))
    
    return "\n".join(lines)

def main():
    """主函数"""
    print("=== 剑桥少儿英语词汇表提取 ===")
    
    all_words = extract_all_vocabulary()
    print(f"总词汇量: {len(all_words)}")
    
    # 按级别统计
    for level, words in VOCABULARY.items():
        print(f"{level.value}: {len(words)}词")
    
    print("\n=== 词汇表格式化 ===")
    vocab_string = generate_vocabulary_string()
    print(vocab_string)
    
    # 保存到文件
    with open("cambridge_vocabulary_formatted.txt", "w", encoding="utf-8") as f:
        f.write(vocab_string)
    
    print(f"\n✅ 词汇表已保存到 cambridge_vocabulary_formatted.txt")
    print(f"📊 词汇统计: 总计 {len(all_words)} 个单词")

if __name__ == "__main__":
    main()
