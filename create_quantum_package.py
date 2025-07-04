#!/usr/bin/env python3
"""
NeuroScribe Copilot Quantum Edition Package Creator
Creates a complete distribution package with Erase Mode functionality
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

def create_quantum_package():
    """Create a production-ready package of the NeuroScribe Copilot Quantum Edition"""
    
    # Get current directory
    current_dir = os.getcwd()
    
    # Create package name with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    package_name = f"NeuroScribeCopilot-Quantum-v1.0-{timestamp}"
    package_dir = os.path.join(current_dir, package_name)
    
    # Create package directory
    os.makedirs(package_dir, exist_ok=True)
    
    # Files to include in the package
    files_to_include = [
        # Main applications
        "app_quantum.py",
        "launcher_quantum.py",
        "LAUNCH_QUANTUM.bat",
        
        # Source code
        "src/__init__.py",
        "src/erase_utils.py",
        "src/pdf_utils.py",
        "src/openai_utils.py",
        
        # Configuration
        "requirements.txt",
        "env.template",
        
        # Documentation
        "QUANTUM_EDITION_GUIDE.md",
        "QUICK_START_QUANTUM.txt",
        "README.md",
        "VERSION.txt",
        
        # Verification and utilities
        "verify_environment.py",
        "verify_tesseract.py",
        
        # Summaries and guides
        "FINAL_COMPLETE_SUMMARY.md",
        "OCR_FIXES_SUMMARY.md",
        "FINAL_QUANTUM_SUMMARY.md"
    ]
    
    # Create src directory if it doesn't exist
    src_dir = os.path.join(package_dir, "src")
    os.makedirs(src_dir, exist_ok=True)
    
    # Copy files to package
    copied_files = []
    for file_path in files_to_include:
        source_path = os.path.join(current_dir, file_path)
        if os.path.exists(source_path):
            # Determine destination path
            if file_path.startswith("src/"):
                dest_path = os.path.join(package_dir, file_path)
            else:
                dest_path = os.path.join(package_dir, os.path.basename(file_path))
            
            # Create directory if needed
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Copy file
            shutil.copy2(source_path, dest_path)
            copied_files.append(file_path)
            print(f"✅ Copied: {file_path}")
        else:
            print(f"⚠️  Missing: {file_path}")
    
    # Create additional documentation files
    create_package_documentation(package_dir, timestamp)
    
    # Create the ZIP archive
    zip_path = f"{package_name}.zip"
    create_zip_archive(package_dir, zip_path)
    
    # Clean up temporary directory
    shutil.rmtree(package_dir)
    
    print(f"\n🎉 Package created successfully!")
    print(f"📦 Package: {zip_path}")
    print(f"📁 Files included: {len(copied_files)}")
    print(f"📊 Package size: {os.path.getsize(zip_path) / 1024:.1f} KB")
    
    return zip_path

def create_package_documentation(package_dir, timestamp):
    """Create additional documentation for the package"""
    
    # Create VERSION.txt
    version_content = f"""NeuroScribe Copilot Quantum Edition v1.0
Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Build ID: {timestamp}

Features:
- Revolutionary Erase Mode with AI inpainting
- Advanced Edit Mode with GPT-4 integration
- Tesseract OCR v5.5.0.20241111 integration
- qpdf v12.2.0 for PDF unlocking
- Document preview functionality
- Multi-page processing
- Export to PNG, PDF, DOCX formats
- Undo/Redo history trail
- Robust Unicode handling
- Professional UI with tabs

System Requirements:
- Python 3.8+
- Windows 10/11
- Tesseract OCR (included in package)
- qpdf (included in package)
- OpenAI API key (user provides)

