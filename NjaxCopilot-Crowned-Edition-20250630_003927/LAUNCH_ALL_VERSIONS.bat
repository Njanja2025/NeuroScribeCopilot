@echo off
title NeuroScribe PDF Copilot - All Versions Launcher
color 0A

echo.
echo    +===============================================================+
echo    |                    NEUROSCRIBE PDF COPILOT                    |
echo    |                    ALL VERSIONS LAUNCHER                      |
echo    |                                                                |
echo    |  AVAILABLE VERSIONS:                                           |
echo    |                                                                |
echo    |  1. Basic Edition (Port 8505)                                  |
echo    |     * PDF text editing with GPT-4                              |
echo    |     * OCR processing                                           |
echo    |     * Simple interface                                         |
echo    |                                                                |
echo    |  2. Quantum Edition (Port 8506)                                |
echo    |     * Advanced AI features                                     |
echo    |     * Erase mode with inpainting                               |
echo    |     * Document preview                                         |
echo    |     * Multi-page support                                       |
echo    |                                                                |
echo    |  3. Professional Edition (Port 8508)                           |
echo    |     * Black & Gold theme                                       |
echo    |     * Live document preview                                    |
echo    |     * Real-time updates                                        |
echo    |     * Professional UI                                          |
echo    |     * Enterprise ready                                         |
echo    |                                                                |
echo    |  4. System Verification                                        |
echo    |     * Check all dependencies                                   |
echo    |     * Verify installations                                     |
echo    |     * Test configurations                                      |
echo    |                                                                |
echo    |  5. Exit                                                        |
echo    |                                                                |
echo    +===============================================================+
echo.

:menu
set /p choice="Select version to launch (1-5): "

if "%choice%"=="1" goto basic
if "%choice%"=="2" goto quantum
if "%choice%"=="3" goto professional
if "%choice%"=="4" goto verify
if "%choice%"=="5" goto exit

echo Invalid choice. Please select 1-5.
goto menu

:basic
echo.
echo Launching Basic Edition...
echo Opening browser...
start http://localhost:8505
echo Starting Streamlit app...
streamlit run app.py --server.port 8505
goto end

:quantum
echo.
echo Launching Quantum Edition...
echo Opening browser...
start http://localhost:8506
echo Starting Streamlit app...
streamlit run app_quantum.py --server.port 8506
goto end

:professional
echo.
echo Launching Professional Edition...
echo Opening browser...
start http://localhost:8508
echo Starting Streamlit app...
streamlit run app_professional.py --server.port 8508
goto end

:verify
echo.
echo Running system verification...
python verify_installations.py
echo.
echo Checking Tesseract OCR...
python verify_tesseract.py
echo.
pause
goto menu

:exit
echo.
echo Thank you for using NeuroScribe PDF Copilot!
echo All versions are ready for professional use.
echo.
pause
exit

:end
echo.
echo Application launched successfully!
echo Check your browser for the application.
echo.
pause 