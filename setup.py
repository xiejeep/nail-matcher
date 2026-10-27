#!/usr/bin/env python3
"""
从 Excel 提取图片并建立特征向量索引
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
import numpy as np
from PIL import Image

# 设置项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "货盘分类.db"
IMAGES_DIR = PROJECT_ROOT / "货盘分类图片"

def extract_images_from_excel(excel_path):
    """从 Excel 文件中提取图片"""
    import zipfile
    
    print(f"正在从 {excel_path} 提取图片...")
    
    with zipfile.ZipFile(excel_path, 'r') as z:
        img_count = 0
        for f in z.namelist():
            if f.startswith('xl/media/'):
                z.extract(f, IMAGES_DIR)
                img_count += 1
                if img_count % 100 == 0:
                    print(f"  已提取 {img_count} 张...")
    
    # 移动图片到根目录
    import shutil
    media_dir = IMAGES_DIR / 'xl' / 'media'
    if media_dir.exists():
        for f in media_dir.iterdir():
            shutil.move(str(f), str(IMAGES_DIR / f.name))
        shutil.rmtree(IMAGES_DIR / 'xl')
    
    print(f"提取完成: {img_count} 张图片")
    return img_count

def setup_database():
    """设置数据库，添加特征向量表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建特征向量表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS image_features (
            id INTEGER PRIMARY KEY,
            item_id INTEGER,
            image_path TEXT,
            feature_vector BLOB,
            FOREIGN KEY (item_id) REFERENCES items(id)
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_features_item ON image_features(item_id)')
    
    conn.commit()
    conn.close()
    print("数据库表已创建")

def get_image_paths():
    """获取所有图片路径"""
    images = list(IMAGES_DIR.glob('image*'))
    return {img.name: str(img) for img in images}

if __name__ == "__main__":
    # 设置数据库
    setup_database()
    
    # 获取图片路径
    images = get_image_paths()
    print(f"找到 {len(images)} 张图片")