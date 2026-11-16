# B2B-Smart-Inquiry-Matcher

> Cross-border B2B Smart Inquiry & Specification Matcher — TF-IDF + Cosine Similarity powered matching engine with one-click quote email

## Project Overview

This project is a smart inquiry matching system for cross-border B2B trade scenarios. Overseas buyers typically describe their needs in natural language text (inquiries), while supplier product information is stored in structured databases. This system uses **TF-IDF Vectorization** + **Cosine Similarity** algorithms to automatically match buyer inquiry text against the supplier product library, recommending the best-matching product specifications, with support for **one-click quote email sending**.

### Key Features

- Input/paste buyer inquiry text, smart-match the best-fitting supplier products
- **Large-scale data**: 3200+ supplier products (covering 15 manufacturing countries, 131 cities, 297 supplier companies), 500 buyer inquiries (covering 42 countries)
- Match result cards: product name, supplier company, contact email, unit price, MOQ, certification, lead time
- **One-click quote email**: auto-generates a professional English quote email template, click to open your email client and send
- Buyer inquiry list tab: shows buyer company, contact person, email, country, with one-click reply to buyer
- Batch inquiry matching: process all inquiries at once, output a match overview table
- Professional B2B SaaS style UI (custom CSS, gradient banner, card-based layout)
- Sidebar supplier product library browsing + production city filter

### Tech Stack

| Module | Technology |
|--------|-----------|
| Algorithm | scikit-learn (TfidfVectorizer + cosine_similarity) |
| Frontend | Streamlit + Custom CSS |
| Data Processing | pandas |
| Email | mailto: protocol (no backend needed, uses system email client) |
| Language | Python 3.8+ |

## Project Structure

```
B2B-Smart-Inquiry-Matcher/
├── data/
│   ├── generate_mock_data.py      # Mock data generation script (supplier names, emails, certifications, etc.)
│   ├── suppliers_products.csv     # Supplier product library (3200+ records, 12 fields)
│   └── inquiries.csv              # Buyer inquiry samples (500 records, with buyer company, email, country)
├── src/
│   ├── __init__.py
│   └── matcher.py                 # Core matching algorithm (TF-IDF + Cosine Similarity)
├── app.py                         # Streamlit web app (professional UI + one-click email)
├── requirements.txt
├── .gitignore
└── README.md
```

## Quick Start

> **The fastest way**: On Windows, double-click **`setup.bat`** in the project folder. It checks Python, installs dependencies, generates data if missing, and opens the app in your browser.
> For the full step-by-step guide, see `START_HERE.md`.

> **Note**: All commands below should be run from the project root directory `B2B-Smart-Inquiry-Matcher/`.
> If you are currently in `C:\Windows\System32` or a system directory, please `cd` to the project directory first.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone https://github.com/panpan54847/B2B-Smart-Inquiry-Matcher.git
```

Then open the folder you just cloned. For example, if you cloned into your user folder, open PowerShell there:

```powershell
cd "C:\Users\48247\B2B-Smart-Inquiry-Matcher"
```

> Replace `C:\Users\48247\B2B-Smart-Inquiry-Matcher` with the **actual path** where you cloned the project. Do not literally type `C:\path\to\...`.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Generate Mock Data (Optional)

The repository already includes pre-generated CSV data files. If you want to regenerate them:

```bash
python data/generate_mock_data.py
```

This will generate in the `data/` directory:
- `suppliers_products.csv` — 3200+ supplier product records (with supplier company name, email, city, certification, lead time)
- `inquiries.csv` — 500 buyer inquiry samples (with buyer company, email, country)

### Step 4: Test the Matching Algorithm (CLI)

```bash
python src/matcher.py
```

### Step 5: Launch the Streamlit Web App

```bash
streamlit run app.py
```

Your browser will automatically open `http://localhost:8501`.

If the browser doesn't open automatically, you can manually visit:
- http://localhost:8501
- http://127.0.0.1:8501

---

## Algorithm Explanation

### TF-IDF + Cosine Similarity

1. **Text preprocessing**: Combine supplier product `product_name` + `material` + `supplier_name` into full text
2. **TF-IDF Vectorization**:
   - Use `TfidfVectorizer` to convert text into TF-IDF feature vectors
   - `ngram_range=(1,2)`: Use both unigram and bigram to capture phrases like "dog toy", "rubber ball"
   - `stop_words="english"`: Remove English stop words (a, the, for, etc.) to reduce noise
3. **Cosine Similarity**: Compute cosine similarity between inquiry vector and all product vectors, take Top-N best matches

### Matching Examples

| Buyer Inquiry | Best Match Product | Supplier | Similarity |
|--------------|-------------------|----------|-----------|
| "Looking for plush squeaky dog toys, 20cm, MOQ 500" | Plush Squeaky Dog Toy - Bone Shape | Yiwu Mayer Pet Products Co., Ltd. | ~52% |
| "Need natural rubber dog balls, bouncy, 6-8cm" | Natural Rubber Dog Ball - Bouncy | Ningbo Champion Rubber Tech Ltd. | ~63% |
| "Searching for cotton rope tug toys, 30-50cm" | Thick Rope Tug Toy for Large Dogs | Cangnan Greenleaf Textile Ltd. | ~48% |

## One-Click Quote Email Feature

Each product card in the match results has a "One-Click Quote Email" expander:

1. **Email Preview**: Auto-generates a professional English quote email with product specs, order quantity, pricing, and original buyer inquiry text
2. **Send Settings**: Edit sender name/email, recipient (auto-filled with supplier email), order quantity, quoted unit price, currency
3. **One-Click Send**: Click the "📧 Send Quote Email" button to automatically open your system's default email client (Outlook/Gmail/Mail etc.) with recipient, subject, and body all pre-filled

Technical implementation: Uses `mailto:` URI scheme + `urllib.parse.urlencode` to encode subject and body. No backend email service required — clicking opens the email client directly.

## Data Field Schema

### suppliers_products.csv

| Field | Type | Description |
|-------|------|-------------|
| product_id | string | Product ID (e.g. SP001) |
| product_name | string | Product name (English) |
| material | string | Material description |
| dimensions | string | Dimension specifications |
| moq | int | Minimum Order Quantity |
| unit_price | float | Unit price (USD) |
| supplier_name | string | Supplier company name |
| contact_email | string | Supplier contact email |
| country | string | Supplier country |
| city | string | Supplier city |
| lead_time | string | Delivery lead time |
| certification | string | Certifications (e.g. BSCI, CE, FDA) |

### inquiries.csv

| Field | Type | Description |
|-------|------|-------------|
| inquiry_id | string | Inquiry ID (e.g. INQ001) |
| buyer_text | string | Buyer inquiry text (English natural language) |
| buyer_name | string | Buyer contact name |
| buyer_email | string | Buyer contact email |
| company | string | Buyer company name |
| country | string | Buyer country |

## License

MIT
