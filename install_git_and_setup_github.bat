@echo off
title NeuroScribe PDF Copilot - Git Installation & GitHub Setup
color 0B

echo.
echo    +===============================================================+
echo    |                NEUROSCRIBE PDF COPILOT                        |
echo    |                   GIT INSTALLATION & GITHUB SETUP             |
echo    |                                                                |
echo    |  This script will help you install Git and set up GitHub.     |
echo    |                                                                |
echo    +===============================================================+
echo.

echo Step 1: Downloading Git for Windows...
echo.

REM Download Git for Windows
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe' -OutFile 'Git-Installer.exe'"

if exist "Git-Installer.exe" (
    echo.
    echo ✅ Git installer downloaded successfully!
    echo.
    echo Step 2: Installing Git...
    echo Please follow the installation prompts in the popup window.
    echo.
    echo IMPORTANT: Use default settings during installation.
    echo.
    start /wait Git-Installer.exe
    
    echo.
    echo Step 3: Verifying Git installation...
    echo.
    
    REM Refresh environment variables
    call refreshenv 2>nul
    
    git --version
    if %errorlevel% equ 0 (
        echo.
        echo ✅ Git installed successfully!
        echo.
        echo Step 4: Setting up GitHub repository...
        echo.
        
        REM Initialize Git repository
        git init
        git add .
        git commit -m "Initial commit - NeuroScribe PDF Copilot v1.0"
        
        echo.
        echo ✅ Git repository initialized!
        echo.
        echo Step 5: GitHub Repository Setup Instructions
        echo ============================================
        echo.
        echo 1. Go to https://github.com/new
        echo 2. Create a new repository named: neuroscribe-pdf-copilot
        echo 3. Make it Public or Private (your choice)
        echo 4. DO NOT initialize with README, .gitignore, or license
        echo 5. Click "Create repository"
        echo 6. Copy the repository URL (it will look like: https://github.com/yourusername/neuroscribe-pdf-copilot.git)
        echo.
        echo After creating the repository, run the next script:
        echo   setup_github_push.bat
        echo.
        
    ) else (
        echo.
        echo ❌ Git installation failed or needs restart.
        echo Please restart your computer and try again.
        echo.
    )
    
    REM Clean up installer
    del Git-Installer.exe
    
) else (
    echo.
    echo ❌ Failed to download Git installer.
    echo.
    echo Manual Installation Instructions:
    echo ================================
    echo.
    echo 1. Go to: https://git-scm.com/download/win
    echo 2. Download Git for Windows
    echo 3. Run the installer with default settings
    echo 4. Restart your computer
    echo 5. Run this script again
    echo.
)

echo.
echo Press any key to continue...
pause >nul 