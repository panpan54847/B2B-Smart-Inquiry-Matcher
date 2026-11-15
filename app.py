"""
app.py
======
Cross-border B2B Smart Inquiry & Specification Matcher - Streamlit Web App

Features:
  - Professional B2B SaaS style UI (custom CSS, gradient banner, card layout)
  - Input/paste buyer inquiry text, TF-IDF + Cosine Similarity smart matching
  - Match result cards: product name, supplier company, contact email, unit price, MOQ, certification, lead time
  - One-click quote email sending (mailto: auto-generated template with product specs, quantity, pricing)
  - Inquiry sample showcase: buyer company name, contact person, email, country
  - Sidebar: supplier product library browsing + city filter
  - Batch inquiry matching demo

Run:
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
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="B2B Smart Inquiry Matcher",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS - Professional B2B SaaS style
# ---------------------------------------------------------------------------

st.markdown("""
<style>
/* ---------- Global ---------- */
.stApp {
    background: #f0f2f5;
}

/* ---------- Top Banner ---------- */
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

/* ---------- Stat Cards ---------- */
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

/* ---------- Match Result Cards ---------- */
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

/* ---------- Inquiry Cards ---------- */
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

/* ---------- Email Template Box ---------- */
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

/* ---------- Button Enhancement ---------- */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e2e8f0;
}

/* ---------- Divider ---------- */
hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Data loading & caching
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
    st.error("Supplier product data not found! Please run `python data/generate_mock_data.py` first.")
    st.code("python data/generate_mock_data.py", language="bash")
    st.stop()

matcher = get_matcher(SUPPLIERS_CSV)
suppliers_df = load_suppliers(SUPPLIERS_CSV)
inquiries_df = load_inquiries(INQUIRIES_CSV) if os.path.exists(INQUIRIES_CSV) else pd.DataFrame()

# ---------------------------------------------------------------------------
# Top Banner
# ---------------------------------------------------------------------------

