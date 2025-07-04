#!/usr/bin/env python3
"""
NeuroScribe PDF Copilot - Deployment Package Creator
Creates a complete deployment package with all necessary files.
"""

import os
import shutil
import zipfile
from datetime import datetime

def main():
    print("🚀 Creating NeuroScribe PDF Copilot Deployment Package...")
    
    # Create deployment directory
    deployment_dir = "NeuroScribeCopilot-Deployment"
    if os.path.exists(deployment_dir):
        shutil.rmtree(deployment_dir)
    os.makedirs(deployment_dir)
    
    # Files to include in deployment
    files_to_copy = [
        "app.py",
        "launcher.py", 
        "launch.bat",
        "requirements.txt",
        "env.template",
        "README.md"
    ]
    
    # Directories to include
    dirs_to_copy = ["src"]
    
    print("📦 Copying application files...")
    
    # Copy files
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, deployment_dir)
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} (not found)")
    
    # Copy directories
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(deployment_dir, dir_name))
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ⚠️  {dir_name}/ (not found)")
    
    # Create enhanced launcher (without emojis for Windows compatibility)
    launcher_content = """@echo off
title NeuroScribe PDF Copilot
color 0A

echo.
echo ========================================
echo    NeuroScribe PDF Copilot Launcher
echo ========================================
echo.

echo Starting NeuroScribe PDF Copilot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo OK: Python found
echo.

REM Check if required packages are installed
echo Checking dependencies...
python -c "import streamlit, fitz, openai, dotenv" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Some dependencies are missing. Installing...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo OK: Dependencies installed
    echo.
)

echo Opening browser...
start http://localhost:8502
echo.

echo Launching NeuroScribe PDF Copilot...
echo.
echo The app will open in your browser at: http://localhost:8502
echo Press Ctrl+C to stop the application
echo.

python launcher.py

echo.
echo NeuroScribe PDF Copilot has been stopped.
pause
"""
    
    with open(f"{deployment_dir}/Launch-NeuroScribe.bat", "w", encoding='utf-8') as f:
        f.write(launcher_content)
    
    # Create installation script
    install_script = """@echo off
title NeuroScribe PDF Copilot - Installation
color 0B

echo.
echo ========================================
echo  NeuroScribe PDF Copilot Installation
echo ========================================
echo.

echo Welcome to NeuroScribe PDF Copilot!
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    echo.
    echo Please install Python 3.8+ from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    echo After installing Python, run this script again.
    pause
    exit /b 1
)

echo OK: Python is installed
echo.

REM Install dependencies
echo Installing required packages...
echo This may take a few minutes...
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo OK: Installation completed successfully!
echo.
echo NeuroScribe PDF Copilot is ready to use!
echo.
echo To start the application:
echo    1. Double-click "Launch-NeuroScribe.bat"
echo    2. Or run: python launcher.py
echo.
echo The app will open in your browser automatically
echo.
pause
"""
    
    with open(f"{deployment_dir}/Install.bat", "w", encoding='utf-8') as f:
        f.write(install_script)
    
    # Create comprehensive README
    readme_content = """# NeuroScribe PDF Copilot

## AI-Powered PDF Editing with GPT-4

NeuroScribe PDF Copilot is a powerful desktop application that combines AI technology with PDF processing to provide intelligent text editing, OCR capabilities, and automated content enhancement.

## Features

- **AI-Powered Editing**: Leverage GPT-4 for intelligent text rewriting and enhancement
- **PDF Processing**: Handle encrypted, scanned, and complex PDF documents
- **OCR Support**: Extract text from scanned documents using Tesseract
- **Auto-Unlock**: Automatically detect and unlock encrypted PDFs
- **Web Interface**: Modern, responsive web-based user interface
- **Fast Processing**: Optimized for speed and reliability

## Requirements

- **Windows 10/11** (64-bit)
- **Python 3.8+** (included in package)
- **Internet connection** (for GPT-4 features)
- **Optional**: Tesseract OCR for enhanced scanning support

## Installation

### Quick Start (Recommended)
1. **Extract** the NeuroScribeCopilot-Deployment folder
2. **Double-click** `Install.bat` to install dependencies
3. **Double-click** `Launch-NeuroScribe.bat` to start the app
4. **Enjoy** AI-powered PDF editing!

### Manual Installation
1. Install Python 3.8+ from https://python.org
2. Open Command Prompt in the deployment folder
3. Run: `pip install -r requirements.txt`
4. Run: `python launcher.py`

## Usage

1. **Launch** the application using `Launch-NeuroScribe.bat`
2. **Upload** your PDF document
3. **Enter** your editing command (e.g., "Make this more professional")
4. **Review** the AI-enhanced text
5. **Download** the improved version

## Configuration

### OpenAI API Setup (Optional)
1. Get an API key from https://platform.openai.com
2. Copy `env.template` to `.env`
3. Add your API key: `OPENAI_API_KEY=your_key_here`

### Tesseract OCR Setup (Optional)
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to system PATH
3. Restart the application

## File Structure

```
NeuroScribeCopilot-Deployment/
├── app.py                 # Main Streamlit application
├── launcher.py           # Application launcher
├── Launch-NeuroScribe.bat # Windows launcher
├── Install.bat           # Installation script
├── requirements.txt      # Python dependencies
├── env.template          # Environment variables template
├── README.md            # This file
└── src/                 # Source code modules
    ├── __init__.py
    ├── openai_utils.py  # OpenAI integration
    └── pdf_utils.py     # PDF processing utilities
```

## Troubleshooting

### Common Issues

**App won't start:**
- Ensure Python is installed and in PATH
- Run `Install.bat` to install dependencies
- Check Windows Defender isn't blocking the app

**PDF processing errors:**
- Ensure PDF is not corrupted
- Try with a different PDF file
- Check file permissions

**OCR not working:**
- Install Tesseract OCR
- Add Tesseract to system PATH
- Restart the application

**GPT features not working:**
- Check internet connection
- Verify OpenAI API key in `.env` file
- Ensure API key has sufficient credits

### Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all requirements are met
3. Try running the app from command line for detailed error messages

## Security & Privacy

- **Local Processing**: PDFs are processed locally on your machine
- **API Calls**: Only text content is sent to OpenAI (no PDF data)
- **No Data Storage**: No files or data are stored permanently
- **Secure**: Uses industry-standard encryption for API communications

## License

This software is provided as-is for educational and personal use.

## Version History

**v1.0.0** - Initial Release
- AI-powered PDF text editing
- OCR support for scanned documents
- PDF encryption detection and unlocking
- Modern web interface
- Comprehensive error handling

---

**Enjoy your AI-powered PDF editing experience!**
"""
    
    with open(f"{deployment_dir}/README.md", "w", encoding='utf-8') as f:
        f.write(readme_content)
    
    # Create ZIP archive
    print("📦 Creating ZIP archive...")
    zip_filename = f"NeuroScribeCopilot-v1.0.0-{datetime.now().strftime('%Y%m%d')}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deployment_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, deployment_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ ZIP archive created: {zip_filename}")
    
    # Create desktop shortcut creator
    shortcut_creator = """@echo off
title Create Desktop Shortcut
color 0E

echo.
echo ========================================
echo   Create Desktop Shortcut
echo ========================================
echo.

set "current_dir=%~dp0"
set "shortcut_path=%USERPROFILE%\\Desktop\\NeuroScribe PDF Copilot.lnk"

echo Creating desktop shortcut...
echo.

REM Create VBS script to make shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\\CreateShortcut.vbs"
echo sLinkFile = "%shortcut_path%" >> "%temp%\\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\\CreateShortcut.vbs"
echo oLink.TargetPath = "%current_dir%Launch-NeuroScribe.bat" >> "%temp%\\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%current_dir%" >> "%temp%\\CreateShortcut.vbs"
echo oLink.Description = "NeuroScribe PDF Copilot - AI-Powered PDF Editor" >> "%temp%\\CreateShortcut.vbs"
echo oLink.IconLocation = "%SystemRoot%\\System32\\shell32.dll,21" >> "%temp%\\CreateShortcut.vbs"
echo oLink.Save >> "%temp%\\CreateShortcut.vbs"

cscript //nologo "%temp%\\CreateShortcut.vbs"
del "%temp%\\CreateShortcut.vbs"

if exist "%shortcut_path%" (
    echo OK: Desktop shortcut created successfully!
    echo.
    echo Shortcut location: %shortcut_path%
    echo.
    echo You can now launch NeuroScribe from your desktop!
) else (
    echo ERROR: Failed to create desktop shortcut
    echo.
    echo Please try running as administrator
)

echo.
pause
"""
    
    with open(f"{deployment_dir}/Create-Desktop-Shortcut.bat", "w", encoding='utf-8') as f:
        f.write(shortcut_creator)
    
    # Final summary
    print("\n🎉 Deployment package created successfully!")
    print(f"📁 Location: {deployment_dir}/")
    print(f"📦 ZIP Archive: {zip_filename}")
    print("\n📋 Package contents:")
    print("  ✅ Main application (app.py)")
    print("  ✅ Launcher scripts (Launch-NeuroScribe.bat)")
    print("  ✅ Installation script (Install.bat)")
    print("  ✅ Desktop shortcut creator")
    print("  ✅ Source code modules (src/)")
    print("  ✅ Dependencies list (requirements.txt)")
    print("  ✅ Configuration template (env.template)")
    print("  ✅ Comprehensive documentation (README.md)")
    print("\n🚀 Ready for distribution!")
    print("\n📋 Next steps:")
    print("  1. Test the package on a clean system")
    print("  2. Share the ZIP file with users")
    print("  3. Users can extract and run Install.bat")
    print("  4. Users can create desktop shortcuts")

if __name__ == "__main__":
    main() 