@echo off
title NeuroScribe PDF Copilot - GitHub Push Setup
color 0A

echo.
echo    +===============================================================+
echo    |                NEUROSCRIBE PDF COPILOT                        |
echo    |                      GITHUB PUSH SETUP                        |
echo    |                                                                |
echo    |  This script will push your project to GitHub.                |
echo    |                                                                |
echo    +===============================================================+
echo.

echo Step 1: Checking Git installation...
git --version
if %errorlevel% neq 0 (
    echo.
    echo ❌ Git is not installed or not in PATH.
    echo Please run install_git_and_setup_github.bat first.
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Git is installed!
echo.

echo Step 2: Checking if repository is initialized...
if not exist ".git" (
    echo.
    echo Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit - NeuroScribe PDF Copilot v1.0"
    echo ✅ Repository initialized!
) else (
    echo ✅ Repository already initialized!
)

echo.
echo Step 3: GitHub Repository URL Setup
echo ====================================
echo.
echo Please provide your GitHub repository URL.
echo It should look like: https://github.com/yourusername/neuroscribe-pdf-copilot.git
echo.
set /p repo_url="Enter your GitHub repository URL: "

if "%repo_url%"=="" (
    echo.
    echo ❌ No repository URL provided.
    echo Please create a repository on GitHub first and provide the URL.
    echo.
    pause
    exit /b 1
)

echo.
echo Step 4: Adding remote repository...
git remote add origin "%repo_url%"
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Remote might already exist. Trying to set URL...
    git remote set-url origin "%repo_url%"
)

echo.
echo Step 5: Pushing to GitHub...
echo.
echo This will push your code to the main branch.
echo.

git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ Successfully pushed to GitHub!
    echo.
    echo Step 6: Creating GitHub Release
    echo ===============================
    echo.
    echo Your code is now on GitHub at: %repo_url%
    echo.
    echo To create a release:
    echo 1. Go to your repository on GitHub
    echo 2. Click "Releases" on the right side
    echo 3. Click "Create a new release"
    echo 4. Tag version: v1.0
    echo 5. Title: NeuroScribe PDF Copilot v1.0
    echo 6. Description: Add the content from FINAL_STATUS_SUMMARY.md
    echo 7. Upload the ZIP files as assets:
    echo    - NeuroScribe-Portable-v1.0.zip
    echo    - NeuroScribeCopilot-Quantum-Installer-20250629_184356.zip
    echo 8. Click "Publish release"
    echo.
    
    echo Step 7: Streamlit Cloud Deployment
    echo ==================================
    echo.
    echo Now you can deploy to Streamlit Cloud:
    echo 1. Go to https://share.streamlit.io/
    echo 2. Sign in with GitHub
    echo 3. Click "New app"
    echo 4. Select your repository: neuroscribe-pdf-copilot
    echo 5. Set main file path: app.py
    echo 6. Click "Deploy!"
    echo.
    
    echo 🎉 GitHub setup complete! Your app is ready for deployment.
    echo.
    
) else (
    echo.
    echo ❌ Failed to push to GitHub.
    echo.
    echo Possible issues:
    echo - Repository URL is incorrect
    echo - You need to authenticate with GitHub
    echo - Repository doesn't exist
    echo.
    echo To authenticate with GitHub:
    echo 1. Run: git config --global user.name "Your Name"
    echo 2. Run: git config --global user.email "your.email@example.com"
    echo 3. Try pushing again
    echo.
)

echo.
echo Press any key to continue...
pause >nul 