"""
matcher.py
==========
核心匹配算法模块 — 基于 TF-IDF + 余弦相似度（Cosine Similarity）的
跨境 B2B 智能询盘与规格匹配引擎。

工作原理：
  1. 读取供应商产品库 CSV（product_name + material 作为被检索文本）
  2. 使用 scikit-learn TfidfVectorizer 对产品文本进行向量化
  3. 对买家询盘文本同样向量化
  4. 计算 cosine_similarity，返回 Top-N 最匹配的产品

使用方式：
    from src.matcher import InquiryMatcher
    matcher = InquiryMatcher("data/suppliers_products.csv")
    results = matcher.match("Looking for plush squeaky dog toys, 20cm", top_n=3)
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class InquiryMatcher:
    """询盘智能匹配器。

    将买家询盘文本与供应商产品库进行语义相似度匹配，
    返回最吻合的 Top-N 产品推荐。

    Attributes:
        data_path (str): 供应商产品库 CSV 路径
        df (pd.DataFrame): 加载后的产品数据
        vectorizer (TfidfVectorizer): TF-IDF 向量化器
        tfidf_matrix: 产品文本的 TF-IDF 矩阵
    """

    def __init__(self, data_path):
        """初始化匹配器，加载产品数据并构建 TF-IDF 索引。

        Args:
            data_path (str): suppliers_products.csv 的路径
        """
        self.data_path = data_path
        self.df = pd.read_csv(data_path)

        # 将产品名称 + 材质 + 供应商名称拼接为完整文本，用于向量化
        # 这样既能匹配产品类型（如 "plush toy"）也能匹配材质（如 "natural rubber"）
        product_texts = (
            self.df["product_name"].fillna("") + " " +
            self.df["material"].fillna("") + " " +
            self.df.get("supplier_name", pd.Series([""] * len(self.df))).fillna("")
        )

        # 初始化 TF-IDF 向量化器
        # - ngram_range=(1,2): 使用 unigram + bigram，捕获 "dog toy"、"rubber ball" 等短语
        # - stop_words="english": 去除英文停用词（a, the, for 等），减少噪声
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            lowercase=True,
        )

        # 对产品文本进行 fit_transform，构建 TF-IDF 矩阵（索引）
        self.tfidf_matrix = self.vectorizer.fit_transform(product_texts)

    def match(self, buyer_text, top_n=3):
        """将买家询盘文本与产品库匹配，返回 Top-N 结果。

        Args:
            buyer_text (str): 买家询盘文本，例如：
                "Looking for plush squeaky dog toys, size around 20cm, MOQ 500 pcs."
            top_n (int): 返回的匹配数量，默认 3

        Returns:
            pd.DataFrame: 包含以下列的匹配结果表：
                - product_id: 产品编号
                - product_name: 产品名称
                - material: 材质
                - dimensions: 尺寸
                - moq: 起订量
                - unit_price: 单价
                - similarity: 相似度得分（0~1，越高越匹配）
                - similarity_pct: 相似度百分比（如 "89.5%"）
        """
        # 将买家询盘文本向量化（使用已 fit 的 vectorizer，只做 transform）
        inquiry_vec = self.vectorizer.transform([buyer_text])

        # 计算询盘向量与所有产品向量的余弦相似度
        # cosine_similarity 返回 shape=(1, n_products) 的矩阵
        similarities = cosine_similarity(inquiry_vec, self.tfidf_matrix).flatten()

        # 取相似度最高的 Top-N 索引
        top_indices = similarities.argsort()[-top_n:][::-1]

        # 组装结果 DataFrame
        results = self.df.iloc[top_indices].copy()
        results["similarity"] = similarities[top_indices]
        results["similarity_pct"] = (results["similarity"] * 100).round(1).astype(str) + "%"

        # 按相似度降序排列
        results = results.sort_values("similarity", ascending=False).reset_index(drop=True)

        return results

    def match_batch(self, inquiries_df, top_n=3):
        """批量匹配多条询盘。

        Args:
            inquiries_df (pd.DataFrame): 包含 inquiry_id 和 buyer_text 的 DataFrame
            top_n (int): 每条询盘返回的匹配数量

        Returns:
            dict: {inquiry_id: pd.DataFrame} 映射
        """
        results = {}
        for _, row in inquiries_df.iterrows():
            results[row["inquiry_id"]] = self.match(row["buyer_text"], top_n=top_n)
        return results


# ---------------------------------------------------------------------------
# 命令行直接运行时的演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os

    # 定位数据文件
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "suppliers_products.csv")
    inquiries_path = os.path.join(base_dir, "data", "inquiries.csv")

    # 初始化匹配器
    matcher = InquiryMatcher(data_path)

    # 演示：单条询盘匹配
    print("=" * 80)
    print("B2B 智能询盘匹配系统 — 演示")
    print("=" * 80)

    demo_inquiry = "Looking for plush squeaky dog toys, size around 20cm, durable material, MOQ 500 pcs."
    print(f"\n[买家询盘] {demo_inquiry}\n")

    results = matcher.match(demo_inquiry, top_n=3)

    print(f"{'排名':<6}{'产品编号':<12}{'产品名称':<45}{'相似度':<12}{'单价':<10}{'起订量':<10}")
    print("-" * 95)
    for i, row in results.iterrows():
        print(f"{i+1:<6}{row['product_id']:<12}{row['product_name']:<45}{row['similarity_pct']:<12}${row['unit_price']:<9.2f}{row['moq']} pcs")

    print("\n" + "=" * 80)

    # 演示：批量匹配
    if os.path.exists(inquiries_path):
        inquiries_df = pd.read_csv(inquiries_path)
        print(f"\n[批量匹配] 共 {len(inquiries_df)} 条询盘\n")

        batch_results = matcher.match_batch(inquiries_df, top_n=1)
        for inq_id, res in batch_results.items():
            if len(res) > 0:
                top = res.iloc[0]
                original_text = inquiries_df[inquiries_df["inquiry_id"] == inq_id]["buyer_text"].values[0]
                print(f"  {inq_id}: {top['product_name']} (相似度 {top['similarity_pct']})")
                print(f"         询盘: {original_text[:60]}...")
                print()
