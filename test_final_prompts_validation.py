#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Prompts Validation Script

全面验证config/prompts.json的语法正确性、内容完整性和格式一致性。

Created: 2025-06-20
"""

import json
import os
import sys

def main():
    config_dir = "config"
    prompts_file = os.path.join(config_dir, "prompts.json")
    
    print("🔍 最终Prompts验证报告")
    print("=" * 60)
    
    # 1. JSON语法验证
    print("\n1️⃣ JSON语法验证")
    try:
        with open(prompts_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON语法正确")
    except json.JSONDecodeError as e:
        print(f"❌ JSON语法错误: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ 文件不存在: {prompts_file}")
        return False
    
    # 2. 结构验证
    print("\n2️⃣ 文件结构验证")
    required_keys = ["default_prompt", "saved_prompts"]
    missing_keys = [key for key in required_keys if key not in data]
    
    if missing_keys:
        print(f"❌ 缺少必要字段: {missing_keys}")
        return False
    else:
        print("✅ 文件结构完整")
    
    # 3. 内容完整性检查
    print("\n3️⃣ 内容完整性检查")
    
    # 检查default_prompt
    default_prompt = data["default_prompt"]
    cambridge_keywords = [
        "Cambridge English Young Learners vocabulary",
        "782 words",
        "PRESERVED TERMS",
        "REWRITING RULES",
        "EXAMPLES"
    ]
    
    missing_content = []
    for keyword in cambridge_keywords:
        if keyword not in default_prompt:
            missing_content.append(keyword)
    
    if missing_content:
        print(f"❌ default_prompt缺少内容: {missing_content}")
    else:
        print("✅ default_prompt内容完整")
    
    # 检查saved_prompts
    saved_prompts = data["saved_prompts"]
    if not isinstance(saved_prompts, list):
        print("❌ saved_prompts应该是列表")
        return False
    
    print(f"✅ saved_prompts包含 {len(saved_prompts)} 个提示词模板")
    
    # 4. 剑桥词汇表检查
    print("\n4️⃣ 剑桥词汇表检查")
    cambridge_vocab_count = default_prompt.count(',') + 1  # 粗略估算
    if cambridge_vocab_count > 700:  # 应该有782个词
        print(f"✅ 剑桥词汇表已集成 (估算 {cambridge_vocab_count} 词)")
    else:
        print(f"⚠️ 剑桥词汇表可能不完整 (估算 {cambridge_vocab_count} 词)")
    
    # 5. 格式一致性检查
    print("\n5️⃣ 格式一致性检查")
    
    # 检查转义字符是否正确
    if '\\n' in default_prompt:
        print("✅ 使用了正确的JSON换行转义")
    else:
        print("⚠️ 可能缺少换行符")
    
    # 检查是否有非法字符
    illegal_chars = ["'''", '"""']
    has_illegal = any(char in default_prompt for char in illegal_chars)
    if has_illegal:
        print("❌ 发现非法引号字符")
    else:
        print("✅ 无非法引号字符")
    
    # 6. My Little Pony专用检查
    print("\n6️⃣ My Little Pony专用内容检查")
    
    mlp_prompt = None
    for prompt in saved_prompts:
        if "小马宝莉" in prompt.get("name", ""):
            mlp_prompt = prompt["content"]
            break
    
    if mlp_prompt:
        mlp_keywords = [
            "Twilight Sparkle",
            "Rainbow Dash", 
            "Pinkie Pie",
            "unicorn",
            "pegasus",
            "Equestria"
        ]
        
        missing_mlp = [kw for kw in mlp_keywords if kw not in mlp_prompt]
        if missing_mlp:
            print(f"⚠️ 小马宝莉提示词缺少内容: {missing_mlp}")
        else:
            print("✅ 小马宝莉提示词内容完整")
    else:
        print("⚠️ 未找到小马宝莉专用提示词")
    
    # 7. 统计信息
    print("\n7️⃣ 统计信息")
    default_lines = default_prompt.count('\\n') + 1
    print(f"📊 default_prompt: {default_lines} 行")
    print(f"📊 saved_prompts: {len(saved_prompts)} 个")
    
    for i, prompt in enumerate(saved_prompts, 1):
        name = prompt.get("name", f"未命名-{i}")
        content_lines = prompt.get("content", "").count('\\n') + 1
        print(f"  📝 {i}. {name}: {content_lines} 行")
    
    print("\n🎉 所有验证完成!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
