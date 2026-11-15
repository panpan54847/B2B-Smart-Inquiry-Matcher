# B2B-Smart-Inquiry-Matcher

> 跨境 B2B 智能询盘与规格匹配助手 — 基于 TF-IDF + 余弦相似度的智能匹配引擎，含一键报价邮件发送

## 项目简介

本项目是一个跨境 B2B 贸易场景下的智能询盘匹配系统。海外买家通常以自然语言文本（询盘）描述需求，
而供应商的产品信息存储在结构化数据库中。本系统利用 **TF-IDF 向量化** + **余弦相似度（Cosine Similarity）**
算法，自动将买家询盘文本与供应商产品库进行语义匹配，推荐最契合的产品规格，并支持**一键发送报价邮件**。

### 核心功能

- 输入/粘贴海外买家询盘文本，智能匹配最吻合的供应商产品
- **大规模数据**：3200+ 条供应商产品（覆盖 15 个制造国、131 个城市、297 家供应商企业），500 条买家询盘（覆盖 42 个国家）
- 匹配结果卡片展示：产品名、供应商公司、联系邮箱、单价、MOQ、认证、交期
- **一键发送报价邮件**：自动生成专业英文报价邮件模板，点击即可打开邮件客户端发送
- 买家询盘列表 Tab：展示买家公司、联系人、邮箱、国家，支持一键回复买家
- 批量询盘匹配：一键处理所有询盘，输出匹配总览表
- 专业 B2B SaaS 风格 UI（自定义 CSS，渐变头部，卡片式布局）
- 侧边栏供应商产品库浏览 + 产地城市筛选

### 技术栈

| 模块 | 技术 |
|------|------|
| 算法 | scikit-learn (TfidfVectorizer + cosine_similarity) |
| 前端 | Streamlit + Custom CSS |
| 数据处理 | pandas |
| 邮件 | mailto: 协议（无需后端，直接调用系统邮件客户端） |
| 语言 | Python 3.8+ |

## 项目结构

```
B2B-Smart-Inquiry-Matcher/
├── data/
│   ├── generate_mock_data.py      # 模拟数据生成脚本（含供应商公司名、邮箱、认证等）
│   ├── suppliers_products.csv     # 供应商产品库（40 条，12 个字段）
│   └── inquiries.csv              # 买家询盘样本（15 条，含买家公司、邮箱、国家）
├── src/
│   ├── __init__.py
│   └── matcher.py                 # 核心匹配算法（TF-IDF + Cosine Similarity）
├── app.py                         # Streamlit 网页应用（专业 UI + 一键邮件）
├── requirements.txt
├── .gitignore
└── README.md
```

## 快速开始

> **注意**：以下所有命令都需要在项目根目录 `B2B-Smart-Inquiry-Matcher/` 下运行。
> 如果你当前在 `C:\Windows\System32` 或系统目录，请先 `cd` 到项目目录，例如：
> ```powershell
> cd "C:\Users\48247\WorkBuddy AI\2026-11-14-11-19-41\B2B-Smart-Inquiry-Matcher"
> ```

### 1. 环境准备

```bash
# 克隆仓库
git clone https://github.com/panpan54847/B2B-Smart-Inquiry-Matcher.git

# 进入项目目录
cd B2B-Smart-Inquiry-Matcher

# 安装依赖
pip install -r requirements.txt
```

**Windows PowerShell 用户请注意**：路径中包含空格时，请用英文双引号包裹路径：
```powershell
cd "C:\Users\48247\WorkBuddy AI\2026-11-14-11-19-41\B2B-Smart-Inquiry-Matcher"
pip install -r requirements.txt
```

### 2. 生成模拟数据

```bash
python data/generate_mock_data.py
```

运行后会在 `data/` 目录下生成：
- `suppliers_products.csv` — 40 条供应商产品数据（含供应商公司名、邮箱、城市、认证、交期）
- `inquiries.csv` — 15 条买家询盘样本（含买家公司、邮箱、国家）

### 3. 测试匹配算法（命令行）

```bash
python src/matcher.py
```

### 4. 启动 Streamlit 网页应用

```bash
streamlit run app.py
```

浏览器将自动打开 `http://localhost:8501`。

如果浏览器没有自动打开，可以手动访问：
- http://localhost:8501
- http://127.0.0.1:8501

---

## 算法说明

### TF-IDF + 余弦相似度

1. **文本预处理**：将供应商产品的 `product_name` + `material` + `supplier_name` 拼接为完整文本
2. **TF-IDF 向量化**：
   - 使用 `TfidfVectorizer` 将文本转为 TF-IDF 特征向量
   - `ngram_range=(1,2)`：同时使用 unigram 和 bigram，捕获 "dog toy"、"rubber ball" 等短语
   - `stop_words="english"`：去除英文停用词（a, the, for 等），减少噪声
3. **余弦相似度**：计算询盘向量与所有产品向量的余弦相似度，取 Top-N 最匹配的结果

### 匹配示例

| 买家询盘 | 最佳匹配产品 | 供应商 | 相似度 |
|---------|------------|-------|-------|
| "Looking for plush squeaky dog toys, 20cm, MOQ 500" | Plush Squeaky Dog Toy - Bone Shape | Yiwu Mayer Pet Products Co., Ltd. | ~52% |
| "Need natural rubber dog balls, bouncy, 6-8cm" | Natural Rubber Dog Ball - Bouncy | Ningbo Champion Rubber Tech Ltd. | ~63% |
| "Searching for cotton rope tug toys, 30-50cm" | Thick Rope Tug Toy for Large Dogs | Cangnan Greenleaf Textile Ltd. | ~48% |

## 一键报价邮件功能

匹配结果中每个产品卡片下方有「一键发送报价邮件」展开区域：

1. **邮件预览**：自动生成专业英文报价邮件，含产品规格、采购数量、价格、买家询盘原文
2. **发送设置**：可编辑发件人姓名/邮箱、收件人（自动填入供应商邮箱）、采购数量、报价单价、币种
3. **一键发送**：点击「📧 一键发送报价邮件」按钮，自动调用系统默认邮件客户端（Outlook/Gmail/Mail 等），收件人、主题、正文全部预填好

技术实现：使用 `mailto:` URI scheme + `urllib.parse.urlencode` 编码 subject 和 body，无需后端邮件服务，点击即打开邮件客户端。

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
| supplier_name | string | 供应商公司名称 |
| contact_email | string | 供应商联系邮箱 |
| country | string | 供应商所在国家 |
| city | string | 供应商所在城市 |
| lead_time | string | 交货周期 |
| certification | string | 认证资质（如 BSCI, CE, FDA） |

### inquiries.csv

| 字段 | 类型 | 说明 |
|------|------|------|
| inquiry_id | string | 询盘编号（如 INQ001） |
| buyer_text | string | 买家询盘文本（英文自然语言） |
| buyer_name | string | 买家联系人姓名 |
| buyer_email | string | 买家联系邮箱 |
| company | string | 买家公司名称 |
| country | string | 买家所在国家 |

## License

MIT
