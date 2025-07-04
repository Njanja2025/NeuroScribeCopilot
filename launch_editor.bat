@echo off
chcp 65001 >nul
title NeuroScribe Copilot Quantum Launcher

echo.
echo ========================================
echo 🧠 NeuroScribe PDF Copilot Quantum
echo ========================================
echo.

echo 🔄 Starting the NeuroScribe PDF Copilot app...
cd /d "C:\Users\kavha\OneDrive\Documents\NeuroScribe PDF  Copilot Editor"

echo.
echo 📡 Launching Streamlit server...
start "" streamlit run app_quantum.py --server.port 8501

echo.
echo ⏳ Waiting for server to start...
timeout /t 5 /nobreak >nul

echo.
echo 🌐 Opening app in your browser...
start http://localhost:8501

echo.
echo ========================================
echo ✅ NeuroScribe Copilot Quantum is ready!
echo 📱 App URL: http://localhost:8501
echo ========================================
echo.
echo 💡 Tips:
echo    • Upload a PDF to get started
echo    • Try Edit Mode for AI-powered text editing
echo    • Try Erase Mode for text removal
echo    • Use OCR for scanned documents
echo.
echo 🚀 Happy editing!
echo.

exit 