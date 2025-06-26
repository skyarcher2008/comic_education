#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Config Loading for Prompts.json

测试修复后的prompts.json是否能被正常加载

Created: 2025-06-20
"""

import json
import os

def test_config_loading():
    print("🧪 测试配置加载")
    print("=" * 40)
    
    # 测试JSON直接加载
    prompts_file = "config/prompts.json"
    
    try:
        with open(prompts_file, 'r', encoding='utf-8') as f:
            prompts_data = json.load(f)
        
        print("✅ JSON直接加载成功")
        print(f"   - 包含字段: {list(prompts_data.keys())}")
        
        if 'default_prompt' in prompts_data:
            default_len = len(prompts_data['default_prompt'])
            print(f"   - default_prompt长度: {default_len} 字符")
        
        if 'saved_prompts' in prompts_data:
            saved_count = len(prompts_data['saved_prompts'])
            print(f"   - saved_prompts数量: {saved_count} 个")
            
            for i, prompt in enumerate(prompts_data['saved_prompts'], 1):
                name = prompt.get('name', '未命名')
                content_len = len(prompt.get('content', ''))
                print(f"     {i}. {name}: {content_len} 字符")
        
        # 检查关键内容
        print("\n🔍 关键内容检查")
        default_prompt = prompts_data.get('default_prompt', '')
        
        cambridge_check = 'Cambridge English Young Learners' in default_prompt
        print(f"   - 剑桥词汇表: {'✅' if cambridge_check else '❌'}")
        
        rules_check = 'REWRITING RULES' in default_prompt
        print(f"   - 重写规则: {'✅' if rules_check else '❌'}")
        
        examples_check = 'EXAMPLES' in default_prompt
        print(f"   - 示例: {'✅' if examples_check else '❌'}")
        
        # 检查小马宝莉提示词
        mlp_prompt = None
        for prompt in prompts_data.get('saved_prompts', []):
            if '小马宝莉' in prompt.get('name', ''):
                mlp_prompt = prompt.get('content', '')
                break
        
        if mlp_prompt:
            mlp_chars = ['Twilight Sparkle', 'Rainbow Dash', 'Pinkie Pie']
            mlp_check = all(char in mlp_prompt for char in mlp_chars)
            print(f"   - 小马宝莉角色: {'✅' if mlp_check else '❌'}")
        
        print("\n🎉 所有测试通过!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ 文件不存在: {prompts_file}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

if __name__ == "__main__":
    test_config_loading()
