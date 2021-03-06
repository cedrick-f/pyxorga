#!/usr/bin/python
# -*- coding: utf-8 -*-

##################################################################################################
#
#    Script pour générer un pack avec executable :
#    c:\python27\python setup.py build
#
##################################################################################################

import sys, os
from glob import glob
from cx_Freeze import setup, Executable
from version import *

#reload(sys)
#sys.setdefaultencoding('utf-8')

## Remove the build folder, a bit slower but ensures that build contains the latest
import shutil
shutil.rmtree("build", ignore_errors=True)

# Inculsion des fichiers de donn�es
#################################################################################################
includefiles = [('C:\Users\Cedrick\Documents\Developp\Microsoft.VC90.CRT', "Microsoft.VC90.CRT"),
                     'LICENSE.txt', 
                     'Types.cfg',
                     'pyXorga_icone.ico',
#                     ('../images', 'images')
                     ]

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "xmind"], 
                     "excludes": ["tkinter",
                                  '_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
                                  'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
                                  'Tkconstants', 'pydoc', 'doctest', 'test', 'sqlite3',
                                  "PyQt4", "PyQt4.QtGui","PyQt4._qt",
                                  "matplotlib",
                                  "numpy",
                                  ],
                     "include_files": includefiles,
                     'bin_excludes' : ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl85.dll',
                                              'tk85.dll', "UxTheme.dll", "mswsock.dll", "POWRPROF.dll",
                                              "QtCore4.dll", "QtGui4.dll" ],
                     "includes": ['xmind']}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

cible = Executable(
    script = "pyXorga.py",
    base = base,
    compress = True,
    icon = os.path.join("", 'pyXorga_icone.ico'),
    initScript = None,
    copyDependentFiles = True,
    appendScriptToExe = False,
    appendScriptToLibrary = False
    )


setup(  name = "pyXorga",
        version = GetVersion_cxFreeze(),
        author = "Cedrick FAURY",
        description = u"pyXorga",
        options = {"build_exe": build_exe_options},
#        include-msvcr = True,
        executables = [cible])
