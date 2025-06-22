#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文本渲染优化功能
测试横向文本渲染中的智能分词功能，确保英文单词不被分割
"""

import os
import sys
import logging
from PIL import Image, ImageDraw, ImageFont

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.core.rendering import draw_multiline_text_horizontal, draw_multiline_text_vertical, get_font
from src.shared import constants

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TextRenderingTest")

def test_horizontal_text_rendering():
    """测试横向文本渲染的智能分词功能"""
    logger.info("开始测试横向文本渲染优化...")
    
    # 创建测试图像
    test_image = Image.new('RGB', (800, 600), 'white')
    draw = ImageDraw.Draw(test_image)
    
    # 加载字体
    try:
        font = get_font(constants.DEFAULT_FONT_RELATIVE_PATH, 24)
        logger.info(f"成功加载字体: {constants.DEFAULT_FONT_RELATIVE_PATH}")
    except Exception as e:
        logger.error(f"加载字体失败: {e}")
        # 使用默认字体
        font = ImageFont.load_default()
    
    # 测试文本（包含中英文混合）
    test_texts = [
        "Hello world, this is a test sentence with some longer words like 'optimization' and 'functionality'.",
        "这是一个测试句子，包含English words和中文字符的混合文本。",
        "Testing very long words like 'supercalifragilisticexpialidocious' in small bubbles.",
        "短句测试。Short test.",
        "Programming languages like Python, JavaScript, and C++ are powerful tools for developers.",
        "人工智能AI和机器学习ML正在改变世界，especially in fields like NLP自然语言处理。"
    ]
    
    y_position = 50
    max_width = 300  # 模拟较窄的气泡宽度
    
    for i, text in enumerate(test_texts):
        logger.info(f"渲染测试文本 {i+1}: {text[:50]}...")
        
        # 绘制边框表示气泡区域
        draw.rectangle([50, y_position-10, 50+max_width, y_position+80], outline='red', width=2)
        
        # 渲染文本
        try:
            draw_multiline_text_horizontal(
                draw=draw,
                text=text,
                font=font,
                x=55,  # 稍微偏移边框
                y=y_position,
                max_width=max_width-10,  # 留出边距
                fill='black'
            )
            logger.info(f"✓ 成功渲染文本 {i+1}")
        except Exception as e:
            logger.error(f"✗ 渲染文本 {i+1} 失败: {e}")
        
        y_position += 90
    
    # 保存测试图像
    output_path = os.path.join(project_root, 'data', 'temp', 'horizontal_text_test.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    test_image.save(output_path)
    logger.info(f"测试图像已保存到: {output_path}")
    
    return True

def test_vertical_text_rendering():
    """测试竖向文本渲染的优化功能"""
    logger.info("开始测试竖向文本渲染优化...")
    
    # 创建测试图像
    test_image = Image.new('RGB', (800, 600), 'white')
    draw = ImageDraw.Draw(test_image)
    
    # 加载字体
    try:
        font = get_font(constants.DEFAULT_FONT_RELATIVE_PATH, 24)
        logger.info(f"成功加载字体: {constants.DEFAULT_FONT_RELATIVE_PATH}")
    except Exception as e:
        logger.error(f"加载字体失败: {e}")
        font = ImageFont.load_default()
    
    # 测试文本（适合竖排）
    test_texts = [
        "这是竖排文本测试。",
        "包含English的混合文本。",
        "AI人工智能技术发展迅速。",
        "短文本测试。",
        "竖排文本中的标点符号：「」、（）等。"
    ]
    
    x_position = 100
    max_height = 200  # 模拟气泡高度
    
    for i, text in enumerate(test_texts):
        logger.info(f"渲染竖排测试文本 {i+1}: {text}")
        
        # 绘制边框表示气泡区域
        draw.rectangle([x_position-20, 50, x_position+50, 50+max_height], outline='blue', width=2)
        
        # 渲染竖排文本
        try:
            draw_multiline_text_vertical(
                draw=draw,
                text=text,
                font=font,
                x=x_position,
                y=55,  # 稍微偏移边框
                max_height=max_height-10,  # 留出边距
                fill='black',
                bubble_width=70
            )
            logger.info(f"✓ 成功渲染竖排文本 {i+1}")
        except Exception as e:
            logger.error(f"✗ 渲染竖排文本 {i+1} 失败: {e}")
        
        x_position += 80
    
    # 保存测试图像
    output_path = os.path.join(project_root, 'data', 'temp', 'vertical_text_test.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    test_image.save(output_path)
    logger.info(f"测试图像已保存到: {output_path}")
    
    return True

def test_word_breaking_prevention():
    """专门测试英文单词不被分割的功能"""
    logger.info("开始测试英文单词分割防护功能...")
    
    # 创建测试图像
    test_image = Image.new('RGB', (600, 400), 'white')
    draw = ImageDraw.Draw(test_image)
    
    # 加载字体
    try:
        font = get_font(constants.DEFAULT_FONT_RELATIVE_PATH, 20)
    except:
        font = ImageFont.load_default()
    
    # 测试用例：包含各种长度的英文单词
    test_cases = [
        {
            'text': "This sentence contains some relatively long words like 'optimization' and 'functionality'.",
            'max_width': 200,
            'description': "窄宽度测试 - 检查长单词处理"
        },
        {
            'text': "Testing hyphenated-words and contractions like don't, won't, can't in narrow bubbles.",
            'max_width': 180,
            'description': "连字符和缩写测试"
        },
        {
            'text': "Mixed 中文 and English words should be handled properly without breaking English words.",
            'max_width': 220,
            'description': "中英混合测试"
        }
    ]
    
    y_pos = 30
    for i, case in enumerate(test_cases):
        logger.info(f"测试用例 {i+1}: {case['description']}")
        
        # 绘制气泡边框
        draw.rectangle([30, y_pos-5, 30+case['max_width'], y_pos+80], outline='green', width=2)
        
        # 添加测试用例描述
        draw.text((35, y_pos-25), case['description'], fill='gray', font=font)
        
        # 渲染文本
        try:
            draw_multiline_text_horizontal(
                draw=draw,
                text=case['text'],
                font=font,
                x=35,
                y=y_pos,
                max_width=case['max_width']-10,
                fill='black'
            )
            logger.info(f"✓ 测试用例 {i+1} 渲染成功")
        except Exception as e:
            logger.error(f"✗ 测试用例 {i+1} 渲染失败: {e}")
        
        y_pos += 110
    
    # 保存测试图像
    output_path = os.path.join(project_root, 'data', 'temp', 'word_breaking_test.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    test_image.save(output_path)
    logger.info(f"单词分割测试图像已保存到: {output_path}")
    
    return True

def main():
    """运行所有测试"""
    logger.info("=" * 60)
    logger.info("开始文本渲染优化功能测试")
    logger.info("=" * 60)
    
    try:
        # 确保输出目录存在
        temp_dir = os.path.join(project_root, 'data', 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # 运行测试
        tests = [
            ("横向文本渲染测试", test_horizontal_text_rendering),
            ("竖向文本渲染测试", test_vertical_text_rendering),
            ("英文单词分割防护测试", test_word_breaking_prevention)
        ]
        
        results = []
        for test_name, test_func in tests:
            logger.info(f"\n--- {test_name} ---")
            try:
                result = test_func()
                results.append((test_name, result))
                logger.info(f"✓ {test_name} 完成")
            except Exception as e:
                logger.error(f"✗ {test_name} 失败: {e}")
                results.append((test_name, False))
        
        # 输出测试结果摘要
        logger.info("\n" + "=" * 60)
        logger.info("测试结果摘要:")
        logger.info("=" * 60)
        
        for test_name, result in results:
            status = "✓ 通过" if result else "✗ 失败"
            logger.info(f"{test_name}: {status}")
        
        all_passed = all(result for _, result in results)
        if all_passed:
            logger.info("\n🎉 所有测试通过！文本渲染优化功能正常工作。")
        else:
            logger.warning("\n⚠️  部分测试未通过，请检查相关功能。")
        
        logger.info(f"\n测试图像保存在: {temp_dir}")
        logger.info("可以查看这些图像来验证文本渲染效果。")
        
        return all_passed
        
    except Exception as e:
        logger.error(f"测试执行出错: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
