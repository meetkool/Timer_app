# Timer Application - Build Instructions

This document explains how to build the Timer Application into a standalone executable file.

## 🚀 Quick Start

### Windows Users (Easiest)

1. Double-click `build.bat` and follow the menu options
2. Or run in PowerShell: `.\build.ps1`
3. Your executable will be in the `dist` folder

### All Platforms

```bash
python build_exe.py --type release
```

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

The build script will automatically install required dependencies:
- PyInstaller (for creating executables)
- pygame (for audio functionality)
- Pillow (for image processing)
- mutagen (for audio metadata)

## 🛠️ Build Options

### Build Types

| Type | Description | Output | Console |
|------|-------------|--------|---------|
| `release` | Production build | Single .exe file | Hidden |
| `debug` | Development build | Folder with files | Visible |
| `all` | Both builds | Both outputs | Mixed |

### 1. Using Python Script (Cross-platform)

```bash
# Release build (recommended for distribution)
python build_exe.py --type release

# Debug build (for troubleshooting)
python build_exe.py --type debug

# Build both versions
python build_exe.py --type all

# Clean build directories
python build_exe.py --clean-only
```

### 2. Using Batch File (Windows)

```cmd
# Double-click build.bat or run:
build.bat
```

Interactive menu with options:
1. Release Build (Single EXE, No Console)
2. Debug Build (With Console, Separate Files)
3. Both Builds
4. Clean Build Directories Only
5. Install Dependencies Only

### 3. Using PowerShell (Windows/Cross-platform)

```powershell
# Release build
.\build.ps1 -BuildType release

# Debug build
.\build.ps1 -BuildType debug

# All builds
.\build.ps1 -BuildType all

# Clean only
.\build.ps1 -BuildType clean

# Install dependencies only
.\build.ps1 -BuildType deps

# Show help
.\build.ps1 -Help
```

## 📁 Output Structure

After building, you'll find your executables in the `dist` folder:

```
dist/
├── TimerApp_v1.0.0.exe          # Release build (single file)
└── TimerApp_debug_v1.0.0/       # Debug build (folder)
    ├── TimerApp_debug_v1.0.0.exe
    ├── _internal/               # Dependencies
    └── ...
```

## 🔧 What Gets Included

The build process automatically includes:

### Application Files
- All Python modules from `timer_app/` package
- Main application entry point (`main.py`)
- Configuration files (`media_player_settings.json`)
- Resource files (`icon.ico`, `links.txt`)

### Python Dependencies
- tkinter (GUI framework)
- pygame (audio system)
- Pillow (image processing)
- mutagen (audio metadata)
- All timer_app submodules

### Directories (if they exist)
- `sessions/` - Saved timer sessions
- `storage/` - Application data storage
- `models/` - Data models
- `services/` - Service layers

## 🐛 Troubleshooting

### Common Issues

1. **"Python not found"**
   - Install Python 3.8+ from python.org
   - Make sure Python is added to your PATH

2. **"Module not found" errors**
   - Run: `pip install -r requirements.txt`
   - Or use the dependency installation options in the build scripts

3. **Large executable size**
   - This is normal for Python applications with GUI and audio support
   - Release builds are typically 50-100MB due to included libraries

4. **Executable won't start**
   - Try the debug build to see error messages
   - Check that all required DLLs are available
   - Run from command line to see any error output

5. **Missing files at runtime**
   - Ensure all resource files are in the same directory as the .exe
   - Check that the `sessions/` folder exists for saving data

### Debug Build Benefits

Use debug builds when:
- Testing the application
- Troubleshooting issues
- Seeing console output and error messages
- Faster startup (files aren't compressed)

### Getting Help

If you encounter issues:

1. Try the debug build first to see error messages
2. Check that all dependencies are installed
3. Ensure you're using Python 3.8+
4. Verify that the `timer_app` package structure is intact

## 📦 Distribution

### For End Users (Release Build)
- Distribute the single `.exe` file from `dist/`
- Include the `sessions/` folder if you want to preserve saved sessions
- The executable is self-contained and doesn't require Python installation

### For Developers (Debug Build)
- Distribute the entire folder from `dist/`
- Include source code for modifications
- Useful for troubleshooting and development

## 🔄 Updating Builds

When you make changes to the application:

1. Clean previous builds: `python build_exe.py --clean-only`
2. Rebuild: `python build_exe.py --type release`
3. Test the new executable thoroughly

## ⚙️ Advanced Configuration

You can modify `build_exe.py` to:
- Change the application name and version
- Add/remove included files
- Modify PyInstaller settings
- Add custom build hooks
- Change icon or other resources

### Key Configuration Variables

```python
APP_NAME = "TimerApp"           # Application name
VERSION = "1.0.0"               # Version number
ICON_FILE = "icon.ico"          # Application icon
MAIN_SCRIPT = "main.py"         # Entry point script
```

## 📈 Build Performance

Typical build times:
- Release build: 30-60 seconds
- Debug build: 15-30 seconds
- Clean build: 45-90 seconds

Build output sizes:
- Release build: ~50-80 MB (single file)
- Debug build: ~40-60 MB (distributed files)

---

**Happy Building! 🎉**

For more information about the Timer Application itself, see the main README.md file.