st.markdown("""
<div class="main-banner">
    <h1>🏭 Cross-Border B2B Smart Inquiry & Specification Matcher</h1>
    <p>TF-IDF + Cosine Similarity matching engine · Auto-recommends best-matching supplier products · One-click quote email</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Statistics bar
# ---------------------------------------------------------------------------

stat_cols = st.columns(5)
with stat_cols[0]:
    st.markdown('<div class="stat-card"><div class="stat-value">{}</div><div class="stat-label">Supplier Products</div></div>'.format(len(suppliers_df)), unsafe_allow_html=True)
with stat_cols[1]:
    unique_suppliers = suppliers_df["supplier_name"].nunique() if "supplier_name" in suppliers_df.columns else 0
    st.markdown('<div class="stat-card"><div class="stat-value">{}</div><div class="stat-label">Supplier Companies</div></div>'.format(unique_suppliers), unsafe_allow_html=True)
with stat_cols[2]:
    st.markdown('<div class="stat-card"><div class="stat-value">{}</div><div class="stat-label">Buyer Inquiries</div></div>'.format(len(inquiries_df)), unsafe_allow_html=True)
with stat_cols[3]:
    countries = inquiries_df["country"].nunique() if "country" in inquiries_df.columns and len(inquiries_df) > 0 else 0
    st.markdown('<div class="stat-card"><div class="stat-value">{}</div><div class="stat-label">Buyer Countries</div></div>'.format(countries), unsafe_allow_html=True)
with stat_cols[4]:
    cities = suppliers_df["city"].nunique() if "city" in suppliers_df.columns else 0
    st.markdown('<div class="stat-card"><div class="stat-value">{}</div><div class="stat-label">Production Cities</div></div>'.format(cities), unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------------------------
# Sidebar - Supplier Product Library
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### 📦 Supplier Product Library")
    st.caption(f"{len(suppliers_df)} products · {unique_suppliers} suppliers")

    # City filter
    if "city" in suppliers_df.columns:
        all_cities = ["All"] + sorted(suppliers_df["city"].unique().tolist())
        selected_city = st.selectbox("🏭 Filter by production city", all_cities)
        if selected_city != "All":
            filtered = suppliers_df[suppliers_df["city"] == selected_city]
        else:
            filtered = suppliers_df
    else:
        filtered = suppliers_df

    # Country filter
    if "country" in filtered.columns and filtered["country"].nunique() > 1:
        all_countries = ["All"] + sorted(filtered["country"].unique().tolist())
        selected_country = st.selectbox("🌍 Filter by supplier country", all_countries)
        if selected_country != "All":
            filtered = filtered[filtered["country"] == selected_country]

    st.caption(f"Current filter: {len(filtered)} products")

    # Product table
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
    st.markdown("### 📊 Tech Stack")
    st.markdown("""
    - **Algorithm**: TF-IDF Vectorizer + Cosine Similarity
    - **N-gram**: Unigram + Bigram
    - **Stop words**: English stopwords
    - **Frontend**: Streamlit + Custom CSS
    - **Data**: pandas
    """)

# ---------------------------------------------------------------------------
# Main panel - Tab navigation
# ---------------------------------------------------------------------------

tab_match, tab_inquiries = st.tabs(["🔍 Smart Match", "📋 Buyer Inquiry List"])

# ===========================================================================
# Tab 1: Smart Match
# ===========================================================================

with tab_match:
    col_input, col_examples = st.columns([3, 2])

    with col_examples:
        st.markdown("#### 📝 Sample Inquiries")
        st.caption("Select a real buyer inquiry to try it out")

        if len(inquiries_df) > 0:
            # Country filter - avoid overly long dropdown
            inq_countries = ["All"] + sorted(inquiries_df["country"].unique().tolist())
            sel_inq_country = st.selectbox("🌍 Filter by buyer country", inq_countries, key="inq_country")
            if sel_inq_country != "All":
                filtered_inq = inquiries_df[inquiries_df["country"] == sel_inq_country]
            else:
                filtered_inq = inquiries_df

            # Random sample up to 50 for selection
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
            example_labels = [f"Example #{i+1}" for i in range(len(example_options))]

        selected_idx = st.selectbox(
            "Select an inquiry sample:",
            options=range(len(example_options)),
            format_func=lambda i: example_labels[i] if i < len(example_labels) else "",
        )

        use_example = st.button("📋 Load into input box", use_container_width=True)

        # Display selected inquiry buyer info
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
        st.markdown("#### 🔍 Buyer Inquiry Input")

        default_text = example_options[selected_idx] if (use_example or selected_idx is not None) else ""

        buyer_inquiry = st.text_area(
            "Inquiry text (supports English):",
            value=default_text,
            height=100,
            placeholder="e.g.: Looking for plush squeaky dog toys, size around 20cm, durable material, MOQ 500 pcs.",
        )

        col_n, col_btn = st.columns([1, 2])
        with col_n:
            top_n = st.slider("Match count (Top-N)", min_value=1, max_value=10, value=3)
        with col_btn:
            st.write("")
            st.write("")
            match_btn = st.button("🚀 Smart Match", type="primary", use_container_width=True)

    # ---------- Match results ----------

    if match_btn:
        if not buyer_inquiry.strip():
            st.warning("Please enter inquiry text before matching.")
        else:
            with st.spinner("Smart matching supplier products..."):
                results = matcher.match(buyer_inquiry, top_n=top_n)

            st.markdown("---")
            st.markdown(f"#### ✅ Match Results (Top-{len(results)})")
            st.write(f"Scanned {len(matcher.df)} products. Here are the best-matching suppliers:")

            for i, row in results.iterrows():
                sim_score = row["similarity"]

                # Similarity level
                if sim_score >= 0.5:
                    badge_class = "sim-high"
                    badge_text = "High Match"
                elif sim_score >= 0.25:
                    badge_class = "sim-mid"
                    badge_text = "Medium Match"
                else:
                    badge_class = "sim-low"
                    badge_text = "Low Match"

                # Supplier info
                supplier_name = row.get("supplier_name", "N/A")
                contact_email = row.get("contact_email", "")
                country = row.get("country", "")
                city = row.get("city", "")
                lead_time = row.get("lead_time", "")
                certification = row.get("certification", "")

                # Render card
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
                            <div class="info-label">Unit Price</div>
                            <div class="info-value">${row['unit_price']:.2f}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">MOQ</div>
                            <div class="info-value">{row['moq']} pcs</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Dimensions</div>
                            <div class="info-value">{row['dimensions']}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Material</div>
                            <div class="info-value">{row['material']}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Lead Time</div>
                            <div class="info-value">{lead_time}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Certification</div>
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

                # ---------- One-click quote email ----------
                with st.expander(f"✉️ One-Click Quote Email — {row['product_name']}", expanded=(i == 0)):
                    email_tab_view, email_tab_send = st.tabs(["📋 Email Preview", "📤 Send Settings"])

                    with email_tab_send:
                        # Sender info
                        sender_cols = st.columns(2)
                        with sender_cols[0]:
                            sender_name = st.text_input("Your name", value="Export Manager", key=f"sender_name_{i}")
                        with sender_cols[1]:
                            sender_email = st.text_input("Your email", value="export@mycompany.com", key=f"sender_email_{i}")

                        # Recipient (supplier email)
                        recipient = st.text_input("Recipient (supplier email)", value=contact_email, key=f"recipient_{i}")

                        # Quote parameters
                        qty_cols = st.columns(3)
                        with qty_cols[0]:
                            order_qty = st.number_input("Order quantity", min_value=int(row["moq"]), value=int(row["moq"]), step=100, key=f"qty_{i}")
                        with qty_cols[1]:
                            quoted_price = st.number_input("Quoted unit price ($)", min_value=0.01, value=float(row["unit_price"]), step=0.05, key=f"price_{i}")
                        with qty_cols[2]:
                            currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "CNY"], key=f"curr_{i}")

                    with email_tab_view:
                        # Generate email template
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

                        # One-click send button - mailto link
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
                        ">📧 Send Quote Email</a>
                        """, unsafe_allow_html=True)

                        st.caption(f"Clicking this will open your default email client. Recipient: {recipient}")

            # ---------- Match results table ----------
            st.markdown("---")
            st.markdown("#### 📊 Match Results Detail Table")
            table_cols = [c for c in ["product_id", "product_name", "supplier_name", "material", "dimensions", "moq", "unit_price", "lead_time", "certification", "similarity_pct"] if c in results.columns]
            rename_map = {
                "product_id": "Product ID", "product_name": "Product Name", "supplier_name": "Supplier",
                "material": "Material", "dimensions": "Dimensions", "moq": "MOQ", "unit_price": "Unit Price",
                "lead_time": "Lead Time", "certification": "Certification", "similarity_pct": "Similarity",
            }
            st.dataframe(
                results[table_cols].rename(columns=rename_map),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Unit Price": st.column_config.NumberColumn(format="$%.2f"),
                },
            )

