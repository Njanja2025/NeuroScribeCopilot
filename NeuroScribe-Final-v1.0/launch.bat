@echo off
echo Starting NeuroScribe PDF Copilot...
cd /d "%~dp0"

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate
) else (
    echo Virtual environment not found, using system Python...
)

echo Starting NeuroScribe with auto-browser launch...
python launcher.py
pause
