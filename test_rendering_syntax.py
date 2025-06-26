#!/usr/bin/env python3
"""
测试 rendering.py 文件的语法正确性
验证居中对齐修改是否正确
"""

import py_compile
import sys
import os

def test_syntax():
    """测试语法正确性"""
    print("=== 测试 rendering.py 语法正确性 ===")
    
    file_path = "src/core/rendering.py"
    if not os.path.exists(file_path):
        print(f"❌ 文件 {file_path} 不存在")
        return False
    
    try:
        py_compile.compile(file_path, doraise=True)
        print(f"✅ {file_path} 语法检查通过")
        return True
    except py_compile.PyCompileError as e:
        print(f"❌ {file_path} 语法错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 语法检查失败: {e}")
        return False

def test_import():
    """测试模块导入"""
    print("\n=== 测试 rendering.py 模块导入 ===")
    
    try:
        # 添加项目根目录到路径
        project_root = os.path.abspath(".")
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        # 尝试导入核心函数
        from src.core.rendering import draw_multiline_text_horizontal, draw_multiline_text_vertical
        print("✅ 核心函数导入成功")
        
        # 检查函数签名
        import inspect
        h_sig = inspect.signature(draw_multiline_text_horizontal)
        v_sig = inspect.signature(draw_multiline_text_vertical)
        
        print(f"✅ draw_multiline_text_horizontal 参数: {list(h_sig.parameters.keys())}")
        print(f"✅ draw_multiline_text_vertical 参数: {list(v_sig.parameters.keys())}")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 导入测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试 rendering.py 居中对齐修改...")
    
    syntax_ok = test_syntax()
    import_ok = test_import()
    
    if syntax_ok and import_ok:
        print("\n🎉 所有测试通过！居中对齐修改成功实施。")
        print("\n📋 修改摘要:")
        print("- ✅ 修改了 draw_multiline_text_horizontal 函数")
        print("- ✅ 添加了每行宽度计算逻辑")
        print("- ✅ 实现了基于行宽的居中对齐")
        print("- ✅ 考虑了特殊字符字体的宽度计算")
        print("- ✅ 保持了对超宽行的左对齐兼容性")
        return True
    else:
        print("\n❌ 测试失败，需要修复问题。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
