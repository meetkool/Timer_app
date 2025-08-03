# PowerShell script for creating Timer Application installers
# Provides cross-platform installer creation with advanced options

param(
    [ValidateSet("wix", "inno", "nsis", "cx_freeze", "all")]
    [string]$InstallerType = "all",
    
    [switch]$Help,
    [switch]$InstallTools,
    [switch]$ShowRequirements
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
        "Magenta" = [System.ConsoleColor]::Magenta
    }
    
    Write-Host $Message -ForegroundColor $colors[$Color]
}

function Show-Help {
    Write-ColorOutput "Timer Application Installer Creator" "Cyan"
    Write-ColorOutput "===================================" "Cyan"
    Write-Host ""
    Write-Host "Usage: .\create_installer.ps1 [-InstallerType <type>] [-Help] [-InstallTools] [-ShowRequirements]"
    Write-Host ""
    Write-Host "Installer Types:"
    Write-Host "  wix        - Create WiX Toolset MSI installer script (professional)"
    Write-Host "  inno       - Create Inno Setup installer script (recommended)"
    Write-Host "  nsis       - Create NSIS installer script (lightweight)"
    Write-Host "  cx_freeze  - Create cx_Freeze MSI setup (Python-based)"
    Write-Host "  all        - Create all installer types (default)"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -InstallTools      - Install required Python packages"
    Write-Host "  -ShowRequirements  - Show download links for installer tools"
    Write-Host "  -Help              - Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\create_installer.ps1                           # Create all installer scripts"
    Write-Host "  .\create_installer.ps1 -InstallerType inno       # Create Inno Setup script only"
    Write-Host "  .\create_installer.ps1 -ShowRequirements         # Show tool requirements"
    Write-Host "  .\create_installer.ps1 -InstallTools             # Install Python packages"
    Write-Host ""
}

function Show-Requirements {
    Write-ColorOutput "📋 INSTALLER TOOL REQUIREMENTS" "Cyan"
    Write-ColorOutput "===============================" "Cyan"
    Write-Host ""
    
    Write-ColorOutput "1. WiX Toolset (Professional MSI Installers)" "Yellow"
    Write-Host "   • Download: https://wixtoolset.org/releases/"
    Write-Host "   • Free and open-source"
    Write-Host "   • Creates professional MSI packages"
    Write-Host "   • Best for: Enterprise distribution"
    Write-Host ""
    
    Write-ColorOutput "2. Inno Setup (Recommended for Beginners)" "Yellow"
    Write-Host "   • Download: https://jrsoftware.org/isinfo.php"
    Write-Host "   • Free and user-friendly"
    Write-Host "   • Visual script editor included"
    Write-Host "   • Best for: Most users, easy to use"
    Write-Host ""
    
    Write-ColorOutput "3. NSIS (Lightweight Installers)" "Yellow"
    Write-Host "   • Download: https://nsis.sourceforge.io/"
    Write-Host "   • Creates compact .exe installers"
    Write-Host "   • Very small installer size"
    Write-Host "   • Best for: Minimal installations"
    Write-Host ""
    
    Write-ColorOutput "4. cx_Freeze (Python-based MSI)" "Yellow"
    Write-Host "   • Install: pip install cx_Freeze"
    Write-Host "   • No additional tools needed"
    Write-Host "   • Creates MSI packages directly"
    Write-Host "   • Best for: Python developers"
    Write-Host ""
    
    Write-ColorOutput "💡 RECOMMENDATION:" "Green"
    Write-Host "Start with Inno Setup - it's the easiest to use and most popular!"
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

function Install-PythonTools {
    Write-ColorOutput "📦 Installing Python packages for installer creation..." "Blue"
    
    $packages = @("cx_Freeze")
    
    foreach ($package in $packages) {
        try {
            Write-Host "Installing $package..."
            python -m pip install $package --upgrade
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput "✅ $package installed successfully" "Green"
            } else {
                Write-ColorOutput "❌ Failed to install $package" "Red"
                return $false
            }
        }
        catch {
            Write-ColorOutput "❌ Error installing $package : $_" "Red"
            return $false
        }
    }
    
    Write-ColorOutput "✅ All Python packages installed successfully!" "Green"
    return $true
}

function Invoke-InstallerCreation {
    param([string]$Type)
    
    Write-ColorOutput "🔨 Creating $Type installer script(s)..." "Blue"
    
    $arguments = @("create_installer.py", "--type", $Type)
    
    try {
        $process = Start-Process -FilePath "python" -ArgumentList $arguments -Wait -NoNewWindow -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-ColorOutput "✅ Installer script(s) created successfully!" "Green"
            return $true
        } else {
            Write-ColorOutput "❌ Installer creation failed with exit code: $($process.ExitCode)" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Error running installer creation script: $_" "Red"
        return $false
    }
}

function Show-InstallationSummary {
    Write-ColorOutput "`n🎉 INSTALLER CREATION SUMMARY" "Cyan"
    Write-ColorOutput "=============================" "Cyan"
    
    $installerPath = Join-Path $PSScriptRoot "installer"
    
    if (Test-Path $installerPath) {
        Write-ColorOutput "📁 Installer scripts created in: $installerPath" "Blue"
        
        $subDirs = Get-ChildItem $installerPath -Directory -ErrorAction SilentlyContinue
        foreach ($dir in $subDirs) {
            Write-ColorOutput "  📂 $($dir.Name)/" "Green"
            $files = Get-ChildItem $dir.FullName -File | Select-Object -First 3
            foreach ($file in $files) {
                Write-Host "    📄 $($file.Name)"
            }
        }
        
        Write-Host ""
        Write-ColorOutput "🚀 Next Steps:" "Yellow"
        Write-Host "1. Choose your preferred installer type"
        Write-Host "2. Install the required tool (see -ShowRequirements)"
        Write-Host "3. Build your installer using the generated scripts"
        Write-Host "4. Test the installer on a clean Windows machine"
        
    } else {
        Write-ColorOutput "❌ No installer directory found!" "Red"
    }
}

# Main script execution
function Main {
    if ($Help) {
        Show-Help
        return
    }
    
    if ($ShowRequirements) {
        Show-Requirements
        return
    }
    
    Write-ColorOutput "🚀 Timer Application Installer Creator" "Cyan"
    Write-ColorOutput "======================================" "Cyan"
    Write-Host ""
    
    # Check Python installation
    if (-not (Test-PythonInstallation)) {
        exit 1
    }
    
    # Install Python tools if requested
    if ($InstallTools) {
        if (-not (Install-PythonTools)) {
            Write-ColorOutput "`n❌ Failed to install required tools!" "Red"
            exit 1
        }
        Write-Host ""
    }
    
    # Create installer scripts
    if (Invoke-InstallerCreation $InstallerType) {
        Show-InstallationSummary
        Write-ColorOutput "`n🎊 Installer creation completed successfully!" "Green"
    } else {
        Write-ColorOutput "`n💥 Installer creation failed!" "Red"
        exit 1
    }
}

# Run the main function
Main