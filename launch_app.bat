@echo off
echo 🚀 NeuroScribe PDF Copilot - Launching...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Verify dependencies
echo 🔍 Verifying dependencies...
python verify_installations.py
if errorlevel 1 (
    echo ❌ Some dependencies are missing. Please install them first.
    pause
    exit /b 1
)

echo.
echo ✅ All dependencies verified! Starting NeuroScribe...
echo 🌐 Opening browser...
start http://localhost:8505

REM Start Streamlit app
streamlit run app.py --server.port 8505

pause 