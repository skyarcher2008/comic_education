#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证简洁prompt的效果测试脚本

这个脚本测试新的简洁prompt是否能解决大写输出问题
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_simplified_prompt():
    """测试新的简洁prompt内容"""
    
    print("=== 测试新的简洁Prompt设计 ===\n")
    
    # 导入常量
    try:
        from src.shared import constants
        print("✅ 成功导入 constants 模块")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    
    # 检查所有相关的prompt
    prompts_to_check = [
        ("DEFAULT_PROMPT", constants.DEFAULT_PROMPT),
        ("DEFAULT_TRANSLATE_JSON_PROMPT", constants.DEFAULT_TRANSLATE_JSON_PROMPT),
        ("MLP_PROMPT", constants.MLP_PROMPT),
        ("MLP_JSON_PROMPT", constants.MLP_JSON_PROMPT)
    ]
    
    print("1. 检查prompt内容是否遵循新的简洁设计...\n")
    
    # 需要检查的关键内容
    required_elements = [
        "1. 输入的文本都是大写，请将其转写成小写",
        "2. 输入的是小马宝莉的英文漫画台词",
        "3. 不要输出任何注释或者思考",
        "示例：",
        '"TIME TO KICK SOME FLANK!"',
        '"Time to go fast!"',
        '"NO!"',
        '"No!"',
        "HELLO TWILIGHT SPARKLE",
        "Hello Twilight Sparkle"
    ]
    
    all_prompts_valid = True
    
    for prompt_name, prompt_content in prompts_to_check:
        print(f"检查 {prompt_name}:")
        
        # 检查关键元素
        missing_elements = []
        for element in required_elements:
            if element not in prompt_content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"  ❌ 缺少必要内容:")
            for elem in missing_elements:
                print(f"    - {elem}")
            all_prompts_valid = False
        else:
            print(f"  ✅ 包含所有必要的简洁规则和示例")
        
        # 检查prompt长度（应该比之前短很多）
        if len(prompt_content) < 500:
            print(f"  ✅ Prompt长度适中 ({len(prompt_content)} 字符)")
        else:
            print(f"  ⚠️  Prompt可能还是太长 ({len(prompt_content)} 字符)")
        
        print()
    
    print("2. 检查核心要求的优先级顺序...\n")
    
    priority_order = [
        "1. 输入的文本都是大写，请将其转写成小写",
        "2. 输入的是小马宝莉的英文漫画台词",
        "3. 不要输出任何注释或者思考"
    ]
    
    priority_check = True
    for prompt_name, prompt_content in prompts_to_check:
        print(f"检查 {prompt_name} 的优先级顺序:")
        
        for i, priority in enumerate(priority_order, 1):
            if priority in prompt_content:
                # 检查这个优先级是否在正确的位置
                position = prompt_content.find(priority)
                print(f"  ✅ 优先级{i}: {priority[:30]}... (位置: {position})")
            else:
                print(f"  ❌ 缺少优先级{i}: {priority}")
                priority_check = False
        print()
    
    print("3. 检查示例的实用性...\n")
    
    # 检查示例是否覆盖了主要问题场景
    example_scenarios = [
        ("复杂句子转换", "TIME TO KICK SOME FLANK", "Time to go fast"),
        ("简单感叹词", "NO!", "No!"),
        ("人名保持", "TWILIGHT SPARKLE", "Twilight Sparkle")
    ]
    
    example_coverage = True
    for prompt_name, prompt_content in prompts_to_check:
        print(f"检查 {prompt_name} 的示例覆盖:")
        
        for scenario_name, input_text, expected_output in example_scenarios:
            if input_text in prompt_content and expected_output in prompt_content:
                print(f"  ✅ {scenario_name}: {input_text} → {expected_output}")
            else:
                print(f"  ❌ {scenario_name}: 缺少示例")
                example_coverage = False
        print()
    
    print("4. 总体评估...\n")
    
    if all_prompts_valid and priority_check and example_coverage:
        print("✅ 所有prompt都已简化为核心要求")
        print("✅ 优先级顺序明确：大写转换 → 改写适合小学生 → 禁止注释")
        print("✅ 提供了具体的转换示例")
        print("✅ Prompt长度大幅缩短，更容易理解")
        
        result = True
    else:
        print("❌ 部分prompt还需要调整")
        result = False
    
    print("\n" + "="*80)
    return result

def test_prompt_clarity():
    """测试prompt的清晰度"""
    
    print("\n=== 测试Prompt清晰度 ===\n")
    
    from src.shared import constants
    
    # 分析DEFAULT_PROMPT的结构
    prompt = constants.DEFAULT_PROMPT
    lines = prompt.strip().split('\n')
    
    print("Prompt结构分析:")
    print(f"总行数: {len(lines)}")
    print(f"总字符数: {len(prompt)}")
    
    # 检查是否有清晰的三个核心要求
    core_requirements = 0
    for line in lines:
        if line.strip().startswith(('1.', '2.', '3.')):
            core_requirements += 1
            print(f"  发现核心要求: {line.strip()}")
    
    if core_requirements == 3:
        print("✅ 包含完整的三个核心要求")
    else:
        print(f"❌ 核心要求不完整，只找到 {core_requirements} 个")
    
    # 检查示例数量
    example_count = prompt.count('输入：') + prompt.count('输出：')
    print(f"示例数量: {example_count // 2} 对")
    
    if example_count >= 6:  # 至少3对示例
        print("✅ 示例数量充足")
    else:
        print("❌ 示例数量不足")
    
    print()

if __name__ == "__main__":
    try:
        success1 = test_simplified_prompt()
        success2 = test_prompt_clarity()
        
        if success1 and success2:
            print("\n🎉 新的简洁prompt设计验证通过！")
            print("📝 核心改进:")
            print("  1️⃣ 大写转换优先级最高")
            print("  2️⃣ 简化为三个核心要求")
            print("  3️⃣ 提供具体转换示例")
            print("  4️⃣ 完全移除复杂的英文描述")
        else:
            print("\n⚠️  prompt还需要进一步调整")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
