@echo off
title B2B Smart Inquiry Matcher - Setup & Launch
color 0B

echo ============================================================
echo   B2B Smart Inquiry Matcher - Setup & Launch
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [1/4] Python found:
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available. Please reinstall Python with pip.
    pause
    exit /b 1
)

REM Install dependencies
echo [2/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo Dependencies installed successfully.
echo.

REM Check if data files exist, generate if not
if not exist "data\suppliers_products.csv" (
    echo [3/4] Data files not found. Generating mock data...
    python data\generate_mock_data.py
    if errorlevel 1 (
        echo [ERROR] Failed to generate data.
        pause
        exit /b 1
    )
) else (
    echo [3/4] Data files found. Skipping data generation.
)
echo.

REM Launch Streamlit app
echo [4/4] Launching Streamlit web app...
echo.
echo ============================================================
echo   The app will open in your browser automatically.
echo   URL: http://localhost:8501
echo   Press Ctrl+C in this window to stop the server.
echo ============================================================
echo.
streamlit run app.py

pause
