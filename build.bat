@echo off
REM Build script for Timer Application
REM This batch file provides easy building options for Windows users

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Timer Application Build Script
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to your PATH
    pause
    exit /b 1
)

echo Python is available: 
python --version

echo.
echo Build Options:
echo [1] Release Build (Single EXE, No Console)
echo [2] Debug Build (With Console, Separate Files)
echo [3] Both Builds
echo [4] Clean Build Directories Only
echo [5] Install Dependencies Only
echo.

set /p choice="Select option (1-5): "

if "%choice%"=="1" (
    echo.
    echo Building Release Version...
    python build_exe.py --type release
) else if "%choice%"=="2" (
    echo.
    echo Building Debug Version...
    python build_exe.py --type debug
) else if "%choice%"=="3" (
    echo.
    echo Building All Versions...
    python build_exe.py --type all
) else if "%choice%"=="4" (
    echo.
    echo Cleaning Build Directories...
    python build_exe.py --clean-only
) else if "%choice%"=="5" (
    echo.
    echo Installing Dependencies...
    pip install -r requirements.txt --upgrade
) else (
    echo Invalid choice. Please run the script again.
    pause
    exit /b 1
)

echo.
if errorlevel 1 (
    echo Build process completed with errors.
) else (
    echo Build process completed successfully!
    echo.
    echo Your executable(s) can be found in the 'dist' folder.
)

echo.
echo Press any key to exit...
pause >nul