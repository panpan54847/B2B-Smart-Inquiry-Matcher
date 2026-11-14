"""
app.py
======
跨境 B2B 智能询盘与规格匹配助手 — Streamlit 网页应用

功能：
  - 输入/粘贴海外买家询盘文本
  - 基于 TF-IDF + 余弦相似度自动匹配最吻合的供应商产品
  - 展示 Top-3 匹配结果（相似度、单价、起订量等）
  - 支持批量询盘匹配演示
  - 内置示例询盘快速体验

运行方式：
    streamlit run app.py
"""

import os
import sys

import streamlit as st
import pandas as pd

# 将 src 目录加入路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
from matcher import InquiryMatcher

# ---------------------------------------------------------------------------
# 页面配置
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="B2B 智能询盘匹配助手",
    page_icon="🐶",
    layout="wide",
)

# ---------------------------------------------------------------------------
# 数据加载 & 缓存
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUPPLIERS_CSV = os.path.join(BASE_DIR, "data", "suppliers_products.csv")
INQUIRIES_CSV = os.path.join(BASE_DIR, "data", "inquiries.csv")


@st.cache_resource
def get_matcher(csv_path):
    """缓存初始化匹配器，避免每次交互都重新加载。"""
    return InquiryMatcher(csv_path)


@st.cache_data
def load_inquiries(csv_path):
    """缓存加载询盘样本数据。"""
    return pd.read_csv(csv_path)


# 确保数据文件存在，不存在则提示生成
if not os.path.exists(SUPPLIERS_CSV):
    st.error("⚠️ 未找到供应商产品数据！请先运行 `python data/generate_mock_data.py` 生成模拟数据。")
    st.code("python data/generate_mock_data.py", language="bash")
    st.stop()

matcher = get_matcher(SUPPLIERS_CSV)

# ---------------------------------------------------------------------------
# 页面标题 & 简介
# ---------------------------------------------------------------------------

st.title("🐶 跨境 B2B 智能询盘与规格匹配助手")
st.markdown("""
> 基于 **TF-IDF + 余弦相似度（Cosine Similarity）** 的智能匹配引擎，
> 将海外买家询盘文本与本地供应商产品库自动匹配，推荐最契合的产品规格。
""")

st.divider()

