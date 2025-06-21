#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小马宝莉漫画文本改写示例
使用剑桥少儿英语词汇表和专有名词保护
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mlp_vocabulary import get_mlp_prompt_with_vocabulary, get_mlp_json_prompt
from cambridge_english import VOCABULARY, EnglishLevel

def test_mlp_rewriting():
    """测试小马宝莉文本改写功能"""
    
    # 测试用的原始文本（来自小马宝莉漫画）
    test_texts = [
        "That's absolutely magnificent, Rainbow Dash! Your aerial maneuvers are quite spectacular!",
        "I'm completely flabbergasted by this mysterious occurrence in Ponyville!",
        "Darling, your ensemble is positively exquisite! The craftsmanship is impeccable.",
        "We must expeditiously gather the Elements of Harmony to vanquish this threat!",
        "Princess Celestia, I'm thoroughly perplexed by this enigmatic magical phenomenon."
    ]
    
    print("=== 小马宝莉漫画文本改写示例 ===\n")
    
    # 显示词汇表信息
    a1_count = len(VOCABULARY[EnglishLevel.A1_MOVERS])
    a2_count = len(VOCABULARY[EnglishLevel.A2_FLYERS])
    print(f"可用词汇统计:")
    print(f"- A1 Movers: {a1_count} 个单词")
    print(f"- A2 Flyers: {a2_count} 个单词")
    print(f"- 总计: {a1_count + a2_count} 个单词\n")
    
    # 显示改写示例
    print("改写示例：")
    expected_results = [
        "That is very good, Rainbow Dash! Your flying is beautiful!",
        "I am very surprised by this strange thing in Ponyville!",
        "Your clothes are very pretty! The work is very good.",
        "We must quickly get the Elements of Harmony to stop this bad thing!",
        "Princess Celestia, I am confused by this strange magic."
    ]
    
    for i, (original, expected) in enumerate(zip(test_texts, expected_results), 1):
        print(f"\n{i}. 原文:")
        print(f"   {original}")
        print(f"   期望改写:")
        print(f"   {expected}")
    
    print(f"\n=== 提示词预览 ===")
    print("普通提示词:")
    prompt = get_mlp_prompt_with_vocabulary()
    print(prompt[:500] + "...(截断)")
    
    print(f"\nJSON提示词:")
    json_prompt = get_mlp_json_prompt()
    print(json_prompt[:300] + "...(截断)")

def analyze_vocabulary_coverage():
    """分析词汇表覆盖情况"""
    print("\n=== 词汇分析 ===")
    
    # 获取所有词汇
    all_words = set()
    for level_words in VOCABULARY.values():
        all_words.update(level_words)
    
    # 基础词汇统计
    basic_words = {"the", "a", "an", "and", "but", "or", "so", "because", "is", "are", "am", "was", "were"}
    available_basic = basic_words.intersection(all_words)
    
    print(f"基础词汇覆盖: {len(available_basic)}/{len(basic_words)}")
    print(f"可用基础词: {', '.join(sorted(available_basic))}")
    
    # 情感词汇
    emotion_words = {"happy", "sad", "angry", "surprised", "afraid", "excited"}
    available_emotions = emotion_words.intersection(all_words)
    
    print(f"\n情感词汇覆盖: {len(available_emotions)}/{len(emotion_words)}")
    print(f"可用情感词: {', '.join(sorted(available_emotions))}")
    
    # 动作词汇
    action_words = {"run", "walk", "fly", "jump", "dance", "sing", "play", "help", "go", "come"}
    available_actions = action_words.intersection(all_words)
    
    print(f"\n动作词汇覆盖: {len(available_actions)}/{len(action_words)}")
    print(f"可用动作词: {', '.join(sorted(available_actions))}")

if __name__ == "__main__":
    test_mlp_rewriting()
    analyze_vocabulary_coverage()
    
    print("\n=== 使用说明 ===")
    print("1. 在翻译界面选择'小马宝莉-小学生版'提示词")
    print("2. 输入小马宝莉漫画的英文文本")
    print("3. 模型会自动:")
    print("   - 保留所有角色名、地名、专有名词")
    print("   - 使用简单的剑桥英语词汇")
    print("   - 将长句拆分为短句")
    print("   - 避免复杂语法和美国俚语")
    print("   - 使用适合小学生的语言风格")
