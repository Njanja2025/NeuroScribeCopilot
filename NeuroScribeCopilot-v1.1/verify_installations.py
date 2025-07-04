#!/usr/bin/env python3
"""
Verification script for NeuroScribe PDF Copilot dependencies.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_tesseract():
    """Check if Tesseract OCR is properly installed."""
    print("🔍 Checking Tesseract OCR...")
    
    # Check common installation paths
    tesseract_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        "tesseract"  # If in PATH
    ]
    
    for path in tesseract_paths:
        try:
            if path == "tesseract":
                result = subprocess.run([path, "--version"], 
                                      capture_output=True, text=True, timeout=10)
            else:
                if os.path.exists(path):
                    result = subprocess.run([path, "--version"], 
                                          capture_output=True, text=True, timeout=10)
                else:
                    continue
                    
            if result.returncode == 0:
                print(f"✅ Tesseract found: {path}")
                print(f"   Version: {result.stdout.strip()}")
                return True
        except Exception as e:
            continue
    
    print("❌ Tesseract not found or not working")
    return False

def check_qpdf():
    """Check if QPDF is properly installed."""
    print("\n🔍 Checking QPDF...")
    
    # Check common installation paths
    qpdf_paths = [
        r"C:\Program Files\qpdf 12.2.0\bin\qpdf.exe",
        r"C:\Program Files\qpdf\bin\qpdf.exe",
        r"C:\Program Files (x86)\qpdf\bin\qpdf.exe",
        "qpdf"  # If in PATH
    ]
    
    for path in qpdf_paths:
        try:
            if path == "qpdf":
                result = subprocess.run([path, "--version"], 
                                      capture_output=True, text=True, timeout=10)
            else:
                if os.path.exists(path):
                    result = subprocess.run([path, "--version"], 
                                          capture_output=True, text=True, timeout=10)
                else:
                    continue
                    
            if result.returncode == 0:
                print(f"✅ QPDF found: {path}")
                print(f"   Version: {result.stdout.strip()}")
                return True
        except Exception as e:
            continue
    
    print("❌ QPDF not found or not working")
    return False

def check_python_dependencies():
    """Check if required Python packages are installed."""
    print("\n🔍 Checking Python dependencies...")
    
    required_packages = [
        ("streamlit", "streamlit"),
        ("PyMuPDF", "fitz"),  # PyMuPDF is imported as fitz
        ("pytesseract", "pytesseract"),
        ("Pillow", "PIL"),    # Pillow is imported as PIL
        ("openai", "openai")
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - MISSING")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install " + " ".join(missing_packages))
        return False
    
    return True

def main():
    """Main verification function."""
    print("🚀 NeuroScribe PDF Copilot - Dependency Verification")
    print("=" * 50)
    
    tesseract_ok = check_tesseract()
    qpdf_ok = check_qpdf()
    python_ok = check_python_dependencies()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"   Tesseract OCR: {'✅ Ready' if tesseract_ok else '❌ Missing'}")
    print(f"   QPDF: {'✅ Ready' if qpdf_ok else '❌ Missing'}")
    print(f"   Python Dependencies: {'✅ Ready' if python_ok else '❌ Missing'}")
    
    if tesseract_ok and qpdf_ok and python_ok:
        print("\n🎉 All dependencies are ready! NeuroScribe should work perfectly.")
        print("   You can now run: streamlit run app.py")
    else:
        print("\n⚠️  Some dependencies are missing. Please install them before using NeuroScribe.")
        
        if not tesseract_ok:
            print("\n📝 To install Tesseract:")
            print("   winget install -e --id tesseract-ocr.tesseract")
            
        if not qpdf_ok:
            print("\n📝 To install QPDF:")
            print("   winget install -e --id QPDF.QPDF")

if __name__ == "__main__":
    main() 