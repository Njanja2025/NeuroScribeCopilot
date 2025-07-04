@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🧪 NeuroScribe PDF Copilot - Quick Test
echo ========================================
echo.

echo ✅ Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.10+
    pause
    exit /b 1
)

echo.
echo ✅ Checking Streamlit installation...
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
if %errorlevel% neq 0 (
    echo ❌ Streamlit not found! Installing...
    pip install streamlit==1.28.1
)

echo.
echo ✅ Checking app modules...
python -c "from src.pdf_utils import extract_text_blocks; from src.openai_utils import rewrite_with_gpt; from src.erase_utils import erase_mode; print('All modules imported successfully')"
if %errorlevel% neq 0 (
    echo ❌ Module import failed! Check src/ directory
    pause
    exit /b 1
)

echo.
echo ✅ Checking available ports...
netstat -ano | findstr :8509
if %errorlevel% equ 0 (
    echo ⚠️ Port 8509 is in use, trying alternative ports...
    echo 🔄 Starting app on port 8510...
    start "" http://localhost:8510
    streamlit run app.py --server.port 8510
) else (
    echo 🚀 Starting app on port 8509...
    start "" http://localhost:8509
    streamlit run app.py --server.port 8509
)

echo.
echo ========================================
echo 🎉 App launched successfully!
echo 📱 Open your browser to test the app
echo 📦 All packages are ready in release-package/
echo ========================================
pause 