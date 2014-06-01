#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

##This file is part of pyXorga
#############################################################################
#############################################################################
##                                                                         ##
##                                  pyXorga                                ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2014 Cédrick FAURY

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
pyXorga.py
Organiser ses fichiers à l'aide de Xmind
*************
Copyright (C) 2014
@author: Cedrick FAURY

"""
__appname__= "pyXorga"
__author__ = u"Cédrick FAURY"
__version__ = "1.0"


####################################################################################
#
#   Import des modules nécessaires
#
####################################################################################
# GUI wxpython
import wx

# sdk
import xmind
from xmind.core import workbook,saver, loader
from xmind.core.markerref import MarkerId, MarkerRefElement
from xmind.core.topic import TopicElement
from xmind import utils

import Images
import subprocess
# mekk
#from mekk.xmind import XMindDocument

import sys
import os
import os.path 
import glob
import ConfigParser
import shutil


PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(PATH)
FICHIER_CFG = os.path.join(PATH, "pyXorga.cfg")
FICHIER_TYPES = os.path.join(PATH, "Types.cfg")

FILE_ENCODING = sys.getfilesystemencoding()
DEFAUT_ENCODING = "utf-8"


#######################################################################################################
#   Paramètres par défaut
#######################################################################################################
EXCLURE_DIR = [u"Ressources"]
INCLURE_DIR = [u"*"]

INCLURE_FIC = [u"*.docx"]
EXCLURE_FIC = [u"*.jpg", u"*.png"]

INCLURE_TYP = [u"Cours"]
EXCLURE_TYP = [u"*"]


#SEPARATEUR = u" _ "
##         nom              préfixe       marqueur   
#TYPES = { u"Cours"      : [u"C"     ,   "flag-blue"],
#          u"TD"         : [u"TD"    ,   "flag-green"],
#          u"Devoir"     : [u"DS"    ,   "flag-red"],
#          u"DevoirM"    : [u"DM"    ,   "flag-red"],
#          u"Test"       : [u"Test"  ,   "flag-red"],
#          u"QCM"        : [u"QCM"   ,   "flag-red"],
#          u"TP"         : [u"TP"    ,   "flag-purple"],
#          u"AP"         : [u"AP"    ,   "flag-yellow"],
#          u"DT"         : [u"DT"    ,   "flag-orange"],
#          u"FicheOutil"         : [u"FO"    ,   "star-blue"],
#          u"FicheMethode"         : [u"FM"    ,   "star-purple"],
#          }


DOSSIER = u""
FICHIER = u""

EXCLURE_DOSSIERS_VIDE = True
STRUCTURE  = 'structure-class="org.xmind.ui.logic.right"'

MARQUEUR_DOSSIER = "Dossier"
#MarqueurIDDossier = MarkerId(MARQUEUR_DOSSIER)

MarqueurDossier = MarkerRefElement()
MarqueurDossier.setMarkerId(MARQUEUR_DOSSIER)

######################################################################################  
def toDefautEncoding(path): 
    path = path.decode(FILE_ENCODING)
    path = path.encode(DEFAUT_ENCODING)
    return path  


def utf8decode(s):
    s = s.encode("iso-8859-1")
    return s.decode("utf-8")


def listdirectory2(path):  
    fichier=[]  
    for root, dirs, files in os.walk(path):  
        for i in files:  
            fichier.append(os.path.join(root, i))  
    return fichier




#
def GetTypeNom(nFich):
    """    Renvoie le type et le nom du document
    """
    parties = nFich.split(SEPARATEUR)
    if len(parties) > 1:
        for t, l in TYPES.items():
            if parties[0] == l[0]:
                return t, parties[1]
    return None, nFich

def GetNomSimple(file, typ):
    return os.path.splitext(file[len(TYPES[typ][0]):])[0]
    



#################################################################################################
#
#   Gestion du fichier de configuration
#
#################################################################################################
SECTION_FICH = u"FichierDossiers"
SECTION_FILTRE = u"Filtres"


    
    
#listdirectory(INPUT_DIR, root_topic)

#
#root_topic.add_subtopic(u"First item")
#root_topic.add_subtopic(u"Second item")
#t = root_topic.add_subtopic(u"Third item")
#t.add_subtopic(u"Second level - 1")
#t.add_subtopic(u"Second level - 2")
#root_topic.add_subtopic(u"Detached topic", detached = True)
#t.add_subtopic(u"Another detached", detached = True)
#t.add_marker("flag-red")
#root_topic.add_subtopic(u"Link example").set_link("http://mekk.waw.pl")
##root_topic.add_subtopic(u"Attachment example").set_attachment(
##    file("map_creator.py").read(), ".txt")
#root_topic.add_subtopic(u"With note").set_note(u"""This is just some dummy note.""")

#MARKER_CODE = "40g6170ftul9bo17p1r31nqk2a"
#XMP = "../../py_mekk_nozbe2xmind/src/mekk/nozbe2xmind/NozbeIconsMarkerPackage.xmp"
#root_topic.add_subtopic(u"With non-standard marker").add_marker(MARKER_CODE)
#
#xmind.embed_markers(XMP)

#

#xmind.pretty_print()



####################################################################################
#
#   Classe définissant l'application
#    --> récupération des paramétres passés en ligne de commande
#
####################################################################################
#from asyncore import dispatcher, loop
#import sys, time, socket, threading

#class SeqApp(wx.App):
#    def OnInit(self):
#        wx.Log.SetLogLevel(0) # ?? Pour éviter le plantage de wxpython 3.0 avec Win XP pro ???
#        



class FilterNB(wx.Notebook):
    def __init__(self, parent, app, exclure_Dir , inclure_Dir,
                     exclure_Fic, inclure_Fic, 
                     exclure_Typ, inclure_Typ):
        
        wx.Notebook.__init__(self, parent, -1, size=(21,21), style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )

        self.winDossiers = PanelInclureExclure(self, app, "D", inclure_Dir, exclure_Dir)
        self.AddPage(self.winDossiers, "Dossiers")
#        self.exclure_D = winDossiers.exclure
#        self.inclure_D = winDossiers.inclure

        # Show how to put an image on one of the notebook tabs,
        # first make the image list:
#        il = wx.ImageList(16, 16)
#        idx1 = il.Add(images.Smiles.GetBitmap())
#        self.AssignImageList(il)

        # now put an image on the first tab we just created:
#        self.SetPageImage(0, idx1)


        self.winExtensions = PanelInclureExclure(self, app, "F", inclure_Fic, exclure_Fic)
        self.AddPage(self.winExtensions, u"Fichiers")
#        self.exclure_F = winExtensions.exclure
#        self.inclure_F = winExtensions.inclure
        
        self.winTypes = PanelInclureExclure(self, app, "T", inclure_Typ, exclure_Typ)
        self.AddPage(self.winTypes, u"Types")
#        self.exclure_T = winTypes.exclure
#        self.inclure_T = winTypes.inclure

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
            
            
    def OnPageChanged(self, event):
#        old = event.GetOldSelection()
#        new = event.GetSelection()
#        sel = self.GetSelection()
#        self.log.write('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    def OnPageChanging(self, event):
#        old = event.GetOldSelection()
#        new = event.GetSelection()
#        sel = self.GetSelection()
#        self.log.write('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()
        
        
        
        
class pyXorgFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "pyXorga", size = (400,600))
        p = wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
                     | wx.CLIP_CHILDREN
                     | wx.FULL_REPAINT_ON_RESIZE
                     )
        
        #
        # Variables
        #
        self.nomFichier = FICHIER
        self.dossier =  DOSSIER
        self.dossierSortie = u""
        self.titreCarte = u""
        
        self.exclure_Dir = EXCLURE_DIR
        self.inclure_Dir = INCLURE_DIR
        self.exclure_Fic = EXCLURE_FIC
        self.inclure_Fic = INCLURE_FIC
        self.exclure_Typ = EXCLURE_TYP
        self.inclure_Typ = INCLURE_TYP
        
        
        self.ouvrirCFG()
        self.ouvrirTypes()
        print TYPES
        print SEPARATEUR
        
        #
        # Dossier à traiter
        #
        box = wx.StaticBox(p, -1, u"Dossier à traiter")
        bsizerd = wx.StaticBoxSizer(box, wx.VERTICAL)

        c = URLSelectorCombo(p, self, self.dossier, "D")
        self.selecteur_D = c
        bsizerd.Add(c, 0, wx.ALL|wx.EXPAND, 5)


        #
        # Sorties
        #
        box = wx.StaticBox(p, -1, u"Structure de sortie")
        bsizerxs = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        st = wx.StaticText(p, -1, u"Nom de la racine")
        ct = self.ctrlTitre = wx.TextCtrl(p, -1, self.titreCarte)
        self.Bind(wx.EVT_TEXT, self.EvtText, ct)
        
        #
        # Fichier Xmind de sortie
        #
        box = wx.StaticBox(p, -1, u"Fichier XMind")
        bsizerx = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        c = URLSelectorCombo(p, self, self.nomFichier, "F")
        bsizerx.Add(c, 1, wx.ALL|wx.EXPAND, 5)
        self.selecteur_F = c
        
        b = self.boutonGenererXMind = wx.Button(p, -1, u"Générer\ncarte", (20, 80)) 
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        self.boutonGenererXMind.Enable(self.nomFichier != u"")
        b.SetToolTipString(u"Générer la carte mentale")
        bsizerx.Add(b, 0, wx.ALL|wx.EXPAND, 5)
        
        b = self.boutonOuvrirXMind = wx.BitmapButton(p, -1, Images.LogoXMind.GetBitmap())
        self.boutonOuvrirXMind.Enable(os.path.exists(self.nomFichier))
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        b.SetToolTipString(u"Ouvrir la carte mentale")
        bsizerx.Add(b, 0, wx.ALL|wx.EXPAND, 5)
        
        #
        # Dossier de sortie
        #
        box = wx.StaticBox(p, -1, u"Dossier de sortie")
        bsizers = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        c = URLSelectorCombo(p, self, self.dossierSortie, "D")
        self.selecteur_DS = c
        bsizers.Add(c, 1, wx.ALL|wx.EXPAND, 5)
        
        b = self.boutonGenererClone = wx.Button(p, -1, u"Générer\ndossier", (20, 80)) 
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        self.boutonGenererClone.Enable(self.dossierSortie != u"")
        b.SetToolTipString(u"Générer une copie du dossier")
        bsizers.Add(b, 0, wx.ALL|wx.EXPAND, 5)
        
        
        b = self.boutonOuvrirDossier = wx.BitmapButton(p, -1, wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (42, 42)))
        self.boutonOuvrirDossier.Enable(os.path.exists(self.dossierSortie))
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        b.SetToolTipString(u"Ouvrir le dossier généré")
        bsizers.Add(b, 0, wx.ALL|wx.EXPAND, 5)
        #
        # Filtres
        #
        box =  wx.StaticBox(p, -1, u"Filtres")
        bsizerf = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.FilterNB = FilterNB(p, self, self.exclure_Dir , self.inclure_Dir,
                     self.exclure_Fic, self.inclure_Fic, 
                     self.exclure_Typ, self.inclure_Typ)
        bsizerf.Add(self.FilterNB, 1, wx.ALL|wx.EXPAND, 5)
        
        
        #
        # Mise en place
        #
        bsizerxs.Add(st, 0, wx.ALL|wx.EXPAND, 5)
        bsizerxs.Add(self.ctrlTitre, 0, wx.ALL|wx.EXPAND, 5)
        bsizerxs.Add(bsizerx, 0, wx.ALL|wx.EXPAND, 5)
        bsizerxs.Add(bsizers, 0, wx.ALL|wx.EXPAND, 5)
        bsizerxs.Add(bsizerf, 1, wx.ALL|wx.EXPAND, 5)
        
        gbs = self.gbs = wx.GridBagSizer(5, 5)
        gbs.Add( bsizerd, (0,0), (1,1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
        gbs.Add( bsizerxs, (1,0), (1,1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
#        gbs.Add( bsizers, (2,0), (1,1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
#        gbs.Add( bsizerf, (3,0), (1,1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)

        gbs.AddGrowableRow(1)
        gbs.AddGrowableCol(0)

        box = wx.BoxSizer()
        box.Add(gbs, 1, wx.ALL|wx.EXPAND, 5)
        p.SetSizerAndFit(box)
        
        self.SetMinSize((400, 600))
        self.SetClientSize(p.GetBestSize())
        
        # Interception de la demande de fermeture
        self.Bind(wx.EVT_CLOSE, self.OnClose)


    ##########################################################################################
    def EvtText(self, event):
        self.titreCarte = event.GetString()
        
        
    ##########################################################################################
    def testerDossierExistant(self):
        
        os.chdir(self.dossierSortie)
        d = os.path.join(self.dossierSortie, self.titreCarte)
        while os.path.exists(d) and len(os.listdir(d)) > 0:
            os.chdir(d)
            dlg = wx.MessageDialog(self, u"Le dossier suivant existe déja, et n'est pas vide !\n\n\n" \
                                         u"%s\n\n"\
                                         u"Voulez-vous effacer son contenu ?\n" %os.path.join(self.dossierSortie, self.titreCarte),
                                         u'Dossier existant et non vide',
                                         wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                         )
            retCode = dlg.ShowModal()
            dlg.Destroy() 
            if retCode == wx.ID_YES:
                os.chdir(d)
                for f in os.listdir(d):
                    shutil.rmtree(f, ignore_errors = True)
                os.chdir(d)
            elif retCode == wx.ID_NO:
                return False
            else:
                return False
        
        return True
    
    
    ##########################################################################################
    def OnClick(self, event):
        if event.GetEventObject() == self.boutonOuvrirXMind:
            try:
                os.startfile(self.nomFichier)
#            subprocess.Popen(["xmind", self.nomFichier])
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'accéder au fichier\n\n%s\n" %toDefautEncoding(self.nomFichier))
    
    
    
    

        #####################################################################################################################
        elif event.GetEventObject() == self.boutonOuvrirDossier:
            try:
                os.startfile(os.path.join(self.dossierSortie, self.titreCarte))
#            subprocess.Popen(["xmind", self.nomFichier])
            except:
                messageErreur(None, u"Ouverture impossible",
                              u"Impossible d'accéder au dossier\n\n%s\n" %toDefautEncoding(self.dossierSortie))
    
    
    
    
        #####################################################################################################################
        elif event.GetEventObject() == self.boutonGenererXMind:
            if os.path.exists(self.nomFichier):
                dlg = wx.MessageDialog(self, u"La carte mentale %s existe déja !\n\n" \
                                             u"Voulez-vous l'écraser ?\n" %self.nomFichier,
                                             u'Carte existante',
                                             wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                             )
                retCode = dlg.ShowModal()
                dlg.Destroy() 
                if retCode == wx.ID_YES:
                    os.remove(self.nomFichier)
                elif retCode == wx.ID_NO:
                    return
                else:
                    return
            
            try:
                self.dossier = unicode(self.dossier, DEFAUT_ENCODING)
            except:
                pass
            
            wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
            
            # Version sdk
            xm = xmind.load(self.nomFichier)
            first_sheet=xm.getPrimarySheet() # get the first sheet
            first_sheet.setTitle(self.titreCarte) # set its title
            root_topic=first_sheet.getRootTopic() # get the root topic of this sheet
            root_topic.setTitle(self.titreCarte) # set its title
            root_topic.setAttribute("structure-class", "org.xmind.ui.logic.right")
            # Version mekk
    #        xmind = XMindDocument.create(self.titreCarte, self.titreCarte)
    #        first_sheet = xmind.get_first_sheet()
    #        root_topic = first_sheet.get_root_topic()
    
            self.genererCarte(self.dossier, root_topic)
            
            if os.path.splitext(self.nomFichier)[1] != ".xmind":
                self.nomFichier = os.path.splitext(self.nomFichier)[0] + ".xmind"
            
            # mekk
    #        xmind.save(self.nomFichier)
            
            # sdk
            xmind.save(xm, self.nomFichier) # and we save

            wx.EndBusyCursor()
            
            self.boutonOuvrirXMind.Enable(True)
            dlg = wx.MessageDialog(self, u"La carte mentale à été correctement générée\n\n" \
                                   u"Fichier :\n" + self.nomFichier, 
                                   u"Génération terminée",
                           wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            


            
        #####################################################################################################################
        elif event.GetEventObject() == self.boutonGenererClone:

            try:
                self.dossierSortie = unicode(self.dossierSortie, DEFAUT_ENCODING)
            except:
                pass
            
            try:
                self.dossier = unicode(self.dossier, DEFAUT_ENCODING)
            except:
                pass
            
            if self.testerDossierExistant():
                wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
                os.chdir(self.dossierSortie)
                if not os.path.exists(self.titreCarte):
                    os.mkdir(self.titreCarte)
                os.chdir(self.titreCarte)
                self.genererDossier(self.dossier, os.getcwd())
                
                wx.EndBusyCursor()
                
                dlg = wx.MessageDialog(self, u"Le dossier a été correctement généré\n\n" \
                                       u"Dossier :\n" + os.path.join(self.dossierSortie, self.titreCarte), 
                                       u"Génération terminée",
                               wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            

            
    ##########################################################################################
    def getListNomGlob(self, path, liste):
        os.chdir(path)
        
        l = []
        for f in liste:
            l.extend(glob.glob(f))
#        l = [f.encode(FILE_ENCODING) for f in l]
        return l

    
    
    ##########################################################################################
    def getListeIE(self, IE, typ):
        return self.FilterNB.getListeIE(IE, typ)
            
            
            
    ##########################################################################################
    def genererCarte(self, path, topic):
        vide = True

        if not os.path.exists(path) or len(path) > 255:
            return

        dirs = os.listdir(path)
        
        for file in dirs:
            
            path_file = os.path.join(path, file)
            
            if os.path.isdir(path_file):
                inclureD = self.getListNomGlob(path, self.inclure_Dir)
                exclureD = self.getListNomGlob(path, self.exclure_Dir)
                if not file in exclureD and file in inclureD:
                    if len(os.listdir(path))>0:
                        # mekk
#                        t = topic.add_subtopic(file)
                        
                        # sdk
                        t = TopicElement()
                        t.setTitle(file)
                        t.addMarker("Folder.png")

                        dv = self.genererCarte(path_file, t)
                        
                        if EXCLURE_DOSSIERS_VIDE and not dv:
                            topic.addSubTopic(t)
                            vide = False
                        
                        
            else:
                ext = os.path.splitext(file)[1]
                typ, nom = GetTypeNom(file)
                inclureF = self.getListNomGlob(path, self.inclure_Fic)
                exclureF = self.getListNomGlob(path, self.exclure_Fic)
                if not file in exclureF and file in inclureF and typ in self.inclure_Typ:
                    # mekk
#                    t = topic.add_subtopic(GetNomSimple(file, typ))
#                    t.set_link(os.path.join(path, file))
#                    t.add_marker(TYPES[typ][1])
                    
                    # sdk
                    t = TopicElement()
                    t.setTitle(nom.split(ext)[0])
#                    t.setFileHyperlink(os.path.join(path, file)) # set a file hyperlink
                    
                    t.setFileHyperlink("file://" + utils.get_abs_path(os.path.join(path, file)))
                    if typ != None:
                        t.addMarker(TYPES[typ][1])
                    
                    topic.addSubTopic(t)

                    vide = False
        return vide


    ##########################################################################################
    def genererDossier(self, path, sortie):
        vide = True
        try:
            sortie = unicode(sortie, DEFAUT_ENCODING)
        except:
            pass
        
        if not os.path.exists(path) or len(path) > 255:
            return
        
        dirs = os.listdir(path)

        for file in dirs:  
            path_file = os.path.join(path, file)

            if os.path.isdir(path_file):
                inclureD = self.getListNomGlob(path, self.inclure_Dir)
                exclureD = self.getListNomGlob(path, self.exclure_Dir)
                if not file in exclureD and file in inclureD:
                    if len(os.listdir(path))>0:
                        os.chdir(sortie)
                        os.mkdir(file)
                        dv = self.genererDossier(path_file, os.path.join(sortie, file))
                        
                        if EXCLURE_DOSSIERS_VIDE and not dv:
                            vide = False
                        else:
                            os.chdir(sortie)
                            os.rmdir(file)
                        
                        
            else:
                ext = os.path.splitext(file)[1]
                typ, nom = GetTypeNom(file)
                inclureF = self.getListNomGlob(path, self.inclure_Fic)
                exclureF = self.getListNomGlob(path, self.exclure_Fic)
                if not file in exclureF and file in inclureF and typ in self.inclure_Typ:
                    shutil.copy2(os.path.join(path, file), sortie)

                    vide = False
        return vide
    
    
    #############################################################################
    def OnPathModified(self, selecteur, lien):
        if selecteur == self.selecteur_F:
            self.nomFichier = lien
            self.boutonOuvrirXMind.Enable(os.path.exists(self.nomFichier))

        elif   selecteur == self.selecteur_D:
            self.dossier = lien
            self.ctrlTitre.SetValue(os.path.basename(self.dossier))
            self.boutonGenererXMind.Enable(self.nomFichier != u"")
        
        elif   selecteur == self.selecteur_DS:
            self.dossierSortie = lien
            self.boutonGenererClone.Enable(self.dossierSortie != u"")
    
    #############################################################################
    def MiseAJourFiltres(self, inc, exc, typ = "D"):
        if typ == "D":
            self.exclure_Dir = exc
            self.inclure_Dir = inc
        elif typ == "F":
            self.exclure_Fic = exc
            self.inclure_Fic = inc
        elif typ == "T":
            self.exclure_Typ = exc
            self.inclure_Typ = inc
    
    #############################################################################
    def OnClose(self, evt):
        self.enregistrerCFG()
        evt.Skip()
        sys.exit()
    
    
    
    #############################################################################
    def ouvrirCFG(self):
        if not os.path.isfile(FICHIER_CFG):
            return
        config = ConfigParser.ConfigParser()
        config.read(FICHIER_CFG)
        self.dossier = config.get(SECTION_FICH, "Dossier", u"")
        self.dossierSortie = config.get(SECTION_FICH, "DossierSortie", u"")
        self.nomFichier = config.get(SECTION_FICH, "Fichier", u"")
        self.titreCarte = config.get(SECTION_FICH, "Titre", u"")
        
        self.exclure_Dir = config.get(SECTION_FILTRE, "Exclure_Dir").split("\t")
        self.inclure_Dir = config.get(SECTION_FILTRE, "Inclure_Dir").split("\t")
        self.exclure_Fic = config.get(SECTION_FILTRE, "Exclure_Fic").split("\t")
        self.inclure_Fic = config.get(SECTION_FILTRE, "Inclure_Fic").split("\t")
        self.exclure_Typ = config.get(SECTION_FILTRE, "Exclure_Typ").split("\t")
        self.inclure_Typ = config.get(SECTION_FILTRE, "Inclure_Typ").split("\t")
       
    #############################################################################
    def ouvrirTypes(self):
        global SEPARATEUR, TYPES
        
        if not os.path.isfile(FICHIER_TYPES):
            return
        
        config = ConfigParser.ConfigParser()
        
        config.read(FICHIER_TYPES)
        SEPARATEUR = config.get("Format", "Separateur", u"")[1:-1]
        TYPES = {}
        
        i = 1
        continuer = True
        while continuer:
            try :
                t = config.get("Types", "T"+str(i))
                print t
                n, p, f = t.split("#")
                TYPES[n] = [p, f]
                i += 1
            except:
                continuer = False
#            if i == 100:
#                continuer = False
        
    #############################################################################
    def enregistrerCFG(self):
        config = ConfigParser.ConfigParser()
        
    
        config.add_section(SECTION_FICH)
        config.set(SECTION_FICH, "Dossier", self.dossier)
        config.set(SECTION_FICH, "Fichier", self.nomFichier)
        config.set(SECTION_FICH, "DossierSortie", self.dossierSortie)
        config.set(SECTION_FICH, "Titre", self.titreCarte)
    
        config.add_section(SECTION_FILTRE)
        config.set(SECTION_FILTRE, "Exclure_Dir", "\t".join(self.exclure_Dir))
        config.set(SECTION_FILTRE, "Inclure_Dir", "\t".join(self.inclure_Dir))
        config.set(SECTION_FILTRE, "Exclure_Fic", "\t".join(self.exclure_Fic))
        config.set(SECTION_FILTRE, "Inclure_Fic", "\t".join(self.inclure_Fic))
        config.set(SECTION_FILTRE, "Exclure_Typ", "\t".join(self.exclure_Typ))
        config.set(SECTION_FILTRE, "Inclure_Typ", "\t".join(self.inclure_Typ))
        
        
        config.write(open(FICHIER_CFG,'w'))
    
    

class URLSelectorCombo(wx.Panel):
    def __init__(self, parent, app, lien = "", typ = "D", ext = ""):
        wx.Panel.__init__(self, parent, -1)
        
        print "INIT URLSelectorCombo", typ, lien
        
        self.app = app
        
        self.SetMaxSize((-1,22))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.texte = wx.TextCtrl(self, -1, lien, size = (-1, 16))
        
        if typ == "D":
            bt1 =wx.BitmapButton(self, 100, wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
            bt1.SetToolTipString(u"Sélectionner un dossier")
            self.Bind(wx.EVT_BUTTON, self.OnClick, bt1)
            self.Bind(wx.EVT_TEXT, self.EvtText, self.texte)
            sizer.Add(bt1)
        elif typ == "F":
            bt2 =wx.BitmapButton(self, 101, wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))
            bt2.SetToolTipString(u"Sélectionner un fichier")
            self.Bind(wx.EVT_BUTTON, self.OnClick, bt2)
            self.Bind(wx.EVT_TEXT, self.EvtText, self.texte)
            sizer.Add(bt2)
            
        self.ext = u"Xmind (.xmind)|*.xmind|" \
                       u"Tous les fichiers|*.*'"
        self.typ = typ
        
        
        sizer.Add(self.texte,1,flag = wx.EXPAND)
        self.SetSizerAndFit(sizer)
        self.lien = lien
     

    # Overridden from ComboCtrl, called when the combo button is clicked
    def OnClick(self, event):
        
        if event.GetId() == 100:
            dlg = wx.DirDialog(self, u"Sélectionner un dossier",
                          style=wx.DD_DEFAULT_STYLE,
                          defaultPath = self.lien
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
            if dlg.ShowModal() == wx.ID_OK:
                self.SetPath(dlg.GetPath())
    
            dlg.Destroy()
        else:
            dlg = wx.FileDialog(self, u"Sélectionner un fichier",
                                wildcard = self.ext,
    #                           defaultPath = globdef.DOSSIER_EXEMPLES,
                               style = wx.DD_DEFAULT_STYLE
                               #| wx.DD_DIR_MUST_EXIST
                               #| wx.DD_CHANGE_DIR
                               )
    
            if dlg.ShowModal() == wx.ID_OK:
                self.SetPath(dlg.GetPath())
    
            dlg.Destroy()
        
        self.SetFocus()


    ##########################################################################################
    def EvtText(self, event):
        self.SetPath(event.GetString())


    ##########################################################################################
    def GetPath(self):
        return self.lien
    
    
    ##########################################################################################
    def SetPath(self, lien):
        """ lien doit être de type 'String'
        """
        if self.typ == "D":
            if os.path.exists(lien) and os.path.isdir(lien):
                self.texte.ChangeValue(toDefautEncoding(lien)) # On le met en DEFAUT_ENCODING
                self.lien = lien
                self.texte.SetBackgroundColour(("white"))
            else:
                self.texte.SetBackgroundColour(("pink"))
        else:
            self.texte.ChangeValue(toDefautEncoding(lien))
            self.lien = lien
            
        self.app.OnPathModified(self, self.lien)
        self.Refresh()
        
    
        
        
class PanelInclureExclure(wx.Panel):
    def __init__(self, parent, app, typ = "D", inclure = [], exclure = []):
        wx.Panel.__init__(self, parent, -1)
        
        self.inclure = inclure
        self.exclure = exclure
        self.typ = typ
        self.app = app
        
        ti = wx.StaticText(self, -1, u"Inclure")
        te = wx.StaticText(self, -1, u"Exclure")
        
        si = self.si = wx.TextCtrl(self, -1, u"\n".join(inclure), style=wx.TE_MULTILINE)
        self.Bind(wx.EVT_TEXT, self.EvtText, si)
        se = self.se = wx.TextCtrl(self, -1, u"\n".join(exclure), style=wx.TE_MULTILINE)
        self.Bind(wx.EVT_TEXT, self.EvtText, se)

        gbs = wx.GridBagSizer()
        gbs.Add(ti, (0,0), flag = wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border = 4)
        gbs.Add(te, (0,1), flag = wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border = 4)
        gbs.Add(si, (1,0), flag = wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, border = 4)
        gbs.Add(se, (1,1), flag = wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, border = 4)
        gbs.AddGrowableRow(1)
        
        self.SetSizer(gbs)
        
    def EvtText(self, event):
        s = event.GetString()
        if event.GetEventObject() == self.si:
            self.inclure = s.split("\n")
        elif event.GetEventObject() == self.se:
            self.exclure = s.split("\n")
        self.app.MiseAJourFiltres(self.inclure, self.exclure, typ = self.typ)

#############################################################################################################
def messageErreur(parent, titre, message):
    dlg = wx.MessageDialog(parent, message, titre,
                           wx.OK | wx.ICON_WARNING)
    dlg.ShowModal()
    dlg.Destroy()
    

if __name__ == '__main__':

#    if len(sys.argv) > 1:
#        arg = sys.argv[1]
#    else:
#        arg = ''
#    sys.exit()
        
    
    app = wx.App()
    app.frame = pyXorgFrame()
    app.frame.Show()
    app.MainLoop()
    

