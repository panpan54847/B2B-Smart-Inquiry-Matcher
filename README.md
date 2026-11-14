# B2B-Smart-Inquiry-Matcher

> 跨境 B2B 智能询盘与规格匹配助手 — 基于 TF-IDF + 余弦相似度的智能匹配引擎

## 项目简介

本项目是一个跨境 B2B 贸易场景下的智能询盘匹配系统。海外买家通常以自然语言文本（询盘）描述需求，
而供应商的产品信息存储在结构化数据库中。本系统利用 **TF-IDF 向量化** + **余弦相似度（Cosine Similarity）**
算法，自动将买家询盘文本与供应商产品库进行语义匹配，推荐最契合的产品规格（单价、起订量等）。

### 核心功能

- 输入/粘贴海外买家询盘文本
- 基于 TF-IDF + Cosine Similarity 自动匹配最吻合的供应商产品
- 展示 Top-N 匹配结果（相似度得分、单价、起订量）
- 支持批量询盘匹配
- Streamlit 网页应用，交互式演示

### 技术栈

| 模块 | 技术 |
|------|------|
| 算法 | scikit-learn (TfidfVectorizer + cosine_similarity) |
| 前端 | Streamlit |
| 数据处理 | pandas |
| 语言 | Python 3.8+ |

## 项目结构

```
B2B-Smart-Inquiry-Matcher/
├── data/
│   ├── generate_mock_data.py      # 模拟数据生成脚本
│   ├── suppliers_products.csv     # 供应商产品库（40 条）— 运行生成脚本后自动产出
│   └── inquiries.csv              # 买家询盘样本（15 条）— 运行生成脚本后自动产出
├── src/
│   ├── __init__.py
│   └── matcher.py                 # 核心匹配算法（TF-IDF + Cosine Similarity）
├── app.py                         # Streamlit 网页应用入口
├── requirements.txt               # Python 依赖
├── .gitignore
└── README.md                      # 项目说明文档
```

## 快速开始

### 1. 环境准备

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/B2B-Smart-Inquiry-Matcher.git
cd B2B-Smart-Inquiry-Matcher

# 安装依赖
pip install -r requirements.txt
```

### 2. 生成模拟数据

```bash
python data/generate_mock_data.py
```

运行后会在 `data/` 目录下生成：
- `suppliers_products.csv` — 40 条供应商产品数据（宠物玩具/外贸商品）
- `inquiries.csv` — 15 条买家询盘样本

### 3. 测试匹配算法（命令行）

```bash
python src/matcher.py
```

### 4. 启动 Streamlit 网页应用

```bash
streamlit run app.py
```

浏览器将自动打开 `http://localhost:8501`。

## 算法说明

### TF-IDF + 余弦相似度

1. **文本预处理**：将供应商产品的 `product_name` + `material` 拼接为完整文本
2. **TF-IDF 向量化**：
   - 使用 `TfidfVectorizer` 将文本转为 TF-IDF 特征向量
   - `ngram_range=(1,2)`：同时使用 unigram 和 bigram，捕获 "dog toy"、"rubber ball" 等短语
   - `stop_words="english"`：去除英文停用词（a, the, for 等），减少噪声
3. **余弦相似度**：计算询盘向量与所有产品向量的余弦相似度，取 Top-N 最匹配的结果

### 匹配示例

| 买家询盘 | 最佳匹配产品 | 相似度 |
|---------|------------|-------|
| "Looking for plush squeaky dog toys, 20cm, MOQ 500" | Plush Squeaky Dog Toy - Bone Shape | ~89% |
| "Need natural rubber dog balls, bouncy, 6-8cm" | Natural Rubber Dog Ball - Bouncy | ~75% |
| "Searching for cotton rope tug toys, 30-50cm" | Cotton Rope Dog Toy - Tug Knot | ~70% |

## 数据字段说明

### suppliers_products.csv

| 字段 | 类型 | 说明 |
|------|------|------|
| product_id | string | 产品编号（如 SP001） |
| product_name | string | 产品名称（英文） |
| material | string | 材质描述 |
| dimensions | string | 尺寸规格 |
| moq | int | 起订量（Minimum Order Quantity） |
| unit_price | float | 单价（美元） |

### inquiries.csv

| 字段 | 类型 | 说明 |
|------|------|------|
| inquiry_id | string | 询盘编号（如 INQ001） |
| buyer_text | string | 买家询盘文本（英文自然语言） |

## License

MIT
