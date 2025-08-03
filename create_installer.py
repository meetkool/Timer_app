#!/usr/bin/env python3
"""
MSI Installer Creator for Timer Application
Creates professional Windows installers using multiple methods.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json
import uuid

# Configuration
APP_NAME = "Timer Application"
APP_VERSION = "1.0.0"
MANUFACTURER = "Timer App Developer"
APP_DESCRIPTION = "Professional Timer Application for Problem Solving"
EXECUTABLE_NAME = "TimerApp_v1.0.0.exe"
APP_ID = str(uuid.uuid4())  # Generate unique app ID

class InstallerCreator:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.installer_dir = self.project_root / "installer"
        
    def check_executable(self):
        """Check if the executable exists"""
        exe_path = self.dist_dir / EXECUTABLE_NAME
        if not exe_path.exists():
            # Try alternative names
            test_exe = self.dist_dir / "TimerApp_Test.exe"
            if test_exe.exists():
                print(f"✅ Found test executable: {test_exe}")
                return test_exe
            else:
                print(f"❌ Executable not found. Please build the app first:")
                print(f"   Expected: {exe_path}")
                print(f"   Run: python build_exe.py --type release")
                return None
        return exe_path
    
    def create_wix_installer(self, exe_path):
        """Create MSI installer using WiX Toolset"""
        print("🔨 Creating WiX MSI installer...")
        
        # Create installer directory
        wix_dir = self.installer_dir / "wix"
        wix_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate WiX source file
        wix_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="{APP_ID}" 
           Name="{APP_NAME}" 
           Language="1033" 
           Version="{APP_VERSION}" 
           Manufacturer="{MANUFACTURER}" 
           UpgradeCode="{str(uuid.uuid4())}">
    
    <Package InstallerVersion="200" 
             Compressed="yes" 
             InstallScope="perMachine" 
             Description="{APP_DESCRIPTION}"
             Comments="Timer Application Installer"
             Manufacturer="{MANUFACTURER}" />
    
    <MajorUpgrade DowngradeErrorMessage="A newer version is already installed." />
    <MediaTemplate EmbedCab="yes" />
    
    <!-- Application Icon -->
    <Icon Id="AppIcon" SourceFile="{self.project_root / 'icon.ico'}" />
    <Property Id="ARPPRODUCTICON" Value="AppIcon" />
    
    <!-- Installation Directory -->
    <Feature Id="ProductFeature" Title="{APP_NAME}" Level="1">
      <ComponentGroupRef Id="ProductComponents" />
    </Feature>
    
    <!-- Directory Structure -->
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="{APP_NAME}">
          <!-- Main executable -->
          <Component Id="MainExecutable" Guid="{str(uuid.uuid4())}">
            <File Id="TimerAppExe" 
                  Source="{exe_path}" 
                  KeyPath="yes" 
                  Checksum="yes">
              <Shortcut Id="StartMenuShortcut"
                        Directory="ProgramMenuFolder"
                        Name="{APP_NAME}"
                        Description="{APP_DESCRIPTION}"
                        Icon="AppIcon"
                        WorkingDirectory="INSTALLFOLDER" />
              <Shortcut Id="DesktopShortcut"
                        Directory="DesktopFolder"
                        Name="{APP_NAME}"
                        Description="{APP_DESCRIPTION}"
                        Icon="AppIcon"
                        WorkingDirectory="INSTALLFOLDER" />
            </File>
          </Component>
          
          <!-- Sessions Directory -->
          <Directory Id="SessionsDir" Name="sessions">
            <Component Id="SessionsDirectory" Guid="{str(uuid.uuid4())}">
              <CreateFolder />
            </Component>
          </Directory>
          
          <!-- Storage Directory -->
          <Directory Id="StorageDir" Name="storage">
            <Component Id="StorageDirectory" Guid="{str(uuid.uuid4())}">
              <CreateFolder />
            </Component>
          </Directory>
        </Directory>
      </Directory>
      
      <!-- System Directories -->
      <Directory Id="ProgramMenuFolder" />
      <Directory Id="DesktopFolder" />
    </Directory>
    
    <!-- Component Group -->
    <ComponentGroup Id="ProductComponents">
      <ComponentRef Id="MainExecutable" />
      <ComponentRef Id="SessionsDirectory" />
      <ComponentRef Id="StorageDirectory" />
    </ComponentGroup>
    
    <!-- UI -->
    <UIRef Id="WixUI_InstallDir" />
    <Property Id="WIXUI_INSTALLDIR" Value="INSTALLFOLDER" />
    
    <!-- License Agreement (optional) -->
    <WixVariable Id="WixUILicenseRtf" Value="license.rtf" />
    
  </Product>
</Wix>'''
        
        # Write WiX source file
        wxs_file = wix_dir / f"{APP_NAME.replace(' ', '')}.wxs"
        with open(wxs_file, 'w', encoding='utf-8') as f:
            f.write(wix_content)
        
        # Create simple license file
        license_file = wix_dir / "license.rtf"
        license_content = r'''{{\rtf1\ansi\deff0 {{\fonttbl {{\f0 Times New Roman;}}}}
\f0\fs24 Timer Application License Agreement\par
\par
This software is provided "as is" without warranty of any kind.\par
\par
You may use this software for personal and commercial purposes.\par
}}'''
        
        with open(license_file, 'w', encoding='utf-8') as f:
            f.write(license_content)
        
        print(f"✅ WiX source files created in: {wix_dir}")
        print(f"📝 To build MSI installer:")
        print(f"   1. Install WiX Toolset from: https://wixtoolset.org/releases/")
        print(f"   2. Run: candle.exe {wxs_file}")
        print(f"   3. Run: light.exe -ext WixUIExtension {wxs_file.with_suffix('.wixobj')}")
        
        return wxs_file
    
    def create_inno_setup_installer(self, exe_path):
        """Create installer using Inno Setup"""
        print("🔨 Creating Inno Setup installer...")
        
        # Create installer directory
        inno_dir = self.installer_dir / "inno"
        inno_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate Inno Setup script
        inno_content = f'''; Timer Application Inno Setup Script
; Generated automatically

#define MyAppName "{APP_NAME}"
#define MyAppVersion "{APP_VERSION}"
#define MyAppPublisher "{MANUFACTURER}"
#define MyAppURL "https://example.com"
#define MyAppExeName "{exe_path.name}"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{{{B7B4E4D1-A3F4-4C6E-8B7A-1234567890AB}}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes
LicenseFile={inno_dir / "license.txt"}
OutputDir={self.installer_dir / "output"}
OutputBaseFilename={APP_NAME.replace(' ', '_')}_Setup_v{APP_VERSION}
SetupIconFile={self.project_root / "icon.ico"}
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "{exe_path}"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{self.project_root / 'icon.ico'}"; DestDir: "{{app}}"; Flags: ignoreversion
; Create directories for app data
Source: "{self.project_root / 'sessions'}\\*"; DestDir: "{{app}}\\sessions"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists('{self.project_root / "sessions"}')
Source: "{self.project_root / 'storage'}\\*"; DestDir: "{{app}}\\storage"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists('{self.project_root / "storage"}')

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{group}}\\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{{app}}\\sessions"
Type: filesandordirs; Name: "{{app}}\\storage"

[Code]
function DirExists(Path: string): Boolean;
begin
  Result := DirExists(ExpandConstant(Path));
end;
'''
        
        # Write Inno Setup script
        iss_file = inno_dir / f"{APP_NAME.replace(' ', '')}_Setup.iss"
        with open(iss_file, 'w', encoding='utf-8') as f:
            f.write(inno_content)
        
        # Create license file
        license_file = inno_dir / "license.txt"
        license_content = f"""Timer Application License Agreement