# ===========================================================================
# Tab 2: Buyer Inquiry List
# ===========================================================================

with tab_inquiries:
    st.markdown("#### 📋 Buyer Inquiry List")
    st.caption(f"{len(inquiries_df)} inquiries · from {inquiries_df['country'].nunique() if len(inquiries_df) > 0 else 0} countries")

    if len(inquiries_df) > 0:
        # Country filter
        country_list = ["All"] + sorted(inquiries_df["country"].unique().tolist())
        filter_country = st.selectbox("🌍 Filter by country", country_list, key="country_filter")
        filtered_inq = inquiries_df if filter_country == "All" else inquiries_df[inquiries_df["country"] == filter_country]

        # Pagination - 20 per page
        page_size = 20
        total_pages = max(1, (len(filtered_inq) + page_size - 1) // page_size)
        page = st.number_input("📄 Page", min_value=1, max_value=total_pages, value=1, key="inq_page")
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_data = filtered_inq.iloc[start_idx:end_idx]

        st.caption(f"Page {page}/{total_pages} · showing {len(page_data)} of {len(filtered_inq)} inquiries")

        # Inquiry card list
        for _, row in page_data.iterrows():
            # Quick match button
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
                if st.button(f"🔍 Match", key=f"quick_match_{row['inquiry_id']}", use_container_width=True):
                    # Quick match -> switch to Match tab
                    st.session_state["quick_inquiry"] = row["buyer_text"]
                    st.info(f"Inquiry loaded. Please switch to the \"Smart Match\" tab to view results.\n\n**Inquiry:** {row['buyer_text'][:80]}...")

                # One-click email to reply to buyer
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
                ">📧 Reply to Buyer</a>
                """, unsafe_allow_html=True)

        # Batch matching
        st.markdown("---")
        st.markdown("#### 📊 Batch Match Overview")
        batch_limit = st.slider("Batch match limit", min_value=10, max_value=min(200, len(filtered_inq)), value=min(50, len(filtered_inq)), key="batch_limit_slider")
        if st.button(f"🚀 Batch match filtered inquiries (up to {batch_limit})", type="primary"):
            batch_inq = filtered_inq.head(batch_limit)
            with st.spinner(f"Batch matching {len(batch_inq)} inquiries against {len(matcher.df)} products..."):
                batch_results = matcher.match_batch(batch_inq, top_n=1)

            batch_rows = []
            for _, inq_row in batch_inq.iterrows():
                inq_id = inq_row["inquiry_id"]
                res = batch_results.get(inq_id)
                if res is not None and len(res) > 0:
                    top = res.iloc[0]
                    batch_rows.append({
                        "Inquiry ID": inq_id,
                        "Buyer": inq_row["buyer_name"],
                        "Buyer Company": inq_row["company"],
                        "Country": inq_row["country"],
                        "Inquiry Summary": inq_row["buyer_text"][:55] + "...",
                        "Best Match Product": top["product_name"],
                        "Supplier": top.get("supplier_name", ""),
                        "Similarity": top["similarity_pct"],
                        "Unit Price": f"${top['unit_price']:.2f}",
                        "MOQ": f"{top['moq']} pcs",
                        "Supplier Email": top.get("contact_email", ""),
                    })

            batch_df = pd.DataFrame(batch_rows)
            st.dataframe(batch_df, use_container_width=True, hide_index=True)

            st.success(f"Batch matching complete! Processed {len(batch_rows)} inquiries.")

    else:
        st.info("No inquiry data available. Please run `python data/generate_mock_data.py` first to generate data.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.divider()
st.caption("© B2B Smart Inquiry Matcher | TF-IDF + Cosine Similarity | Streamlit + Custom CSS")
