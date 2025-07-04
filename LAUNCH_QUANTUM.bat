@echo off
title NeuroScribe Copilot Quantum Edition
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🧠 NEUROSCRIBE COPILOT                    ║
echo ║                        QUANTUM EDITION                       ║
echo ║                                                              ║
echo ║  🎯 MODES:                                                   ║
echo ║  📝 Edit Mode: AI-powered text editing with GPT-4           ║
echo ║  🧽 Erase Mode: Remove text with background restoration     ║
echo ║  🔊 Avatar Mode: Voice commands (coming soon)               ║
echo ║                                                              ║
echo ║  🚀 POWER FEATURES:                                          ║
echo ║  ✅ AI-Inpaint background restoration                        ║
echo ║  ✅ Seamless erase with visual match                         ║
echo ║  ✅ Precision bounding box targeting                         ║
echo ║  ✅ Export to PNG, PDF, or DOCX formats                      ║
echo ║  ✅ Undo / Redo history trail                                ║
echo ║  ✅ Multi-page processing                                     ║
echo ║  ✅ OCR support for scanned documents                        ║
echo ║  ✅ PDF unlocking and decryption                             ║
echo ║                                                              ║
echo ║  🧬 TECH UNDER THE HOOD:                                     ║
echo ║  • cv2.inpaint() and rembg for intelligent content filling  ║
echo ║  • OpenCV contour tracing for exact word block erase        ║
echo ║  • PIL with alpha masking to preserve transparency          ║
echo ║  • GPT-4 integration for smart erase suggestions            ║
echo ║                                                              ║
echo ║  🎮 ERASE COMMAND SYNTAX:                                    ║
echo ║  • "Remove invoice number" → highlights and erases          ║
echo ║  • "Remove date 2023" → finds and removes date              ║
echo ║  • "Remove text 'LTD 2023'" → precise text removal          ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 Starting NeuroScribe Copilot Quantum Edition...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    echo 💡 Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if app_quantum.py exists
if not exist "app_quantum.py" (
    echo ❌ app_quantum.py not found! Please ensure you're in the correct directory.
    pause
    exit /b 1
)

REM Check if requirements are installed
echo 🔍 Checking dependencies...
python -c "import streamlit, openai, fitz, cv2, rembg" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Some dependencies are missing. Installing...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo ✅ Dependencies ready!

REM Find available port
set PORT=8506
:check_port
netstat -ano | findstr :%PORT% >nul 2>&1
if not errorlevel 1 (
    set /a PORT+=1
    if %PORT% gtr 8510 (
        echo ❌ No available ports found (8506-8510)
        pause
        exit /b 1
    )
    goto check_port
)

echo 🌐 Starting on port %PORT%...
echo.

REM Start Streamlit
start "NeuroScribe Quantum" python launcher_quantum.py

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Open browser
start http://localhost:%PORT%

echo.
echo 🎉 NeuroScribe Copilot Quantum Edition is starting!
echo 🌐 Local URL: http://localhost:%PORT%
echo 🌐 Network URL: http://192.168.0.30:%PORT%
echo.
echo 🎮 QUANTUM EDITION FEATURES:
echo 📝 Edit Mode: Upload PDF → Enter command → Get AI-edited version
echo 🧽 Erase Mode: Upload PDF → Select 'Erase Mode' → Remove text
echo 🔄 History: Undo/Redo your erase operations
echo 📤 Export: Download as PNG, PDF, or DOCX
echo.
echo 💡 TIP: The app will open in your default browser automatically
echo 💡 TIP: Press Ctrl+C in the Python window to stop the server
echo.
echo Press any key to exit this launcher (app will continue running)...
pause >nul 