#!/bin/bash
# 美甲图片匹配器 - 一键启动脚本

cd "$(dirname "$0")"

echo "=========================================="
echo "美甲图片匹配器 - 一键启动"
echo "=========================================="
echo

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "检查依赖..."
pip install -q flask pillow numpy sentence-transformers modelscope

# 检查模型
MODEL_DIR="models/sentence-transformers/clip-ViT-B-32"
if [ ! -d "$MODEL_DIR" ]; then
    echo
    echo "AI模型未找到，开始下载..."
    echo "模型大小: 约 1.1GB"
    echo "下载时间: 约 2-5 分钟"
    echo
    python download_model.py
else
    echo "AI模型已存在，跳过下载"
fi

echo
echo "=========================================="
echo "启动应用..."
echo "=========================================="
echo
echo "访问地址: http://127.0.0.1:3001"
echo "按 Ctrl+C 关闭应用"
echo

# 启动应用
python app.py