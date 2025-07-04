@echo off
chcp 65001 >nul
title Restart NeuroScribe App

echo.
echo ========================================
echo 🔄 Restarting NeuroScribe Copilot
echo ========================================
echo.

echo 🛑 Stopping all Python processes...
taskkill /f /im python.exe >nul 2>&1
echo ✅ Killed old processes

echo.
echo ⏳ Waiting for cleanup...
timeout /t 3 /nobreak >nul

echo.
echo 🚀 Starting fresh instance...
cd /d "C:\Users\kavha\OneDrive\Documents\NeuroScribe PDF  Copilot Editor"
start "" streamlit run app_quantum.py --server.port 8501

echo.
echo ⏳ Waiting for server to start...
timeout /t 5 /nobreak >nul

echo.
echo 🌐 Opening in browser...
start http://localhost:8501

echo.
echo ✅ App restarted successfully!
echo 📱 URL: http://localhost:8501
echo.
echo Press any key to close...
pause >nul 