@echo off
chcp 65001 >nul
title Create Desktop Shortcut

echo.
echo ========================================
echo 🧠 Creating Desktop Shortcut
echo ========================================
echo.

echo 📁 Creating desktop shortcut for NeuroScribe Copilot Quantum...

REM Get the current directory
set "CURRENT_DIR=%~dp0"
set "LAUNCHER_PATH=%CURRENT_DIR%launch_quantum.bat"

REM Create the shortcut using PowerShell
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\🧠 NeuroScribe Copilot Quantum.lnk'); $Shortcut.TargetPath = '%LAUNCHER_PATH%'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'Launch NeuroScribe PDF Copilot Quantum Edition'; $Shortcut.Save()"

if %errorlevel% equ 0 (
    echo ✅ Desktop shortcut created successfully!
    echo 📍 Location: %USERPROFILE%\Desktop\🧠 NeuroScribe Copilot Quantum.lnk
    echo.
    echo 💡 You can now double-click the shortcut on your desktop to launch the app!
) else (
    echo ❌ Failed to create desktop shortcut
    echo 💡 You can manually create a shortcut by:
    echo    1. Right-click on launch_quantum.bat
    echo    2. Select "Send to" → "Desktop (create shortcut)"
    echo    3. Rename the shortcut to "🧠 NeuroScribe Copilot Quantum"
)

echo.
echo Press any key to close...
pause >nul 