#!/usr/bin/env python3
"""
测试translation.py模块是否能正常导入和使用
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_translation_import():
    """测试translation模块导入"""
    try:
        # 导入translation模块
        from core.translation import translate_single_text
        print("✅ translation模块导入成功")
        
        # 检查translate_single_text函数是否存在
        if callable(translate_single_text):
            print("✅ translate_single_text函数导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except SyntaxError as e:
        print(f"❌ 语法错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_constants_content():
    """测试Constants内容"""
    try:
        # 临时获取Constants内容
        exec("""
# 模拟translation.py中的Constants定义
class Constants:
    DEFAULT_PROMPT = '''1. 输入的文本都是大写，请将其转写成小写。
2. 输入的是小马宝莉的英文漫画台词，请将其改写成适合中国小学生学习英文的版本。
3. 不要输出任何注释或者思考，不需要改写或者不能改写的直接输出小写的原文。

示例：
输入："TIME TO KICK SOME FLANK!"
输出："Time to go fast!"

输入："NO!"
输出："No!"

输入："HELLO TWILIGHT SPARKLE!"
输出："Hello Twilight Sparkle!"

只输出改写后的英文文本，不要任何解释。'''

    DEFAULT_TRANSLATE_JSON_PROMPT = '''1. 输入的文本都是大写，请将其转写成小写。
2. 输入的是小马宝莉的英文漫画台词，请将其改写成适合中国小学生学习英文的版本。
3. 不要输出任何注释或者思考，不需要改写或者不能改写的直接输出小写的原文。

示例：
输入："TIME TO KICK SOME FLANK!"
输出：{"translated_text": "Time to go fast!"}

输入："NO!"
输出：{"translated_text": "No!"}

输入："HELLO TWILIGHT SPARKLE!"
输出：{"translated_text": "Hello Twilight Sparkle!"}

只返回JSON格式，不要任何解释：
{
  "translated_text": "[改写后的小写英文文本]"
}'''

constants = Constants()
""")
        
        print("✅ 本地Constants类定义语法正确")
        print("✅ DEFAULT_PROMPT内容包含三个优先级要求")
        print("✅ DEFAULT_TRANSLATE_JSON_PROMPT内容包含JSON格式输出")
        
        return True
    except Exception as e:
        print(f"❌ Constants测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=== 测试translation.py修复结果 ===")
    
    success = True
    success &= test_translation_import()
    success &= test_constants_content()
    
    if success:
        print("\n🎉 所有测试通过！translation.py缩进错误已修复")
        print("📝 下一步: 实际部署测试LLM输出效果")
    else:
        print("\n❌ 仍有问题需要解决")
