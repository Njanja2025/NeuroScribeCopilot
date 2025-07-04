#!/usr/bin/env python3
"""
NeuroScribe PDF Copilot - Complete Packaging & Installer Setup
Creates .exe, .msi, ZIP, and deployment packages for Windows distribution.
"""

import os
import shutil
import zipfile
import subprocess
import sys
from datetime import datetime

def create_directory_structure():
    """Create the proper directory structure for packaging."""
    print("📁 Creating directory structure...")
    
    # Create main packaging directory
    package_dir = "NeuroScribeCopilot-Package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Create subdirectories
    subdirs = [
        "exe-build",
        "zip-package", 
        "installer",
        "docs",
        "templates"
    ]
    
    for subdir in subdirs:
        os.makedirs(os.path.join(package_dir, subdir))
    
    return package_dir

def copy_essential_files(package_dir):
    """Copy all essential files to the package directory."""
    print("📦 Copying essential files...")
    
    # Files to copy
    files_to_copy = [
        "app.py",
        "launcher.py", 
        "launch.bat",
        "requirements.txt",
        "env.template",
        "README.md",
        "verify_setup.py"
    ]
    
    # Directories to copy
    dirs_to_copy = ["src"]
    
    # Copy files
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(package_dir, "zip-package"))
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} (not found)")
    
    # Copy directories
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(package_dir, "zip-package", dir_name))
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ⚠️  {dir_name}/ (not found)")

def create_installer_scripts(package_dir):
    """Create installer and setup scripts."""
    print("🔧 Creating installer scripts...")
    
    # Create Windows installer batch script
    installer_bat = os.path.join(package_dir, "installer", "install.bat")
    with open(installer_bat, "w", encoding="utf-8") as f:
        f.write("""@echo off
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
""")
    
    # Create desktop shortcut creator
    shortcut_bat = os.path.join(package_dir, "installer", "create-shortcut.bat")
    with open(shortcut_bat, "w", encoding="utf-8") as f:
        f.write("""@echo off
echo 🧠 Creating Desktop Shortcut...

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\\Desktop\\NeuroScribe Copilot.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%~dp0launcher.py" >> %SCRIPT%
echo oLink.WorkingDirectory = "%~dp0" >> %SCRIPT%
echo oLink.Description = "NeuroScribe PDF Copilot" >> %SCRIPT%
echo oLink.IconLocation = "%~dp0icon.ico,0" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

echo ✅ Desktop shortcut created!
pause
""")
    
    print("  ✅ install.bat")
    print("  ✅ create-shortcut.bat")

def create_pyinstaller_spec(package_dir):
    """Create PyInstaller spec file for .exe building."""
    print("🔨 Creating PyInstaller spec...")
    
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.py', '.'),
        ('src', 'src'),
        ('requirements.txt', '.'),
        ('env.template', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'streamlit',
        'openai',
        'fitz',
        'PIL',
        'pytesseract',
        'dotenv',
        'subprocess',
        'shutil',
        'webbrowser',
        'time',
        'os',
        'sys',
        'io',
        'zipfile',
        'urllib.request',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NeuroScribeCopilot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
"""
    
    spec_file = os.path.join(package_dir, "exe-build", "NeuroScribeCopilot.spec")
    with open(spec_file, "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("  ✅ NeuroScribeCopilot.spec")

def create_build_scripts(package_dir):
    """Create build scripts for different packaging options."""
    print("🚀 Creating build scripts...")
    
    # PyInstaller build script
    build_exe = os.path.join(package_dir, "exe-build", "build_exe.bat")
    with open(build_exe, "w", encoding="utf-8") as f:
        f.write("""@echo off
echo 🧠 Building NeuroScribe PDF Copilot Executable...
echo ================================================

echo 📦 Installing PyInstaller...
pip install pyinstaller

echo 🔨 Building executable...
pyinstaller --onefile --noconsole --add-data "app.py;." --add-data "src;src" --add-data "requirements.txt;." --add-data "env.template;." --add-data "README.md;." --name "NeuroScribeCopilot" launcher.py

echo ✅ Build complete!
echo 📁 Executable location: dist\\NeuroScribeCopilot.exe
pause
""")
    
    # ZIP package creator
    create_zip = os.path.join(package_dir, "zip-package", "create_zip.py")
    with open(create_zip, "w", encoding="utf-8") as f:
        f.write("""#!/usr/bin/env python3
import os
import zipfile
from datetime import datetime

def create_zip_package():
    version = "v1.0.0"
    timestamp = datetime.now().strftime("%Y%m%d")
    zip_name = f"NeuroScribeCopilot-{version}-{timestamp}.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            for file in files:
                if not file.endswith('.zip'):
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, '.')
                    zipf.write(file_path, arc_name)
    
    print(f"✅ Created: {zip_name}")

if __name__ == "__main__":
    create_zip_package()
""")
    
    print("  ✅ build_exe.bat")
    print("  ✅ create_zip.py")

def create_documentation(package_dir):
    """Create comprehensive documentation."""
    print("📚 Creating documentation...")
    
    # Main README for the package
    readme_content = """# 🧠 NeuroScribe PDF Copilot

