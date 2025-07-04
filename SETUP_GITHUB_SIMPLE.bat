@echo off
title NeuroScribe PDF Copilot - Simple GitHub Setup
color 0A

echo.
echo    +===============================================================+
echo    |                NEUROSCRIBE PDF COPILOT                        |
echo    |                    SIMPLE GITHUB SETUP                        |
echo    |                                                                |
echo    |  This script will set up Git and connect to GitHub.           |
echo    |                                                                |
echo    +===============================================================+
echo.

echo Step 1: Checking Git installation...
git --version
if %errorlevel% neq 0 (
    echo.
    echo ❌ Git is not installed or not in PATH.
    echo.
    echo Please install Git manually:
    echo 1. Go to: https://git-scm.com/download/win
    echo 2. Download and install Git for Windows
    echo 3. Make sure "Add Git to PATH" is selected
    echo 4. Restart your terminal
    echo 5. Run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Git is installed!
echo.

echo Step 2: Initializing Git repository...
if not exist ".git" (
    git init
    echo ✅ Git repository initialized!
) else (
    echo ✅ Git repository already exists!
)

echo.
echo Step 3: Adding all files to Git...
git add .
git commit -m "Initial commit - NeuroScribe PDF Copilot v1.0"
echo ✅ Files committed to Git!

echo.
echo Step 4: Connecting to GitHub...
echo.
echo Your GitHub repository URL: https://github.com/Njanja2025/NeuroScribeCopilot.git
echo.
git remote add origin https://github.com/Njanja2025/NeuroScribeCopilot.git
if %errorlevel% neq 0 (
    echo ⚠️  Remote might already exist. Setting URL...
    git remote set-url origin https://github.com/Njanja2025/NeuroScribeCopilot.git
)

echo.
echo Step 5: Pulling from GitHub (allowing unrelated histories)...
git pull origin main --allow-unrelated-histories
echo ✅ Pulled from GitHub!

echo.
echo Step 6: Pushing to GitHub...
git branch -M main
git push -u origin main
echo ✅ Pushed to GitHub!

echo.
echo 🎉 GitHub setup complete!
echo.
echo Your repository is now available at:
echo https://github.com/Njanja2025/NeuroScribeCopilot
echo.
echo Next steps:
echo 1. Go to GitHub and create a release
echo 2. Upload the ZIP files as assets
echo 3. Deploy to Streamlit Cloud
echo.
pause 