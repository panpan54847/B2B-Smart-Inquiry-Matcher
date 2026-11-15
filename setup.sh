#!/bin/bash
# B2B Smart Inquiry Matcher - Setup & Launch (macOS/Linux)
set -e

echo "============================================================"
echo "  B2B Smart Inquiry Matcher - Setup & Launch"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH."
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

echo "[1/4] Python found:"
python3 --version
echo ""

# Install dependencies
echo "[2/4] Installing dependencies..."
pip3 install -r requirements.txt
echo "Dependencies installed successfully."
echo ""

# Check if data files exist, generate if not
if [ ! -f "data/suppliers_products.csv" ]; then
    echo "[3/4] Data files not found. Generating mock data..."
    python3 data/generate_mock_data.py
else
    echo "[3/4] Data files found. Skipping data generation."
fi
echo ""

# Launch Streamlit app
echo "[4/4] Launching Streamlit web app..."
echo ""
echo "============================================================"
echo "  The app will open in your browser automatically."
echo "  URL: http://localhost:8501"
echo "  Press Ctrl+C in this window to stop the server."
echo "============================================================"
echo ""
streamlit run app.py
