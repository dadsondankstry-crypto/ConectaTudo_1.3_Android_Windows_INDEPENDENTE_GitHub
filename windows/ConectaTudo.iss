#define AppName "ConectaTudo 1.3"
#define AppVersion "1.3"
#define AppExe "ConectaTudo-Windows-1.3.exe"
[Setup]
AppId={{B693E182-1943-4FBD-9C4E-47A72043F13D}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=Projeto ConectaTudo
DefaultDirName={localappdata}\Programs\ConectaTudo-1.3
DefaultGroupName=ConectaTudo 1.3
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=..\dist
OutputBaseFilename=ConectaTudo-Setup-1.3
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#AppExe}
[Files]
Source: "..\dist\{#AppExe}"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{autoprograms}\ConectaTudo 1.3"; Filename: "{app}\{#AppExe}"
Name: "{autodesktop}\ConectaTudo 1.3"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon
[Tasks]
Name: desktopicon; Description: "Criar atalho na área de trabalho"; Flags: unchecked
[Run]
Filename: "{app}\{#AppExe}"; Description: "Abrir ConectaTudo"; Flags: nowait postinstall skipifsilent
