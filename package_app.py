import os
import shutil
import zipfile
from datetime import datetime

def create_final_package():
    """Create final deployment package"""
    print("Creating NeuroScribe Final Package...")
    
    # Create package directory
    package_dir = "NeuroScribe-Final-v1.0"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy main files
    files_to_copy = [
        "app.py", "launcher.py", "requirements.txt", "env.template",
        "verify_installations.py", "Dockerfile", "docker-compose.yml",
        "README.md", "DEPLOYMENT_SUMMARY.md", "CI_CD_GUIDE.md",
        "deploy_to_production.bat", "launch.bat", "setup_cicd.bat"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"✅ {file}")
    
    # Copy src directory
    if os.path.exists("src"):
        shutil.copytree("src", os.path.join(package_dir, "src"))
        print("✅ src/ directory")
    
    # Copy GitHub workflows
    if os.path.exists(".github"):
        shutil.copytree(".github", os.path.join(package_dir, ".github"))
        print("✅ .github/ directory")
    
    # Create quick start script
    quick_start = os.path.join(package_dir, "QUICK_START.bat")
    with open(quick_start, "w", encoding='utf-8') as f:
        f.write("""@echo off
echo NeuroScribe PDF Copilot - Quick Start
echo ======================================
python launcher.py
""")
    
    # Create ZIP package
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_name = f"NeuroScribe-PDF-Copilot-v1.0-{timestamp}.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
    
    print(f"\n🎉 Package created: {zip_name}")
    return zip_name

if __name__ == "__main__":
    create_final_package() 