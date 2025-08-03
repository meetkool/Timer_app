@echo off
REM Installer Creation Script for Timer Application
REM This batch file helps create Windows installers

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Timer Application Installer Creator
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
echo Installer Options:
echo [1] Create All Installer Scripts (Recommended)
echo [2] WiX Toolset MSI (Professional)
echo [3] Inno Setup Installer (Easy to Use)
echo [4] NSIS Installer (Lightweight)
echo [5] cx_Freeze MSI (Python-based)
echo [6] Show Requirements
echo.

set /p choice="Select option (1-6): "

if "%choice%"=="1" (
    echo.
    echo Creating all installer scripts...
    python create_installer.py --type all
) else (
    if "%choice%"=="2" (
        echo.
        echo Creating WiX Toolset MSI script...
        python create_installer.py --type wix
    ) else (
        if "%choice%"=="3" (
            echo.
            echo Creating Inno Setup installer script...
            python create_installer.py --type inno
        ) else (
            if "%choice%"=="4" (
                echo.
                echo Creating NSIS installer script...
                python create_installer.py --type nsis
            ) else (
                if "%choice%"=="5" (
                    echo.
                    echo Creating cx_Freeze MSI setup...
                    python create_installer.py --type cx_freeze
                ) else (
                    if "%choice%"=="6" (
                        echo.
                        echo INSTALLER TOOL REQUIREMENTS:
                        echo ========================================
                        echo.
                        echo 1. WiX Toolset ^(for MSI installers^):
                        echo    Download: https://wixtoolset.org/releases/
                        echo    Free and professional-grade
                        echo.
                        echo 2. Inno Setup ^(easiest to use^):
                        echo    Download: https://jrsoftware.org/isinfo.php
                        echo    Free and user-friendly
                        echo.
                        echo 3. NSIS ^(lightweight installers^):
                        echo    Download: https://nsis.sourceforge.io/
                        echo    Creates .exe installers
                        echo.
                        echo 4. cx_Freeze ^(Python-based^):
                        echo    Install: pip install cx_Freeze
                        echo    No additional tools needed
                        echo.
                        echo RECOMMENDED: Start with Inno Setup for beginners!
                        echo.
                    ) else (
                        echo Invalid choice. Please run the script again.
                        pause
                        exit /b 1
                    )
                )
            )
        )
    )
)

echo.
if errorlevel 1 (
    echo Installer creation completed with errors.
) else (
    echo Installer creation completed successfully!
    echo.
    echo Next steps:
    echo 1. Navigate to the 'installer' folder
    echo 2. Choose your preferred installer type
    echo 3. Install the required tool and build your installer
    echo.
    echo Files created in: installer\
)

echo.
echo Press any key to exit...
pause >nul