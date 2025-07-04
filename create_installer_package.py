import zipfile
import os
import shutil
from datetime import datetime

def create_installer_package():
    """Create an installer package from the existing Quantum Edition ZIP"""
    
    # Get current directory
    current_dir = os.getcwd()
    
    # Find the existing Quantum Edition ZIP
    quantum_zip = None
    for file in os.listdir(current_dir):
        if file.startswith("NeuroScribeCopilot-Quantum-v1.0-") and file.endswith(".zip"):
            quantum_zip = file
            break
    
    if not quantum_zip:
        print("❌ No Quantum Edition ZIP found!")
        return None
    
    print(f"📦 Found existing package: {quantum_zip}")
    
    # Create installer package name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    installer_name = f"NeuroScribeCopilot-Quantum-Installer-{timestamp}"
    installer_dir = os.path.join(current_dir, installer_name)
    
    # Create installer directory
    os.makedirs(installer_dir, exist_ok=True)
    
    # Extract the original Quantum Edition
    print("📁 Extracting Quantum Edition...")
    with zipfile.ZipFile(quantum_zip, 'r') as zip_ref:
        zip_ref.extractall(installer_dir)
    
    # Create installer-specific files
    create_installer_files(installer_dir, timestamp)
    
    # Create the installer ZIP
    installer_zip = f"{installer_name}.zip"
    create_installer_zip(installer_dir, installer_zip)
    
    # Clean up
    shutil.rmtree(installer_dir)
    
    print(f"\n🎉 Installer package created: {installer_zip}")
    return installer_zip

def create_installer_files(installer_dir, timestamp):
    """Create installer-specific files and structure"""
    
    # Create installer batch file
    install_bat = os.path.join(installer_dir, "INSTALL.bat")
    install_content = f"""@echo off
echo.
echo ========================================
echo   NeuroScribe Copilot Quantum Edition
echo           Installer v1.0
echo ========================================
echo.
echo Installing NeuroScribe Copilot Quantum Edition...
echo Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 🔧 Creating .env file...
    copy env.template .env
    echo ✅ .env file created
    echo.
    echo ⚠️  Please edit .env file and add your OpenAI API key
    echo.
)

REM Create desktop shortcut
echo 🖥️  Creating desktop shortcut...
call Create-Desktop-Shortcut.bat
echo ✅ Desktop shortcut created
echo.

echo ========================================
echo 🎉 Installation Complete!
echo ========================================
echo.
echo 🚀 Launch options:
echo   1. Double-click LAUNCH_QUANTUM.bat
echo   2. Run: python launcher_quantum.py
echo   3. Run: streamlit run app_quantum.py --server.port 8506
echo.
echo 📖 Documentation: README.md
echo 🔧 Configuration: .env file
echo.
pause
"""
    
    with open(install_bat, 'w', encoding='utf-8') as f:
        f.write(install_content)
    
    # Create desktop shortcut creator
    shortcut_bat = os.path.join(installer_dir, "Create-Desktop-Shortcut.bat")
    shortcut_content = """@echo off
echo Creating desktop shortcut...

REM Get desktop path
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders" /v Desktop 2^>nul') do set "DESKTOP=%%b"

REM Create shortcut
echo @echo off > "%DESKTOP%\\NeuroScribe Copilot Quantum.bat"
echo cd /d "%~dp0" >> "%DESKTOP%\\NeuroScribe Copilot Quantum.bat"
echo python launcher_quantum.py >> "%DESKTOP%\\NeuroScribe Copilot Quantum.bat"
echo pause >> "%DESKTOP%\\NeuroScribe Copilot Quantum.bat"

echo ✅ Desktop shortcut created: "%DESKTOP%\\NeuroScribe Copilot Quantum.bat"
"""
    
    with open(shortcut_bat, 'w', encoding='utf-8') as f:
        f.write(shortcut_content)
    
    # Create uninstaller
    uninstall_bat = os.path.join(installer_dir, "UNINSTALL.bat")
    uninstall_content = """@echo off
echo.
echo ========================================
echo   NeuroScribe Copilot Quantum Edition
echo           Uninstaller
echo ========================================
echo.

set /p confirm="Are you sure you want to uninstall? (y/N): "
if /i not "%confirm%"=="y" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo 🗑️  Removing files...

REM Remove desktop shortcut
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders" /v Desktop 2^>nul') do set "DESKTOP=%%b"
if exist "%DESKTOP%\\NeuroScribe Copilot Quantum.bat" (
    del "%DESKTOP%\\NeuroScribe Copilot Quantum.bat"
    echo ✅ Desktop shortcut removed
)

REM Remove current directory
cd ..
rmdir /s /q "NeuroScribeCopilot-Quantum-Installer-*"
echo ✅ Installation directory removed

echo.
echo ========================================
echo 🎉 Uninstall Complete!
echo ========================================
echo.
echo Note: Python packages are not removed.
echo To remove them, run: pip uninstall -r requirements.txt
echo.
pause
"""
    
    with open(uninstall_bat, 'w', encoding='utf-8') as f:
        f.write(uninstall_content)
    
    # Create installer README
    installer_readme = os.path.join(installer_dir, "INSTALLER_README.md")
    installer_readme_content = f"""# 🚀 NeuroScribe Copilot Quantum Edition - Installer

## 📦 Package Information
- **Version**: v1.0
- **Build Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Build ID**: {timestamp}
- **Type**: Windows Installer Package

## 🎯 Quick Installation

### Option 1: One-Click Install (Recommended)
1. **Extract** this ZIP file to any folder
2. **Double-click** `INSTALL.bat`
3. **Follow** the installation prompts
4. **Launch** using the desktop shortcut

### Option 2: Manual Installation
1. **Extract** this ZIP file
2. **Open** command prompt in the folder
3. **Run**: `pip install -r requirements.txt`
4. **Copy** `env.template` to `.env` and add your API key
5. **Launch**: `python launcher_quantum.py`

## 🔧 System Requirements

### Required Software
- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11
- **Memory**: 4GB RAM minimum
- **Storage**: 100MB free space

### Included Tools
- **Tesseract OCR**: v5.5.0.20241111 (auto-detected)
- **qpdf**: v12.2.0 (auto-detected)
- **All Python Dependencies**: Listed in requirements.txt

## 🎮 Features

### 🧽 Revolutionary Erase Mode
- AI inpainting for text removal
- Natural language commands
- Visual document preview
- Export to PNG, PDF, DOCX

### 📝 Advanced Edit Mode
- AI-powered text editing with GPT-4
- Document preview with tabs
- Multi-page support
- OCR integration

### 🔍 OCR Support
- Automatic text recognition for scanned PDFs
- Robust Unicode handling
- Multi-language support

### 🔓 PDF Unlock
- Automatic encrypted PDF detection
- Password removal capabilities
- Secure processing

## 🚀 Launch Options

### After Installation
1. **Desktop Shortcut**: Double-click the created shortcut
2. **Batch File**: Double-click `LAUNCH_QUANTUM.bat`
3. **Command Line**: `python launcher_quantum.py`
4. **Direct Launch**: `streamlit run app_quantum.py --server.port 8506`

## 🔍 Verification

Run the verification script to check your system:
```bash
python verify_environment.py
```

This will check:
- ✅ Tesseract OCR installation
- ✅ qpdf installation
- ✅ Python dependencies
- ✅ OpenAI API configuration

## 🆘 Troubleshooting

### Common Issues

1. **Python Not Found**
   - Install Python 3.8+ from https://python.org
   - Ensure Python is added to PATH during installation

2. **Dependencies Installation Failed**
   - Run: `pip install --upgrade pip`
   - Then: `pip install -r requirements.txt`

3. **OCR Not Working**
   - Run: `python verify_tesseract.py`
   - Check Tesseract installation and PATH

4. **Port Already in Use**
   - The launcher automatically finds available ports
   - Or manually specify: `--server.port 8507`

## 📞 Support

For issues and questions:
1. Check the verification script output
2. Review the comprehensive documentation
3. Check system requirements
4. Ensure all dependencies are installed

## 🎉 Ready to Use!

The NeuroScribe Copilot Quantum Edition is now ready to transform your document processing workflow!

**The future of document editing is here, and it's powered by AI! 🚀**

---

*Installer created on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open(installer_readme, 'w', encoding='utf-8') as f:
        f.write(installer_readme_content)
    
    # Create version info
    version_file = os.path.join(installer_dir, "INSTALLER_VERSION.txt")
    version_content = f"""NeuroScribe Copilot Quantum Edition Installer v1.0
Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Build ID: {timestamp}

