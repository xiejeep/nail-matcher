# 美甲图片匹配器 - 用户使用指南

## 安装与启动

### 方式一：一键启动（推荐）

**macOS用户：**
1. 打开终端
2. 进入项目目录：`cd nail-matcher`
3. 运行：`./run.sh`

**Windows用户：**
1. 双击 `run.bat` 文件

脚本会自动完成所有设置：
- ✓ 创建Python虚拟环境
- ✓ 安装必要依赖
- ✓ 下载AI模型（首次需要2-5分钟）
- ✓ 启动应用
- ✓ 自动打开浏览器

### 方式二：手动启动

如遇问题，可手动执行：

```bash
# macOS/Linux
cd nail-matcher
source venv/bin/activate
python download_model.py  # 首次必须
python app.py

# Windows
cd nail-matcher
venv\Scripts\activate.bat
python download_model.py  # 首次必须
python app.py
```

## 使用流程

1. 浏览器自动打开界面（或手动访问 http://127.0.0.1:3001）
2. 点击上传区域，选择美甲图片
3. 或直接拖拽图片到上传区域
4. 系统自动搜索相似款式
5. 查看搜索结果：
   - 相似度百分比
   - 货号
   - 价格
   - 分类
   - 图片预览

## 关闭应用

在终端窗口按 `Ctrl+C` 关闭应用

## 常见问题

### Q1: 首次启动很慢？
A: 首次启动需要下载AI模型（约1.1GB），需要2-5分钟。之后启动很快。

### Q2: 浏览器没有自动打开？
A: 手动访问 http://127.0.0.1:3001

### Q3: 无法上传图片？
A: 检查图片格式（支持PNG/JPG/WEBP），大小不超过16MB

### Q4: 搜索速度慢？
A: 首次搜索需加载模型，约2秒。之后搜索<1秒。

### Q5: Windows上运行报错？
A: 确保已安装Python 3.11+，并勾选了"Add Python to PATH"

## 支持的图片格式

- PNG
- JPG / JPEG
- WEBP
- GIF
- 最大文件大小：16MB

## 技术参数

- AI模型：CLIP ViT-B-32
- 特征维度：512维
- 数据库：1069张美甲图片
- 搜索速度：<1秒
- 相似度阈值：自动排序

## 注意事项

1. 应用运行时请勿关闭终端窗口
2. 首次使用必须下载模型
3. 模型只需下载一次，后续可重复使用
4. 支持 macOS / Windows / Linux

---

**技术支持：** 如有问题请联系开发者