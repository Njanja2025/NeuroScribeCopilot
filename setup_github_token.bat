@echo off
echo 🔐 NeuroScribe GitHub Token Setup
echo =================================
echo.

REM Check if .env exists
if exist .env (
    echo ✅ .env file found
) else (
    echo 📝 Creating .env file from template...
    copy env.template .env
    echo ✅ .env file created
)

echo.
echo 📋 Instructions:
echo 1. Get your GitHub token from: https://github.com/settings/tokens
echo 2. Open .env file and replace 'your_github_token_here' with your actual token
echo 3. Save the file
echo 4. Run this script again to test the connection
echo.

REM Check if token is set
findstr /C:"GITHUB_TOKEN=your_github_token_here" .env >nul
if %errorlevel% equ 0 (
    echo ⚠️  GitHub token not configured yet
    echo 💡 Please edit .env file and add your GitHub token
    echo.
    echo Opening .env file for editing...
    notepad .env
) else (
    echo ✅ GitHub token appears to be configured
    echo 🧪 Testing GitHub integration...
    python github_integration.py
)

echo.
echo 📚 Next steps:
echo - Push your code to GitHub
echo - Set up GitHub Actions in your repository
echo - Add GITHUB_TOKEN as a repository secret
echo.
pause 