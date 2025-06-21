#!/usr/bin/env python3
"""
测试PDF图像提取颜色修复功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.pdf_processor import extract_images_from_pdf, convert_image_to_rgb
from PIL import Image
import io
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PDFColorTest")

def test_color_conversion():
    """测试颜色转换功能"""
    print("=== 测试颜色转换功能 ===")
    
    # 创建测试用的不同颜色模式图像
    test_modes = {
        'CMYK': (100, 100, 100, 100),  # CMYK模式
        'L': 128,  # 灰度模式
        'P': None,  # 调色板模式
    }
    
    for mode, color in test_modes.items():
        try:
            print(f"\n测试 {mode} 模式转换...")
            
            if mode == 'CMYK':
                # 创建CMYK测试图像
                test_img = Image.new('CMYK', (100, 100), color)
            elif mode == 'L':
                # 创建灰度测试图像
                test_img = Image.new('L', (100, 100), color)
            elif mode == 'P':
                # 创建调色板模式测试图像
                test_img = Image.new('P', (100, 100))
                test_img.putpalette([i for i in range(256*3)])  # 简单调色板
            
            print(f"  原始图像: 模式={test_img.mode}, 尺寸={test_img.size}")
            
            # 转换为RGB
            rgb_img = convert_image_to_rgb(test_img)
            print(f"  转换后图像: 模式={rgb_img.mode}, 尺寸={rgb_img.size}")
            
            # 验证转换是否成功
            if rgb_img.mode == 'RGB':
                print(f"  ✓ {mode} -> RGB 转换成功")
            else:
                print(f"  ✗ {mode} -> RGB 转换失败")
                
        except Exception as e:
            print(f"  ✗ 测试 {mode} 模式时出错: {e}")

def create_test_summary():
    """创建测试总结"""
    print("\n" + "="*50)
    print("PDF图像颜色修复功能说明")
    print("="*50)
    print("1. 问题分析:")
    print("   - PDF文件中的图像常使用CMYK颜色模式")
    print("   - CMYK图像在屏幕显示时颜色会不正确")
    print("   - 需要转换为RGB模式以确保正确显示")
    print()
    print("2. 解决方案:")
    print("   - 添加 convert_image_to_rgb() 函数")
    print("   - 自动检测图像颜色模式")
    print("   - 支持 CMYK、L、P、RGBA 等模式转换")
    print("   - 在提取PDF图像时自动应用颜色转换")
    print()
    print("3. 技术细节:")
    print("   - 使用 PIL/Pillow 的 convert() 方法")
    print("   - 对CMYK模式采用标准转换算法")
    print("   - 包含异常处理和fallback机制")
    print("   - 详细的日志记录用于调试")
    print()
    print("4. 预期效果:")
    print("   - 从PDF提取的图像颜色正确")
    print("   - 所有图像统一为RGB模式")
    print("   - 提升OCR和处理准确性")
    print("="*50)

if __name__ == "__main__":
    print("PDF图像颜色修复测试")
    print("=" * 30)
    
    # 测试颜色转换功能
    test_color_conversion()
    
    # 显示总结
    create_test_summary()
    
    print("\n注意: 要测试实际PDF文件，请将PDF文件放置在适当位置并运行主程序。")
