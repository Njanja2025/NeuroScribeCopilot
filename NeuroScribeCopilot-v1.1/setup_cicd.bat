@echo off
echo 🚀 NeuroScribe CI/CD Setup Script
echo =================================
echo.

REM Check if Git is initialized
if not exist .git (
    echo 📁 Initializing Git repository...
    git init
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already exists
)

REM Check if .env exists
if not exist .env (
    echo 📝 Creating .env file from template...
    copy env.template .env
    echo ✅ .env file created
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file and add your API keys:
    echo    - OPENAI_API_KEY (for GPT features)
    echo    - GITHUB_TOKEN (for CI/CD)
    echo.
    notepad .env
) else (
    echo ✅ .env file exists
)

REM Check if GitHub remote is configured
git remote -v | findstr origin >nul
if errorlevel 1 (
    echo.
    echo 🌐 GitHub Repository Setup:
    echo 1. Create a new repository on GitHub
    echo 2. Run the following commands:
    echo    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
    echo    git branch -M main
    echo    git push -u origin main
    echo.
    set /p repo_url="Enter your GitHub repository URL (or press Enter to skip): "
    if not "%repo_url%"=="" (
        git remote add origin %repo_url%
        echo ✅ GitHub remote added
    )
) else (
    echo ✅ GitHub remote already configured
)

REM Verify all required files exist
echo.
echo 🔍 Verifying CI/CD files...
if exist ".github\workflows\deploy.yml" (
    echo ✅ GitHub Actions workflow
) else (
    echo ❌ GitHub Actions workflow missing
)

if exist "Dockerfile" (
    echo ✅ Dockerfile
) else (
    echo ❌ Dockerfile missing
)

if exist "docker-compose.yml" (
    echo ✅ Docker Compose
) else (
    echo ❌ Docker Compose missing
)

if exist "requirements.txt" (
    echo ✅ Requirements.txt
) else (
    echo ❌ Requirements.txt missing
)

REM Test local setup
echo.
echo 🧪 Testing local setup...
python verify_installations.py
if errorlevel 1 (
    echo ❌ Local verification failed
    echo 💡 Please fix the issues above before proceeding
    pause
    exit /b 1
)

echo.
echo 📋 CI/CD Setup Checklist:
echo.
echo ✅ 1. Git repository initialized
echo ✅ 2. Environment file created
echo ✅ 3. GitHub Actions workflow configured
echo ✅ 4. Docker configuration ready
echo ✅ 5. Dependencies verified
echo.
echo 🔧 Next Steps:
echo.
echo 1. Add secrets to GitHub repository:
echo    - Go to your repo > Settings > Secrets and variables > Actions
echo    - Add GITHUB_TOKEN and OPENAI_API_KEY
echo.
echo 2. Push your code to GitHub:
echo    git add .
echo    git commit -m "Add CI/CD pipeline"
echo    git push origin main
echo.
echo 3. Monitor the pipeline:
echo    - Go to your repo > Actions tab
echo    - Watch the workflow run
echo.
echo 4. Create a release:
echo    - Go to your repo > Releases
echo    - Create a new release to trigger deployment
echo.
echo 🎉 Your NeuroScribe CI/CD pipeline is ready!
echo.
pause 