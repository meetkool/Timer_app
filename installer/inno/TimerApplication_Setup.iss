; Timer Application Inno Setup Script
; Generated automatically

#define MyAppName "Timer Application"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Timer App Developer"
#define MyAppURL "https://example.com"
#define MyAppExeName "TimerApp_v1.0.0.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{B7B4E4D1-A3F4-4C6E-8B7A-1234567890AB}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=C:\Users\LENOVO\Desktop\cp50\timer\installer\inno\license.txt
OutputDir=C:\Users\LENOVO\Desktop\cp50\timer\installer\output
OutputBaseFilename=Timer_Application_Setup_v1.0.0
SetupIconFile=C:\Users\LENOVO\Desktop\cp50\timer\icon.ico
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "C:\Users\LENOVO\Desktop\cp50\timer\dist\TimerApp_v1.0.0.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\LENOVO\Desktop\cp50\timer\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
; Create directories for app data
Source: "C:\Users\LENOVO\Desktop\cp50\timer\sessions\*"; DestDir: "{app}\sessions"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists('C:\Users\LENOVO\Desktop\cp50\timer\sessions')
Source: "C:\Users\LENOVO\Desktop\cp50\timer\storage\*"; DestDir: "{app}\storage"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists('C:\Users\LENOVO\Desktop\cp50\timer\storage')

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\sessions"
Type: filesandordirs; Name: "{app}\storage"

[Code]
function DirExists(Path: string): Boolean;
begin
  Result := DirExists(ExpandConstant(Path));
end;
