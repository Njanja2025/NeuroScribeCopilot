#!/usr/bin/env python3
"""
NeuroScribe PDF Copilot - qpdf Installation Script
Installs qpdf for PDF unlock functionality on Windows.
"""

import os
import subprocess
import sys
import urllib.request
import zipfile
import shutil

def main():
    print("🔧 Installing qpdf for PDF unlock functionality...")
    
    # Check if qpdf is already installed
    try:
        result = subprocess.run(["qpdf", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ qpdf is already installed!")
            print(f"   Version: {result.stdout.strip()}")
            return
    except FileNotFoundError:
        pass
    
    print("📦 qpdf not found. Installing...")
    
    # Option 1: Try Chocolatey first
    try:
        print("🟦 Trying Chocolatey installation...")
        subprocess.run(["choco", "install", "qpdf", "-y"], check=True, capture_output=True)
        print("✅ qpdf installed via Chocolatey!")
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Chocolatey not available, trying manual installation...")
    
    # Option 2: Manual installation
    try:
        # Create installation directory
        install_dir = r"C:\Program Files\qpdf"
        bin_dir = os.path.join(install_dir, "bin")
        
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)
        
        # Download qpdf
        print("📥 Downloading qpdf...")
        qpdf_url = "https://github.com/qpdf/qpdf/releases/download/v11.9.1/qpdf-11.9.1-bin-msvc.zip"
        zip_path = "qpdf.zip"
        
        urllib.request.urlretrieve(qpdf_url, zip_path)
        
        # Extract
        print("📂 Extracting qpdf...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(install_dir)
        
        # Clean up
        os.remove(zip_path)
        
        # Add to PATH
        print("🔧 Adding qpdf to system PATH...")
        add_to_path(bin_dir)
        
        print("✅ qpdf installed successfully!")
        print(f"   Location: {bin_dir}")
        print("   Please restart your terminal/command prompt for PATH changes to take effect.")
        
    except Exception as e:
        print(f"❌ Manual installation failed: {str(e)}")
        print("\n📋 Manual Installation Instructions:")
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