This software is provided "as is" without warranty of any kind.

You may use this software for personal and commercial purposes.

Version: {APP_VERSION}
"""
        
        with open(license_file, 'w', encoding='utf-8') as f:
            f.write(license_content)
        
        print(f"✅ Inno Setup script created: {iss_file}")
        print(f"📝 To build installer:")
        print(f"   1. Install Inno Setup from: https://jrsoftware.org/isinfo.php")
        print(f"   2. Open {iss_file} in Inno Setup Compiler")
        print(f"   3. Click 'Build' or press F9")
        
        return iss_file
    
    def create_nsis_installer(self, exe_path):
        """Create installer using NSIS"""
        print("🔨 Creating NSIS installer...")
        
        # Create installer directory
        nsis_dir = self.installer_dir / "nsis"
        nsis_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate NSIS script
        nsis_content = f'''; Timer Application NSIS Installer Script
; Generated automatically

!define APPNAME "{APP_NAME}"
!define COMPANYNAME "{MANUFACTURER}"
!define DESCRIPTION "{APP_DESCRIPTION}"
!define VERSIONMAJOR "1"
!define VERSIONMINOR "0"
!define VERSIONBUILD "0"
!define HELPURL "https://example.com"
!define UPDATEURL "https://example.com"
!define ABOUTURL "https://example.com"
!define INSTALLSIZE 80000  ; Estimated size in KB

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\\${{APPNAME}}"
Name "${{APPNAME}}"
Icon "{self.project_root / 'icon.ico'}"
OutFile "{self.installer_dir / 'output'}/Timer_Application_Setup_v{APP_VERSION}.exe"

!include LogicLib.nsh
!include MUI2.nsh

; Modern UI Configuration
!define MUI_WELCOMEPAGE_TITLE "Welcome to ${{APPNAME}} Setup"
!define MUI_WELCOMEPAGE_TEXT "This wizard will guide you through the installation of ${{APPNAME}}.$\\r$\\n$\\r$\\nClick Next to continue."
!define MUI_ICON "{self.project_root / 'icon.ico'}"
!define MUI_UNICON "{self.project_root / 'icon.ico'}"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "{nsis_dir / 'license.txt'}"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Install"
    SetOutPath $INSTDIR
    
    ; Install main executable
    File "{exe_path}"
    File "{self.project_root / 'icon.ico'}"
    
    ; Create directories
    CreateDirectory "$INSTDIR\\sessions"
    CreateDirectory "$INSTDIR\\storage"
    
    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\\${{APPNAME}}"
    CreateShortCut "$SMPROGRAMS\\${{APPNAME}}\\${{APPNAME}}.lnk" "$INSTDIR\\{exe_path.name}" "" "$INSTDIR\\icon.ico"
    CreateShortCut "$SMPROGRAMS\\${{APPNAME}}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
    CreateShortCut "$DESKTOP\\${{APPNAME}}.lnk" "$INSTDIR\\{exe_path.name}" "" "$INSTDIR\\icon.ico"
    
    ; Write uninstaller
    WriteUninstaller "$INSTDIR\\uninstall.exe"
    
    ; Registry entries for Add/Remove Programs
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "DisplayName" "${{APPNAME}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "UninstallString" "$\\"$INSTDIR\\uninstall.exe$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "QuietUninstallString" "$\\"$INSTDIR\\uninstall.exe$\\" /S"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "InstallLocation" "$\\"$INSTDIR$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "DisplayIcon" "$\\"$INSTDIR\\icon.ico$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "Publisher" "${{COMPANYNAME}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "HelpLink" "${{HELPURL}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "URLUpdateInfo" "${{UPDATEURL}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "URLInfoAbout" "${{ABOUTURL}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "DisplayVersion" "${{VERSIONMAJOR}}.${{VERSIONMINOR}}.${{VERSIONBUILD}}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "VersionMajor" ${{VERSIONMAJOR}}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "VersionMinor" ${{VERSIONMINOR}}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "NoRepair" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "EstimatedSize" ${{INSTALLSIZE}}
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\{exe_path.name}"
    Delete "$INSTDIR\\icon.ico"
    Delete "$INSTDIR\\uninstall.exe"
    
    RMDir /r "$INSTDIR\\sessions"
    RMDir /r "$INSTDIR\\storage"
    RMDir "$INSTDIR"
    
    Delete "$SMPROGRAMS\\${{APPNAME}}\\${{APPNAME}}.lnk"
    Delete "$SMPROGRAMS\\${{APPNAME}}\\Uninstall.lnk"
    RMDir "$SMPROGRAMS\\${{APPNAME}}"
    Delete "$DESKTOP\\${{APPNAME}}.lnk"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}"
SectionEnd
'''
        
        # Write NSIS script
        nsi_file = nsis_dir / f"{APP_NAME.replace(' ', '')}_Setup.nsi"
        with open(nsi_file, 'w', encoding='utf-8') as f:
            f.write(nsis_content)
        
        # Create license file
        license_file = nsis_dir / "license.txt"
        license_content = f"""Timer Application License Agreement

