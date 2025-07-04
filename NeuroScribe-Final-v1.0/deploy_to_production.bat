@echo off
echo 🚀 NeuroScribe Production Deployment
echo ====================================
echo.

REM Check if Git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git not found. Please install Git first.
    echo Download from: https://git-scm.com/downloads
    pause
    exit /b 1
)

REM Check if .env exists and has required tokens
if not exist .env (
    echo ❌ .env file not found. Creating from template...
    copy env.template .env
    echo ⚠️  Please edit .env file and add your API keys:
    echo    - GITHUB_TOKEN (required for CI/CD)
    echo    - OPENAI_API_KEY (for GPT features)
    echo.
    notepad .env
    echo.
    echo 💡 After adding your tokens, run this script again.
    pause
    exit /b 1
)

REM Check if tokens are configured
findstr /C:"GITHUB_TOKEN=your_github_token_here" .env >nul
if %errorlevel% equ 0 (
    echo ❌ GitHub token not configured in .env
    echo 💡 Please edit .env file and add your actual GitHub token
    pause
    exit /b 1
)

REM Verify all required files
echo 🔍 Verifying deployment files...
set missing_files=0

if not exist ".github\workflows\deploy.yml" (
    echo ❌ GitHub Actions workflow missing
    set /a missing_files+=1
) else (
    echo ✅ GitHub Actions workflow
)

if not exist "Dockerfile" (
    echo ❌ Dockerfile missing
    set /a missing_files+=1
) else (
    echo ✅ Dockerfile
)

if not exist "requirements.txt" (
    echo ❌ Requirements.txt missing
    set /a missing_files+=1
) else (
    echo ✅ Requirements.txt
)

if not exist "verify_installations.py" (
    echo ❌ Verification script missing
    set /a missing_files+=1
) else (
    echo ✅ Verification script
)

if %missing_files% gtr 0 (
    echo.
    echo ❌ Some required files are missing. Please ensure all files are present.
    pause
    exit /b 1
)

REM Run final verification
echo.
echo 🧪 Running final verification...
python verify_installations.py
if errorlevel 1 (
    echo ❌ Verification failed. Please fix the issues above.
    pause
    exit /b 1
)

REM Check Git status
echo.
echo 📁 Checking Git status...
git status --porcelain
if errorlevel 1 (
    echo ❌ Git repository not initialized
    echo 💡 Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit: NeuroScribe PDF Copilot"
    git branch -M main
) else (
    echo ✅ Git repository ready
)

REM Check if remote is configured
git remote -v | findstr origin >nul
if errorlevel 1 (
    echo.
    echo 🌐 GitHub Repository Setup Required:
    echo 1. Create a new repository on GitHub
    echo 2. Copy the repository URL
    echo 3. Enter it below when prompted
    echo.
    set /p repo_url="Enter your GitHub repository URL: "
    if not "%repo_url%"=="" (
        git remote add origin %repo_url%
        echo ✅ GitHub remote added
    ) else (
        echo ❌ No repository URL provided
        echo 💡 Please create a GitHub repository and run this script again
        pause
        exit /b 1
    )
) else (
    echo ✅ GitHub remote configured
)

REM Final deployment steps
echo.
echo 🚀 Starting production deployment...
echo.

REM Add all files
echo 📦 Adding files to Git...
git add .

REM Commit changes
echo 💾 Committing changes...
git commit -m "Deploy NeuroScribe PDF Copilot v1.0.0 - Complete CI/CD setup"

REM Push to GitHub
echo 🌐 Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo ❌ Push failed. Please check your GitHub token and repository access.
    echo 💡 Make sure your GitHub token has 'repo' permissions
    pause
    exit /b 1
)

echo.
echo 🎉 DEPLOYMENT SUCCESSFUL!
echo.
echo 📋 Next Steps:
echo.
echo 1. 🌐 Go to your GitHub repository
echo 2. 📊 Click the "Actions" tab to monitor the CI/CD pipeline
echo 3. 🔧 Add repository secrets (if not done):
echo    - Go to Settings > Secrets and variables > Actions
echo    - Add GITHUB_TOKEN and OPENAI_API_KEY
echo 4. 🚀 Create a release:
echo    - Go to Releases > Create a new release
echo    - Tag: v1.0.0
echo    - Title: NeuroScribe PDF Copilot v1.0.0
echo.
echo 📊 Your CI/CD pipeline will automatically:
echo    ✅ Run tests on multiple Python versions
echo    ✅ Build executable and Docker image
echo    ✅ Run security scans
echo    ✅ Upload artifacts to releases
echo.
echo 🌍 Your app is now ready for global deployment!
echo.
pause 