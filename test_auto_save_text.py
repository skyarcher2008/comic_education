"""
测试自动文本保存功能
"""
import requests
import json
import os

def test_save_text_file_api():
    """测试保存文本文件API"""
    
    # 测试数据
    test_data = {
        "images": [
            {
                "originalTexts": ["Hello", "World", "This is a test"],
                "bubbleTexts": ["你好", "世界", "这是一个测试"],
                "filename": "test_page1.jpg"
            },
            {
                "originalTexts": ["Good morning", "How are you?"],
                "bubbleTexts": ["早上好", "你好吗？"],
                "filename": "test_page2.png"
            },
            {
                "originalTexts": ["Empty page"],
                "bubbleTexts": [],
                "filename": "test_page3.jpg"
            }
        ]
    }
    
    try:
        # 发送POST请求到API
        url = "http://localhost:5000/api/save_text_file"
        headers = {"Content-Type": "application/json"}
        
        print("发送测试请求到:", url)
        print("测试数据:", json.dumps(test_data, ensure_ascii=False, indent=2))
        
        response = requests.post(url, json=test_data, headers=headers)
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ API测试成功!")
            print(f"消息: {result.get('message')}")
            print(f"文件路径: {result.get('file_path')}")
            print(f"统计信息: {result.get('statistics')}")
            
            # 检查文件是否真的被创建
            file_path = result.get('file_path')
            if file_path and os.path.exists(file_path):
                print(f"\n✅ 文件已成功创建: {file_path}")
                
                # 读取并显示文件内容的前几行
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:10]  # 只显示前10行
                    print("\n文件内容预览:")
                    print("".join(lines))
                    if len(f.readlines()) > 10:
                        print("... (还有更多内容)")
            else:
                print(f"\n❌ 文件未找到: {file_path}")
        else:
            print(f"\n❌ API测试失败: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Flask应用正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    print("=== 自动文本保存功能测试 ===")
    test_save_text_file_api()
