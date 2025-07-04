@echo off
echo 🧠 NeuroScribe PDF Copilot - Quick Start
echo ======================================

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🔧 Setting up environment...
if not exist .env (
    copy env.template .env
    echo ⚠️  Please edit .env file with your OpenAI API key
)

echo 🚀 Starting NeuroScribe...
python launcher.py

pause
