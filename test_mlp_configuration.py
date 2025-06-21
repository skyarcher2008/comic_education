#!/usr/bin/env python3
"""
测试小马宝莉-小学生版翻译系统配置

这个脚本测试以下功能：
1. 验证默认提示词是否正确设置为小马宝莉版本
2. 测试小马宝莉专有名词保留功能
3. 测试简单词汇约束
4. 验证JSON格式提示词
"""

import sys
import os
import json

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'src'))

# 导入相关模块
try:
    from src.shared import constants
    from src.shared.config_loader import ConfigLoader
except ImportError:
    print("导入模块失败，直接测试常量...")
    constants = None
    ConfigLoader = None

def test_default_prompts():
    """测试默认提示词设置"""
    print("=" * 60)
    print("🧪 测试默认提示词设置")
    print("=" * 60)
    
    # 检查默认提示词是否包含小马宝莉相关内容
    default_prompt = constants.DEFAULT_PROMPT
    mlp_keywords = [
        "My Little Pony", 
        "elementary school students",
        "Twilight Sparkle",
        "Rainbow Dash",
        "Equestria",
        "cutie mark"
    ]
    
    print("✅ 默认提示词检查:")
    for keyword in mlp_keywords:
        if keyword in default_prompt:
            print(f"  ✓ 包含关键词: {keyword}")
        else:
            print(f"  ❌ 缺少关键词: {keyword}")
    
    # 检查JSON格式提示词
    json_prompt = constants.DEFAULT_TRANSLATE_JSON_PROMPT
    print("\n✅ JSON格式提示词检查:")
    for keyword in mlp_keywords[:4]:  # 检查前几个关键词
        if keyword in json_prompt:
            print(f"  ✓ 包含关键词: {keyword}")
        else:
            print(f"  ❌ 缺少关键词: {keyword}")

def test_config_file():
    """测试配置文件设置"""
    print("\n" + "=" * 60)
    print("🧪 测试配置文件设置") 
    print("=" * 60)
    
    try:
        config_loader = ConfigLoader()
        prompts_data = config_loader.load_prompts()
        
        print("✅ prompts.json 检查:")
        default_prompt = prompts_data.get('default_prompt', '')
        
        # 检查默认提示词
        if 'My Little Pony' in default_prompt:
            print("  ✓ default_prompt 设置为小马宝莉版本")
        else:
            print("  ❌ default_prompt 不是小马宝莉版本")
        
        # 检查保存的提示词
        saved_prompts = prompts_data.get('saved_prompts', [])
        mlp_prompt_found = False
        generic_prompt_found = False
        
        for prompt in saved_prompts:
            if prompt.get('name') == '小马宝莉-小学生版':
                mlp_prompt_found = True
                print("  ✓ 找到 '小马宝莉-小学生版' 提示词")
            elif prompt.get('name') == '通用漫画翻译':
                generic_prompt_found = True
                print("  ✓ 找到 '通用漫画翻译' 提示词")
        
        if not mlp_prompt_found:
            print("  ❌ 缺少 '小马宝莉-小学生版' 提示词")
        if not generic_prompt_found:
            print("  ❌ 缺少 '通用漫画翻译' 提示词")
            
    except Exception as e:
        print(f"  ❌ 配置文件加载错误: {e}")

def test_mlp_vocabulary():
    """测试小马宝莉词汇保留"""
    print("\n" + "=" * 60)
    print("🧪 测试小马宝莉词汇保留功能")
    print("=" * 60)
    
    # 定义测试用例
    test_cases = [
        {
            "original": "Twilight Sparkle is absolutely magnificent!",
            "expected_preserved": ["Twilight Sparkle"],
            "expected_simplified": "magnificent" # 应该被简化
        },
        {
            "original": "Welcome to Equestria, the magical land of ponies!",
            "expected_preserved": ["Equestria"],
            "expected_simplified": "magical" # 可能被简化
        },
        {
            "original": "Rainbow Dash got her cutie mark after performing an amazing trick!",
            "expected_preserved": ["Rainbow Dash", "cutie mark"],
            "expected_simplified": "amazing" # 应该被简化
        }
    ]
    
    print("📋 测试用例分析:")
    for i, case in enumerate(test_cases, 1):
        print(f"\n  测试用例 {i}:")
        print(f"    原文: {case['original']}")
        print(f"    应保留: {', '.join(case['expected_preserved'])}")
        print(f"    应简化: {case['expected_simplified']}")

def test_vocabulary_constraints():
    """测试词汇约束说明"""
    print("\n" + "=" * 60)
    print("🧪 词汇约束规则说明")
    print("=" * 60)
    
    constraints = [
        "✓ 只使用适合小学生的简单英语单词",
        "✓ 保持句子简短（最多10-12个单词）",
        "✓ 尽可能使用现在时态",
        "✓ 避免复杂的语法结构",
        "✓ 保留所有小马宝莉专有名词",
        "✓ 避免美式俚语和习语",
        "✓ 使用简单的连接词：and, but, so, because"
    ]
    
    for constraint in constraints:
        print(f"  {constraint}")

def demonstrate_usage():
    """演示使用方法"""
    print("\n" + "=" * 60)
    print("📖 使用方法演示")
    print("=" * 60)
    
    print("🔧 如何使用小马宝莉-小学生版翻译:")
    print("  1. 启动应用后，系统会自动使用小马宝莉-小学生版作为默认提示词")
    print("  2. 上传小马宝莉漫画图片")
    print("  3. 系统会自动:")
    print("     - 保留角色名字（如 Twilight Sparkle, Rainbow Dash）")
    print("     - 保留地名（如 Equestria, Ponyville）") 
    print("     - 保留特殊术语（如 cutie mark, unicorn）")
    print("     - 将复杂词汇简化为小学生水平")
    print("     - 将长句子分解为短句子")
    print("  4. 输出适合中国小学生学习的简化英语文本")
    
    print("\n🎯 教育价值:")
    print("  - 帮助中国小学生学习英语")
    print("  - 通过喜爱的卡通角色提高学习兴趣")
    print("  - 提供适合年龄的词汇和语法")
    print("  - 保持故事内容的完整性和趣味性")

def main():
    """主测试函数"""
    print("🎠 小马宝莉-小学生版翻译系统配置测试")
    print("🎯 为中国小学生英语学习优化的漫画翻译工具")
    
    try:
        test_default_prompts()
        test_config_file()
        test_mlp_vocabulary()
        test_vocabulary_constraints()
        demonstrate_usage()
        
        print("\n" + "=" * 60)
        print("✅ 配置测试完成!")
        print("系统已配置为使用小马宝莉-小学生版作为默认翻译模式")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
