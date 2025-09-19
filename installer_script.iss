[Setup]
AppName=Bluetooth Multi-Device Music Player
AppVersion=1.0
AppPublisher=Your Name
AppPublisherURL=https://github.com/yourusername/bluetooth-music-player
AppSupportURL=https://github.com/yourusername/bluetooth-music-player
AppUpdatesURL=https://github.com/yourusername/bluetooth-music-player
DefaultDirName={autopf}\BluetoothMusicPlayer
DefaultGroupName=Bluetooth Music Player
AllowNoIcons=yes
LicenseFile=
InfoBeforeFile=README.md
OutputDir=installer
OutputBaseFilename=BluetoothMusicPlayerSetup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
; Main executable files
Source: "dist\BluetoothMusicPlayer.exe"; DestDir: "{app}"; DestName: "BluetoothMusicPlayer.exe"; Flags: ignoreversion; Check: FileExists('dist\BluetoothMusicPlayer.exe')
Source: "dist\BluetoothMusicDemo.exe"; DestDir: "{app}"; DestName: "BluetoothMusicDemo.exe"; Flags: ignoreversion; Check: FileExists('dist\BluetoothMusicDemo.exe')

; Documentation files
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "SETUP_GUIDE.md"; DestDir: "{app}"; Flags: ignoreversion  
Source: "PROJECT_SUMMARY.md"; DestDir: "{app}"; Flags: ignoreversion

; Source files (optional)
Source: "*.py"; DestDir: "{app}\source"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}\source"; Flags: ignoreversion

[Icons]
; Create program menu icons
Name: "{group}\Bluetooth Music Player"; Filename: "{app}\BluetoothMusicPlayer.exe"; Check: FileExists(ExpandConstant('{app}\BluetoothMusicPlayer.exe'))
Name: "{group}\Bluetooth Music Player (Demo)"; Filename: "{app}\BluetoothMusicDemo.exe"; Check: FileExists(ExpandConstant('{app}\BluetoothMusicDemo.exe'))
Name: "{group}\User Guide"; Filename: "{app}\README.md"
Name: "{group}\Setup Guide"; Filename: "{app}\SETUP_GUIDE.md"
Name: "{group}\{cm:UninstallProgram,Bluetooth Music Player}"; Filename: "{uninstallexe}"

; Desktop icons (optional)
Name: "{autodesktop}\Bluetooth Music Player"; Filename: "{app}\BluetoothMusicPlayer.exe"; Tasks: desktopicon; Check: FileExists(ExpandConstant('{app}\BluetoothMusicPlayer.exe'))
Name: "{autodesktop}\Bluetooth Music Player (Demo)"; Filename: "{app}\BluetoothMusicDemo.exe"; Tasks: desktopicon; Check: FileExists(ExpandConstant('{app}\BluetoothMusicDemo.exe'))

; Quick Launch icons (optional)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Bluetooth Music Player"; Filename: "{app}\BluetoothMusicPlayer.exe"; Tasks: quicklaunchicon; Check: FileExists(ExpandConstant('{app}\BluetoothMusicPlayer.exe'))

[Run]
; Option to run the program after installation
Filename: "{app}\BluetoothMusicDemo.exe"; Description: "{cm:LaunchProgram,Bluetooth Music Player (Demo)}"; Flags: nowait postinstall skipifsilent; Check: FileExists(ExpandConstant('{app}\BluetoothMusicDemo.exe'))
Filename: "{app}\BluetoothMusicPlayer.exe"; Description: "{cm:LaunchProgram,Bluetooth Music Player}"; Flags: nowait postinstall skipifsilent; Check: FileExists(ExpandConstant('{app}\BluetoothMusicPlayer.exe'))

[Code]
function FileExists(FileName: string): Boolean;
begin
  Result := FileExists(FileName);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Post-installation tasks
    if FileExists(ExpandConstant('{app}\BluetoothMusicDemo.exe')) then
      MsgBox('Demo version installed successfully. This version simulates Bluetooth functionality and works on any computer.', mbInformation, MB_OK);
    
    if FileExists(ExpandConstant('{app}\BluetoothMusicPlayer.exe')) then
      MsgBox('Full version installed. This requires compatible Bluetooth hardware and may need additional setup.', mbInformation, MB_OK);
  end;
end;