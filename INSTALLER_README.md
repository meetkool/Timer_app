# Timer Application - MSI Installer Creation Guide

This guide explains how to create professional Windows installers (MSI, EXE) for your Timer Application.

## 🚀 Quick Start

### Easiest Method (Recommended)

1. **Create Installer Scripts:**
   ```cmd
   # Double-click create_installer.bat and select option [1]
   # Or run:
   python create_installer.py --type all
   ```

2. **Choose Your Tool:**
   - **Beginners:** Use Inno Setup (easiest)
   - **Professional:** Use WiX Toolset (MSI)
   - **Lightweight:** Use NSIS

3. **Build Your Installer:**
   - Install the chosen tool
   - Open the generated script
   - Build the installer

## 📋 Prerequisites

- Built executable (run `python build_exe.py --type release` first)
- Windows 10/11 (for testing)
- One of the installer creation tools (see options below)

## 🛠️ Installer Types

### 1. Inno Setup (Recommended for Most Users)

**Best for:** Beginners, most common use cases

```bash
# Create Inno Setup script
python create_installer.py --type inno

# Then:
# 1. Download Inno Setup: https://jrsoftware.org/isinfo.php
# 2. Open: installer/inno/TimerApplication_Setup.iss
# 3. Click "Build" or press F9
```

**Pros:**
- ✅ Very easy to use
- ✅ Visual script editor
- ✅ Great documentation
- ✅ Free and widely used
- ✅ Professional-looking installers

**Output:** `Timer_Application_Setup_v1.0.0.exe`

### 2. WiX Toolset (Professional MSI)

**Best for:** Enterprise environments, professional distribution

```bash
# Create WiX script
python create_installer.py --type wix

# Then:
# 1. Download WiX Toolset: https://wixtoolset.org/releases/
# 2. Run: candle.exe installer/wix/TimerApplication.wxs
# 3. Run: light.exe -ext WixUIExtension TimerApplication.wixobj
```

**Pros:**
- ✅ Creates true MSI packages
- ✅ Professional standard
- ✅ GPO deployment support
- ✅ Advanced customization
- ✅ Microsoft-recommended

**Cons:**
- ❌ Steeper learning curve
- ❌ Command-line based

**Output:** `TimerApplication.msi`

### 3. NSIS (Lightweight)

**Best for:** Minimal installations, small file size

```bash
# Create NSIS script
python create_installer.py --type nsis

# Then:
# 1. Download NSIS: https://nsis.sourceforge.io/
# 2. Right-click installer/nsis/TimerApplication_Setup.nsi
# 3. Select "Compile NSIS Script"
```

**Pros:**
- ✅ Very small installer size
- ✅ Fast installation
- ✅ Scriptable
- ✅ Free and lightweight

**Cons:**
- ❌ Less user-friendly editor
- ❌ Steeper learning curve

**Output:** `Timer_Application_Setup_v1.0.0.exe`

### 4. cx_Freeze (Python-based MSI)

**Best for:** Python developers, automated builds

```bash
# Create cx_Freeze setup
python create_installer.py --type cx_freeze

# Then:
# 1. Install: pip install cx_Freeze
# 2. Run: python setup_msi.py bdist_msi
```

**Pros:**
- ✅ No additional tools needed
- ✅ Pure Python solution
- ✅ Creates MSI files
- ✅ Good for CI/CD

**Cons:**
- ❌ Less customization
- ❌ Larger file sizes

**Output:** `dist/Timer Application-1.0.0-win-amd64.msi`

## 🎯 Step-by-Step Instructions

### Method 1: Using Batch File (Easiest)

1. **Double-click `create_installer.bat`**
2. **Select option [3] for Inno Setup**
3. **Download and install Inno Setup**
4. **Open the generated .iss file**
5. **Click Build (F9)**

### Method 2: Using PowerShell (Advanced)

```powershell
# Show requirements
.\create_installer.ps1 -ShowRequirements

# Create Inno Setup installer
.\create_installer.ps1 -InstallerType inno

# Install Python tools if needed
.\create_installer.ps1 -InstallTools
```

### Method 3: Using Python Script (Direct)

```bash
# Create all installer types
python create_installer.py --type all

# Create specific type
python create_installer.py --type inno
```

## 📁 Output Structure

After running the installer creation script:

```
installer/
├── wix/
│   ├── TimerApplication.wxs      # WiX source file
│   └── license.rtf               # License file
├── inno/
│   ├── TimerApplication_Setup.iss # Inno Setup script
│   └── license.txt               # License file
├── nsis/
│   ├── TimerApplication_Setup.nsi # NSIS script
│   └── license.txt               # License file
└── output/                       # Built installers go here
```

