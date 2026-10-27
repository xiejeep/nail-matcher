#!/bin/bash
# 美甲图片匹配器 - 打包脚本

cd "$(dirname "$0")"

echo "=========================================="
echo "美甲图片匹配器 - 打包脚本"
echo "=========================================="
echo

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python，请先安装Python 3.9+"
    exit 1
fi

# 创建虚拟环境
if [ ! -d "build_venv" ]; then
    echo "创建打包虚拟环境..."
    python3 -m venv build_venv
fi

# 激活虚拟环境
source build_venv/bin/activate

# 安装打包依赖
echo "安装打包依赖..."
pip install -q pyinstaller
pip install -q flask pillow numpy sentence-transformers modelscope torch torchvision

echo
echo "开始打包..."
echo "预计时间: 3-10分钟"
echo

# 执行打包
pyinstaller build.spec --clean

if [ $? -ne 0 ]; then
    echo
    echo "打包失败！"
    exit 1
fi

echo
echo "=========================================="
echo "打包完成！"
echo "=========================================="
echo
echo "输出目录: dist/"
echo "可执行文件: dist/美甲匹配器"
echo
echo "首次运行时会自动下载AI模型（约1.1GB）"
echo