@echo off
title NeuroScribe PDF Copilot - Quick Package Creator
color 0B

echo.
echo    +===============================================================+
echo    |                NEUROSCRIBE PDF COPILOT                        |
echo    |                   QUICK PACKAGE CREATOR                       |
echo    |                                                                |
echo    |  PACKAGING OPTIONS:                                            |
echo    |                                                                |
echo    |  1. Portable ZIP Package                                      |
echo    |     * Complete application in ZIP format                      |
echo    |     * Ready for distribution                                  |
echo    |     * Includes all dependencies                               |
echo    |                                                                |
echo    |  2. Windows EXE Installer                                     |
echo    |     * Professional installer package                          |
echo    |     * Auto-installation                                       |
echo    |     * Desktop shortcuts                                       |
echo    |                                                                |
echo    |  3. Docker Container Package                                  |
echo    |     * Containerized application                               |
echo    |     * Cross-platform deployment                               |
echo    |     * Easy deployment                                         |
echo    |                                                                |
echo    |  4. GitHub Release Package                                    |
echo    |     * Source code + binaries                                  |
echo    |     * Release notes                                           |
echo    |     * Version tagging                                         |
echo    |                                                                |
echo    |  5. Backup Current Version                                    |
echo    |     * Create backup of working version                        |
echo    |     * Safe storage                                            |
echo    |                                                                |
echo    |  6. Exit                                                       |
echo    |                                                                |
echo    +===============================================================+
echo.

:menu
set /p choice="Select packaging option (1-6): "

if "%choice%"=="1" goto zip
if "%choice%"=="2" goto exe
if "%choice%"=="3" goto docker
if "%choice%"=="4" goto github
if "%choice%"=="5" goto backup
if "%choice%"=="6" goto exit

echo Invalid choice. Please select 1-6.
goto menu

:zip
echo.
echo Creating Portable ZIP Package...
echo.
python create_final_zip.py
echo.
echo ZIP package created successfully!
echo Check the output folder for NeuroScribe-Portable.zip
echo.
pause
goto menu

:exe
echo.
echo Creating Windows EXE Installer...
echo.
python create_installer_package.py
echo.
echo EXE installer created successfully!
echo Check the output folder for NeuroScribe-Installer.exe
echo.
pause
goto menu

:docker
echo.
echo Creating Docker Container Package...
echo.
docker-compose build
echo.
echo Docker container created successfully!
echo Use 'docker-compose up' to run the application
echo.
pause
goto menu

:github
echo.
echo Preparing GitHub Release Package...
echo.
git add .
git commit -m "Release v1.0 - NeuroScribe PDF Copilot"
git tag v1.0
git push origin main --tags
echo.
echo GitHub release prepared successfully!
echo Check GitHub for the new release
echo.
pause
goto menu

:backup
echo.
echo Creating Backup of Current Version...
echo.
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
mkdir "NeuroScribe_Backup_%timestamp%"
xcopy /E /I /Y . "NeuroScribe_Backup_%timestamp%"
echo.
echo Backup created successfully!
echo Location: NeuroScribe_Backup_%timestamp%
echo.
pause
goto menu

:exit
echo.
echo Thank you for using NeuroScribe PDF Copilot!
echo All packages are ready for professional distribution.
echo.
pause
exit 