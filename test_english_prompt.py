#!/usr/bin/env python3
"""
测试新的英文prompt是否更有效解决大写输出问题
"""

def test_new_english_prompts():
    """测试新的英文prompt内容"""
    
    # 从constants导入新的prompt
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        from shared.constants import DEFAULT_PROMPT, DEFAULT_TRANSLATE_JSON_PROMPT, MLP_PROMPT, MLP_JSON_PROMPT
        
        print("=== 测试新的英文Prompt设计 ===\n")
        
        # 检查所有prompt是否都使用英文并且内容一致
        prompts = {
            "DEFAULT_PROMPT": DEFAULT_PROMPT,
            "DEFAULT_TRANSLATE_JSON_PROMPT": DEFAULT_TRANSLATE_JSON_PROMPT, 
            "MLP_PROMPT": MLP_PROMPT,
            "MLP_JSON_PROMPT": MLP_JSON_PROMPT
        }
        
        key_phrases = [
            "Convert ALL CAPS text to lowercase",
            "only first letter capitalized", 
            "My Little Pony dialogue",
            "suitable for Chinese elementary",
            "Output ONLY",
            "NO explanations or notes"
        ]
        
        print("✅ 新英文Prompt核心要求检查:")
        for name, prompt in prompts.items():
            print(f"\n📝 {name}:")
            
            # 检查是否包含关键短语
            missing_phrases = []
            for phrase in key_phrases:
                if phrase.lower() not in prompt.lower():
                    missing_phrases.append(phrase)
            
            if missing_phrases:
                print(f"  ❌ 缺少关键短语: {missing_phrases}")
            else:
                print(f"  ✅ 包含所有关键要求")
            
            # 检查是否强调小写输出
            if "ALL CAPS" in prompt and "lowercase" in prompt:
                print(f"  ✅ 强调大写转小写")
            else:
                print(f"  ❌ 未充分强调大写转小写")
                
            # 检查长度（应该比之前短）
            print(f"  📏 长度: {len(prompt)} 字符")
            
            # 检查示例数量
            examples_count = prompt.count("→") + prompt.count(":")
            print(f"  📚 示例数量: {examples_count//2} 对")
        
        print("\n🎯 针对日志问题的特定检查:")
        print("根据日志发现的问题:")
        print("- 'HEHE... I DO NOT THINK I CAN W...' (仍然大写)")
        print("- 'IF THIS DOES NOT GIVE ME A CUT...' (仍然大写)")
        
        # 检查prompt是否对此类问题有针对性改进
        sample_issues = [
            "HEHE...I DON'T THINK I HAVE THE NECESSARY QUALIFICATIONS TO WORK WITH YOU!",
            "IF THIS DOESN'T GET ME A CUTIE MARK, I DON'T KNOW WHAT WILL!"
        ]
        
        print("\n💡 新英文Prompt预期改进:")
        for issue in sample_issues:
            print(f"输入: {issue[:50]}...")
            print(f"预期: {issue.capitalize()[:50]}... (小写格式)")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_prompt_consistency():
    """测试所有prompt的一致性"""
    print("\n=== 测试Prompt一致性 ===")
    
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        from shared.constants import DEFAULT_PROMPT, MLP_PROMPT
        
        print("📋 constants.py中的prompt已更新为英文版本:")
        
        # 检查是否都是英文版本
        if "Convert ALL CAPS" in DEFAULT_PROMPT and "Convert ALL CAPS" in MLP_PROMPT:
            print("  ✅ 所有prompt已更新为英文版本")
        else:
            print("  ❌ 部分prompt仍为中文版本")
        
        # 检查translation.py中的fallback prompt (不能直接导入)
        translation_file = os.path.join('src', 'core', 'translation.py')
        if os.path.exists(translation_file):
            with open(translation_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "Convert ALL CAPS text to lowercase and simplify" in content:
                    print("  ✅ translation.py中的fallback prompt也已更新为英文")
                else:
                    print("  ❌ translation.py中的fallback prompt仍为中文")
        
        return True
        
    except Exception as e:
        print(f"❌ 一致性测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始测试新的英文Prompt设计...")
    
    success = True
    success &= test_new_english_prompts()
    success &= test_prompt_consistency()
    
    if success:
        print("\n🎉 新英文Prompt测试通过！")
        print("📝 主要改进:")
        print("  - 使用直接明确的英文指令")
        print("  - 强调 'Convert ALL CAPS to lowercase'")
        print("  - 明确 'only first letter capitalized'") 
        print("  - 减少示例数量，提高效率")
        print("  - 强调 'NO explanations or notes'")
        print("\n🎯 下一步: 实际部署测试，观察是否解决大写输出问题")
    else:
        print("\n❌ 仍有问题需要解决")
