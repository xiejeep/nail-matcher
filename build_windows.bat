@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ==========================================
echo 美甲图片匹配器 - Windows 打包脚本
echo ==========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.9+
    pause
    exit /b 1
)

REM 创建虚拟环境
if not exist "build_venv" (
    echo 创建打包虚拟环境...
    python -m venv build_venv
)

REM 激活虚拟环境
call build_venv\Scripts\activate.bat

REM 安装打包依赖
echo 安装打包依赖...
pip install -q pyinstaller
pip install -q flask pillow numpy sentence-transformers modelscope torch torchvision

echo.
echo 开始打包...
echo 预计时间: 3-10分钟
echo.

REM 执行打包
pyinstaller build.spec --clean

if errorlevel 1 (
    echo.
    echo 打包失败！
    pause
    exit /b 1
)

echo.
echo ==========================================
echo 打包完成！
echo ==========================================
echo.
echo 输出目录: dist\
echo 可执行文件: dist\美甲匹配器.exe
echo.
echo 首次运行时会自动下载AI模型（约1.1GB）
echo.

pause