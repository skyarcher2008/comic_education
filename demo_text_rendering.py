#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本渲染优化对比演示
对比优化前后的文本渲染效果
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.core.rendering import get_font
from src.shared import constants

def old_style_rendering(draw, text, font, x, y, max_width, fill='black'):
    """
    模拟优化前的简单换行渲染（按字符换行）
    """
    lines = []
    current_line = ""
    current_width = 0
    
    for char in text:
        char_bbox = font.getbbox(char)
        char_width = char_bbox[2] - char_bbox[0]
        
        if current_width + char_width <= max_width:
            current_line += char
            current_width += char_width
        else:
            if current_line:
                lines.append(current_line)
            current_line = char
            current_width = char_width
    
    if current_line:
        lines.append(current_line)
    
    # 渲染文本
    current_y = y
    line_height = font.size + 5
    for line in lines:
        draw.text((x, current_y), line, fill=fill, font=font)
        current_y += line_height

def new_style_rendering(draw, text, font, x, y, max_width, fill='black'):
    """
    新的智能换行渲染（保护英文单词）
    """
    from src.core.rendering import draw_multiline_text_horizontal
    
    draw_multiline_text_horizontal(
        draw=draw,
        text=text,
        font=font,
        x=x,
        y=y,
        max_width=max_width,
        fill=fill
    )

def create_comparison_demo():
    """创建对比演示图像"""
    # 创建图像
    img_width, img_height = 1000, 800
    demo_image = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(demo_image)
    
    # 加载字体
    try:
        font = get_font(constants.DEFAULT_FONT_RELATIVE_PATH, 18)
        title_font = get_font(constants.DEFAULT_FONT_RELATIVE_PATH, 24)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # 测试文本
    test_texts = [
        "Hello world, this is a test sentence with some longer words like optimization and functionality.",
        "Testing hyphenated-words and contractions like don't, won't, can't in narrow bubbles.",
        "Mixed 中文 and English words should be handled properly without breaking English words."
    ]
    
    # 绘制标题
    draw.text((20, 20), "文本渲染优化对比演示", fill='black', font=title_font)
    draw.text((20, 60), "左侧：优化前（按字符换行）                    右侧：优化后（保护英文单词）", fill='gray', font=font)
    
    # 分割线
    draw.line([(img_width//2, 90), (img_width//2, img_height-20)], fill='lightgray', width=2)
    
    y_start = 120
    max_width = 400  # 气泡宽度
    
    for i, text in enumerate(test_texts):
        y_pos = y_start + i * 200
        
        # 绘制测试文本标题
        draw.text((20, y_pos-30), f"测试 {i+1}:", fill='blue', font=font)
        draw.text((520, y_pos-30), f"测试 {i+1}:", fill='blue', font=font)
        
        # 左侧：优化前
        draw.rectangle([20, y_pos, 20+max_width, y_pos+140], outline='red', width=1)
        draw.text((25, y_pos-50), "优化前", fill='red', font=font)
        old_style_rendering(draw, text, font, 25, y_pos+10, max_width-10, 'black')
        
        # 右侧：优化后
        draw.rectangle([520, y_pos, 520+max_width, y_pos+140], outline='green', width=1)
        draw.text((525, y_pos-50), "优化后", fill='green', font=font)
        new_style_rendering(draw, text, font, 525, y_pos+10, max_width-10, 'black')
    
    # 保存图像
    output_path = os.path.join(project_root, 'data', 'temp', 'text_rendering_comparison.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    demo_image.save(output_path)
    
    print(f"对比演示图像已保存到: {output_path}")
    return output_path

def create_feature_showcase():
    """创建功能特性展示图像"""
    img_width, img_height = 800, 600
    showcase_image = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(showcase_image)
    
    # 加载字体
    try:
        font = get_font(constants.DEFAULT_FONT_RELATIVE_PATH, 16)
        title_font = get_font(constants.DEFAULT_FONT_RELATIVE_PATH, 20)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # 标题
    draw.text((20, 20), "文本渲染优化功能特性展示", fill='black', font=title_font)
    
    features = [
        {
            'title': '1. 英文单词保护',
            'text': "Words like 'optimization', 'functionality', 'implementation' are never broken.",
            'color': 'blue'
        },
        {
            'title': '2. 连字符和缩写支持',
            'text': "Handles well-known, state-of-the-art, don't, won't, can't properly.",
            'color': 'green'
        },
        {
            'title': '3. 中英文混合智能处理',
            'text': "中文和English混合文本intelligent处理，确保readability和美观性。",
            'color': 'purple'
        },
        {
            'title': '4. 超长单词处理',
            'text': "Supercalifragilisticexpialidocious gets special treatment in narrow spaces.",
            'color': 'orange'
        }
    ]
    
    y_pos = 80
    max_width = 350
    
    for i, feature in enumerate(features):
        # 功能标题
        draw.text((20, y_pos), feature['title'], fill=feature['color'], font=title_font)
        
        # 气泡边框
        draw.rectangle([20, y_pos+30, 20+max_width, y_pos+120], outline=feature['color'], width=2)
        
        # 渲染文本
        new_style_rendering(draw, feature['text'], font, 25, y_pos+35, max_width-10, 'black')
        
        y_pos += 140
    
    # 保存图像
    output_path = os.path.join(project_root, 'data', 'temp', 'text_rendering_features.png')
    showcase_image.save(output_path)
    
    print(f"功能特性展示图像已保存到: {output_path}")
    return output_path

def main():
    """主函数"""
    print("=" * 60)
    print("文本渲染优化演示")
    print("=" * 60)
    
    try:
        # 创建对比演示
        print("\n1. 创建优化前后的对比演示...")
        comparison_path = create_comparison_demo()
        
        # 创建功能特性展示
        print("\n2. 创建功能特性展示...")
        features_path = create_feature_showcase()
        
        print("\n" + "=" * 60)
        print("演示图像生成完成！")
        print("=" * 60)
        print(f"对比演示: {comparison_path}")
        print(f"功能展示: {features_path}")
        print("\n可以打开这些图像查看文本渲染优化的效果。")
        
        return True
        
    except Exception as e:
        print(f"演示生成失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
