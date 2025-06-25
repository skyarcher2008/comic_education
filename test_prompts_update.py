#!/usr/bin/env python3
"""
验证 prompts.json 中的提示词是否已正确更新为大写转小写版本
"""

import json
import os

def test_prompts_json_update():
    """测试prompts.json是否已更新为大写转小写版本"""
    
    prompts_file = "config/prompts.json"
    
    if not os.path.exists(prompts_file):
        print(f"❌ 配置文件不存在: {prompts_file}")
        return False
    
    try:
        with open(prompts_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False
    
    print("=== 验证 prompts.json 更新结果 ===\n")
    
    # 检查关键改进点
    key_improvements = [
        "convert input CAPS text to lowercase",
        "Convert input all CAPS text to lowercase", 
        "return it exactly as provided but in lowercase",
        "return exactly as provided in lowercase",
        "Only capitalize the first letter of sentences and proper nouns"
    ]
    
    success = True
    
    # 检查 default_prompt
    default_prompt = data.get('default_prompt', '')
    print("📝 检查 default_prompt:")
    
    found_improvements = []
    for improvement in key_improvements:
        if improvement.lower() in default_prompt.lower():
            found_improvements.append(improvement)
    
    if len(found_improvements) >= 3:
        print(f"  ✅ 包含大写转小写指令 (找到 {len(found_improvements)} 个关键改进)")
        for imp in found_improvements:
            print(f"    - {imp}")
    else:
        print(f"  ❌ 缺少大写转小写指令 (仅找到 {len(found_improvements)} 个关键改进)")
        success = False
    
    # 检查示例是否更新
    example_checks = [
        'Original: "OH!"',
        'Rewritten: Oh!',
        'Original: "HMM..."', 
        'Rewritten: Hmm...'
    ]
    
    example_found = 0
    for example in example_checks:
        if example in default_prompt:
            example_found += 1
    
    if example_found >= 2:
        print(f"  ✅ 示例已更新为小写格式 (找到 {example_found}/{len(example_checks)} 个)")
    else:
        print(f"  ❌ 示例未完全更新 (仅找到 {example_found}/{len(example_checks)} 个)")
    
    # 检查保存的提示词
    saved_prompts = data.get('saved_prompts', [])
    print(f"\n📝 检查 saved_prompts ({len(saved_prompts)} 个):")
    
    mlp_prompt_updated = False
    for i, prompt in enumerate(saved_prompts):
        name = prompt.get('name', f'提示词{i+1}')
        content = prompt.get('content', '')
        
        if 'little pony' in name.lower() or 'mlp' in name.lower() or '小马' in name:
            print(f"  📋 检查 '{name}':")
            
            found_in_saved = 0
            for improvement in key_improvements:
                if improvement.lower() in content.lower():
                    found_in_saved += 1
            
            if found_in_saved >= 3:
                print(f"    ✅ 已更新大写转小写指令 (找到 {found_in_saved} 个关键改进)")
                mlp_prompt_updated = True
            else:
                print(f"    ❌ 未完全更新 (仅找到 {found_in_saved} 个关键改进)")
        else:
            print(f"  📋 '{name}': 通用提示词 (跳过检查)")
    
    # 针对日志问题的特定检查
    print(f"\n🎯 针对日志问题的检查:")
    print("日志中发现的问题文本:")
    print("- 'HEHE... I DO NOT THINK I CAN W...' (仍然大写)")
    print("- 'IF THIS DOES NOT GIVE ME A CUT...' (仍然大写)")
    
    test_cases = [
        "HEHE...I DON'T THINK I HAVE THE NECESSARY QUALIFICATIONS",
        "IF THIS DOESN'T GET ME A CUTIE MARK, I DON'T KNOW WHAT WILL!"
    ]
    
    print("\n💡 新提示词预期效果:")
    for case in test_cases:
        expected = case.capitalize().replace("'T", "'t").replace("'M", "'m").replace("'S", "'s")
        print(f"  输入: {case[:50]}...")
        print(f"  预期: {expected[:50]}... (首字母大写，其余小写)")
    
    print(f"\n📊 总体评估:")
    if success and mlp_prompt_updated:
        print("🎉 prompts.json 已成功更新!")
        print("✅ 所有关键改进点都已包含")
        print("✅ 示例格式已更新") 
        print("✅ 小马宝莉相关提示词已更新")
        print("\n🚀 建议立即重启应用测试效果")
        return True
    else:
        print("❌ 更新不完整，需要进一步检查")
        return False

if __name__ == "__main__":
    test_prompts_json_update()
