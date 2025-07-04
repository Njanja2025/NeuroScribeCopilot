@echo off
echo ========================================
echo    NeuroScribe PDF Copilot Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created
echo.

REM Activate virtual environment and install dependencies
echo Installing dependencies...
call .venv\Scripts\activate
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

REM Create .env file from template
if not exist .env (
    echo Creating .env file from template...
    copy env.template .env
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file and add your OpenAI API key
    echo    OPENAI_API_KEY=your-actual-key-here
    echo.
)

echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo To start the app, run: launch.bat
echo.
echo Or manually:
echo 1. Activate virtual environment: .venv\Scripts\activate
echo 2. Start app: streamlit run app.py --server.port 8502
echo.
pause 