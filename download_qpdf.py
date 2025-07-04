#!/usr/bin/env python3
"""
NeuroScribe PDF Copilot - qpdf Downloader
Downloads and helps install qpdf for PDF unlocking functionality.
"""

import os
import urllib.request
import zipfile
import subprocess
import sys
from pathlib import Path

def main():
    print("🔓 NeuroScribe PDF Copilot - qpdf Installation")
    print("=" * 60)
    
    # Check if already installed
    try:
        result = subprocess.run(["qpdf", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ qpdf is already installed!")
            print(f"   Version: {result.stdout.strip()}")
            return
    except FileNotFoundError:
        pass
    
    print("📥 Downloading qpdf...")
    
    # Download URL
    qpdf_url = "https://github.com/qpdf/qpdf/releases/download/v11.9.1/qpdf-11.9.1-bin-msvc.zip"
    zip_path = "qpdf.zip"
    install_dir = Path("C:/Program Files/qpdf")
    bin_dir = install_dir / "bin"
    
    try:
        print("⏳ Downloading qpdf... (this may take a few minutes)")
        urllib.request.urlretrieve(qpdf_url, zip_path)
        print(f"✅ Download complete: {zip_path}")
        
        print("\n📂 Extracting qpdf...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(install_dir)
        
        # Clean up
        os.remove(zip_path)
        print("✅ Extraction complete")
        
        print(f"\n📁 qpdf installed to: {install_dir}")
        print(f"📁 Binary location: {bin_dir}")
        
        print("\n🔧 Adding to PATH...")
        add_to_path(str(bin_dir))
        
        print("\n✅ qpdf installation complete!")
        print("📋 Next steps:")
        print("1. Restart your terminal/command prompt")
        print("2. Run: qpdf --version")
        print("3. If not found, manually add to PATH:")
        print(f"   {bin_dir}")
        
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        print("\n📋 Manual Installation:")
        print("1. Go to: https://github.com/qpdf/qpdf/releases")
        print("2. Download: qpdf-11.9.1-bin-msvc.zip")
        print("3. Extract to: C:\\Program Files\\qpdf\\")
        print("4. Add to PATH: C:\\Program Files\\qpdf\\bin\\")

def add_to_path(new_path):
    """Add a path to the system PATH environment variable."""
    try:
        # Get current PATH
        current_path = os.environ.get('PATH', '')
        
        # Add new path if not already present
        if new_path not in current_path:
            new_path_var = current_path + os.pathsep + new_path
            os.environ['PATH'] = new_path_var
            
            # Try to update system PATH (requires admin privileges)
            try:
                subprocess.run([
                    "setx", "PATH", new_path_var
                ], check=True, capture_output=True)
                print("✅ System PATH updated successfully!")
            except subprocess.CalledProcessError:
                print("⚠️  Could not update system PATH automatically.")
                print("   Please manually add to PATH: " + new_path)
    except Exception as e:
        print(f"⚠️  Could not update PATH: {str(e)}")

if __name__ == "__main__":
    main() 