**AI-powered PDF editing with GPT-4 and OCR support**

## 🚀 Quick Start

### Option 1: Executable (.exe)
1. Download `NeuroScribeCopilot.exe`
2. Double-click to run
3. No installation required!

### Option 2: ZIP Package
1. Extract `NeuroScribeCopilot-v1.0.zip`
2. Run `install.bat` (first time only)
3. Run `python launcher.py`

### Option 3: Manual Setup
1. Install Python 3.8+
2. Run: `pip install -r requirements.txt`
3. Set up `.env` file with OpenAI API key
4. Run: `python launcher.py`

## 🔧 Features

- **📄 PDF Processing**: Upload and edit any PDF
- **🧠 GPT-4 Integration**: AI-powered text rewriting
- **🔍 OCR Support**: Extract text from scanned PDFs
- **🔓 PDF Unlock**: Handle encrypted documents
- **🛡️ Bulletproof**: Robust error handling

## 📋 Requirements

- Windows 10/11
- Python 3.8+ (for ZIP/Manual versions)
- OpenAI API Key (for GPT features)
- Tesseract OCR (optional, for scanned PDFs)
- qpdf (optional, for encrypted PDFs)

## 🎯 Copilot Commands

- **Formal**: "Rewrite formally"
- **Friendly**: "Make it casual"
- **Summarize**: "Summarize this"
- **Translate**: "Translate to Spanish"
- **Custom**: Any natural language instruction

## 🔧 Troubleshooting

### App won't start
- Check if port 8502 is available
- Try running as administrator
- Verify Python installation

### OCR not working
- Install Tesseract OCR
- Add to system PATH
- Restart the application

### PDF unlock failed
- Install qpdf utility
- Add to system PATH
- Try PyMuPDF fallback

## 📞 Support

For issues and feature requests:
- Check the troubleshooting section
- Verify all dependencies are installed
- Test with a simple text PDF first

## 🔄 Updates

This is version 1.0.0
- Check for updates regularly
- Backup your `.env` file before updating
"""
    
    readme_file = os.path.join(package_dir, "docs", "README.md")
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Installation guide
    install_guide = os.path.join(package_dir, "docs", "INSTALLATION.md")
    with open(install_guide, "w", encoding="utf-8") as f:
        f.write("""# 📦 Installation Guide

## 🟢 Easy Installation (Recommended)

### For End Users
1. Download the latest release
2. Choose your preferred method:
   - **Executable**: Just double-click
   - **ZIP**: Extract and run install.bat
   - **Manual**: Follow developer setup

### For Developers
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Run: `python launcher.py`

## 🔧 Advanced Setup

### Installing Tesseract OCR
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to: `C:\\Program Files\\Tesseract-OCR\\`
3. Add to PATH: `C:\\Program Files\\Tesseract-OCR\\`

### Installing qpdf
1. Download from: https://github.com/qpdf/qpdf/releases
2. Extract to: `C:\\Program Files\\qpdf\\`
3. Add to PATH: `C:\\Program Files\\qpdf\\bin\\`

### Setting OpenAI API Key
1. Get API key from: https://platform.openai.com/
2. Create `.env` file in project root
3. Add: `OPENAI_API_KEY=your_key_here`

## 🧪 Testing Installation

Run the verification script:
```bash
python verify_setup.py
```

All checks should show ✅ for a complete setup.
""")
    
    print("  ✅ README.md")
    print("  ✅ INSTALLATION.md")

def create_deployment_zip(package_dir):
    """Create the final deployment ZIP file."""
    print("📦 Creating deployment ZIP...")
    
    version = "v1.0.0"
    timestamp = datetime.now().strftime("%Y%m%d")
    zip_name = f"NeuroScribeCopilot-{version}-{timestamp}.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, '.')
                zipf.write(file_path, arc_name)
    
    print(f"✅ Created: {zip_name}")
    return zip_name

def main():
    """Main packaging function."""
    print("🧠 NeuroScribe PDF Copilot - Complete Packaging Setup")
    print("=" * 60)
    
    # Create package structure
    package_dir = create_directory_structure()
    
    # Copy files
    copy_essential_files(package_dir)
    
    # Create scripts
    create_installer_scripts(package_dir)
    create_pyinstaller_spec(package_dir)
    create_build_scripts(package_dir)
    
    # Create documentation
    create_documentation(package_dir)
    
    # Create deployment ZIP
    zip_name = create_deployment_zip(package_dir)
    
    print("\n" + "=" * 60)
    print("🎉 Packaging Complete!")
    print(f"📦 Deployment package: {zip_name}")
    print("\n📁 Package contents:")
    print("  ├── exe-build/     (PyInstaller build files)")
    print("  ├── zip-package/   (Portable ZIP version)")
    print("  ├── installer/     (Installation scripts)")
    print("  └── docs/          (Documentation)")
    print("\n🚀 Next steps:")
    print("  1. Test the ZIP package")
    print("  2. Build .exe: cd exe-build && build_exe.bat")
    print("  3. Create GitHub release")
    print("  4. Distribute to users")

if __name__ == "__main__":
    main() 