# ---------------------------------------------------------------------------
# 侧边栏 — 供应商产品库概览
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("📦 供应商产品库")
    st.caption(f"共 {len(matcher.df)} 条产品数据")

    # 产品类别筛选
    all_products = matcher.df.copy()
    st.dataframe(
        all_products[["product_id", "product_name", "material", "moq", "unit_price"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "unit_price": st.column_config.NumberColumn(format="$%.2f"),
        },
    )

    st.divider()
    st.markdown("### 📊 技术架构")
    st.markdown("""
    - **算法**: TF-IDF Vectorizer + Cosine Similarity
    - **N-gram**: Unigram + Bigram
    - **停用词**: English stopwords
    - **框架**: Streamlit + scikit-learn
    """)

# ---------------------------------------------------------------------------
# 主面板 — 询盘输入 & 匹配
# ---------------------------------------------------------------------------

col_input, col_examples = st.columns([3, 2])

with col_examples:
    st.subheader("📝 示例询盘")
    st.caption("点击下方按钮快速填充示例询盘文本")

    # 从 inquiries.csv 加载示例
    if os.path.exists(INQUIRIES_CSV):
        inquiries_df = load_inquiries(INQUIRIES_CSV)
        example_options = inquiries_df["buyer_text"].tolist()
    else:
        example_options = [
            "Looking for plush squeaky dog toys, size around 20cm, durable material, MOQ 500 pcs.",
            "Need natural rubber dog balls, bouncy and chew resistant, diameter 6-8cm, bulk order 1000 pcs.",
            "Searching for cotton rope tug toys for medium dogs, approximately 30-50cm, MOQ 500.",
        ]

    selected_example = st.selectbox(
        "选择一个示例询盘：",
        options=range(len(example_options)),
        format_func=lambda i: f"询盘 #{i+1}: {example_options[i][:50]}...",
    )

    use_example = st.button("📋 填充到输入框", use_container_width=True)

with col_input:
    st.subheader("🔍 买家询盘输入")

    default_text = example_options[selected_example] if use_example else (
        "Looking for durable plush squeaky toys for dogs, 20cm, MOQ 500 pcs."
    )

    buyer_inquiry = st.text_area(
        "请输入或粘贴海外买家的询盘文本：",
        value=default_text,
        height=120,
        placeholder="例如：Looking for plush squeaky dog toys, size around 20cm, durable material, MOQ 500 pcs.",
    )

    # 匹配数量选择
    top_n = st.slider("返回匹配数量（Top-N）", min_value=1, max_value=10, value=3)

    match_btn = st.button("🚀 智能匹配供应商产品", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# 匹配结果展示
# ---------------------------------------------------------------------------

if match_btn:
    if not buyer_inquiry.strip():
        st.warning("⚠️ 请输入询盘文本后再进行匹配。")
    else:
        with st.spinner("正在智能匹配供应商产品..."):
            results = matcher.match(buyer_inquiry, top_n=top_n)

        st.divider()
        st.subheader("✅ 匹配结果")
        st.write(f"为您推荐以下 **{len(results)}** 个最契合的供应商及产品规格：")

        # ---------- 卡片式展示 ----------
        for i, row in results.iterrows():
            sim_score = row["similarity"]
            # 根据相似度选择颜色标签
            if sim_score >= 0.5:
                badge = "🟢 高度匹配"
            elif sim_score >= 0.25:
                badge = "🟡 中度匹配"
            else:
                badge = "🔴 低度匹配"

            with st.container():
                cols = st.columns([1, 4, 2])
                with cols[0]:
                    st.metric("排名", f"#{i+1}")
                with cols[1]:
                    st.markdown(f"**{row['product_name']}**")
                    st.caption(f"产品编号: {row['product_id']} | 材质: {row['material']} | 尺寸: {row['dimensions']}")
                with cols[2]:
                    st.markdown(f"**{badge}**")
                    st.metric("相似度", row["similarity_pct"])

                detail_cols = st.columns(3)
                with detail_cols[0]:
                    st.metric("建议单价", f"${row['unit_price']:.2f}")
                with detail_cols[1]:
                    st.metric("起订量 (MOQ)", f"{row['moq']} pcs")
                with detail_cols[2]:
                    st.metric("相似度得分", f"{sim_score:.4f}")

                st.divider()

        # ---------- 表格式展示 ----------
        st.subheader("📊 匹配结果明细表")
        display_df = results[[
            "product_id", "product_name", "material", "dimensions",
            "moq", "unit_price", "similarity_pct"
        ]].rename(columns={
            "product_id": "产品编号",
            "product_name": "产品名称",
            "material": "材质",
            "dimensions": "尺寸",
            "moq": "起订量",
            "unit_price": "单价($)",
            "similarity_pct": "匹配相似度",
        })
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # ---------- 批量询盘匹配 ----------
        st.divider()
        st.subheader("📋 批量询盘匹配演示")
        st.caption("使用 inquiries.csv 中的所有样本询盘进行批量匹配")

        if os.path.exists(INQUIRIES_CSV):
            if st.checkbox("展开批量匹配结果"):
                inquiries_df = load_inquiries(INQUIRIES_CSV)
                batch_results = matcher.match_batch(inquiries_df, top_n=1)

                batch_rows = []
                for inq_id, res in batch_results.items():
                    if len(res) > 0:
                        top = res.iloc[0]
                        inq_text = inquiries_df[inquiries_df["inquiry_id"] == inq_id]["buyer_text"].values[0]
                        batch_rows.append({
                            "询盘编号": inq_id,
                            "询盘文本": inq_text[:60] + "...",
                            "最佳匹配产品": top["product_name"],
                            "匹配相似度": top["similarity_pct"],
                            "建议单价": f"${top['unit_price']:.2f}",
                            "起订量": f"{top['moq']} pcs",
                        })

                batch_df = pd.DataFrame(batch_rows)
                st.dataframe(batch_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# 页脚
# ---------------------------------------------------------------------------

st.divider()
st.caption("© B2B Smart Inquiry Matcher | Powered by TF-IDF + Cosine Similarity | Built with Streamlit")
