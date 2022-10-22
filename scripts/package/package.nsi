; compress
SetCompressor /SOLID LZMA
SetCompress force

; base
!define TEMP_NAME "WxReader"
!define PRODUCT_NAME "WxReader"
!define PRODUCT_VERSION "2.0.0.0"
!define PRODUCT_COMPANY "DoooReyn"

VIProductVersion "${PRODUCT_VERSION}"
VIAddVersionKey FileDescription "${PRODUCT_NAME} Installer"
VIAddVersionKey FileVersion "${PRODUCT_VERSION}"
VIAddVersionKey ProductName "${PRODUCT_NAME} Installer" 
VIAddVersionKey ProductVersion "${PRODUCT_VERSION}"
VIAddVersionKey CompanyName "${PRODUCT_COMPANY}"
VIAddVersionKey LegalCopyright "Copyright (C) 2020-2022 ${PRODUCT_COMPANY}"

;使用现代外观
;Include Modern UI
!include "MUI2.nsh"


; 安装配置
Unicode True
RequestExecutionLevel admin
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "${PRODUCT_NAME}_v${PRODUCT_VERSION}_Installer.exe"
InstallDir "$PROGRAMFILES64\${PRODUCT_NAME}"

!define MUI_ABORTWARNING
!define MUI_LANGDLL_ALLLANGUAGES


; Pages
!insertmacro MUI_PAGE_WELCOME
; !insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\${PRODUCT_NAME}.exe"
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "SimpChinese"
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_RESERVEFILE_LANGDLL


Section "Installer"
  SetOutPath $INSTDIR
  File /r ".\dist\${PRODUCT_NAME}\*.*"
  SetShellVarContext all
  CreateShortCut "$DESKTOP\${PRODUCT_NAME}.lnk" "$INSTDIR\${PRODUCT_NAME}.exe"
  WriteUninstaller "Uninstaller.exe"
SectionEnd

Section "Uninstall"
  SetShellVarContext all
  RMDir /r "$TEMP\${PRODUCT_NAME}"
  RMDir /r "$TEMP\${TEMP_NAME}"
  Delete "$DESKTOP\${PRODUCT_NAME}.lnk"
  Delete "$INSTDIR\Uninstaller.exe"
  RMDir /r $INSTDIR
SectionEnd