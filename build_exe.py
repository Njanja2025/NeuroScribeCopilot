#!/usr/bin/env python3
"""
NeuroScribe PDF Copilot - PyInstaller Build Script
Creates a standalone executable for Windows deployment.
"""

import os
import subprocess
import sys
import shutil

def main():
    print("🚀 Building NeuroScribe PDF Copilot Executable...")
    
    # Step 1: Install PyInstaller if not already installed
    print("📦 Installing PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install PyInstaller")
        return
    
    # Step 2: Create PyInstaller command
    pyinstaller_command = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--console",
        "--name=NeuroScribeCopilot",
        "--add-data=src;src",
        "--add-data=launch.bat;.",
        "--add-data=requirements.txt;.",
        "--add-data=env.template;.",
        "--add-data=README.md;.",
        "--hidden-import=streamlit",
        "--hidden-import=fitz",
        "--hidden-import=pytesseract",
        "--hidden-import=PIL",
        "--hidden-import=openai",
        "--hidden-import=dotenv",
        "app.py"
    ]
    
    # Step 3: Run PyInstaller
    print("🔨 Building executable...")
    try:
        subprocess.run(pyinstaller_command, check=True)
        print("✅ Executable built successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build executable: {e}")
        return
    
    # Step 4: Check if executable was created
    exe_path = "dist/NeuroScribeCopilot.exe"
    if os.path.exists(exe_path):
        print(f"🎉 Executable created: {exe_path}")
        print(f"📁 Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
        
        # Step 5: Create deployment package
        print("📦 Creating deployment package...")
        deployment_dir = "NeuroScribeCopilot-Deployment"
        if os.path.exists(deployment_dir):
            shutil.rmtree(deployment_dir)
        os.makedirs(deployment_dir)
        
        # Copy executable
        shutil.copy2(exe_path, deployment_dir)
        
        # Copy additional files
        files_to_copy = [
            "launch.bat",
            "requirements.txt", 
            "env.template",
            "README.md"
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, deployment_dir)
        
        # Create install instructions
        install_instructions = """# NeuroScribe PDF Copilot - Installation

## Quick Start:
1. Double-click NeuroScribeCopilot.exe
2. The app will open in your browser automatically
3. Upload PDFs and start editing!

## Requirements:
- Windows 10/11
- Internet connection (for GPT-4)
- Optional: Tesseract OCR for scanned PDFs

## Optional Setup:
- Install Tesseract OCR for better OCR support
- Set up OpenAI API key in .env file for GPT features

## Troubleshooting:
- If the app doesn't start, try running as administrator
- Check Windows Defender isn't blocking the executable
- Ensure you have internet connection for GPT features

Enjoy your AI-powered PDF editing! 🚀
"""
        
        with open(f"{deployment_dir}/INSTALL.txt", "w") as f:
            f.write(install_instructions)
        
        print(f"✅ Deployment package created: {deployment_dir}/")
        print("🎉 Your NeuroScribe PDF Copilot is ready for distribution!")
        
    else:
        print("❌ Executable not found in dist folder")

if __name__ == "__main__":
    main() 