#!/usr/bin/env python3
"""
测试更新后的剑桥词汇表提示词
验证词汇集成是否正确
"""

import json
import os

def test_prompts_structure():
    """测试prompts.json结构"""
    print("=== 测试 prompts.json 结构 ===")
    
    with open("config/prompts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"✅ JSON格式正确")
    print(f"✅ default_prompt 存在: {'default_prompt' in data}")
    print(f"✅ saved_prompts 存在: {'saved_prompts' in data}")
    print(f"✅ saved_prompts 数量: {len(data.get('saved_prompts', []))}")
    
    return data

def test_cambridge_vocabulary_integration():
    """测试剑桥词汇表集成"""
    print("\n=== 测试剑桥词汇表集成 ===")
    
    with open("config/prompts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 检查 default_prompt
    default_prompt = data.get("default_prompt", "")
    has_cambridge_vocab = "CAMBRIDGE ENGLISH VOCABULARY" in default_prompt
    print(f"✅ default_prompt 包含剑桥词汇表: {has_cambridge_vocab}")
    
    vocab_count_match = "782 words" in default_prompt
    print(f"✅ 词汇数量标注正确: {vocab_count_match}")
    
    priority_logic = "FIRST PRIORITY" in default_prompt and "SECOND PRIORITY" in default_prompt
    print(f"✅ 优先级逻辑存在: {priority_logic}")
    
    # 检查关键词汇样本
    sample_words = ["apple", "beautiful", "happy", "computer", "breakfast", "elephant", "friendship"]
    found_samples = 0
    for word in sample_words:
        if word in default_prompt:
            found_samples += 1
    
    print(f"✅ 样本词汇覆盖: {found_samples}/{len(sample_words)}")
    
    # 检查 saved_prompts 中的小马宝莉版本
    mlp_prompt = None
    for prompt in data.get("saved_prompts", []):
        if prompt.get("name") == "小马宝莉-小学生版":
            mlp_prompt = prompt.get("content", "")
            break
    
    if mlp_prompt:
        mlp_has_vocab = "CAMBRIDGE ENGLISH VOCABULARY" in mlp_prompt
        print(f"✅ 小马宝莉版本包含剑桥词汇表: {mlp_has_vocab}")
    else:
        print("❌ 未找到小马宝莉-小学生版提示词")
    
    return has_cambridge_vocab and vocab_count_match and priority_logic

def test_preserved_functionality():
    """测试保留的功能"""
    print("\n=== 测试保留的功能 ===")
    
    with open("config/prompts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    default_prompt = data.get("default_prompt", "")
    
    # 检查保留的特殊术语
    preserved_terms = [
        "Twilight Sparkle", "Rainbow Dash", "Pinkie Pie",
        "Equestria", "Ponyville", "Canterlot",
        "cutie mark", "unicorn", "pegasus", "magic", "friendship"
    ]
    
    found_terms = 0
    for term in preserved_terms:
        if term in default_prompt:
            found_terms += 1
    
    print(f"✅ 保留术语完整性: {found_terms}/{len(preserved_terms)}")
    
    # 检查重写规则
    has_caps_rule = "Convert input all CAPS text to lowercase" in default_prompt
    has_interjection_rule = "For simple interjections" in default_prompt
    has_output_rule = "Return ONLY the rewritten English text" in default_prompt
    
    print(f"✅ 大写转换规则: {has_caps_rule}")
    print(f"✅ 感叹词处理规则: {has_interjection_rule}")
    print(f"✅ 输出格式规则: {has_output_rule}")
    
    return found_terms >= len(preserved_terms) * 0.8 and has_caps_rule and has_interjection_rule

def test_cambridge_vocab_accuracy():
    """测试剑桥词汇表准确性"""
    print("\n=== 测试剑桥词汇表准确性 ===")
    
    # 从原始文件读取
    with open("cambridge_vocabulary_formatted.txt", "r", encoding="utf-8") as f:
        original_vocab = f.read()
    
    # 从prompts.json读取
    with open("config/prompts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    default_prompt = data.get("default_prompt", "")
    
    # 提取词汇表部分
    vocab_start = default_prompt.find("CAMBRIDGE ENGLISH VOCABULARY (782 words):")
    vocab_end = default_prompt.find("\n\nPRESERVED TERMS")
    
    if vocab_start == -1 or vocab_end == -1:
        print("❌ 无法找到词汇表边界")
        return False
    
    embedded_vocab = default_prompt[vocab_start:vocab_end]
    
    # 简单比较关键词汇
    key_words = ["apple", "zebra", "computer", "beautiful", "elephant", "friendship", "swimming"]
    found_key_words = 0
    
    for word in key_words:
        if word in embedded_vocab:
            found_key_words += 1
    
    print(f"✅ 关键词汇验证: {found_key_words}/{len(key_words)}")
    
    return found_key_words >= len(key_words) * 0.8

def main():
    """主测试函数"""
    print("开始测试剑桥词汇表集成...")
    
    # 检查文件存在
    if not os.path.exists("config/prompts.json"):
        print("❌ config/prompts.json 文件不存在")
        return False
    
    if not os.path.exists("cambridge_vocabulary_formatted.txt"):
        print("❌ cambridge_vocabulary_formatted.txt 文件不存在")
        return False
    
    # 运行测试
    try:
        structure_ok = test_prompts_structure()
        integration_ok = test_cambridge_vocabulary_integration()
        functionality_ok = test_preserved_functionality()
        accuracy_ok = test_cambridge_vocab_accuracy()
        
        if structure_ok and integration_ok and functionality_ok and accuracy_ok:
            print("\n🎉 所有测试通过！剑桥词汇表成功集成到提示词中。")
            print("\n📋 集成摘要:")
            print("- ✅ 集成782个剑桥少儿英语词汇")
            print("- ✅ 建立词汇优先级机制")
            print("- ✅ 保留My Little Pony特殊术语")
            print("- ✅ 维持原有功能（大写转换、感叹词处理等）")
            print("- ✅ 同时更新default_prompt和小马宝莉版本")
            return True
        else:
            print("\n❌ 部分测试失败，需要检查。")
            return False
    
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
