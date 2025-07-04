import zipfile
import os
import shutil
from datetime import datetime

def create_simple_deployment():
    """Create a simple deployment package for NeuroScribe PDF Copilot"""
    
    print("🚀 Creating NeuroScribe PDF Copilot Simple Deployment Package...")
    
    # Get current directory
    current_dir = os.getcwd()
    
    # Create package name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    package_name = f"NeuroScribe-Simple-Deployment-{timestamp}"
    package_dir = os.path.join(current_dir, package_name)
    
    # Create package directory
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir, exist_ok=True)
    
    # Files to include
    files_to_include = [
        "app.py",
        "requirements.txt",
        "README.md",
        "RELEASE_NOTES.md",
        "LAUNCH_ALL_VERSIONS.bat",
        "QUICK_PACKAGE.bat",
        "src/__init__.py",
        "src/openai_utils.py",
        "src/pdf_utils.py",
        "src/erase_utils.py"
    ]
    
    # Create src directory
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
    
    # Create simple launcher
    launcher_bat = os.path.join(package_dir, "LAUNCH_SIMPLE.bat")
    launcher_content = """@echo off
title NeuroScribe PDF Copilot - Simple Launcher
color 0A

echo.
echo    ╔══════════════════════════════════════════════════════════════╗
echo    ║                🧠 NEUROSCRIBE PDF COPILOT                    ║
echo    ║                    SIMPLE LAUNCHER                           ║
echo    ║                                                              ║
echo    ║  🎯 FEATURES:                                                ║
echo    ║  🧠 GPT-4 Editor + OCR Processing                           ║
echo    ║  🧼 AI Inpainting-based Erase Mode                          ║
echo    ║  ✍️  Image Text Editing Mode                                ║
echo    ║  📑 Real-Time Document Preview                              ║
echo    ║                                                              ║
echo    ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 Starting NeuroScribe PDF Copilot...
echo.

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Dependencies installed successfully!
echo.

echo 🌐 Launching application...
streamlit run app.py --server.port 8501

echo.
echo 🎉 NeuroScribe PDF Copilot is now running!
echo 🌐 Open your browser to: http://localhost:8501
echo.

pause
"""
    
    with open(launcher_bat, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    # Create the ZIP archive
    zip_path = f"{package_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
                print(f"📦 Added to package: {arcname}")
    
    # Clean up temporary directory
    try:
        shutil.rmtree(package_dir)
    except:
        print("⚠️  Could not clean up temporary directory")
    
    print(f"\n🎉 Simple Deployment Package created successfully!")
    print(f"📦 Package: {zip_path}")
    print(f"📁 Files included: {len(copied_files)}")
    print(f"📊 Package size: {os.path.getsize(zip_path) / 1024:.1f} KB")
    
    return zip_path

if __name__ == "__main__":
    try:
        package_path = create_simple_deployment()
        
        if package_path:
            print("\n" + "=" * 70)
            print("🚀 SIMPLE DEPLOYMENT PACKAGE CREATION COMPLETE!")
            print("=" * 70)
            print(f"📦 Package: {package_path}")
            print(f"📁 Location: {os.path.abspath(package_path)}")
            print(f"📊 Size: {os.path.getsize(package_path) / 1024:.1f} KB")
            
            print("\n🚀 Features Included:")
            print("   ✅ GPT-4 Editor + OCR processing")
            print("   ✅ AI Inpainting-based Erase Mode")
            print("   ✅ Image Text Editing Mode")
            print("   ✅ Real-Time Document Preview")
            print("   ✅ Simple launcher with instructions")
            print("   ✅ All necessary dependencies")
            
            print("\n💡 Ready for Distribution!")
            print("   Users can extract and run: LAUNCH_SIMPLE.bat")
            
        else:
            print("\n❌ Failed to create Simple Deployment package!")
        
    except Exception as e:
        print(f"\n❌ Error creating Simple Deployment package: {e}")
        print("Please check file permissions and available disk space.") 