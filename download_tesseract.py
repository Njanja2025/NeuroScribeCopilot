#!/usr/bin/env python3
"""
NeuroScribe PDF Copilot - Tesseract OCR Downloader
Downloads and helps install Tesseract OCR for Windows.
"""

import os
import urllib.request
import subprocess
import sys

def main():
    print("🔍 NeuroScribe PDF Copilot - Tesseract OCR Installation")
    print("=" * 60)
    
    # Check if already installed
    try:
        result = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tesseract OCR is already installed!")
            print(f"   Version: {result.stdout.strip()}")
            return
    except FileNotFoundError:
        pass
    
    print("📥 Downloading Tesseract OCR installer...")
    
    # Download URL
    tesseract_url = "https://github.com/tesseract-ocr/tesseract/releases/download/5.3.3/tesseract-5.3.3.20231005.exe"
    installer_path = "tesseract-installer.exe"
    
    try:
        print("⏳ Downloading... (this may take a few minutes)")
        urllib.request.urlretrieve(tesseract_url, installer_path)
        print(f"✅ Download complete: {installer_path}")
        
        print("\n🔧 Installation Instructions:")
        print("1. Double-click the downloaded file: tesseract-installer.exe")
        print("2. Run as Administrator if prompted")
        print("3. During installation:")
        print("   ✅ Check 'Add to system PATH for all users'")
        print("   ✅ Install to: C:\\Program Files\\Tesseract-OCR\\")
        print("4. Complete the installation")
        print("5. Restart your terminal/command prompt")
        print("6. Run: tesseract --version")
        
        # Ask if user wants to run installer now
        print(f"\n🚀 The installer is ready: {installer_path}")
        print("Would you like to run it now? (y/n): ", end="")
        
        response = input().lower().strip()
        if response in ['y', 'yes']:
            print("🔧 Launching Tesseract installer...")
            subprocess.run([installer_path])
        else:
            print("📋 You can run the installer manually later.")
            
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print("\n📋 Manual Installation:")
        print("1. Go to: https://github.com/tesseract-ocr/tesseract/releases")
        print("2. Download: tesseract-5.3.3.20231005.exe")
        print("3. Run installer as Administrator")
        print("4. Check 'Add to system PATH' during installation")

if __name__ == "__main__":
    main() 