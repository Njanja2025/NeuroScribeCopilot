#!/usr/bin/env python3
"""
NeuroScribe PDF Copilot - Dependency Installation Script
Installs Tesseract OCR and qpdf for full functionality.
"""

import os
import subprocess
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

def check_admin():
    """Check if running as administrator."""
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def install_chocolatey():
    """Install Chocolatey package manager."""
    print("🍫 Installing Chocolatey...")
    try:
        # PowerShell command to install Chocolatey
        cmd = [
            "powershell", "-Command",
            "Set-ExecutionPolicy Bypass -Scope Process -Force; "
            "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print("✅ Chocolatey installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Chocolatey: {e}")
        return False

def install_qpdf_chocolatey():
    """Install qpdf using Chocolatey."""
    print("📦 Installing qpdf via Chocolatey...")
    try:
        subprocess.run(["choco", "install", "qpdf", "-y"], check=True, capture_output=True)
        print("✅ qpdf installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install qpdf: {e}")
        return False
    except FileNotFoundError:
        print("❌ Chocolatey not found")
        return False

def install_qpdf_manual():
    """Install qpdf manually."""
    print("📦 Installing qpdf manually...")
    try:
        # Create installation directory
        install_dir = Path("C:/Program Files/qpdf")
        bin_dir = install_dir / "bin"
        
        if not install_dir.exists():
            install_dir.mkdir(parents=True)
        
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
        print("🔧 Adding qpdf to PATH...")
        add_to_path(str(bin_dir))
        
        print("✅ qpdf installed successfully!")
        print(f"   Location: {bin_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Manual qpdf installation failed: {e}")
        return False

def install_tesseract():
    """Install Tesseract OCR."""
    print("🔍 Installing Tesseract OCR...")
    
    # Try Chocolatey first
    try:
        print("🟦 Trying Chocolatey installation...")
        subprocess.run(["choco", "install", "tesseract", "-y"], check=True, capture_output=True)
        print("✅ Tesseract installed via Chocolatey!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Chocolatey not available, providing manual instructions...")
    
    # Manual installation instructions
    print("\n📋 Manual Tesseract Installation:")
    print("1. Go to: https://github.com/UB-Mannheim/tesseract/wiki")
    print("2. Download: tesseract-ocr-w64-setup-5.3.3.20231005.exe")
    print("3. Run installer as Administrator")
    print("4. Install to: C:\\Program Files\\Tesseract-OCR\\")
    print("5. ✅ Check 'Add to system PATH' during installation")
    print("6. Restart your terminal after installation")
    
    return False

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

def verify_installations():
    """Verify that installations were successful."""
    print("\n🔍 Verifying installations...")
    
    # Check qpdf
    try:
        result = subprocess.run(["qpdf", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ qpdf: " + result.stdout.strip())
        else:
            print("❌ qpdf: Command failed")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ qpdf: Not found in PATH")
    
    # Check Tesseract
    try:
        result = subprocess.run(["tesseract", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Tesseract: " + result.stdout.strip())
        else:
            print("❌ Tesseract: Command failed")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ Tesseract: Not found in PATH")

def main():
    """Main installation function."""
    print("🧠 NeuroScribe PDF Copilot - Dependency Installation")
    print("=" * 60)
    
    # Check if running as admin
    if not check_admin():
        print("⚠️  Some installations may require administrator privileges.")
        print("   If installations fail, try running as Administrator.")
    
    # Install qpdf
    print("\n🔓 Installing qpdf (PDF unlock utility)...")
    qpdf_success = False
    
    # Try Chocolatey first
    try:
        subprocess.run(["choco", "--version"], check=True, capture_output=True)
        print("🍫 Chocolatey found, using it for installation...")
        qpdf_success = install_qpdf_chocolatey()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("🍫 Chocolatey not found, installing it first...")
        if install_chocolatey():
            qpdf_success = install_qpdf_chocolatey()
        else:
            print("📦 Trying manual qpdf installation...")
            qpdf_success = install_qpdf_manual()
    
    # Install Tesseract
    print("\n🔍 Installing Tesseract OCR...")
    tesseract_success = install_tesseract()
    
    # Verify installations
    verify_installations()
    
    print("\n" + "=" * 60)
    print("📋 Installation Summary:")
    
    if qpdf_success:
        print("✅ qpdf: Installed successfully")
    else:
        print("❌ qpdf: Installation failed - see manual instructions above")
    
    if tesseract_success:
        print("✅ Tesseract: Installed successfully")
    else:
        print("❌ Tesseract: Manual installation required")
    
    print("\n🚀 Next steps:")
    print("1. Restart your terminal/command prompt")
    print("2. Run: python verify_setup.py")
    print("3. Run: python launcher.py")
    print("4. Test with a PDF file")

if __name__ == "__main__":
    main() 