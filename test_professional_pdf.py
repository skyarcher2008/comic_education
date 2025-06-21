#!/usr/bin/env python3
"""
测试专业级PDF颜色处理器

这个脚本专门用于测试PDF颜色准确性问题
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_professional_pdf_processor():
    """测试专业PDF处理器"""
    print("🎨 测试专业级PDF颜色处理器")
    print("=" * 50)
    
    try:
        # 导入处理器
        from src.core.pdf_processor_professional import extract_images_from_pdf
        print("✓ 成功导入专业PDF处理器")
        
        # 查找测试PDF文件
        test_folders = [
            Path("data/uploads"),
            Path("uploads"),
            Path("temp"),
            Path("data/temp"),
            Path(".")
        ]
        
        pdf_files = []
        for folder in test_folders:
            if folder.exists():
                pdf_files.extend(list(folder.glob("*.pdf")))
        
        if not pdf_files:
            print("❌ 没有找到PDF测试文件")
            print("请将您的测试PDF文件放到以下任一目录：")
            for folder in test_folders:
                print(f"  - {folder.absolute()}")
            return False
        
        print(f"📁 找到 {len(pdf_files)} 个PDF文件：")
        for pdf_file in pdf_files:
            print(f"  - {pdf_file}")
        
        # 测试每个PDF文件
        for pdf_file in pdf_files:
            print(f"\n🔍 测试文件: {pdf_file.name}")
            print("-" * 30)
            
            try:
                with open(pdf_file, 'rb') as f:
                    images = extract_images_from_pdf(f)
                
                if images:
                    print(f"✅ 成功提取 {len(images)} 个图像")
                    
                    # 保存测试结果
                    output_dir = Path("data/debug/professional_pdf_test")
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    for i, img in enumerate(images):
                        output_path = output_dir / f"{pdf_file.stem}_professional_page_{i+1}.png"
                        img.save(output_path, "PNG", quality=95)
                        print(f"  💾 保存: {output_path}")
                        print(f"    - 模式: {img.mode}")
                        print(f"    - 尺寸: {img.size}")
                        print(f"    - 格式: PNG")
                    
                    print(f"\n📊 颜色处理报告:")
                    print(f"  - 原始PDF: {pdf_file}")
                    print(f"  - 提取方法: 专业级多层次颜色管理")
                    print(f"  - 输出目录: {output_dir}")
                    print(f"  - 处理状态: ✅ 成功")
                    
                else:
                    print("❌ 提取失败")
                    
            except Exception as e:
                print(f"❌ 处理失败: {e}")
                continue
        
        print(f"\n🏆 专业级PDF处理器测试完成！")
        print(f"📁 结果保存在: data/debug/professional_pdf_test/")
        print(f"\n🔍 请对比以下结果:")
        print(f"  1. 用Edge浏览器打开原始PDF")
        print(f"  2. 查看提取的PNG图像")
        print(f"  3. 比较颜色是否一致")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装所需依赖:")
        print("  pip install PyMuPDF pdf2image numpy")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def check_dependencies():
    """检查依赖项"""
    print("🔍 检查专业PDF处理依赖项...")
    
    dependencies = {
        'PyPDF2': 'PyPDF2',
        'PIL': 'Pillow',
        'pdf2image': 'pdf2image',
        'fitz': 'PyMuPDF',
        'numpy': 'numpy'
    }
    
    missing = []
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing.append(package)
    
    if missing:
        print(f"\n📦 需要安装的包:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    print("✅ 所有依赖项都已安装")
    return True

if __name__ == "__main__":
    print("🎨 专业级PDF颜色处理器测试")
    print("=" * 50)
    
    # 检查依赖项
    if not check_dependencies():
        sys.exit(1)
    
    # 运行测试
    success = test_professional_pdf_processor()
    
    if success:
        print("\n🎉 测试完成！请检查颜色是否与Edge浏览器一致。")
    else:
        print("\n💥 测试失败！")
        sys.exit(1)
