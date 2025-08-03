#!/usr/bin/env python3
"""
Build script for Timer Application
Creates an executable using PyInstaller with all necessary dependencies and resources.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Configuration
APP_NAME = "TimerApp"
MAIN_SCRIPT = "main.py"
ICON_FILE = "icon.ico"
VERSION = "1.0.0"

# Build configurations
BUILD_CONFIGS = {
    "release": {
        "console": False,
        "debug": False,
        "onefile": True,
        "name": f"{APP_NAME}_v{VERSION}",
    },
    "debug": {
        "console": True,
        "debug": True,
        "onefile": False,
        "name": f"{APP_NAME}_debug_v{VERSION}",
    }
}

class BuildScript:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.spec_dir = self.project_root / "specs"
        
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        required_packages = ["pyinstaller", "pygame", "PIL", "mutagen"]
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"  ✅ {package} is installed")
            except ImportError:
                missing_packages.append(package)
                print(f"  ❌ {package} is missing")
        
        if missing_packages:
            print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    *missing_packages, "--upgrade"
                ])
                print("✅ Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install dependencies: {e}")
                return False
        
        return True
    
    def create_spec_file(self, config_name, config):
        """Create PyInstaller spec file for the given configuration"""
        print(f"📝 Creating spec file for {config_name} build...")
        
        # Create specs directory if it doesn't exist
        self.spec_dir.mkdir(exist_ok=True)
        
        # Use absolute paths directly
        main_script_path = str(self.project_root / MAIN_SCRIPT)
        project_root_path = str(self.project_root)
        icon_path = str(self.project_root / ICON_FILE)
        
        # Build the EXE section based on configuration
        if config['onefile']:
            exe_section = f"""exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='{config["name"]}',
    debug={config['debug']},
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={config['console']},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[r'{icon_path}'],
)"""
        else:
            exe_section = f"""exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='{config["name"]}',
    debug={config['debug']},
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={config['console']},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[r'{icon_path}'],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{config["name"]}',
)"""
        
        # Generate data files list with absolute paths
        data_files = []
        
        # Required files
        if (self.project_root / ICON_FILE).exists():
            data_files.append(f"(r'{str(self.project_root / ICON_FILE)}', '.')")
        
        # Optional files
        optional_files = ['media_player_settings.json', 'links.txt']
        for opt_file in optional_files:
            if (self.project_root / opt_file).exists():
                data_files.append(f"(r'{str(self.project_root / opt_file)}', '.')")
        
        data_files_str = ',\n        '.join(data_files) if data_files else ""
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
# Auto-generated spec file for {APP_NAME} {config_name} build

# Analysis configuration
a = Analysis(
    [r'{main_script_path}'],
    pathex=[r'{project_root_path}'],
    binaries=[],
    datas=[
        {data_files_str}
    ],
    hiddenimports=[
        'timer_app',
        'timer_app.factories',
        'timer_app.factories.app_factory',
        'timer_app.application',
        'timer_app.application.services',
        'timer_app.application.interfaces',
        'timer_app.domain',
        'timer_app.domain.models',
        'timer_app.infrastructure',
        'timer_app.infrastructure.storage',
        'timer_app.ui',
        'timer_app.ui.views',
        'timer_app.ui.widgets',
        'timer_app.ui.widgets.buttons',
        'timer_app.ui.widgets.close_button',
        'timer_app.ui.widgets.display_widgets',
        'timer_app.ui.widgets.logs_panel',
        'timer_app.ui.widgets.loop_controls',
        'timer_app.ui.widgets.media_player_button',
        'timer_app.ui.widgets.menu_button',
        'timer_app.ui.widgets.notes_window',
        'timer_app.ui.window_manager',
        'timer_app.audio',
        'timer_app.audio.factory',
        'timer_app.audio.interfaces',
        'timer_app.audio.loop_controller',
        'timer_app.audio.loop_manager',
        'timer_app.audio.monitor',
        'timer_app.audio.player',
        'timer_app.audio.playlist',
        'timer_app.audio.system',
        'pygame',
        'pygame.mixer',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'mutagen',
        'mutagen.id3',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.simpledialog',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'notebook',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data)

{exe_section}
'''
        
        spec_file = self.spec_dir / f"{config['name']}.spec"
        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        print(f"✅ Spec file created: {spec_file}")
        return spec_file
    
    def clean_build_dirs(self):
        """Clean previous build directories"""
        print("🧹 Cleaning previous build directories...")
        
        dirs_to_clean = [self.dist_dir, self.build_dir]
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"  🗑️  Removed {dir_path}")
        
        print("✅ Build directories cleaned")
    
    def build_executable(self, config_name, config):
        """Build the executable using PyInstaller"""
        print(f"🔨 Building {config_name} executable...")
        
        # Create spec file
        spec_file = self.create_spec_file(config_name, config)
        
        # Build command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            str(spec_file),
            "--clean",
            "--noconfirm",
        ]
        
        # Note: Don't add --onefile here as it's already configured in the .spec file
        
        print(f"Running: {' '.join(cmd)}")
        
        try:
            # Run PyInstaller
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ Build completed successfully!")
            
            # Show build output if there are warnings
            if result.stdout:
                print("Build output:")
                print(result.stdout)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed with error: {e}")
            if e.stdout:
                print("STDOUT:", e.stdout)
            if e.stderr:
                print("STDERR:", e.stderr)
            return False
    
    def copy_resources(self):
        """Copy additional resources to dist directory"""
        print("📁 Copying additional resources...")
        
        resources_to_copy = [
            "sessions",
            "storage", 
            "models",
            "services",
        ]
        
        for resource in resources_to_copy:
            src_path = self.project_root / resource
            if src_path.exists():
                for dist_subdir in self.dist_dir.iterdir():
                    if dist_subdir.is_dir():
                        dst_path = dist_subdir / resource
                        if src_path.is_dir():
                            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                        else:
                            shutil.copy2(src_path, dst_path)
                        print(f"  📋 Copied {resource} to {dst_path}")
    
    def show_build_summary(self):
        """Show build summary and output locations"""
        print("\n" + "="*60)
        print("🎉 BUILD SUMMARY")
        print("="*60)
        
        if self.dist_dir.exists():
            print(f"📦 Output directory: {self.dist_dir}")
            
            for item in self.dist_dir.iterdir():
                if item.is_file() and item.suffix == '.exe':
                    size_mb = item.stat().st_size / (1024 * 1024)
                    print(f"  🚀 {item.name} ({size_mb:.1f} MB)")
                elif item.is_dir():
                    exe_files = list(item.glob("*.exe"))
                    if exe_files:
                        for exe_file in exe_files:
                            size_mb = exe_file.stat().st_size / (1024 * 1024)
                            print(f"  📁 {item.name}/{exe_file.name} ({size_mb:.1f} MB)")
            
            print(f"\n💡 You can find your executable(s) in: {self.dist_dir.resolve()}")
        else:
            print("❌ No output files found!")
    
    def run(self, build_types=None):
        """Run the complete build process"""
        print(f"🚀 Building {APP_NAME} v{VERSION}")
        print("="*60)
        
        # Check dependencies first
        if not self.check_dependencies():
            print("❌ Dependency check failed. Please install required packages manually.")
            return False
        
        # Clean previous builds
        self.clean_build_dirs()
        
        # Determine which builds to create
        if build_types is None:
            build_types = ["release"]
        
        success_count = 0
        
        # Build each configuration
        for build_type in build_types:
            if build_type not in BUILD_CONFIGS:
                print(f"⚠️  Unknown build type: {build_type}")
                continue
                
            config = BUILD_CONFIGS[build_type]
            print(f"\n{'='*40}")
            print(f"Building {build_type.upper()} version")
            print(f"{'='*40}")
            
            if self.build_executable(build_type, config):
                success_count += 1
                print(f"✅ {build_type.capitalize()} build completed!")
            else:
                print(f"❌ {build_type.capitalize()} build failed!")
        
        # Copy additional resources
        if success_count > 0:
            self.copy_resources()
        
        # Show summary
        self.show_build_summary()
        
        return success_count > 0


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description=f"Build {APP_NAME} executable")
    parser.add_argument(
        "--type", 
        choices=list(BUILD_CONFIGS.keys()) + ["all"], 
        default="release",
        help="Build type (default: release)"
    )
    parser.add_argument(
        "--clean-only", 
        action="store_true",
        help="Only clean build directories"
    )
    
    args = parser.parse_args()
    
    builder = BuildScript()
    
    if args.clean_only:
        builder.clean_build_dirs()
        return
    
    # Determine build types
    if args.type == "all":
        build_types = list(BUILD_CONFIGS.keys())
    else:
        build_types = [args.type]
    
    # Run the build
    success = builder.run(build_types)
    
    if success:
        print(f"\n🎊 All builds completed successfully!")
        sys.exit(0)
    else:
        print(f"\n💥 Some builds failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()