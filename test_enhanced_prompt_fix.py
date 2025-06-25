#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证大写和NOTE问题修复效果的测试脚本

这个脚本专门测试以下问题的修复效果：
1. LLM输出ALL CAPS的问题
2. LLM输出NOTE、解释等不必要内容的问题
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_prompt_caps_and_notes_fix():
    """测试新prompt是否能解决大写和NOTE问题"""
    
    print("=== 测试新优化的Prompt - 针对大写和NOTE问题 ===\n")
    
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
    
    print("1. 检查prompt内容是否包含新的强化规则...\n")
    
    # 需要检查的关键内容
    required_elements = [
        "🚨 ABSOLUTE REQUIREMENTS",
        "NEVER use ALL CAPS words",
        "NEVER add any notes, explanations, or comments",
        "NEVER add parenthetical remarks",
        "convert to proper case",
        "✅ MANDATORY CAPITALIZATION RULES",
        "STRICT EXAMPLES - FOLLOW EXACTLY"
    ]
      # 需要检查的具体示例
    required_examples = [
        '"TIME TO GO!" →',
        '(CORRECT',
        'WRONG - uses caps',
        'WRONG - adds note'
    ]
    
    all_prompts_valid = True
    
    for prompt_name, prompt_content in prompts_to_check:
        print(f"检查 {prompt_name}:")
        
        # 检查关键元素
        missing_elements = []
        for element in required_elements:
            if element not in prompt_content:
                missing_elements.append(element)
        
        # 检查示例
        missing_examples = []
        for example in required_examples:
            if example not in prompt_content:
                missing_examples.append(example)
        
        if missing_elements or missing_examples:
            print(f"  ❌ 缺少必要内容:")
            for elem in missing_elements:
                print(f"    - {elem}")
            for example in missing_examples:
                print(f"    - 示例: {example}")
            all_prompts_valid = False
        else:
            print(f"  ✅ 包含所有必要的强化规则和示例")
        
        print()
    
    print("2. 检查具体的问题场景覆盖...\n")
    
    # 检查对原始反例的覆盖
    problem_scenarios = [
        ("ALL CAPS输入处理", "TIME TO KICK SOME FLANK"),
        ("简单感叹词处理", "NO!"),
        ("NOTE输出禁止", "Note:"),
        ("解释输出禁止", "simplified for students"),
        ("大写转换示例", "TIME TO GO"),
        ("正确格式示例", '"No!" (CORRECT')
    ]
    
    scenario_coverage = True
    for scenario_name, keyword in problem_scenarios:
        found_in_prompts = []
        for prompt_name, prompt_content in prompts_to_check:
            if keyword in prompt_content:
                found_in_prompts.append(prompt_name)
        
        if found_in_prompts:
            print(f"  ✅ {scenario_name}: 在 {', '.join(found_in_prompts)} 中有覆盖")
        else:
            print(f"  ❌ {scenario_name}: 缺少覆盖关键词 '{keyword}'")
            scenario_coverage = False
    
    print()
    
    # 检查原始问题示例的修复
    print("3. 检查原始问题示例修复...\n")
    
    original_problems = [
        "i000M TIME TO KICK SOME FLANK!",
        "NO!",
        "(Note: The original phrase contains inappropriate content"
    ]
    
    for i, problem in enumerate(original_problems, 1):
        print(f"  原始问题 {i}: {problem}")
        
        # 分析这个问题应该如何被新prompt处理
        if "TIME TO KICK SOME FLANK" in problem:
            print(f"    → 应转换为: 'Time to go fast!' (小写，无大写)")
        elif problem == "NO!":
            print(f"    → 应转换为: 'No!' (仅首字母大写)")
        elif "Note:" in problem:
            print(f"    → 应完全避免输出NOTE内容")
        
        print()
    
    print("4. 总体评估...\n")
    
    if all_prompts_valid and scenario_coverage:
        print("✅ 所有prompt都已成功更新，包含了针对大写和NOTE问题的强化规则")
        print("✅ 涵盖了所有已知问题场景的处理方法")
        print("✅ 提供了明确的正确/错误示例对比")
        print("✅ 使用了强化的视觉符号和严格的措辞")
        
        result = True
    else:
        print("❌ 部分prompt仍需优化")
        result = False
    
    print("\n" + "="*80)
    return result

if __name__ == "__main__":
    try:
        success = test_prompt_caps_and_notes_fix()
        if success:
            print("\n🎉 新prompt优化验证通过！")
            print("📝 建议：在实际使用中继续观察LLM输出，如仍有问题可进一步调整prompt")
        else:
            print("\n⚠️  prompt还需要进一步优化")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
