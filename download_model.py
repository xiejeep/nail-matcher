#!/usr/bin/env python3
"""
CLIP模型下载脚本
"""

import os
import sys
from pathlib import Path

def download_model():
    """下载CLIP模型到项目目录"""
    
    model_dir = Path(__file__).parent / "models"
    
    print("=" * 50)
    print("CLIP模型下载工具")
    print("=" * 50)
    print()
    
    # 检查是否已存在
    target_path = model_dir / "sentence-transformers" / "clip-ViT-B-32"
    if target_path.exists():
        print(f"模型已存在于: {target_path}")
        print("如需重新下载，请先删除 models/ 目录")
        return
    
    print("即将下载模型到:", model_dir)
    print("模型大小: 约 1.1GB")
    print("下载时间: 约 2-5 分钟（取决于网络速度）")
    print()
    
    try:
        from modelscope import snapshot_download
    except ImportError:
        print("错误: 未安装 modelscope")
        print("请运行: pip install modelscope")
        sys.exit(1)
    
    print("开始下载...")
    model_path = snapshot_download(
        'sentence-transformers/clip-ViT-B-32',
        cache_dir=str(model_dir)
    )
    
    print()
    print("=" * 50)
    print("下载完成！")
    print(f"模型路径: {model_path}")
    print("=" * 50)

if __name__ == "__main__":
    download_model()