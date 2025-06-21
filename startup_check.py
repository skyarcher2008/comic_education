#!/usr/bin/env python3
"""
小马宝莉-小学生版翻译系统启动检查脚本

这个脚本会检查系统是否正确配置并准备运行。
"""

import os
import sys
import subprocess

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("  请使用Python 3.8或更高版本")
        return False

def check_required_files():
    """检查必需文件是否存在"""
    print("\n📁 检查必需文件...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "config/prompts.json",
        "src/shared/constants.py",
        "src/core/translation.py",
        "src/app/static/js/constants.js"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ❌ {file_path} 不存在")
            all_exist = False
    
    return all_exist

def check_mlp_configuration():
    """检查小马宝莉配置"""
    print("\n🎠 检查小马宝莉配置...")
    
    # 检查 prompts.json
    try:
        import json
        with open('config/prompts.json', 'r', encoding='utf-8') as f:
            prompts_data = json.load(f)
        
        default_prompt = prompts_data.get('default_prompt', '')
        if 'My Little Pony' in default_prompt and 'elementary school students' in default_prompt:
            print("  ✓ prompts.json 配置正确")
        else:
            print("  ❌ prompts.json 配置不正确")
            return False
    except Exception as e:
        print(f"  ❌ 读取prompts.json失败: {e}")
        return False
    
    # 检查 constants.py
    try:
        with open('src/shared/constants.py', 'r', encoding='utf-8') as f:
            constants_content = f.read()
        
        if 'My Little Pony comic translator' in constants_content:
            print("  ✓ constants.py 配置正确")
        else:
            print("  ❌ constants.py 配置不正确")
            return False
    except Exception as e:
        print(f"  ❌ 读取constants.py失败: {e}")
        return False
    
    return True

def check_dependencies():
    """检查依赖包"""
    print("\n📦 检查依赖包...")
    
    try:
        import requirements
        print("  ✓ requirements模块可用")
    except ImportError:
        print("  ℹ️  requirements模块不可用，跳过自动检查")
    
    # 检查关键依赖
    key_packages = ['flask', 'requests', 'pillow', 'opencv-python']
    for package in key_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ❌ {package} 未安装")
    
    return True

def show_startup_info():
    """显示启动信息"""
    print("\n" + "=" * 60)
    print("🎠 小马宝莉-小学生版翻译系统")
    print("🎯 为中国小学生英语学习优化")
    print("=" * 60)
    
    print("\n🚀 启动方法:")
    print("  1. 安装依赖: pip install -r requirements.txt")
    print("  2. 启动应用: python app.py")
    print("  3. 打开浏览器访问: http://localhost:5000")
    
    print("\n✨ 系统特色:")
    print("  - 自动使用小马宝莉-小学生版提示词")
    print("  - 保留所有小马宝莉专有名词")
    print("  - 简化复杂词汇为小学生水平")
    print("  - 将长句子分解为短句子")
    print("  - 提供适合初学者的英语学习材料")
    
    print("\n📚 更多信息:")
    print("  - 用户指南: MLP_USER_GUIDE.md")
    print("  - 配置测试: python test_mlp_config_simple.py")

def main():
    """主函数"""
    print("🔍 小马宝莉-小学生版翻译系统启动检查")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_required_files(),
        check_mlp_configuration(),
        check_dependencies()
    ]
    
    if all(checks):
        print("\n✅ 所有检查通过!")
        print("系统已准备就绪，可以启动应用。")
        show_startup_info()
    else:
        print("\n❌ 部分检查未通过")
        print("请解决上述问题后再次运行此脚本。")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
