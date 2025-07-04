@echo off
title NeuroScribe PDF Copilot - Final Build All Packages
color 0B

echo.
echo    +===============================================================+
echo    |                NEUROSCRIBE PDF COPILOT                        |
echo    |                   FINAL BUILD ALL PACKAGES                    |
echo    |                                                                |
echo    |  This script will create all distribution packages:           |
echo    |  * Portable ZIP Package                                       |
echo    |  * Windows EXE Installer                                      |
echo    |  * Professional MSI Package                                   |
echo    |  * Source Code Archive                                        |
echo    |                                                                |
echo    +===============================================================+
echo.

echo Step 1: Checking Git installation...
git --version
if %errorlevel% neq 0 (
    echo.
    echo ❌ Git is not installed. Please install Git first:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Git is installed!
echo.

echo Step 2: Creating Portable ZIP Package...
echo.
python create_final_zip.py
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  ZIP creation failed, trying alternative method...
    powershell -Command "Compress-Archive -Path 'app.py', 'requirements.txt', 'README.md', 'src' -DestinationPath 'NeuroScribe-Portable-v1.0-FINAL.zip' -Force"
)

echo.
echo Step 3: Creating Windows EXE Installer...
echo.
python create_installer_package.py
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  EXE creation failed, trying alternative method...
    python build_exe.py
)

echo.
echo Step 4: Creating Professional MSI Package...
echo.
python create_crowned_installer.py
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  MSI creation failed, creating alternative package...
    powershell -Command "Compress-Archive -Path 'app.py', 'requirements.txt', 'README.md', 'RELEASE_NOTES.md', 'src', 'LAUNCH_ALL_VERSIONS.bat', 'QUICK_PACKAGE.bat' -DestinationPath 'NeuroScribe-Professional-v1.0.zip' -Force"
)

echo.
echo Step 5: Creating Source Code Archive...
echo.
powershell -Command "Compress-Archive -Path '.' -DestinationPath 'NeuroScribe-Source-v1.0.zip' -Force"

echo.
echo Step 6: Creating GitHub Release Package...
echo.
if not exist "release-package" mkdir release-package
copy "NeuroScribe-Portable-v1.0-FINAL.zip" "release-package\"
copy "NeuroScribeCopilot-Quantum-Installer-*.zip" "release-package\"
copy "NeuroScribe-Professional-v1.0.zip" "release-package\"
copy "NeuroScribe-Source-v1.0.zip" "release-package\"
copy "README.md" "release-package\"
copy "RELEASE_NOTES.md" "release-package\"

echo.
echo Step 7: Setting up Git repository...
echo.
if not exist ".git" (
    git init
    git add .
    git commit -m "Final release v1.0 - NeuroScribe PDF Copilot"
    echo ✅ Git repository initialized!
) else (
    git add .
    git commit -m "Update for final release v1.0"
    echo ✅ Git repository updated!
)

echo.
echo Step 8: Connecting to GitHub...
echo.
git remote add origin https://github.com/Njanja2025/NeuroScribeCopilot.git
if %errorlevel% neq 0 (
    echo ⚠️  Remote might already exist. Setting URL...
    git remote set-url origin https://github.com/Njanja2025/NeuroScribeCopilot.git
)

echo.
echo Step 9: Pushing to GitHub...
echo.
git branch -M main
git push -u origin main

echo.
echo 🎉 FINAL BUILD COMPLETE!
echo.
echo 📦 Created Packages:
echo    - NeuroScribe-Portable-v1.0-FINAL.zip
echo    - NeuroScribeCopilot-Quantum-Installer-*.zip
echo    - NeuroScribe-Professional-v1.0.zip
echo    - NeuroScribe-Source-v1.0.zip
echo    - release-package/ (GitHub release folder)
echo.
echo 📋 Next Steps:
echo    1. Go to GitHub: https://github.com/Njanja2025/NeuroScribeCopilot
echo    2. Create a new release (v1.0)
echo    3. Upload all files from release-package/ folder
echo    4. Deploy to Streamlit Cloud
echo.
echo 🚀 Ready for distribution!
echo.
pause 