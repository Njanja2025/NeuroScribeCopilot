#!/usr/bin/env python3
"""
NeuroScribe PDF Copilot - Setup Verification Script
Verifies that all required tools are installed and working.
"""

import subprocess
import shutil
import sys

def check_tool(tool_name, command, description):
    """Check if a tool is installed and working."""
    print(f"🔍 Checking {tool_name}...")
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ {tool_name}: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {tool_name}: Command failed")
            return False
    except FileNotFoundError:
        print(f"❌ {tool_name}: Not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print(f"⚠️  {tool_name}: Command timed out")
        return False
    except Exception as e:
        print(f"❌ {tool_name}: Error - {str(e)}")
        return False

def check_python_package(package_name, import_name=None):
    """Check if a Python package is installed."""
    if import_name is None:
        import_name = package_name
    
    print(f"🔍 Checking {package_name}...")
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'OK')
        print(f"✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"❌ {package_name}: Not installed")
        return False
    except Exception as e:
        print(f"❌ {package_name}: Error - {str(e)}")
        return False

def main():
    print("🧠 NeuroScribe PDF Copilot - Setup Verification")
    print("=" * 50)
    
    # Check Python packages
    print("\n📦 Python Packages:")
    packages = [
        ("streamlit", "streamlit"),
        ("PyMuPDF", "fitz"),
        ("Pillow", "PIL"),
        ("pytesseract", "pytesseract"),
        ("openai", "openai"),
        ("python-dotenv", "dotenv"),
    ]
    
    for package, import_name in packages:
        check_python_package(package, import_name)
    
    # Check external tools
    print("\n🔧 External Tools:")
    tools = [
        ("Tesseract OCR", ["tesseract", "--version"], "OCR for scanned PDFs"),
        ("qpdf", ["qpdf", "--version"], "PDF unlock/decrypt"),
    ]
    
    for tool, command, description in tools:
        check_tool(tool, command, description)
    
    # Check environment variables
    print("\n🔑 Environment Variables:")
    import os
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print(f"✅ OPENAI_API_KEY: {'*' * 10}{openai_key[-4:]}")
    else:
        print("❌ OPENAI_API_KEY: Not set")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Installation Status Summary:")
    
    # Check if Tesseract is in PATH
    tesseract_available = shutil.which("tesseract") is not None
    if tesseract_available:
        print("✅ Tesseract OCR: Available")
    else:
        print("❌ Tesseract OCR: Not found in PATH")
        print("   Download: https://github.com/UB-Mannheim/tesseract/wiki")
    
    # Check if qpdf is in PATH
    qpdf_available = shutil.which("qpdf") is not None
    if qpdf_available:
        print("✅ qpdf: Available")
    else:
        print("❌ qpdf: Not found in PATH")
        print("   Download: https://github.com/qpdf/qpdf/releases")
    
    if openai_key:
        print("✅ OpenAI API Key: Configured")
    else:
        print("❌ OpenAI API Key: Not configured")
    
    print("\n🚀 Ready to launch NeuroScribe PDF Copilot!")
    print("   Run: python launcher.py")

if __name__ == "__main__":
    main() 