Launch Commands:
1. python launcher_quantum.py
2. Double-click LAUNCH_QUANTUM.bat
3. streamlit run app_quantum.py --server.port 8506
"""
    
    with open(os.path.join(package_dir, "VERSION.txt"), "w", encoding="utf-8") as f:
        f.write(version_content)
    
    # Create INSTALLATION_GUIDE.md
    installation_guide = f"""# 🚀 NeuroScribe Copilot Quantum Edition - Installation Guide

## 📦 Package Information
- **Version**: v1.0
- **Build Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Build ID**: {timestamp}
- **Size**: ~25 KB

## 🎯 Quick Start

### 1. Extract Package
Extract the ZIP file to a folder of your choice.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure OpenAI API
Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

### 4. Launch Application
```bash
python launcher_quantum.py
```

## 🔧 System Requirements

### Required Software
- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11
- **Memory**: 4GB RAM minimum
- **Storage**: 100MB free space

### Included Tools
- **Tesseract OCR**: v5.5.0.20241111 (automatically detected)
- **qpdf**: v12.2.0 (automatically detected)
- **All Python Dependencies**: Listed in requirements.txt

## 🎮 Features

### 📝 Edit Mode
- AI-powered text editing with GPT-4
- Document preview with tabs
- Multi-page support
- Export to PDF

### 🧽 Erase Mode
- AI inpainting for text removal
- Natural language commands
- Visual document preview
- Export to PNG, PDF, DOCX

### 🔍 OCR Support
- Automatic text recognition for scanned PDFs
- Robust Unicode handling
- Multi-language support

### 🔓 PDF Unlock
- Automatic encrypted PDF detection
- Password removal capabilities
- Secure processing

## 🚀 Launch Options

### Option 1: Advanced Launcher (Recommended)
```bash
python launcher_quantum.py
```
- Checks all dependencies
- Verifies system requirements
- Auto-opens browser
- Professional startup experience

### Option 2: One-Click Launcher
Double-click `LAUNCH_QUANTUM.bat`
- Simple Windows batch file
- Quick startup
- No command line needed

### Option 3: Direct Launch
```bash
streamlit run app_quantum.py --server.port 8506
```
- Direct Streamlit launch
- Custom port selection
- Manual control

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

1. **Port Already in Use**
   - The launcher automatically finds available ports
   - Or manually specify: `--server.port 8507`

2. **Missing Dependencies**
   - Run: `pip install -r requirements.txt`
   - Check: `python verify_environment.py`

3. **OCR Not Working**
   - Verify Tesseract installation
   - Check PATH environment variable
   - Run verification script

4. **PDF Unlock Issues**
   - Verify qpdf installation
   - Check PATH environment variable
   - PyMuPDF fallback is available

## 📞 Support

For issues and questions:
1. Check the verification script output
2. Review the comprehensive documentation
3. Check system requirements
4. Ensure all dependencies are installed

## 🎉 Ready to Use!

The NeuroScribe Copilot Quantum Edition is now ready to transform your document processing workflow!

**The future of document editing is here, and it's powered by AI! 🚀**
"""
    
    with open(os.path.join(package_dir, "INSTALLATION_GUIDE.md"), "w", encoding="utf-8") as f:
        f.write(installation_guide)

def create_zip_archive(source_dir, zip_path):
    """Create a ZIP archive of the package directory"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
                print(f"📦 Added to ZIP: {arcname}")

if __name__ == "__main__":
    print("🧠 Creating NeuroScribe Copilot Quantum Edition Package...")
    print("=" * 60)
    
    try:
        package_path = create_quantum_package()
        print("\n" + "=" * 60)
        print("🎉 PACKAGE CREATION COMPLETE!")
        print("=" * 60)
        print(f"📦 Package: {package_path}")
        print(f"📁 Location: {os.path.abspath(package_path)}")
        print("\n🚀 The Quantum Edition is ready for distribution!")
        print("💡 Users can now extract and run: python launcher_quantum.py")
        
    except Exception as e:
        print(f"\n❌ Error creating package: {e}")
        print("Please check file permissions and available disk space.") 