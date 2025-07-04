@echo off
echo 🧠 Building NeuroScribe PDF Copilot Executable...
echo ================================================

echo 📦 Installing PyInstaller...
pip install pyinstaller

echo 🔨 Building executable...
pyinstaller --onefile --noconsole --add-data "app.py;." --add-data "src;src" --add-data "requirements.txt;." --add-data "env.template;." --add-data "README.md;." --name "NeuroScribeCopilot" launcher.py

echo ✅ Build complete!
echo 📁 Executable location: dist\NeuroScribeCopilot.exe
pause