## 🔧 Customization Options

### Application Information

Edit `create_installer.py` to customize:

```python
APP_NAME = "Timer Application"
APP_VERSION = "1.0.0"
MANUFACTURER = "Your Company Name"
APP_DESCRIPTION = "Professional Timer Application"
```

### Features Included

All installers include:

- ✅ **Desktop shortcut**
- ✅ **Start menu entry**
- ✅ **Add/Remove Programs entry**
- ✅ **Uninstaller**
- ✅ **Application icon**
- ✅ **Sessions and storage directories**
- ✅ **License agreement**
- ✅ **Modern UI**

### Advanced Customization

**Inno Setup:**
- Edit `.iss` file for custom pages, scripts, registry entries
- Add custom icons, splash screens
- Include additional files or dependencies

**WiX Toolset:**
- Modify `.wxs` file for MSI properties
- Add custom actions, dialogs
- Configure Windows Installer features

**NSIS:**
- Edit `.nsi` file for custom install logic
- Add plugins for extended functionality
- Create custom UI themes

## 🧪 Testing Your Installer

### Before Distribution

1. **Test on Clean Machine:**
   - Use Windows VM or separate computer
   - Install and verify all features work
   - Test uninstallation

2. **Check Installation:**
   - Verify shortcuts are created
   - Test application launches correctly
   - Check sessions/storage directories exist
   - Verify uninstaller works

3. **Test Different Scenarios:**
   - Install as admin vs. regular user
   - Install to different directories
   - Upgrade over previous version

### Automated Testing

```bash
# Create test installer
python create_installer.py --type inno

# Build installer (manually with Inno Setup)

# Test installation
TimerApplication_Setup.exe /SILENT /DIR="C:\Test\TimerApp"

# Verify installation
dir "C:\Test\TimerApp"

# Test uninstall
"C:\Test\TimerApp\unins000.exe" /SILENT
```

## 🚀 Distribution

### For End Users

1. **Build Release Executable:**
   ```bash
   python build_exe.py --type release
   ```

2. **Create Installer:**
   ```bash
   python create_installer.py --type inno
   ```

3. **Build Installer:**
   - Open Inno Setup
   - Load generated `.iss` file
   - Build installer

4. **Distribute:**
   - Upload installer to your website
   - Include in software packages
   - Distribute via email or USB

### For Developers

Include in your development workflow:

```bash
# Complete build and package process
python build_exe.py --type release
python create_installer.py --type all

# Build all installer types
# Test installers
# Deploy to distribution channels
```

## 🔍 Troubleshooting

### Common Issues

1. **"Executable not found"**
   - Run `python build_exe.py --type release` first
   - Check `dist/` folder for .exe file

2. **"Access denied during install"**
   - Run installer as administrator
   - Check antivirus software
   - Ensure target directory is writable

3. **"Application won't start after install"**
   - Missing dependencies (usually handled automatically)
   - Check Windows event logs
   - Test on clean machine

4. **"Installer creation fails"**
   - Ensure all required files exist
   - Check file paths in installer script
   - Verify installer tool is properly installed

### Getting Help

1. **Check tool documentation:**
   - Inno Setup: https://jrsoftware.org/ishelp/
   - WiX Toolset: https://wixtoolset.org/docs/
   - NSIS: https://nsis.sourceforge.io/Docs/

2. **Common solutions:**
   - Rebuild executable first
   - Check file permissions
   - Run as administrator
   - Disable antivirus temporarily

## 📈 Best Practices

### Security

- **Code sign your installer** (requires certificate)
- **Test on multiple Windows versions**
- **Include virus scanner whitelist instructions**

### User Experience

- **Keep installer size reasonable** (under 100MB preferred)
- **Provide clear installation options**
- **Include helpful shortcuts and documentation**
- **Test uninstallation thoroughly**

### Professional Distribution

- **Use consistent branding** (icons, colors, text)
- **Include proper license agreements**
- **Provide installation instructions**
- **Create both MSI and EXE versions** for different use cases

---

## 🎉 Summary

You now have a complete system for creating professional Windows installers:

1. ✅ **Multiple installer types** (MSI, EXE)
2. ✅ **Easy-to-use scripts** (batch, PowerShell, Python)
3. ✅ **Professional features** (shortcuts, uninstaller, Add/Remove Programs)
4. ✅ **Customization options** for branding and features
5. ✅ **Testing guidelines** for quality assurance

**Recommended workflow:**
1. Build executable: `python build_exe.py --type release`
2. Create installer: `python create_installer.py --type inno`
3. Install Inno Setup and build installer
4. Test on clean machine
5. Distribute to users

**Happy packaging! 🎊**