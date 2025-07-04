@echo off
echo 🧠 NeuroScribe PDF Copilot - Installer
echo ======================================

echo 📦 Installing Python dependencies...
pip install -r requirements.txt

echo 🔧 Setting up environment...
if not exist .env (
    copy env.template .env
    echo ⚠️  Please edit .env file with your OpenAI API key
)

echo ✅ Installation complete!
echo 🚀 Run: python launcher.py
pause