This software is provided "as is" without warranty of any kind.

You may use this software for personal and commercial purposes.

Version: {APP_VERSION}
"""
        
        with open(license_file, 'w', encoding='utf-8') as f:
            f.write(license_content)
        
        print(f"✅ NSIS script created: {nsi_file}")
        print(f"📝 To build installer:")
        print(f"   1. Install NSIS from: https://nsis.sourceforge.io/")
        print(f"   2. Right-click {nsi_file} and select 'Compile NSIS Script'")
        print(f"   3. Or run: makensis {nsi_file}")
        
        return nsi_file
    
    def create_cx_freeze_msi(self):
        """Create MSI installer using cx_Freeze"""
        print("🔨 Creating cx_Freeze MSI installer...")
        
        # Create setup script for cx_Freeze
        setup_content = f'''import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some modules need help.
build_options = {{
    'packages': [
        'timer_app',
        'pygame',
        'PIL',
        'mutagen',
        'tkinter'
    ],
    'excludes': ['matplotlib', 'numpy', 'pandas', 'scipy'],
    'include_files': [
        ('icon.ico', 'icon.ico'),
        ('sessions', 'sessions'),
        ('storage', 'storage'),
    ]
}}

# MSI specific options
bdist_msi_options = {{
    'upgrade_code': '{{{APP_ID}}}',
    'add_to_path': False,
    'initial_target_dir': '[ProgramFilesFolder]\\{APP_NAME}',
    'install_icon': 'icon.ico'
}}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable(
        'main.py',
        base=base,
        target_name='{APP_NAME.replace(" ", "_")}.exe',
        icon='icon.ico',
        shortcut_name='{APP_NAME}',
        shortcut_dir='DesktopFolder'
    )
]

setup(
    name='{APP_NAME}',
    version='{APP_VERSION}',
    description='{APP_DESCRIPTION}',
    author='{MANUFACTURER}',
    options={{
        'build_exe': build_options,
        'bdist_msi': bdist_msi_options
    }},
    executables=executables
)
'''
        
        # Write setup script
        setup_file = self.project_root / "setup_msi.py"
        with open(setup_file, 'w', encoding='utf-8') as f:
            f.write(setup_content)
        
        print(f"✅ cx_Freeze setup script created: {setup_file}")
        print(f"📝 To build MSI installer:")
        print(f"   1. Install cx_Freeze: pip install cx_Freeze")
        print(f"   2. Run: python {setup_file} bdist_msi")
        
        return setup_file
    
    def create_all_installers(self):
        """Create all types of installers"""
        print(f"🚀 Creating installers for {APP_NAME} v{APP_VERSION}")
        print("="*60)
        
        # Check if executable exists
        exe_path = self.check_executable()
        if not exe_path:
            return False
        
        # Create output directory
        output_dir = self.installer_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📦 Found executable: {exe_path}")
        print(f"📁 Installer files will be created in: {self.installer_dir}")
        print()
        
        # Create different types of installers
        try:
            self.create_wix_installer(exe_path)
            print()
            self.create_inno_setup_installer(exe_path)
            print()
            self.create_nsis_installer(exe_path)
            print()
            self.create_cx_freeze_msi()
            print()
        except Exception as e:
            print(f"❌ Error creating installers: {e}")
            return False
        
        print("="*60)
        print("🎉 INSTALLER CREATION SUMMARY")
        print("="*60)
        print(f"📁 All installer scripts created in: {self.installer_dir}")
        print()
        print("📝 Next steps:")
        print("1. Choose your preferred installer type:")
        print("   • WiX Toolset (MSI) - Most professional, requires WiX")
        print("   • Inno Setup - Easy to use, popular choice")
        print("   • NSIS - Lightweight, creates .exe installers")
        print("   • cx_Freeze - Python-based MSI creation")
        print()
        print("2. Install the required tool and build your installer")
        print("3. Test the installer on a clean Windows machine")
        print()
        print("💡 Recommended: Start with Inno Setup for ease of use!")
        
        return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description=f"Create installers for {APP_NAME}")
    parser.add_argument(
        "--type", 
        choices=["wix", "inno", "nsis", "cx_freeze", "all"], 
        default="all",
        help="Installer type to create (default: all)"
    )
    
    args = parser.parse_args()
    
    creator = InstallerCreator()
    
    if args.type == "all":
        success = creator.create_all_installers()
    else:
        exe_path = creator.check_executable()
        if not exe_path:
            sys.exit(1)
        
        if args.type == "wix":
            creator.create_wix_installer(exe_path)
        elif args.type == "inno":
            creator.create_inno_setup_installer(exe_path)
        elif args.type == "nsis":
            creator.create_nsis_installer(exe_path)
        elif args.type == "cx_freeze":
            creator.create_cx_freeze_msi()
        
        success = True
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()