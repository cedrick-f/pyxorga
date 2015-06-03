#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pyXorga
#############################################################################
#############################################################################
##                                                                         ##
##                                 util_path                               ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2015 Cédrick FAURY

#    pyXorga is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
    
#    pyXorga is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyXorga; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""

Copyright (C) 2015
@author: Cedrick FAURY

"""
#import _winreg
import os, sys

if sys.platform == 'win32':
    #
    # Les deuxlignes suivantes permettent de lancer le script pymecavideo.py depuis n'importe
    # quel répertoire  sans que l'utilisation de chemins
    # relatifs ne soit perturbée
    #
    PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
    #PATH = os.path.split(PATH)[0]
    os.chdir(PATH)
    sys.path.append(PATH)

else:
    pass


#
# Dossier des données "temporaires" (video*.jpg, crop*.jpg, out.avi)
#
if sys.platform == 'win32':
    #On récupèreﾠ le dossier "Application data" 
    #On lit la clef de registre indiquant le type d'installation
    import win32api, win32con

    try:
        # Vérifie si pyXorga est installé
        regkey = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, 'SOFTWARE\\pyXorga', 0, win32con.KEY_READ)
        (value, keytype) = win32api.RegQueryValueEx(regkey, 'DataFolder')
        APP_DATA_PATH = value
        
        # pyXorga installé : on récupère le dossier d'installation
        try:
            regkey = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\pyXorga 1.0_is1', 0, win32con.KEY_READ)
            (value, keytype) = win32api.RegQueryValueEx(regkey, 'Inno Setup: App Path')
            INSTALL_PATH = value
        except:
            try:
                regkey = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, 'SOFTWARE\\pyXorga', 0, win32con.KEY_READ)
                (value, keytype) = win32api.RegQueryValueEx(regkey, 'UninstallPath')
                INSTALL_PATH = value
            except:
                print u"install_path non trouvé"
        print u"pyXorga installé dans", INSTALL_PATH
        print u"pyXorga démarré dans", PATH
        
        if INSTALL_PATH == os.path.split(PATH)[0]:
            # On est bien en train d'éxécuter la version "installée"
            if not os.path.exists(APP_DATA_PATH):
                os.makedirs(APP_DATA_PATH)
        else:
            print u"Version PORTABLE", PATH
        
        
    except:
        INSTALL_PATH = None
        APP_DATA_PATH = PATH
    sys.path.append(os.path.join(PATH, 'bin'))


else:
    print os.getenv('APPDATA')
    import subprocess
    datalocation = os.path.join(QStandardPaths.standardLocations(QStandardPaths.DataLocation)[0], "data", "pymecavideo")
    PATH = APP_DATA_PATH = datalocation
    if not os.path.exists(datalocation):
        subprocess.call("mkdir -p %s" %datalocation, shell=True)
        

# execution du pyXorga "installé"
if INSTALL_PATH is not None and INSTALL_PATH == os.path.split(PATH)[0]:
    APP_DATA_PATH_USER = os.path.join(os.getenv('APPDATA'), 'pyXorga')
    if not os.path.isdir(APP_DATA_PATH_USER):
        os.mkdir(APP_DATA_PATH_USER)
# execution du pyXorga "portable"
else:
    APP_DATA_PATH = PATH
    APP_DATA_PATH_USER = PATH


def samefile(path1, path2):
    return os.path.normcase(os.path.normpath(os.path.abspath(path1))) == \
           os.path.normcase(os.path.normpath(os.path.abspath(path2)))

print u"Dossier COMMUN pour les données :", APP_DATA_PATH
print u"Dossier USER pour les données :", APP_DATA_PATH_USER


#print "programdata", os.environ['ALLUSERSPROFILE']