@echo off
echo 🧠 NeuroScribe PDF Copilot - Installation Verification
echo =====================================================

echo.
echo 🔍 Checking Tesseract OCR...
tesseract --version
if %errorlevel% equ 0 (
    echo ✅ Tesseract OCR: INSTALLED AND WORKING
) else (
    echo ❌ Tesseract OCR: NOT FOUND
    echo    Please install from: https://github.com/UB-Mannheim/tesseract/wiki
)

echo.
echo 🔓 Checking qpdf...
qpdf --version
if %errorlevel% equ 0 (
    echo ✅ qpdf: INSTALLED AND WORKING
) else (
    echo ❌ qpdf: NOT FOUND
    echo    Please install from: https://github.com/qpdf/qpdf/releases
)

echo.
echo 🧪 Running full system verification...
python verify_setup.py

echo.
echo 🚀 If all checks pass, you can now run:
echo    python launcher.py
echo.
pause 