import os
import subprocess
import sys
from datetime import datetime

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def check_git_installation():
    """Check if Git is installed and accessible"""
    print("🔍 Checking Git installation...")
    if run_command("git --version", "Git version check"):
        return True
    else:
        print("❌ Git is not installed or not in PATH")
        print("💡 Please install Git from: https://git-scm.com/download/win")
        print("💡 Make sure to select 'Add Git to PATH' during installation")
        return False

def setup_git_repository():
    """Set up Git repository and push to GitHub"""
    
    print("🚀 Setting up GitHub repository for NeuroScribe PDF Copilot...")
    print("=" * 70)
    
    # Check Git installation
    if not check_git_installation():
        return False
    
    # Initialize Git repository
    if not run_command("git init", "Initialize Git repository"):
        return False
    
    # Add all files
    if not run_command("git add .", "Add all files to Git"):
        return False
    
    # Create initial commit
    commit_message = f"Initial commit - NeuroScribe PDF Copilot v1.0 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    if not run_command(f'git commit -m "{commit_message}"', "Create initial commit"):
        return False
    
    # Set up remote origin
    remote_url = "https://github.com/Njanja2025/NeuroScribeCopilot.git"
    if not run_command(f"git remote add origin {remote_url}", "Add GitHub remote"):
        # If remote already exists, update it
        run_command(f"git remote set-url origin {remote_url}", "Update GitHub remote URL")
    
    # Set main branch
    run_command("git branch -M main", "Set main branch")
    
    # Push to GitHub
    if not run_command("git push -u origin main", "Push to GitHub"):
        print("⚠️  Push failed - you may need to authenticate with GitHub")
        print("💡 You can manually push using:")
        print(f"   git push -u origin main")
        return False
    
    return True

def create_github_release_script():
    """Create a script for GitHub release creation"""
    
    release_script = """# GitHub Release Creation Script
# Run this after pushing to GitHub

echo "🎉 Creating GitHub Release for NeuroScribe PDF Copilot v1.0..."

# Create release using GitHub CLI (if installed)
if command -v gh &> /dev/null; then
    echo "📦 Creating release with GitHub CLI..."
    gh release create v1.0 \\
        --title "NeuroScribe PDF Copilot v1.0" \\
        --notes-file RELEASE_NOTES.md \\
        release-package/*.zip
    
    echo "✅ Release created successfully!"
else
    echo "📋 Manual Release Creation Required:"
    echo "1. Go to: https://github.com/Njanja2025/NeuroScribeCopilot"
    echo "2. Click 'Releases' on the right side"
    echo "3. Click 'Create a new release'"
    echo "4. Tag: v1.0"
    echo "5. Title: NeuroScribe PDF Copilot v1.0"
    echo "6. Description: Copy content from RELEASE_NOTES.md"
    echo "7. Upload all files from release-package/ folder"
    echo "8. Click 'Publish release'"
fi

echo "🎉 Release process complete!"
"""
    
    with open("create_github_release.sh", "w", encoding='utf-8') as f:
        f.write(release_script)
    
    # Create Windows batch version
    batch_script = """@echo off
title GitHub Release Creation Script

echo 🎉 Creating GitHub Release for NeuroScribe PDF Copilot v1.0...
echo.

echo 📋 Manual Release Creation Required:
echo 1. Go to: https://github.com/Njanja2025/NeuroScribeCopilot
echo 2. Click 'Releases' on the right side
echo 3. Click 'Create a new release'
echo 4. Tag: v1.0
echo 5. Title: NeuroScribe PDF Copilot v1.0
echo 6. Description: Copy content from RELEASE_NOTES.md
echo 7. Upload all files from release-package/ folder
echo 8. Click 'Publish release'
echo.

echo 🎉 Release process complete!
pause
"""
    
    with open("create_github_release.bat", "w", encoding='utf-8') as f:
        f.write(batch_script)
    
    print("✅ Created GitHub release scripts:")
    print("   - create_github_release.sh (Linux/Mac)")
    print("   - create_github_release.bat (Windows)")

def main():
    """Main function to set up GitHub repository"""
    
    print("🧠 NeuroScribe PDF Copilot - GitHub Setup")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found in current directory")
        print("💡 Please run this script from the NeuroScribe PDF Copilot directory")
        return
    
    # Set up Git repository
    if setup_git_repository():
        print("\n🎉 GitHub repository setup completed successfully!")
        print("📁 Repository: https://github.com/Njanja2025/NeuroScribeCopilot")
        
        # Create release scripts
        create_github_release_script()
        
        print("\n📋 Next Steps:")
        print("1. ✅ Code pushed to GitHub")
        print("2. 📦 Create GitHub release:")
        print("   - Run: create_github_release.bat")
        print("   - Or manually create release on GitHub")
        print("3. 🚀 Deploy to Streamlit Cloud")
        print("4. 📢 Share your application!")
        
    else:
        print("\n❌ GitHub setup failed")
        print("💡 You can manually set up GitHub:")
        print("1. Install Git from: https://git-scm.com/download/win")
        print("2. Open new terminal and run:")
        print("   git init")
        print("   git add .")
        print("   git commit -m 'Initial commit'")
        print("   git remote add origin https://github.com/Njanja2025/NeuroScribeCopilot.git")
        print("   git push -u origin main")

if __name__ == "__main__":
    main() 