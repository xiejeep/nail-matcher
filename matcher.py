#!/usr/bin/env python3
"""
美甲图片匹配器 - 使用 CLIP 深度特征
"""

import os
import sys
import sqlite3
from pathlib import Path
import numpy as np
from PIL import Image
import json

PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "货盘分类.db"
IMAGES_DIR = PROJECT_ROOT / "货盘分类图片"
MODEL_PATH = Path(__file__).parent / "models" / "sentence-transformers" / "clip-ViT-B-32"

class NailMatcher:
    def __init__(self):
        self.model = None
        self.feature_dim = 512
        
    def load_model(self):
        if self.model is not None:
            return
            
        print(f"正在加载本地模型...")
        
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(str(MODEL_PATH))
        print("模型加载完成")
    
    def extract_features(self, image_path):
        """提取单张图片的特征向量"""
        self.load_model()
        
        try:
            image = Image.open(image_path).convert('RGB')
            features = self.model.encode(image)
            return features.astype(np.float32)
        except Exception as e:
            print(f"处理图片失败 {image_path}: {e}")
            return None
    
    def batch_extract(self, image_paths, batch_size=32):
        """批量提取特征"""
        self.load_model()
        
        images = []
        valid_paths = []
        
        for path in image_paths:
            try:
                img = Image.open(path).convert('RGB')
                images.append(img)
                valid_paths.append(path)
            except Exception as e:
                print(f"跳过无效图片 {path}: {e}")
        
        if not images:
            return [], []
        
        print(f"正在提取 {len(images)} 张图片的特征...")
        features = self.model.encode(images, batch_size=batch_size, show_progress_bar=True)
        
        return valid_paths, features
    
    def build_index(self):
        """构建所有图片的特征索引"""
        print("=" * 50)
        print("开始构建特征索引")
        print("=" * 50)
        
        # 获取数据库中有图片的货品
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT i.id, i.item_code, i.category_id, i.image_path, c.name as category_name
            FROM items i
            JOIN categories c ON i.category_id = c.id
            WHERE i.image_path IS NOT NULL
        ''')
        
        items = cursor.fetchall()
        print(f"找到 {len(items)} 个有图片的货品")
        
        # 清空旧特征
        cursor.execute('DELETE FROM image_features')
        conn.commit()
        
        # 批量提取特征
        image_paths = []
        for item_id, item_code, cat_id, img_path, cat_name in items:
            full_path = PROJECT_ROOT / img_path
            if full_path.exists():
                image_paths.append((item_id, str(full_path)))
        
        if not image_paths:
            print("没有找到有效的图片文件")
            return
        
        paths_only = [p[1] for p in image_paths]
        valid_paths, features = self.batch_extract(paths_only)
        
        # 存入数据库
        print("正在保存特征到数据库...")
        for i, (item_id, _) in enumerate(image_paths):
            if i < len(features):
                feature_blob = features[i].tobytes()
                cursor.execute('''
                    INSERT INTO image_features (item_id, image_path, feature_vector)
                    VALUES (?, ?, ?)
                ''', (item_id, valid_paths[i], feature_blob))
        
        conn.commit()
        conn.close()
        
        print(f"完成！已索引 {len(features)} 张图片")
    
    def search(self, query_image_path, top_k=10):
        """搜索相似图片"""
        print(f"\n搜索相似图片: {query_image_path}")
        
        # 提取查询图片特征
        query_features = self.extract_features(query_image_path)
        if query_features is None:
            return []
        
        # 从数据库加载所有特征
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.item_id, f.feature_vector, i.item_code, i.price, c.name as category
            FROM image_features f
            JOIN items i ON f.item_id = i.id
            JOIN categories c ON i.category_id = c.id
        ''')
        
        results = []
        for item_id, feat_blob, item_code, price, category in cursor.fetchall():
            feat = np.frombuffer(feat_blob, dtype=np.float32)
            # 计算余弦相似度
            similarity = np.dot(query_features, feat) / (
                np.linalg.norm(query_features) * np.linalg.norm(feat)
            )
            results.append({
                'item_id': item_id,
                'item_code': item_code,
                'price': price,
                'category': category,
                'similarity': float(similarity)
            })
        
        conn.close()
        
        # 排序并返回 top_k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
    
    def search_and_display(self, query_image_path, top_k=10):
        """搜索并显示结果"""
        results = self.search(query_image_path, top_k)
        
        if not results:
            print("未找到相似图片")
            return
        
        print("\n" + "=" * 60)
        print(f"Top {len(results)} 相似图片:")
        print("=" * 60)
        print(f"{'排名':<4} {'相似度':<8} {'货号':<10} {'价格':<8} {'分类':<15}")
        print("-" * 60)
        
        for i, r in enumerate(results, 1):
            price_str = f"{r['price']}" if r['price'] is not None else "N/A"
            print(f"{i:<4} {r['similarity']:.4f}   {r['item_code']:<10} {price_str:<8} {r['category']:<15}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='美甲图片匹配器')
    parser.add_argument('command', choices=['index', 'search'], help='命令: index(建立索引) 或 search(搜索)')
    parser.add_argument('--image', '-i', help='搜索用的图片路径')
    parser.add_argument('--top-k', '-k', type=int, default=10, help='返回结果数量')
    
    args = parser.parse_args()
    
    matcher = NailMatcher()
    
    if args.command == 'index':
        matcher.build_index()
    elif args.command == 'search':
        if not args.image:
            print("请提供图片路径: --image 或 -i")
            sys.exit(1)
        matcher.search_and_display(args.image, args.top_k)


if __name__ == "__main__":
    main()