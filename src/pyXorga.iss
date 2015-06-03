
;This file is part of pyXorga.
;
; Copyright (C) 2015 Cédrick FAURY
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

[Setup]
;Informations générales sur l'application
AppName=pyXorga 2.0
AppVerName=pyXorga 2.0
AppVersion=2.0
AppPublisher=Cédrick FAURY
AppCopyright=Copyright (C) 2015 Cédrick FAURY <fauryc@free.fr>
VersionInfoVersion = 2.0.0.0

;Répertoire de base contenant les fichiers
SourceDir=D:\Developpement\pyXorga

;Repertoire d'installation
DefaultDirName={pf}\pyXorga
DefaultGroupName=pyXorga
LicenseFile=LICENSE.txt

;Paramètres de compression
;lzma ou zip
Compression=lzma/max
SolidCompression=yes

;Par défaut, pas besoin d'être administrateur pour installer
PrivilegesRequired=none

;Nom du fichier généré et répertoire de destination
OutputBaseFilename=pyXorga_2.0_setup
OutputDir=releases

;Dans le panneau de configuration de Windows2000/NT/XP, c'est l'icone de pymecavideo.exe qui
;apparaît à gauche du nom du fichier pour la désinstallation
UninstallDisplayIcon={app}\images\pyXorga_logo_500x500.png

;Fenêtre en background
WindowResizable=false
WindowStartMaximized=true
WindowShowCaption=true
BackColorDirection=lefttoright


AlwaysUsePersonalGroup=no

[Languages]
Name: fr; MessagesFile: "compiler:Languages\French.isl"

[Messages]
BeveledLabel=pyXorga 2.0 installation


[CustomMessages]
;
; French
;
fr.uninstall=Désinstaller
fr.gpl_licence=Prendre connaissance du contrat de licence pour le logiciel
fr.fdl_licence=Prendre connaissance du contrat de licence pour la documentation associée
fr.CreateDesktopIcon=Créer un raccourci sur le bureau vers
fr.CreateQuickLaunchIcon=Créer un icône dans la barre de lancement rapide
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
Name: {group}\pyXorga;Filename: {app}\bin\pyXorga.exe; WorkingDir: {app}\bin; IconFileName: {app}\bin\pyXorga.exe
Name: {group}\{cm:uninstall} pyXorga; Filename: {app}\unins000.exe;IconFileName: {app}\unins000.exe
;
; On ajoute sur le Bureau l'icône pyXorga
;
Name: {code:DefDesktop}\pyXorga 2;   Filename: {app}\bin\pyXorga.exe; WorkingDir: {app}\bin; MinVersion: 4,4; Tasks: desktopicon2; IconFileName: {app}\bin\pyXorga.exe


[_ISTool]
Use7zip=true


[Registry]
; Tout ce qui concerne les fichiers .mecavideo
;Root: HKCR; SubKey: .mecavideo; ValueType: string; ValueData: {cm:FileExtensionName}; Flags: uninsdeletekey
;Root: HKCR; SubKey: {cm:FileExtensionName}; ValueType: string; Flags: uninsdeletekey; ValueData: {cm:FileExtensionName}
;Root: HKCR; SubKey: {cm:FileExtensionName}\Shell\Open\Command; ValueType: string; ValueData: """{app}\bin\pymecavideo.exe"" ""-f %1"""; Flags: uninsdeletekey;
;Root: HKCR; Subkey: {cm:FileExtensionName}\DefaultIcon; ValueType: string; ValueData: {app}\data\icones\pymecavideo.ico,0; Flags: uninsdeletekey;

; Pour stocker le style d'installation : "All users" ou "Current user"
Root: HKLM; Subkey: Software\pyXorga; Flags: uninsdeletekey;
Root: HKLM; Subkey: Software\pyXorga; ValueType: string; ValueName: DataFolder; ValueData: {code:DefAppDataFolder}\pyXorga ; Flags: uninsdeletekey;
Root: HKLM; Subkey: Software\pyXorga; ValueName: "UninstallPath" ; ValueType: string; ValueData: {uninstallexe}; Flags: uninsdeletekey;


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


{ Renvoie le dossier "Application Data" à utiliser }
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















