@echo off
REM Quick build script - just builds release version without prompts
echo Building Timer Application (Release Version)...
echo.

python build_exe.py --type release

if errorlevel 1 (
    echo.
    echo Build failed! Check the error messages above.
    pause
) else (
    echo.
    echo Build completed successfully!
    echo Your executable is in the 'dist' folder.
    echo.
    if exist "dist\TimerApp_v1.0.0.exe" (
        echo Found: dist\TimerApp_v1.0.0.exe
    )
    pause
)