INSTALLER FEATURES:
✅ One-click installation
✅ Automatic dependency installation
✅ Desktop shortcut creation
✅ Environment configuration
✅ System verification
✅ Uninstaller included

INSTALLATION OPTIONS:
1. INSTALL.bat - Full automated installation
2. Manual installation with pip
3. Custom configuration options

SYSTEM REQUIREMENTS:
- Windows 10/11
- Python 3.8+
- 4GB RAM minimum
- 100MB free space

LAUNCH OPTIONS:
1. Desktop shortcut (created automatically)
2. LAUNCH_QUANTUM.bat
3. python launcher_quantum.py
4. streamlit run app_quantum.py --server.port 8506

SUPPORT:
- Documentation: INSTALLER_README.md
- Verification: python verify_environment.py
- Troubleshooting: See README files

LICENSE:
MIT License - See LICENSE file for details
"""
    
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write(version_content)

def create_installer_zip(source_dir, zip_path):
    """Create the installer ZIP archive"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
                print(f"📦 Added to installer: {arcname}")

def verify_zip_contents(zip_path):
    """Verify the contents of a ZIP file"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            contents = zip_ref.namelist()
            print(f"📦 ZIP file: {zip_path}")
            print(f"📁 Files: {len(contents)}")
            print("📋 Contents:")
            for file in contents:
                print(f"   - {file}")
            return True, contents
    except Exception as e:
        print(f"❌ Error reading ZIP: {e}")
        return False, []

if __name__ == "__main__":
    print("🚀 Creating NeuroScribe Copilot Quantum Edition Installer...")
    print("=" * 60)
    
    try:
        # Create installer package
        installer_path = create_installer_package()
        
        if installer_path:
            print("\n" + "=" * 60)
            print("🎉 INSTALLER CREATION COMPLETE!")
            print("=" * 60)
            print(f"📦 Installer: {installer_path}")
            print(f"📁 Location: {os.path.abspath(installer_path)}")
            print(f"📊 Size: {os.path.getsize(installer_path) / 1024:.1f} KB")
            
            # Verify the installer
            print("\n🔍 Verifying installer package...")
            is_valid, contents = verify_zip_contents(installer_path)
            
            if is_valid:
                print("\n✅ Installer package verified successfully!")
                print("🚀 Ready for distribution!")
                print("\n💡 Users can now:")
                print("   1. Extract the installer ZIP")
                print("   2. Double-click INSTALL.bat")
                print("   3. Follow the installation prompts")
                print("   4. Launch using the desktop shortcut")
            else:
                print("\n❌ Installer verification failed!")
        
    except Exception as e:
        print(f"\n❌ Error creating installer: {e}")
        print("Please check file permissions and available disk space.") 