
;This file is part of pyXorga.
;
; Copyright (C) 2015 C�drick FAURY
;
;pyXorga is free software; you can redistribute it and/or modify
;it under the terms of the GNU General Public License as published by
;the Free Software Foundation; either version 2 of the License, or
;(at your option) any later version.
;
;pyXorga is distributed in the hope that it will be useful,
;but WITHOUT ANY WARRANTY; without even the implied warranty of
;MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;GNU General Public License for more details.
;
;You should have received a copy of the GNU General Public License
;along with pyXorga; if not, write to the Free Software
;Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

[ISPP]
#define AppName "pyXorga"
#define AppVersion "2.1"
#define AppVersionInfo "2.1.0"
#define AppVersionBase "2"

#define AppURL "https://github.com/cedrick-f/pyXorga"

[Setup]
;Informations g�n�rales sur l'application
AppName={#AppName}
AppVerName={#AppName} {#AppVersion}
AppVersion={#AppVersion}
AppPublisher=C�drick FAURY
AppCopyright=Copyright (C) 2015 C�drick FAURY <fauryc@free.fr>
VersionInfoVersion = {#AppVersionInfo}

;R�pertoire de base contenant les fichiers
SourceDir=D:\Developpement\pyXorga

;Repertoire d'installation
DefaultDirName={pf}\pyXorga
DefaultGroupName=pyXorga
LicenseFile=LICENSE.txt

;Param�tres de compression
;lzma ou zip
Compression=lzma/max
SolidCompression=yes

;Par d�faut, pas besoin d'�tre administrateur pour installer
PrivilegesRequired=none

;Nom du fichier g�n�r� et r�pertoire de destination
OutputBaseFilename=pyXorga_{#AppVersion}_setup
OutputDir=releases

;Dans le panneau de configuration de Windows2000/NT/XP, c'est l'icone de pymecavideo.exe qui
;appara�t � gauche du nom du fichier pour la d�sinstallation
UninstallDisplayIcon={app}\images\pyXorga_logo_500x500.png

;Fen�tre en background
WindowResizable=false
WindowStartMaximized=true
WindowShowCaption=true
BackColorDirection=lefttoright


AlwaysUsePersonalGroup=no

[Languages]
Name: fr; MessagesFile: "compiler:Languages\French.isl"

[Messages]
BeveledLabel=pyXorga {#AppVersion} installation


[CustomMessages]
;
; French
;
fr.uninstall=D�sinstaller
fr.gpl_licence=Prendre connaissance du contrat de licence pour le logiciel
fr.fdl_licence=Prendre connaissance du contrat de licence pour la documentation associ�e
fr.CreateDesktopIcon=Cr�er un raccourci sur le bureau vers
fr.CreateQuickLaunchIcon=Cr�er un ic�ne dans la barre de lancement rapide
fr.FileExtensionName=Fichier pymecavideo
fr.InstallFor=Installer pour :
fr.AllUsers=Tous les utilisateurs
fr.JustMe=Seulement moi
fr.ShortCut=Raccourcis :
fr.ContextCommand=Organiser avex pyXorga



[Types]
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "program"; Description: "pyXorga"; Types: custom; Flags: fixed


[Files]
;
; Fichiers de la distribution
;
Source: src\build\exe.win32-2.7\*.*; DestDir: {app}\bin; Flags : ignoreversion recursesubdirs;
Source: README.md; DestDir: {app}; Flags : ignoreversion;
Source: LICENSE.txt; DestDir: {app}; Flags : ignoreversion;
;Source: images\*.*; DestDir: {app}\images; Flags : ignoreversion recursesubdirs; 


[Tasks]
Name: desktopicon2; Description: {cm:CreateDesktopIcon} pyXorga ;GroupDescription: {cm:ShortCut}; MinVersion: 4,4
Name: common; Description: {cm:AllUsers}; GroupDescription: {cm:InstallFor}; Flags: exclusive
Name: local;  Description: {cm:JustMe}; GroupDescription: {cm:InstallFor}; Flags: exclusive unchecked

[Icons]
Name: {group}\{#AppName};Filename: {app}\bin\pyXorga.exe; WorkingDir: {app}\bin; IconFileName: {app}\bin\pyXorga.exe
Name: {group}\{cm:uninstall} {#AppName}; Filename: {app}\unins000.exe;IconFileName: {app}\unins000.exe
;
; On ajoute sur le Bureau l'ic�ne pyXorga
;
Name: {code:DefDesktop}\{#AppName} {#AppVersionBase};   Filename: {app}\bin\pyXorga.exe; WorkingDir: {app}\bin; MinVersion: 4,4; Tasks: desktopicon2; IconFileName: {app}\bin\pyXorga.exe


[_ISTool]
Use7zip=true


[Registry]
; Tout ce qui concerne les fichiers .mecavideo
;Root: HKCR; SubKey: .mecavideo; ValueType: string; ValueData: {cm:FileExtensionName}; Flags: uninsdeletekey
;Root: HKCR; SubKey: {cm:FileExtensionName}; ValueType: string; Flags: uninsdeletekey; ValueData: {cm:FileExtensionName}
;Root: HKCR; SubKey: {cm:FileExtensionName}\Shell\Open\Command; ValueType: string; ValueData: """{app}\bin\pymecavideo.exe"" ""-f %1"""; Flags: uninsdeletekey;
;Root: HKCR; Subkey: {cm:FileExtensionName}\DefaultIcon; ValueType: string; ValueData: {app}\data\icones\pymecavideo.ico,0; Flags: uninsdeletekey;

; Pour stocker le style d'installation : "All users" ou "Current user"
Root: HKLM; Subkey: Software\{#AppName}; Flags: uninsdeletekey;
Root: HKLM; Subkey: Software\{#AppName}; ValueType: string; ValueName: DataFolder; ValueData: {code:DefAppDataFolder}\{#AppName} ; Flags: uninsdeletekey;
Root: HKLM; Subkey: Software\{#AppName}; ValueType: string; ValueName: UninstallPath; ValueData: {uninstallexe}; Flags: uninsdeletekey;


; Ajout d'une commande au menu contextuel
Root: HKCR; Subkey: Directory\shell\ContextCommand; ValueType: string; ValueData: {cm:ContextCommand} ; Flags: uninsdeletekey;
Root: HKCR; Subkey: Directory\shell\ContextCommand\command; ValueType: string; ValueData: """{app}\bin\pyXorga.exe"" ""%1""" ; Flags: uninsdeletekey;



[Code]
Procedure URLLabelOnClick(Sender: TObject);
var
  ErrorCode: Integer;
begin
  ShellExec('open', 'http://fauryc.free.fr/', '', '', SW_SHOWNORMAL, ewNoWait, ErrorCode);
end;

{*** INITIALISATION ***}
Procedure InitializeWizard;
var
  URLLabel: TNewStaticText;
begin
  URLLabel := TNewStaticText.Create(WizardForm);
  URLLabel.Caption := 'S.I.I. applications';
  URLLabel.Cursor := crHand;
  URLLabel.OnClick := @URLLabelOnClick;
  URLLabel.Parent := WizardForm;
  { Alter Font *after* setting Parent so the correct defaults are inherited first }
  URLLabel.Font.Style := URLLabel.Font.Style + [fsUnderline];
  URLLabel.Font.Color := clBlue;
  URLLabel.Top := WizardForm.ClientHeight - URLLabel.Height - 15;
  URLLabel.Left := ScaleX(20);
end;


{ Renvoie le dossier "Application Data" � utiliser }
function DefAppDataFolder(Param: String): String;
begin
  if IsTaskSelected('common') then
    Result := ExpandConstant('{commonappdata}')
  else
    Result := ExpandConstant('{localappdata}')
end;


{ Renvoie le bureau sur lequel placer le raccourci de pyXorga }
function DefDesktop(Param: String): String;
begin
  if IsTaskSelected('common') then
    Result := ExpandConstant('{commondesktop}')
  else
    Result := ExpandConstant('{userdesktop}')
end;















