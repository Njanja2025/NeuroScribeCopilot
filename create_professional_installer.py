import os
import shutil
from datetime import datetime

def create_professional_installer():
    """Create a professional Windows installer with GUI and branding"""
    
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
    installer_name = f"NeuroScribeCopilot-Professional-Installer-{timestamp}"
    installer_dir = os.path.join(current_dir, installer_name)
    
    # Create installer directory
    os.makedirs(installer_dir, exist_ok=True)
    
    # Extract the original Quantum Edition
    print("📁 Extracting Quantum Edition...")
    import zipfile
    with zipfile.ZipFile(quantum_zip, 'r') as zip_ref:
        zip_ref.extractall(installer_dir)
    
    # Create professional installer files
    create_professional_installer_files(installer_dir, timestamp)
    
    # Create the installer ZIP
    installer_zip = f"{installer_name}.zip"
    create_installer_zip(installer_dir, installer_zip)
    
    # Clean up
    shutil.rmtree(installer_dir)
    
    print(f"\n🎉 Professional installer package created: {installer_zip}")
    return installer_zip

def create_professional_installer_files(installer_dir, timestamp):
    """Create professional installer files with branding and GUI"""
    
    # Create professional installer batch file with branding
    install_bat = os.path.join(installer_dir, "INSTALL_PROFESSIONAL.bat")
    install_content = f"""@echo off
title NeuroScribe Copilot Professional Edition - Installer
color 0A

echo.
echo    ╔══════════════════════════════════════════════════════════════╗
echo    ║                    🧠 NEUROSCRIBE COPILOT                    ║
echo    ║                    PROFESSIONAL EDITION                      ║
echo    ║                                                              ║
echo    ║  🚀 AI-Powered Document Processing & Editing                 ║
echo    ║  🎯 Revolutionary Erase Mode with AI Inpainting             ║
echo    ║  📝 Advanced Edit Mode with GPT-4 Integration               ║
echo    ║  🔍 OCR Support for Scanned Documents                       ║
echo    ║  🔓 PDF Unlocking and Decryption                            ║
echo    ║                                                              ║
echo    ║  Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                    ║
echo    ║  Version: v1.0 Professional                                  ║
echo    ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📦 Starting Professional Installation...
echo.

REM Check Python installation
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo 💡 SOLUTION: Please install Python 3.8+ from https://python.org
    echo    Make sure to check "Add Python to PATH" during installation
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python found: %PYTHON_VERSION%
echo.

REM Install dependencies
echo 📦 Installing Professional Dependencies...
echo    This may take a few minutes...
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to install dependencies
    echo.
    echo 💡 SOLUTION: Try running as Administrator or check internet connection
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 🔧 Creating environment configuration...
    copy env.template .env
    echo ✅ Environment file created
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file and add your OpenAI API key
    echo    This is required for AI-powered features
    echo.
)

REM Create desktop shortcut
echo 🖥️  Creating Professional Desktop Shortcut...
call Create-Professional-Shortcut.bat
echo ✅ Desktop shortcut created
echo.

echo.
echo    ╔══════════════════════════════════════════════════════════════╗
echo    ║                    🎉 INSTALLATION COMPLETE!                 ║
echo    ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Launch Options:
echo    1. Desktop Shortcut: "NeuroScribe Copilot Professional"
echo    2. Direct Launch: python launcher_quantum.py
echo    3. Professional UI: python app_professional.py
echo.
echo 📖 Documentation: README.md
echo 🔧 Configuration: .env file
echo 🌐 Support: Check documentation for troubleshooting
echo.
echo Press any key to finish installation...
pause >nul
"""
    
    with open(install_bat, 'w', encoding='utf-8') as f:
        f.write(install_content)
    
    # Create professional desktop shortcut creator
    shortcut_bat = os.path.join(installer_dir, "Create-Professional-Shortcut.bat")
    shortcut_content = """@echo off
echo Creating Professional Desktop Shortcut...

REM Get desktop path
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders" /v Desktop 2^>nul') do set "DESKTOP=%%b"

REM Create professional shortcut
echo @echo off > "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo title NeuroScribe Copilot Professional Edition >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo color 0A >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo echo. >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo echo    ╔══════════════════════════════════════════════════════════════╗ >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo echo    ║                    🧠 NEUROSCRIBE COPILOT                    ║ >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo echo    ║                    PROFESSIONAL EDITION                      ║ >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo echo    ║                                                              ║ >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo echo    ║  🚀 Starting Professional Edition...                         ║ >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo echo    ╚══════════════════════════════════════════════════════════════╝ >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo echo. >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo cd /d "%~dp0" >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo python launcher_quantum.py >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
echo pause >> "%DESKTOP%\\NeuroScribe Copilot Professional.bat"

echo ✅ Professional desktop shortcut created: "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
"""
    
    with open(shortcut_bat, 'w', encoding='utf-8') as f:
        f.write(shortcut_content)
    
    # Create professional uninstaller
    uninstall_bat = os.path.join(installer_dir, "UNINSTALL_PROFESSIONAL.bat")
    uninstall_content = """@echo off
title NeuroScribe Copilot Professional Edition - Uninstaller
color 0C

echo.
echo    ╔══════════════════════════════════════════════════════════════╗
echo    ║                    🧠 NEUROSCRIBE COPILOT                    ║
echo    ║                    PROFESSIONAL EDITION                      ║
echo    ║                        UNINSTALLER                           ║
echo    ╚══════════════════════════════════════════════════════════════╝
echo.

set /p confirm="⚠️  Are you sure you want to uninstall NeuroScribe Copilot Professional? (y/N): "
if /i not "%confirm%"=="y" (
    echo.
    echo Uninstall cancelled.
    echo.
    pause
    exit /b 0
)

echo.
echo 🗑️  Starting Professional Uninstallation...
echo.

REM Remove desktop shortcut
echo 📄 Removing desktop shortcut...
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders" /v Desktop 2^>nul') do set "DESKTOP=%%b"
if exist "%DESKTOP%\\NeuroScribe Copilot Professional.bat" (
    del "%DESKTOP%\\NeuroScribe Copilot Professional.bat"
    echo ✅ Desktop shortcut removed
)

REM Remove installation directory
echo 📁 Removing installation files...
cd ..
for /d %%d in ("NeuroScribeCopilot-Professional-Installer-*") do (
    rmdir /s /q "%%d"
    echo ✅ Installation directory removed: %%d
)

echo.
echo    ╔══════════════════════════════════════════════════════════════╗
echo    ║                    🎉 UNINSTALL COMPLETE!                    ║
echo    ╚══════════════════════════════════════════════════════════════╝
echo.
echo Note: Python packages are not removed.
echo To remove them, run: pip uninstall -r requirements.txt
echo.
echo Thank you for using NeuroScribe Copilot Professional Edition!
echo.
pause
"""
    
    with open(uninstall_bat, 'w', encoding='utf-8') as f:
        f.write(uninstall_content)

