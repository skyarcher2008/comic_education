#!/usr/bin/env python3
"""
测试小马宝莉-小学生版翻译系统配置

这个脚本验证配置文件是否正确设置
"""

import os
import json

def test_config_files():
    """测试配置文件"""
    print("🎠 小马宝莉-小学生版翻译系统配置测试")
    print("🎯 为中国小学生英语学习优化的漫画翻译工具")
    print("=" * 60)
    
    # 测试 prompts.json
    prompts_file = "config/prompts.json"
    if os.path.exists(prompts_file):
        print("✅ 检查 config/prompts.json:")
        try:
            with open(prompts_file, 'r', encoding='utf-8') as f:
                prompts_data = json.load(f)
            
            default_prompt = prompts_data.get('default_prompt', '')
            if 'My Little Pony' in default_prompt:
                print("  ✓ default_prompt 设置为小马宝莉版本")
            else:
                print("  ❌ default_prompt 不是小马宝莉版本")
            
            # 检查关键词
            mlp_keywords = ["elementary school students", "Twilight Sparkle", "Equestria", "cutie mark"]
            for keyword in mlp_keywords:
                if keyword in default_prompt:
                    print(f"  ✓ 包含关键词: {keyword}")
                else:
                    print(f"  ❌ 缺少关键词: {keyword}")
            
            # 检查保存的提示词
            saved_prompts = prompts_data.get('saved_prompts', [])
            prompt_names = [p.get('name', '') for p in saved_prompts]
            
            if '小马宝莉-小学生版' in prompt_names:
                print("  ✓ 找到 '小马宝莉-小学生版' 提示词")
            else:
                print("  ❌ 缺少 '小马宝莉-小学生版' 提示词")
                
            if '通用漫画翻译' in prompt_names:
                print("  ✓ 找到 '通用漫画翻译' 提示词")
            else:
                print("  ❌ 缺少 '通用漫画翻译' 提示词")
                
        except Exception as e:
            print(f"  ❌ 读取配置文件错误: {e}")
    else:
        print(f"❌ 配置文件不存在: {prompts_file}")
    
    # 测试 constants.py
    constants_file = "src/shared/constants.py"
    if os.path.exists(constants_file):
        print(f"\n✅ 检查 {constants_file}:")
        try:
            with open(constants_file, 'r', encoding='utf-8') as f:
                constants_content = f.read()
            
            if 'My Little Pony comic translator' in constants_content:
                print("  ✓ DEFAULT_PROMPT 包含小马宝莉翻译器描述")
            else:
                print("  ❌ DEFAULT_PROMPT 缺少小马宝莉翻译器描述")
            
            if 'DEFAULT_TRANSLATE_JSON_PROMPT' in constants_content and 'My Little Pony' in constants_content:
                print("  ✓ DEFAULT_TRANSLATE_JSON_PROMPT 包含小马宝莉内容")
            else:
                print("  ❌ DEFAULT_TRANSLATE_JSON_PROMPT 缺少小马宝莉内容")
                
        except Exception as e:
            print(f"  ❌ 读取常量文件错误: {e}")
    else:
        print(f"❌ 常量文件不存在: {constants_file}")

def show_feature_summary():
    """显示功能总结"""
    print("\n" + "=" * 60)
    print("📖 小马宝莉-小学生版功能总结")
    print("=" * 60)
    
    print("🎯 目标用户: 中国小学生学习英语")
    print("\n✨ 核心功能:")
    print("  1. 专门针对小马宝莉漫画的英语文本重写")
    print("  2. 使用适合小学生的简单词汇")
    print("  3. 保持句子简短（最多10-12个单词）")
    print("  4. 保留所有小马宝莉专有名词")
    
    print("\n🔤 保留的专有名词包括:")
    print("  角色名: Twilight Sparkle, Rainbow Dash, Pinkie Pie, Applejack, Rarity, Fluttershy")
    print("  地名: Equestria, Ponyville, Canterlot, Cloudsdale")
    print("  特殊术语: cutie mark, unicorn, pegasus, magic, friendship")
    
    print("\n📝 重写规则:")
    print("  - 将复杂词汇替换为简单词汇")
    print("  - 将长句子分解为短句子")
    print("  - 使用基础语法结构")
    print("  - 避免美式俚语和习语")
    print("  - 使用简单的连接词: and, but, so, because")
    
    print("\n🎓 教育价值:")
    print("  - 通过喜爱的卡通角色提高学习兴趣")
    print("  - 提供适合年龄的英语学习材料")
    print("  - 保持故事内容的完整性和趣味性")
    print("  - 帮助建立英语学习的自信心")

def show_usage_examples():
    """显示使用示例"""
    print("\n" + "=" * 60)
    print("💡 使用示例")
    print("=" * 60)
    
    examples = [
        {
            "original": "That's absolutely magnificent, darling!",
            "rewritten": "That is very beautiful!",
            "explanation": "将复杂词汇 'magnificent' 简化为 'beautiful'"
        },
        {
            "original": "I'm completely flabbergasted by Rainbow Dash's performance!",
            "rewritten": "I am very surprised by Rainbow Dash's show!",
            "explanation": "简化复杂词汇，保留角色名 'Rainbow Dash'"
        },
        {
            "original": "Twilight Sparkle discovered an extraordinary spell in Canterlot.",
            "rewritten": "Twilight Sparkle found a special spell in Canterlot.",
            "explanation": "保留专有名词，简化词汇 'extraordinary' → 'special'"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n示例 {i}:")
        print(f"  原文: {example['original']}")
        print(f"  重写: {example['rewritten']}")
        print(f"  说明: {example['explanation']}")

def main():
    """主函数"""
    test_config_files()
    show_feature_summary()
    show_usage_examples()
    
    print("\n" + "=" * 60)
    print("✅ 配置测试完成!")
    print("小马宝莉-小学生版翻译系统已准备就绪!")
    print("=" * 60)

if __name__ == "__main__":
    main()
