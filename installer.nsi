
; Bluetooth Music Player Installer
; Created with NSIS

!define APP_NAME "Bluetooth Music Player"
!define APP_VERSION "1.0"
!define APP_PUBLISHER "Your Name"
!define APP_URL "https://github.com/yourusername/bluetooth-music-player"

; Main Install settings
Name "${APP_NAME}"
InstallDir "$PROGRAMFILES\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" ""
OutFile "BluetoothMusicPlayerInstaller.exe"

; Interface Settings
!include "MUI2.nsh"
!define MUI_ABORTWARNING
!define MUI_ICON "app.ico"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installation
Section "Main Application" SecMain
    SetOutPath "$INSTDIR"
    
    ; Copy executable files
    File "dist\BluetoothMusicConsole.exe"
    File "dist\BluetoothMusicPlayer.exe"
    
    ; Copy documentation
    File "README.md"
    File "portable\README.txt"
    File "FIX_GUIDE.md"
    
    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\BluetoothMusicConsole.exe"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME} (Advanced).lnk" "$INSTDIR\BluetoothMusicPlayer.exe"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
    
    ; Create desktop shortcut
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\BluetoothMusicConsole.exe"
    
    ; Registry
    WriteRegStr HKLM "Software\${APP_NAME}" "" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "URLInfoAbout" "${APP_URL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    
    ; Uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

; Uninstallation
Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\BluetoothMusicConsole.exe"
    Delete "$INSTDIR\BluetoothMusicPlayer.exe"
    Delete "$INSTDIR\README.md"
    Delete "$INSTDIR\README.txt"
    Delete "$INSTDIR\FIX_GUIDE.md"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Remove shortcuts
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME} (Advanced).lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    
    ; Remove registry keys
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    DeleteRegKey HKLM "Software\${APP_NAME}"
    
    ; Remove directory
    RMDir "$INSTDIR"
SectionEnd
