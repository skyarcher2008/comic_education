#!/usr/bin/env python3
"""
快速验证专业PDF处理器
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def quick_test():
    """快速测试处理器导入和基本功能"""
    print("🔍 快速验证专业PDF处理器...")
    
    try:
        # 测试导入
        from src.core.pdf_processor import extract_images_from_pdf
        print("✅ 处理器导入成功")
        
        # 测试依赖项
        import PyPDF2
        print("✅ PyPDF2 可用")
        
        import PIL
        print("✅ PIL 可用")
        
        try:
            import pdf2image
            print("✅ pdf2image 可用")
        except ImportError:
            print("⚠️ pdf2image 不可用（可选）")
        
        try:
            import fitz
            print("✅ PyMuPDF 可用")
        except ImportError:
            print("⚠️ PyMuPDF 不可用（可选）")
        
        try:
            import numpy
            print("✅ numpy 可用")
        except ImportError:
            print("⚠️ numpy 不可用（可选）")
        
        print("\n🎉 专业PDF处理器已就绪！")
        print("\n📝 使用说明:")
        print("1. 将PDF文件放到以下目录之一:")
        print("   - data/uploads/")
        print("   - uploads/")
        print("   - temp/")
        print("2. 运行: python test_professional_pdf.py")
        print("3. 检查结果: data/debug/professional_pdf_test/")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    if not success:
        sys.exit(1)
