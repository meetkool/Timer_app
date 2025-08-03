# PowerShell build script for Timer Application
# Provides cross-platform building with better error handling

param(
    [ValidateSet("release", "debug", "all", "clean", "deps")]
    [string]$BuildType = "release",
    
    [switch]$Help
)

# Color functions for better output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    
    $colors = @{
        "Red" = [System.ConsoleColor]::Red
        "Green" = [System.ConsoleColor]::Green
        "Yellow" = [System.ConsoleColor]::Yellow
        "Blue" = [System.ConsoleColor]::Blue
        "Cyan" = [System.ConsoleColor]::Cyan
        "White" = [System.ConsoleColor]::White
    }
    
    Write-Host $Message -ForegroundColor $colors[$Color]
}

function Show-Help {
    Write-ColorOutput "Timer Application Build Script" "Cyan"
    Write-ColorOutput "===============================" "Cyan"
    Write-Host ""
    Write-Host "Usage: .\build.ps1 [-BuildType <type>] [-Help]"
    Write-Host ""
    Write-Host "Build Types:"
    Write-Host "  release  - Create release build (single EXE, no console)"
    Write-Host "  debug    - Create debug build (with console, separate files)"
    Write-Host "  all      - Create both release and debug builds"
    Write-Host "  clean    - Clean build directories only"
    Write-Host "  deps     - Install dependencies only"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\build.ps1                    # Build release version"
    Write-Host "  .\build.ps1 -BuildType debug   # Build debug version"
    Write-Host "  .\build.ps1 -BuildType all     # Build all versions"
    Write-Host "  .\build.ps1 -BuildType clean   # Clean build directories"
    Write-Host "  .\build.ps1 -BuildType deps    # Install dependencies"
    Write-Host ""
}

function Test-PythonInstallation {
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Python is available: $pythonVersion" "Green"
            return $true
        }
    }
    catch {
        # Python not found
    }
    
    Write-ColorOutput "❌ Python is not installed or not in PATH" "Red"
    Write-ColorOutput "Please install Python 3.8+ and add it to your PATH" "Yellow"
    return $false
}

function Install-Dependencies {
    Write-ColorOutput "📦 Installing dependencies..." "Blue"
    
    try {
        python -m pip install -r requirements.txt --upgrade
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Dependencies installed successfully" "Green"
            return $true
        } else {
            Write-ColorOutput "❌ Failed to install dependencies" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Error installing dependencies: $_" "Red"
        return $false
    }
}

function Invoke-Build {
    param([string]$Type)
    
    Write-ColorOutput "🔨 Starting $Type build..." "Blue"
    
    $arguments = @("build_exe.py")
    
    switch ($Type) {
        "release" { $arguments += "--type", "release" }
        "debug" { $arguments += "--type", "debug" }
        "all" { $arguments += "--type", "all" }
        "clean" { $arguments += "--clean-only" }
    }
    
    try {
        $process = Start-Process -FilePath "python" -ArgumentList $arguments -Wait -NoNewWindow -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-ColorOutput "✅ Build completed successfully!" "Green"
            return $true
        } else {
            Write-ColorOutput "❌ Build failed with exit code: $($process.ExitCode)" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Error running build script: $_" "Red"
        return $false
    }
}

function Show-BuildSummary {
    Write-ColorOutput "`n🎉 BUILD SUMMARY" "Cyan"
    Write-ColorOutput "================" "Cyan"
    
    $distPath = Join-Path $PSScriptRoot "dist"
    
    if (Test-Path $distPath) {
        Write-ColorOutput "📦 Output directory: $distPath" "Blue"
        
        Get-ChildItem $distPath -Recurse -Include "*.exe" | ForEach-Object {
            $sizeMB = [math]::Round($_.Length / 1MB, 1)
            $relativePath = $_.FullName.Replace($distPath, "").TrimStart("\")
            Write-ColorOutput "  🚀 $relativePath ($sizeMB MB)" "Green"
        }
        
        Write-ColorOutput "`n💡 Your executable(s) can be found in: $distPath" "Yellow"
    } else {
        Write-ColorOutput "❌ No output directory found!" "Red"
    }
}

# Main script execution
function Main {
    if ($Help) {
        Show-Help
        return
    }
    
    Write-ColorOutput "🚀 Timer Application Build Script" "Cyan"
    Write-ColorOutput "==================================" "Cyan"
    Write-Host ""
    
    # Check Python installation
    if (-not (Test-PythonInstallation)) {
        exit 1
    }
    
    # Handle different build types
    switch ($BuildType) {
        "deps" {
            if (Install-Dependencies) {
                Write-ColorOutput "`n✅ Dependencies installed successfully!" "Green"
            } else {
                Write-ColorOutput "`n❌ Failed to install dependencies!" "Red"
                exit 1
            }
        }
        
        "clean" {
            if (Invoke-Build "clean") {
                Write-ColorOutput "`n✅ Build directories cleaned!" "Green"
            } else {
                Write-ColorOutput "`n❌ Failed to clean build directories!" "Red"
                exit 1
            }
        }
        
        default {
            # First install dependencies if requirements.txt exists
            if (Test-Path "requirements.txt") {
                Write-ColorOutput "📋 Checking dependencies..." "Blue"
                Install-Dependencies | Out-Null
            }
            
            # Run the build
            if (Invoke-Build $BuildType) {
                Show-BuildSummary
                Write-ColorOutput "`n🎊 Build process completed successfully!" "Green"
            } else {
                Write-ColorOutput "`n💥 Build process failed!" "Red"
                exit 1
            }
        }
    }
}

# Run the main function
Main