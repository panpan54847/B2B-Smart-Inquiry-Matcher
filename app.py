"""
app.py
======
跨境 B2B 智能询盘与规格匹配助手 — Streamlit 网页应用

功能：
  - 专业 B2B SaaS 风格 UI（自定义 CSS，渐变头部，卡片式布局）
  - 输入/粘贴海外买家询盘文本，TF-IDF + Cosine Similarity 智能匹配
  - 匹配结果卡片展示：产品名、供应商公司、联系邮箱、单价、MOQ、认证、交期
  - 一键发送报价邮件（mailto: 自动生成模板，含产品规格、数量、价格）
  - 询盘样本展示：买家公司名、联系人、邮箱、国家
  - 侧边栏：供应商产品库浏览 + 城市筛选
  - 批量询盘匹配演示

运行方式：
    streamlit run app.py
"""

import os
import sys
import urllib.parse

import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
from matcher import InquiryMatcher

# ---------------------------------------------------------------------------
# 页面配置
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="B2B 智能询盘匹配助手",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# 自定义 CSS — 专业 B2B SaaS 风格
# ---------------------------------------------------------------------------

st.markdown("""
<style>
/* ---------- 全局 ---------- */
.stApp {
    background: #f0f2f5;
}

/* ---------- 顶部 Banner ---------- */
.main-banner {
    background: linear-gradient(135deg, #1a365d 0%, #2563eb 50%, #1e40af 100%);
    padding: 28px 36px;
    border-radius: 0 0 20px 20px;
    margin: -1rem -1rem 1.5rem -1rem;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.3);
}
.main-banner h1 {
    color: #ffffff;
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 6px;
}
.main-banner p {
    color: #bfdbfe;
    font-size: 14px;
    margin: 0;
}

/* ---------- 统计卡片 ---------- */
.stat-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-left: 4px solid #2563eb;
    text-align: center;
}
.stat-card .stat-value {
    font-size: 28px;
    font-weight: 800;
    color: #1a365d;
    line-height: 1.2;
}
.stat-card .stat-label {
    font-size: 12px;
    color: #64748b;
    margin-top: 4px;
}

/* ---------- 匹配结果卡片 ---------- */
.result-card {
    background: #ffffff;
    border-radius: 14px;
    margin-bottom: 14px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    border: 1px solid #e2e8f0;
    transition: box-shadow 0.2s;
}
.result-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.12);
}
.result-card-header {
    padding: 14px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #f1f5f9;
}
.result-card-rank {
    background: #2563eb;
    color: white;
    font-weight: 700;
    font-size: 16px;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
.result-card-name {
    font-size: 17px;
    font-weight: 700;
    color: #1e293b;
    flex: 1;
    margin-left: 12px;
}
.similarity-badge {
    font-size: 13px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
}
.sim-high {
    background: #dcfce7;
    color: #166534;
}
.sim-mid {
    background: #fef9c3;
    color: #854d0e;
}
.sim-low {
    background: #fee2e2;
    color: #991b1b;
}
.result-card-body {
    padding: 16px 20px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
}
.info-item .info-label {
    font-size: 11px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
}
.info-item .info-value {
    font-size: 14px;
    font-weight: 600;
    color: #334155;
}
.result-card-footer {
    padding: 10px 20px;
    background: #f8fafc;
    border-top: 1px solid #f1f5f9;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.supplier-info {
    font-size: 13px;
    color: #475569;
}
.supplier-info strong {
    color: #1e293b;
}

/* ---------- 询盘卡片 ---------- */
.inquiry-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    border-left: 4px solid #2563eb;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
}
.inquiry-card .buyer-name {
    font-size: 15px;
    font-weight: 700;
    color: #1e293b;
}
.inquiry-card .buyer-meta {
    font-size: 12px;
    color: #64748b;
    margin-top: 2px;
}
.inquiry-card .buyer-text {
    font-size: 13px;
    color: #475569;
    margin-top: 8px;
    padding: 10px;
    background: #f8fafc;
    border-radius: 8px;
    line-height: 1.5;
    border-left: 3px solid #cbd5e1;
}

/* ---------- 邮件模板区 ---------- */
.email-template-box {
    background: #1e293b;
    color: #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
    border: 1px solid #334155;
}

/* ---------- 按钮样式增强 ---------- */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

/* ---------- 侧边栏 ---------- */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e2e8f0;
}

/* ---------- 分割线 ---------- */
hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 数据加载 & 缓存
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUPPLIERS_CSV = os.path.join(BASE_DIR, "data", "suppliers_products.csv")
INQUIRIES_CSV = os.path.join(BASE_DIR, "data", "inquiries.csv")


@st.cache_resource
def get_matcher(csv_path):
    return InquiryMatcher(csv_path)


@st.cache_data
def load_inquiries(csv_path):
    return pd.read_csv(csv_path)


@st.cache_data
def load_suppliers(csv_path):
    return pd.read_csv(csv_path)


if not os.path.exists(SUPPLIERS_CSV):
    st.error("未找到供应商产品数据！请先运行 `python data/generate_mock_data.py`")
    st.code("python data/generate_mock_data.py", language="bash")
    st.stop()

matcher = get_matcher(SUPPLIERS_CSV)
suppliers_df = load_suppliers(SUPPLIERS_CSV)
inquiries_df = load_inquiries(INQUIRIES_CSV) if os.path.exists(INQUIRIES_CSV) else pd.DataFrame()

# ---------------------------------------------------------------------------
# 顶部 Banner
# ---------------------------------------------------------------------------

st.markdown("""
<div class="main-banner">
    <h1>🏭 跨境 B2B 智能询盘与规格匹配助手</h1>
    <p>TF-IDF + Cosine Similarity 智能匹配引擎 · 自动推荐最契合的供应商产品 · 一键发送报价邮件</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 统计数据条
# ---------------------------------------------------------------------------

stat_cols = st.columns(5)
with stat_cols[0]:
    st.markdown('<div class="stat-card"><div class="stat-value">{}</div><div class="stat-label">供应商产品</div></div>'.format(len(suppliers_df)), unsafe_allow_html=True)
with stat_cols[1]:
    unique_suppliers = suppliers_df["supplier_name"].nunique() if "supplier_name" in suppliers_df.columns else 0
    st.markdown('<div class="stat-card"><div class="stat-value">{}</div><div class="stat-label">供应商企业</div></div>'.format(unique_suppliers), unsafe_allow_html=True)
with stat_cols[2]:
    st.markdown('<div class="stat-card"><div class="stat-value">{}</div><div class="stat-label">买家询盘</div></div>'.format(len(inquiries_df)), unsafe_allow_html=True)
with stat_cols[3]:
    countries = inquiries_df["country"].nunique() if "country" in inquiries_df.columns and len(inquiries_df) > 0 else 0
    st.markdown('<div class="stat-card"><div class="stat-value">{}</div><div class="stat-label">买家国家</div></div>'.format(countries), unsafe_allow_html=True)
with stat_cols[4]:
    cities = suppliers_df["city"].nunique() if "city" in suppliers_df.columns else 0
    st.markdown('<div class="stat-card"><div class="stat-value">{}</div><div class="stat-label">产地城市</div></div>'.format(cities), unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------------------------
# 侧边栏 — 供应商产品库
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### 📦 供应商产品库")
    st.caption(f"共 {len(suppliers_df)} 条产品 · {unique_suppliers} 家供应商")

    # 城市筛选
    if "city" in suppliers_df.columns:
        all_cities = ["全部"] + sorted(suppliers_df["city"].unique().tolist())
        selected_city = st.selectbox("🏭 按产地城市筛选", all_cities)
        if selected_city != "全部":
            filtered = suppliers_df[suppliers_df["city"] == selected_city]
        else:
            filtered = suppliers_df
    else:
        filtered = suppliers_df

    # 国家筛选
    if "country" in filtered.columns and filtered["country"].nunique() > 1:
        all_countries = ["全部"] + sorted(filtered["country"].unique().tolist())
        selected_country = st.selectbox("🌍 按供应商国家筛选", all_countries)
        if selected_country != "全部":
            filtered = filtered[filtered["country"] == selected_country]

    st.caption(f"当前筛选: {len(filtered)} 条产品")

    # 产品表格
    display_cols = ["product_id", "product_name", "supplier_name", "country", "unit_price", "moq"]
    available_cols = [c for c in display_cols if c in filtered.columns]
    st.dataframe(
        filtered[available_cols].head(500),
        use_container_width=True,
        hide_index=True,
        height=400,
        column_config={
            "unit_price": st.column_config.NumberColumn(format="$%.2f"),
            "product_name": st.column_config.TextColumn(width="medium"),
            "supplier_name": st.column_config.TextColumn(width="medium"),
        },
    )

    st.divider()
    st.markdown("### 📊 技术架构")
    st.markdown("""
    - **算法**: TF-IDF Vectorizer + Cosine Similarity
    - **N-gram**: Unigram + Bigram
    - **停用词**: English stopwords
    - **前端**: Streamlit + Custom CSS
    - **数据**: pandas
    """)

# ---------------------------------------------------------------------------
# 主面板 — Tab 切换
# ---------------------------------------------------------------------------

tab_match, tab_inquiries = st.tabs(["🔍 智能匹配", "📋 买家询盘列表"])

# ===========================================================================
# Tab 1: 智能匹配
# ===========================================================================

with tab_match:
    col_input, col_examples = st.columns([3, 2])

    with col_examples:
        st.markdown("#### 📝 示例询盘")
        st.caption("选择一条真实买家询盘快速体验")

        if len(inquiries_df) > 0:
            # 国家筛选 — 避免下拉框太长
            inq_countries = ["全部"] + sorted(inquiries_df["country"].unique().tolist())
            sel_inq_country = st.selectbox("🌍 按买家国家筛选", inq_countries, key="inq_country")
            if sel_inq_country != "全部":
                filtered_inq = inquiries_df[inquiries_df["country"] == sel_inq_country]
            else:
                filtered_inq = inquiries_df

            # 随机抽样最多 50 条供选择
            if len(filtered_inq) > 50:
                sample_inq = filtered_inq.sample(n=50, random_state=42).sort_values("inquiry_id").reset_index(drop=True)
            else:
                sample_inq = filtered_inq.reset_index(drop=True)

            example_options = sample_inq["buyer_text"].tolist()
            example_labels = [
                f"{sample_inq.iloc[i]['inquiry_id']} · {sample_inq.iloc[i]['buyer_name']} ({sample_inq.iloc[i]['country']})"
                for i in range(len(sample_inq))
            ]
        else:
            example_options = [
                "Looking for plush squeaky dog toys, size around 20cm, durable material, MOQ 500 pcs.",
                "Need natural rubber dog balls, bouncy and chew resistant, diameter 6-8cm, bulk order 1000 pcs.",
            ]
            example_labels = [f"示例 #{i+1}" for i in range(len(example_options))]

        selected_idx = st.selectbox(
            "选择询盘样本：",
            options=range(len(example_options)),
            format_func=lambda i: example_labels[i] if i < len(example_labels) else "",
        )

        use_example = st.button("📋 填充到输入框", use_container_width=True)

        # 展示选中询盘的买家信息
        if len(sample_inq) > 0 and selected_idx is not None and selected_idx < len(sample_inq):
            sel = sample_inq.iloc[selected_idx]
            st.markdown("---")
            st.markdown(f"""
            <div class="inquiry-card">
                <div class="buyer-name">{sel['buyer_name']}</div>
                <div class="buyer-meta">📧 {sel['buyer_email']} &nbsp;|&nbsp; 🏢 {sel['company']} &nbsp;|&nbsp; 🌍 {sel['country']}</div>
                <div class="buyer-text">{sel['buyer_text']}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_input:
        st.markdown("#### 🔍 买家询盘输入")

        default_text = example_options[selected_idx] if (use_example or selected_idx is not None) else ""

        buyer_inquiry = st.text_area(
            "询盘文本（支持中英文）：",
            value=default_text,
            height=100,
            placeholder="例如：Looking for plush squeaky dog toys, size around 20cm, durable material, MOQ 500 pcs.",
        )

        col_n, col_btn = st.columns([1, 2])
        with col_n:
            top_n = st.slider("匹配数量 (Top-N)", min_value=1, max_value=10, value=3)
        with col_btn:
            st.write("")
            st.write("")
            match_btn = st.button("🚀 智能匹配", type="primary", use_container_width=True)

    # ---------- 匹配结果 ----------

    if match_btn:
        if not buyer_inquiry.strip():
            st.warning("请输入询盘文本后再进行匹配。")
        else:
            with st.spinner("正在智能匹配供应商产品..."):
                results = matcher.match(buyer_inquiry, top_n=top_n)

            st.markdown("---")
            st.markdown(f"#### ✅ 匹配结果（Top-{len(results)}）")
            st.write(f"共扫描 {len(matcher.df)} 条产品，为您推荐以下最契合的供应商：")

            for i, row in results.iterrows():
                sim_score = row["similarity"]

                # 相似度等级
                if sim_score >= 0.5:
                    badge_class = "sim-high"
                    badge_text = "高度匹配"
                elif sim_score >= 0.25:
                    badge_class = "sim-mid"
                    badge_text = "中度匹配"
                else:
                    badge_class = "sim-low"
                    badge_text = "低度匹配"

                # 供应商信息
                supplier_name = row.get("supplier_name", "N/A")
                contact_email = row.get("contact_email", "")
                country = row.get("country", "")
                city = row.get("city", "")
                lead_time = row.get("lead_time", "")
                certification = row.get("certification", "")

                # 渲染卡片
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-card-header">
                        <div style="display:flex;align-items:center;flex:1;">
                            <span class="result-card-rank">{i+1}</span>
                            <span class="result-card-name">{row['product_name']}</span>
                        </div>
                        <span class="similarity-badge {badge_class}">{badge_text} · {row['similarity_pct']}</span>
                    </div>
                    <div class="result-card-body">
                        <div class="info-item">
                            <div class="info-label">单价</div>
                            <div class="info-value">${row['unit_price']:.2f}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">起订量 MOQ</div>
                            <div class="info-value">{row['moq']} pcs</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">尺寸</div>
                            <div class="info-value">{row['dimensions']}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">材质</div>
                            <div class="info-value">{row['material']}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">交期</div>
                            <div class="info-value">{lead_time}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">认证</div>
                            <div class="info-value">{certification}</div>
                        </div>
                    </div>
                    <div class="result-card-footer">
                        <div class="supplier-info">
                            🏭 <strong>{supplier_name}</strong> &nbsp;|&nbsp; 📍 {city}, {country} &nbsp;|&nbsp; 📧 {contact_email}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ---------- 一键发送报价邮件 ----------
                with st.expander(f"✉️ 一键发送报价邮件 — {row['product_name']}", expanded=(i == 0)):
                    email_tab_view, email_tab_send = st.tabs(["📋 邮件预览", "📤 发送设置"])

                    with email_tab_send:
                        # 发件人信息
                        sender_cols = st.columns(2)
                        with sender_cols[0]:
                            sender_name = st.text_input("您的称呼", value="Export Manager", key=f"sender_name_{i}")
                        with sender_cols[1]:
                            sender_email = st.text_input("您的邮箱", value="export@mycompany.com", key=f"sender_email_{i}")

                        # 收件人（供应商邮箱）
                        recipient = st.text_input("收件人（供应商邮箱）", value=contact_email, key=f"recipient_{i}")

                        # 报价参数
                        qty_cols = st.columns(3)
                        with qty_cols[0]:
                            order_qty = st.number_input("采购数量", min_value=int(row["moq"]), value=int(row["moq"]), step=100, key=f"qty_{i}")
                        with qty_cols[1]:
                            quoted_price = st.number_input("报价单价 ($)", min_value=0.01, value=float(row["unit_price"]), step=0.05, key=f"price_{i}")
                        with qty_cols[2]:
                            currency = st.selectbox("币种", ["USD", "EUR", "GBP", "CNY"], key=f"curr_{i}")

                    with email_tab_view:
                        # 生成邮件模板
                        subject = f"Inquiry Quote: {row['product_name']} - Order {order_qty} pcs"
                        body = f"""Dear {supplier_name} Team,

We received a buyer inquiry that closely matches your product. Please find the details below:

----------------------------------------
PRODUCT MATCH DETAILS
----------------------------------------
Product:        {row['product_name']}
Product ID:     {row['product_id']}
Material:       {row['material']}
Dimensions:     {row['dimensions']}
Match Score:    {row['similarity_pct']}

----------------------------------------
ORDER REQUIREMENTS
----------------------------------------
Quantity:       {order_qty} pcs
Unit Price:     {currency} {quoted_price:.2f}
Total Amount:   {currency} {order_qty * quoted_price:.2f}
MOQ:            {row['moq']} pcs

----------------------------------------
BUYER INQUIRY (Original Text)
----------------------------------------
"{buyer_inquiry}"

----------------------------------------
REQUEST
----------------------------------------
1. Please confirm availability and production lead time.
2. Provide FOB / EXW pricing for the requested quantity.
3. Share product catalog and certification documents ({certification}).
4. Confirm payment terms (T/T, L/C, etc.).

We look forward to your prompt quotation.

Best regards,
{sender_name}
{sender_email}
"""

                        st.markdown(f"**Subject:** {subject}")
                        st.markdown("")
                        st.markdown(f'<div class="email-template-box">{body}</div>', unsafe_allow_html=True)

                        # 一键发送按钮 — mailto 链接
                        mailto_url = urllib.parse.urlencode({
                            "subject": subject,
                            "body": body,
                        })
                        mailto_link = f"mailto:{recipient}?{mailto_url}"

                        st.markdown(f"""
                        <a href="{mailto_link}" style="
                            display: inline-block;
                            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
                            color: white;
                            font-weight: 700;
                            font-size: 15px;
                            padding: 12px 32px;
                            border-radius: 10px;
                            text-decoration: none;
                            margin-top: 12px;
                            box-shadow: 0 2px 10px rgba(37, 99, 235, 0.3);
                        ">📧 一键发送报价邮件</a>
                        """, unsafe_allow_html=True)

                        st.caption(f"点击后将打开您的默认邮件客户端，收件人：{recipient}")

            # ---------- 匹配明细表 ----------
            st.markdown("---")
            st.markdown("#### 📊 匹配结果明细表")
            table_cols = [c for c in ["product_id", "product_name", "supplier_name", "material", "dimensions", "moq", "unit_price", "lead_time", "certification", "similarity_pct"] if c in results.columns]
            rename_map = {
                "product_id": "产品编号", "product_name": "产品名称", "supplier_name": "供应商",
                "material": "材质", "dimensions": "尺寸", "moq": "MOQ", "unit_price": "单价",
                "lead_time": "交期", "certification": "认证", "similarity_pct": "相似度",
            }
            st.dataframe(
                results[table_cols].rename(columns=rename_map),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "单价": st.column_config.NumberColumn(format="$%.2f"),
                },
            )

# ===========================================================================
# Tab 2: 买家询盘列表
# ===========================================================================

with tab_inquiries:
    st.markdown("#### 📋 买家询盘列表")
    st.caption(f"共 {len(inquiries_df)} 条询盘 · 来自 {inquiries_df['country'].nunique() if len(inquiries_df) > 0 else 0} 个国家")

    if len(inquiries_df) > 0:
        # 国家筛选
        country_list = ["全部"] + sorted(inquiries_df["country"].unique().tolist())
        filter_country = st.selectbox("🌍 按国家筛选", country_list, key="country_filter")
        filtered_inq = inquiries_df if filter_country == "全部" else inquiries_df[inquiries_df["country"] == filter_country]

        # 分页 — 每页 20 条
        page_size = 20
        total_pages = max(1, (len(filtered_inq) + page_size - 1) // page_size)
        page = st.number_input("📄 页码", min_value=1, max_value=total_pages, value=1, key="inq_page")
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_data = filtered_inq.iloc[start_idx:end_idx]

        st.caption(f"第 {page}/{total_pages} 页 · 显示 {len(page_data)} 条（共 {len(filtered_inq)} 条）")

        # 询盘卡片列表
        for _, row in page_data.iterrows():
            # 快速匹配按钮
            col_card, col_action = st.columns([4, 1])

            with col_card:
                st.markdown(f"""
                <div class="inquiry-card">
                    <div class="buyer-name">{row['buyer_name']}</div>
                    <div class="buyer-meta">
                        📧 {row['buyer_email']} &nbsp;|&nbsp; 🏢 {row['company']} &nbsp;|&nbsp; 🌍 {row['country']} &nbsp;|&nbsp; 🏷️ {row['inquiry_id']}
                    </div>
                    <div class="buyer-text">{row['buyer_text']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_action:
                st.write("")
                st.write("")
                if st.button(f"🔍 匹配", key=f"quick_match_{row['inquiry_id']}", use_container_width=True):
                    # 快速匹配 → 切到匹配 Tab
                    st.session_state["quick_inquiry"] = row["buyer_text"]
                    st.info(f"已加载询盘，请切换到「智能匹配」Tab 查看结果。\n\n**询盘内容：** {row['buyer_text'][:80]}...")

                # 一键邮件联系买家
                mailto_buyer = f"mailto:{row['buyer_email']}?subject=Re: Product Inquiry ({row['inquiry_id']})&body=Dear {row['buyer_name']},%0D%0A%0D%0AThank you for your inquiry. We have reviewed your requirements and would like to propose the following products for your consideration.%0D%0A%0D%0APlease find attached our product catalog and quotation for your reference.%0D%0A%0D%0ABest regards"
                st.markdown(f"""
                <a href="{mailto_buyer}" style="
                    display: inline-block;
                    background: #059669;
                    color: white;
                    font-weight: 600;
                    font-size: 13px;
                    padding: 8px 16px;
                    border-radius: 8px;
                    text-decoration: none;
                    text-align: center;
                    width: 100%;
                ">📧 回复买家</a>
                """, unsafe_allow_html=True)

        # 批量匹配
        st.markdown("---")
        st.markdown("#### 📊 批量匹配总览")
        batch_limit = st.slider("批量匹配数量上限", min_value=10, max_value=min(200, len(filtered_inq)), value=min(50, len(filtered_inq)), key="batch_limit_slider")
        if st.button(f"🚀 批量匹配当前筛选下的询盘（最多 {batch_limit} 条）", type="primary"):
            batch_inq = filtered_inq.head(batch_limit)
            with st.spinner(f"正在批量匹配 {len(batch_inq)} 条询盘，扫描 {len(matcher.df)} 条产品..."):
                batch_results = matcher.match_batch(batch_inq, top_n=1)

            batch_rows = []
            for _, inq_row in batch_inq.iterrows():
                inq_id = inq_row["inquiry_id"]
                res = batch_results.get(inq_id)
                if res is not None and len(res) > 0:
                    top = res.iloc[0]
                    batch_rows.append({
                        "询盘编号": inq_id,
                        "买家": inq_row["buyer_name"],
                        "买家公司": inq_row["company"],
                        "国家": inq_row["country"],
                        "询盘摘要": inq_row["buyer_text"][:55] + "...",
                        "最佳匹配产品": top["product_name"],
                        "供应商": top.get("supplier_name", ""),
                        "相似度": top["similarity_pct"],
                        "单价": f"${top['unit_price']:.2f}",
                        "MOQ": f"{top['moq']} pcs",
                        "供应商邮箱": top.get("contact_email", ""),
                    })

            batch_df = pd.DataFrame(batch_rows)
            st.dataframe(batch_df, use_container_width=True, hide_index=True)

            st.success(f"批量匹配完成！共处理 {len(batch_rows)} 条询盘。")

    else:
        st.info("暂无询盘数据。请先运行 `python data/generate_mock_data.py` 生成数据。")

# ---------------------------------------------------------------------------
# 页脚
# ---------------------------------------------------------------------------

st.divider()
st.caption("© B2B Smart Inquiry Matcher | TF-IDF + Cosine Similarity | Streamlit + Custom CSS")
