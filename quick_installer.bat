@echo off
REM Quick Installer Creation - Creates Inno Setup installer (recommended)
echo Creating Timer Application Installer (Inno Setup)...
echo.

REM Check if executable exists
if not exist "dist\*.exe" (
    echo Building executable first...
    python build_exe.py --type release
    if errorlevel 1 (
        echo Failed to build executable!
        pause
        exit /b 1
    )
)

REM Create Inno Setup installer script
echo Creating installer script...
python create_installer.py --type inno

if errorlevel 1 (
    echo Failed to create installer script!
    pause
    exit /b 1
)

echo.
echo ✅ Installer script created successfully!
echo.
echo Next steps:
echo 1. Download Inno Setup from: https://jrsoftware.org/isinfo.php
echo 2. Install Inno Setup
echo 3. Open: installer\inno\TimerApplication_Setup.iss
echo 4. Click 'Build' or press F9
echo.
echo Your installer will be created in the installer\output\ folder
echo.

REM Ask if user wants to open the installer folder
set /p openFolder="Open installer folder now? (Y/N): "
if /i "%openFolder%"=="Y" (
    explorer installer\inno
)

echo.
pause