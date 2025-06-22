@echo off
echo 启动漫画翻译器应用程序...
echo.
echo 新功能：自动保存文本文件
echo - 每次翻译完成后，会自动将所有文本保存到 data/output/ 目录
echo - 文件格式：comic_text_年-月-日_时-分-秒.txt
echo - 包含每张图片的页码标记和原文译文对照
echo - 同时保留原有的"导出纯文本"按钮功能
echo.

cd /d "c:\Users\EVA\Documents\github\comic_education"

echo 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误：未找到Python环境
    pause
    exit /b 1
)

echo.
echo 启动Flask应用程序...
echo 请在浏览器中访问 http://localhost:5000
echo.
echo 按Ctrl+C停止服务器
echo.

python app.py

pause
