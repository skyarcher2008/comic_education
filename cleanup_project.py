#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目清理脚本 - 删除临时测试文件
"""

import os
import shutil
from pathlib import Path

def cleanup_project():
    """清理项目中的临时文件"""
    
    # 需要删除的临时测试文件
    test_files_to_delete = [
        # 测试脚本
        'test_*.py',
        'demo_*.py',
        'quick_*.py',
        'validate_*.py',
        'verify_*.py',
        'analyze_*.py',
        'extract_*.py',
        'format_*.py',
        'show_*.py',
        'simple_*.py',
        'startup_check.py',
        'check_deps.py',
        'poppler_installer.py',
        'PDF_COLOR_SOLUTION.py',
        
        # 临时生成的文档
        '*_GUIDE.md',
        '*_REPORT.md',
        '*_SUMMARY.md',
        '*_UPDATE.md',
        '*_COMPLETE.md',
        '*_INTEGRATION_REPORT.md',
        '*_IMPLEMENTATION_REPORT.md',
        '*_OPTIMIZATION*.md',
        
        # 临时数据文件
        'test_*.txt',
        'test_*.md',
        'test_*.html',
        'cambridge_vocabulary_formatted.txt',
        'mlp_vocabulary.py',
        
        # 临时配置和批处理文件
        'start_with_plain_text_export.bat',
        
        # 临时PDF和其他文件
        'Friendship is Magic - 001.pdf',
        '*.mhtml',
    ]
    
    # 核心项目文件（不能删除）
    core_files = {
        'app.py',
        'app.spec',
        'cambridge_english.py',
        'requirements.txt',
        'README.md',
        'LICENSE',
        '.gitignore',
        'VOCABULARY_ANALYSIS_GUIDE.md',
        'VOCABULARY_ANALYSIS_IMPLEMENTATION_SUMMARY.md',
        'VOCABULARY_ANALYSIS_USAGE.md',
    }
    
    # 核心目录（不能删除）
    core_dirs = {
        'src',
        'config',
        'data',
        'logs',
        'models',
        'pic',
        'plugins',
        'scripts',
        'weights',
        'uploads',
        'temp',
        'docs',
        'manga_ocr_model',
        'ultralytics_yolov5_master',
        '.git',
        '__pycache__',
    }
    
    print("🧹 开始清理项目临时文件...")
    print("=" * 60)
    
    project_root = Path('.')
    deleted_files = []
    kept_files = []
    
    # 遍历项目根目录的所有文件
    for item in project_root.iterdir():
        if item.is_file():
            filename = item.name
            
            # 检查是否是核心文件
            if filename in core_files:
                kept_files.append(filename)
                continue
            
            # 检查是否匹配需要删除的模式
            should_delete = False
            for pattern in test_files_to_delete:
                if pattern.startswith('*') and pattern.endswith('*'):
                    # 包含模式 *text*
                    middle = pattern[1:-1]
                    if middle in filename:
                        should_delete = True
                        break
                elif pattern.startswith('*'):
                    # 后缀模式 *.py
                    if filename.endswith(pattern[1:]):
                        should_delete = True
                        break
                elif pattern.endswith('*'):
                    # 前缀模式 test_*
                    if filename.startswith(pattern[:-1]):
                        should_delete = True
                        break
                elif pattern == filename:
                    # 精确匹配
                    should_delete = True
                    break
            
            if should_delete:
                try:
                    item.unlink()
                    deleted_files.append(filename)
                    print(f"✓ 删除文件: {filename}")
                except Exception as e:
                    print(f"✗ 删除失败: {filename} - {e}")
            else:
                kept_files.append(filename)
    
    # 检查并删除临时的 __pycache__ 目录
    pycache_dirs = list(project_root.rglob('__pycache__'))
    for pycache_dir in pycache_dirs:
        if pycache_dir.is_dir():
            try:
                shutil.rmtree(pycache_dir)
                print(f"✓ 删除目录: {pycache_dir}")
            except Exception as e:
                print(f"✗ 删除目录失败: {pycache_dir} - {e}")
    
    print("\n" + "=" * 60)
    print("📊 清理统计:")
    print(f"✓ 删除文件数: {len(deleted_files)}")
    print(f"✓ 保留文件数: {len(kept_files)}")
    
    if deleted_files:
        print("\n📋 已删除的文件:")
        for file in sorted(deleted_files):
            print(f"  - {file}")
    
    print("\n✅ 项目清理完成!")
    print("💡 保留的核心文件和目录:")
    print("  - 应用程序: app.py")
    print("  - 源代码: src/")
    print("  - 配置文件: config/")
    print("  - 数据目录: data/")
    print("  - 词汇分析功能: cambridge_english.py")
    print("  - 文档: README.md, LICENSE, VOCABULARY_ANALYSIS_*.md")
    print("  - 其他必要文件和目录")

if __name__ == "__main__":
    cleanup_project()
