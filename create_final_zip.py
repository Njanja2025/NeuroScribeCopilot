#!/usr/bin/env python3
"""
NeuroScribe PDF Copilot - Final ZIP Package Creator
Creates a complete portable package with all dependencies and documentation.
"""

import os
import zipfile
import shutil
import datetime
from pathlib import Path

def create_portable_zip():
    """Create a complete portable ZIP package for NeuroScribe PDF Copilot."""
    
    print("🧠 NeuroScribe PDF Copilot - Creating Portable ZIP Package")
    print("=" * 60)
    
    # Create timestamp for versioning
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"NeuroScribe-Portable-v1.0-{timestamp}.zip"
    
    # Files to include in the package
    core_files = [
        "app.py",
        "app_quantum.py", 
        "app_professional.py",
        "requirements.txt",
        "README.md",
        "LAUNCH_ALL_VERSIONS.bat",
        "QUICK_PACKAGE.bat",
        "launch.bat",
        "launch.sh",
        "FINAL_TESTING_GUIDE.md",
        "FINAL_STATUS_SUMMARY.md",
        "verify_installations.py",
        "verify_environment.py",
        "verify_tesseract.py",
        "env.template",
        "Dockerfile",
        "docker-compose.yml"
    ]
    
    # Directories to include
    directories = [
        "src",
        "NeuroScribe-Final-v1.0",
        "NeuroScribeCopilot-v1.0.0",
        "NeuroScribeCopilot-v1.1"
    ]
    
    # Create the ZIP file
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # Add core files
        print("📁 Adding core application files...")
        for file in core_files:
            if os.path.exists(file):
                zipf.write(file)
                print(f"   ✅ {file}")
            else:
                print(f"   ⚠️  {file} (not found)")
        
        # Add directories recursively
        print("\n📁 Adding directories...")
        for directory in directories:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path)
                        zipf.write(file_path, arc_name)
                        print(f"   ✅ {arc_name}")
            else:
                print(f"   ⚠️  {directory} (not found)")
        
        # Create launcher scripts
        print("\n📝 Creating launcher scripts...")
        
        # Windows launcher
        windows_launcher = """@echo off
title NeuroScribe PDF Copilot - Portable Launcher
color 0A

echo.
echo    +===============================================================+
echo    |                NEUROSCRIBE PDF COPILOT                        |
echo    |                    PORTABLE LAUNCHER                          |
echo    |                                                                |
echo    |  Starting NeuroScribe PDF Copilot...                          |
echo    |                                                                |
echo    |  Features:                                                     |
echo    |  * AI-powered PDF editing with GPT-4                          |
echo    |  * OCR text extraction                                        |
echo    |  * Image erasing with inpainting                              |
echo    |  * Real-time document preview                                 |
echo    |  * Professional UI/UX                                         |
echo    |                                                                |
echo    +===============================================================+
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting application...
echo Opening browser...
start http://localhost:8507

echo Launching NeuroScribe...
streamlit run app.py --server.port 8507

pause
"""
        
        # Linux/Mac launcher
        unix_launcher = """#!/bin/bash
echo "🧠 NeuroScribe PDF Copilot - Portable Launcher"
echo "================================================"
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting application..."
echo "Opening browser..."
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8507 &
elif command -v open &> /dev/null; then
    open http://localhost:8507 &
fi

echo "Launching NeuroScribe..."
streamlit run app.py --server.port 8507
"""
        
        # Add launchers to ZIP
        zipf.writestr("LAUNCH-PORTABLE.bat", windows_launcher)
        zipf.writestr("launch-portable.sh", unix_launcher)
        
        # Create README for the package
        package_readme = """# 🧠 NeuroScribe PDF Copilot - Portable Package

## 🚀 Quick Start

### Windows Users:
1. Extract this ZIP file to any folder
2. Double-click `LAUNCH-PORTABLE.bat`
3. The application will open in your browser at http://localhost:8507

### Linux/Mac Users:
1. Extract this ZIP file to any folder
2. Open terminal in the extracted folder
3. Run: `chmod +x launch-portable.sh && ./launch-portable.sh`
4. The application will open in your browser at http://localhost:8507

## 📋 What's Included

- ✅ Complete NeuroScribe PDF Copilot application
- ✅ All Python dependencies (auto-installed)
- ✅ Multiple application versions (Basic, Quantum, Professional)
- ✅ Comprehensive documentation
- ✅ Verification and testing tools
- ✅ Docker support for containerized deployment

## 🎯 Features

- **AI-Powered PDF Editing** with GPT-4
- **OCR Text Extraction** using Tesseract
- **Image Erasing** with inpainting technology
- **Real-time Document Preview**
- **Professional UI/UX** design
- **Multi-page Support** for documents
- **Avatar Integration** with AI responses

## 🔧 System Requirements

- Python 3.8 or higher
- Windows 10/11, Linux, or macOS
- Internet connection for AI features
- 4GB RAM minimum (8GB recommended)

## 📞 Support

For issues or questions:
1. Check the documentation in this package
2. Run verification scripts: `python verify_installations.py`
3. Review troubleshooting guides in the docs folder

## 🎉 Ready to Use!

NeuroScribe PDF Copilot is now ready for professional use.
Enjoy AI-powered PDF editing and document processing!

---
*NeuroScribe PDF Copilot v1.0 - Portable Package*
"""
        
        zipf.writestr("README-PORTABLE.md", package_readme)
        
        # Create installation guide
        install_guide = """# 📦 Installation Guide

## Windows Installation

1. **Extract the ZIP file** to your desired location
2. **Run the launcher**: Double-click `LAUNCH-PORTABLE.bat`
3. **Wait for setup**: Dependencies will be installed automatically
4. **Access the app**: Browser will open to http://localhost:8507

## Linux/Mac Installation

1. **Extract the ZIP file** to your desired location
2. **Open terminal** in the extracted folder
3. **Make launcher executable**: `chmod +x launch-portable.sh`
4. **Run launcher**: `./launch-portable.sh`
5. **Access the app**: Browser will open to http://localhost:8507

## Docker Installation

1. **Extract the ZIP file**
2. **Open terminal** in the extracted folder
3. **Build and run**: `docker-compose up --build`
4. **Access the app**: Browser will open to http://localhost:8501

## Verification

After installation, run:
```bash
python verify_installations.py
```

This will confirm all dependencies are properly installed.

## Troubleshooting

- **Port conflicts**: Change port in launcher scripts
- **Import errors**: Ensure Python 3.8+ is installed
- **OCR issues**: Verify Tesseract installation
- **API errors**: Check OpenAI API key in .env file
"""
        
        zipf.writestr("INSTALLATION-GUIDE.md", install_guide)
    
    print(f"\n🎉 Package created successfully!")
    print(f"📦 File: {zip_name}")
    print(f"📏 Size: {os.path.getsize(zip_name) / (1024*1024):.1f} MB")
    
    # Create a simple launcher for immediate use
    simple_launcher = f"""@echo off
title NeuroScribe PDF Copilot - Quick Launch
color 0A

echo.
echo    +===============================================================+
echo    |                NEUROSCRIBE PDF COPILOT                        |
echo    |                      QUICK LAUNCHER                           |
echo    |                                                                |
echo    |  Package: {zip_name}                                    |
echo    |  Version: v1.0                                                |
echo    |  Status: Ready for use                                        |
echo    |                                                                |
echo    +===============================================================+
echo.

echo Starting NeuroScribe PDF Copilot...
echo Opening browser...
start http://localhost:8507

echo Launching application...
streamlit run app.py --server.port 8507

pause
"""
    
    with open("LAUNCH-QUICK.bat", "w") as f:
        f.write(simple_launcher)
    
    print(f"\n✅ Quick launcher created: LAUNCH-QUICK.bat")
    print(f"\n🚀 Ready for distribution!")
    print(f"📋 Next steps:")
    print(f"   1. Test the package on a clean system")
    print(f"   2. Distribute {zip_name} to clients")
    print(f"   3. Upload to file sharing services")
    
    return zip_name

if __name__ == "__main__":
    create_portable_zip() 