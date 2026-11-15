# START HERE — B2B Smart Inquiry Matcher

A cross-border B2B smart inquiry matching web app (TF-IDF + Cosine Similarity).
**Everything you need is in this folder.** No extra downloads except Python itself.

---

## Requirements

- Python 3.8 or newer → https://www.python.org/downloads/
- **Windows**: during installation, CHECK the box **"Add Python to PATH"** (important!)
- An internet connection for the one-time dependency install

No database, no API keys, no cloud account required. All data is local CSV files.

---

## Option A — One click (easiest)

| Your system | What to do |
|-------------|------------|
| Windows | **Double-click `setup.bat`** |
| macOS / Linux | Open Terminal in this folder, run `bash setup.sh` |

The script will:
1. Check Python is installed
2. Install the 3 dependencies (`streamlit`, `pandas`, `scikit-learn`)
3. Generate the data files if they are missing
4. Launch the app and open your browser at **http://localhost:8501**

To stop the app, close the black window or press `Ctrl+C`.

---

## Option B — Manual commands

Open a terminal **in this folder** and run:

```bash
pip install -r requirements.txt
python data/generate_mock_data.py     # optional, CSV files are already included
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

---

## Option C — Clone from GitHub (for developers)

```bash
git clone https://github.com/panpan54847/B2B-Smart-Inquiry-Matcher.git
cd B2B-Smart-Inquiry-Matcher
pip install -r requirements.txt
streamlit run app.py
```

---

## What's inside

```
├── app.py                      # Streamlit web app (the "website")
├── setup.bat / setup.sh        # One-click install & launch
├── requirements.txt           # Python dependencies
├── README.md                  # Full documentation
├── data/
│   ├── suppliers_products.csv # 3200+ products, 15 countries, 297 suppliers
│   ├── inquiries.csv          # 500 buyer inquiries, 42 countries
│   └── generate_mock_data.py  # Regenerate the data
└── src/
    └── matcher.py             # TF-IDF + Cosine Similarity engine
```

## Sharing with someone else

Just **copy or zip this entire folder** and send it. On the other computer:
install Python 3.8+, double-click `setup.bat`, and it works — no path configuration needed.
All file paths in the code are relative to the app location, so the folder can be
placed anywhere (Desktop, D drive, USB stick, etc.).

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `'python' is not recognized` | Reinstall Python and check "Add Python to PATH" |
| `'streamlit' is not recognized` | Run `pip install -r requirements.txt` again |
| Browser doesn't open | Manually visit http://localhost:8501 |
| Port 8501 already in use | Run `streamlit run app.py --server.port 8502` |
| Email button does nothing | It opens your default mail client; configure one (Outlook / Mail app) |

---

MIT License · See `README.md` for algorithm details and data schema.