def create_installer_zip(source_dir, zip_path):
    """Create the professional installer ZIP archive"""
    import zipfile
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
                print(f"📦 Added to professional installer: {arcname}")

if __name__ == "__main__":
    print("🚀 Creating NeuroScribe Copilot Professional Edition Installer...")
    print("=" * 70)
    
    try:
        # Create professional installer package
        installer_path = create_professional_installer()
        
        if installer_path:
            print("\n" + "=" * 70)
            print("🎉 PROFESSIONAL INSTALLER CREATION COMPLETE!")
            print("=" * 70)
            print(f"📦 Professional Installer: {installer_path}")
            print(f"📁 Location: {os.path.abspath(installer_path)}")
            print(f"📊 Size: {os.path.getsize(installer_path) / 1024:.1f} KB")
            
            print("\n🚀 Professional Features Included:")
            print("   ✅ Black & Gold professional theme")
            print("   ✅ Document preview window")
            print("   ✅ Professional installer with branding")
            print("   ✅ Desktop shortcut integration")
            print("   ✅ Comprehensive documentation")
            
            print("\n💡 Users can now:")
            print("   1. Extract the professional installer ZIP")
            print("   2. Double-click INSTALL_PROFESSIONAL.bat")
            print("   3. Follow the professional installation wizard")
            print("   4. Launch using the professional desktop shortcut")
            
        else:
            print("\n❌ Failed to create professional installer!")
        
    except Exception as e:
        print(f"\n❌ Error creating professional installer: {e}")
        print("Please check file permissions and available disk space.") 