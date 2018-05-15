# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

sys.path.insert(0, './UI')
sys.path.insert(0, './Audio')

import mainWindows
import param
import Audio

import spectrogramme
#import fftGraph

import configuration

class MainWindows(QDialog, mainWindows.Ui_Dialog):

    progressChanged = pyqtSignal(int)

    def __init__(self, widgetFFT, parent=None):
        super(MainWindows, self).__init__(parent)
        self.setupUi(self)
        self.progressBar.setValue(0)
        self.progressChanged.connect(self.progressBar.setValue)
        self.dockWidget.setWidget(widgetFFT)

    def textBrowserSetText(self):
        global audioFile
        self.textBrowser.setText("Fichier selectionne: "+ str(audioFile))

    def setProgressBar(self, value):
        self.progressChanged.emit(value)

    #Rechercher un nouveau fichier audio
    def fileSearchClick(self):
        file_dialog = QFileDialog(self)

        #Définition des différents filtres
        file_dialog.setNameFilters(["Fichier audio (*.wav)"])
        file_dialog.selectNameFilter("Fichier audio (*.wav)")

        #ouverture de la boite de dialogue
        if (file_dialog.exec_()):
            #Définition de la variable global contenant le fichier à lire
            global audioFile
            audioFile = str(file_dialog.selectedFiles().first())
            self.textBrowserSetText();

    # Ecouter la musique à lire
    def ecouterClick(self):
        # si aucun fichier n'à été définit
        if (audioFile == None):
            # on ouvre la boite de dialogue demandant le fichier
            self.fileSearchClick()

        # on écoute ensuite le fichier
        if (audioFile != None):
            lectureAudio.lectureFichier(audioFile)

    def parametreClick(self):
        formParam.show()

    # On veut jouer sur la musique actuelle
    def jouerClick(self):
        # si aucun fichier n'à été définit
        #if (audioFile == None):
            # on ouvre la boite de dialogue demandant le fichier
        #    self.fileSearchClick()

        # on joue sur le fichier
        #if (audioFile != None):
        if enregistrementAudio.recording() == False:
            if (config.getValue("path_saved") != None):
                enregistrementAudio.enregistrementFichier(config.getValue("path_saved")+"/Karaoke_Save.wav")
            print("enregi..")
        else:
            enregistrementAudio.enregistrementStop()
            print("enregistrer")

class ParamWindows(QDialog, param.Ui_Dialog):

    def __init__(self, parent=None):
        super(ParamWindows, self).__init__(parent)
        self.setupUi(self)

    def SetChunk(self, value):
        config.setValue("chunk", value)

    def SetRate(self, value):
        config.setValue("rate", value)

    def SetChannel(self, value):
        config.setValue("channel", value)

    def CheminDEnregistrementClick(self):
        value = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if (value != ""):
            config.setValue("path_saved", value)

# si ce fichier correpond au fichier d'exécution python
if __name__ == "__main__":
    #on initialise la config
    config = configuration.config()
    config.setValue("rate", 8000)# --------------------NE PAS GARDER !!!!----------------------------
    config.setValue("chunk", 128)# --------------------NE PAS GARDER !!!!----------------------------
    config.setValue("path_saved", "/home/andy/Bureau")# --------------------NE PAS GARDER !!!!----------------------------
    #Initialisation de l'app PyQt
    app=QApplication([])

    #on définit le widget FFT
    widgetFFT = spectrogramme.SpectrogramWidget(config.getValue("chunk", 1024), config.getValue("rate", 8000))
    #widgetFFT = fftGraph.widgetFFT(config.getValue("chunk", 1024), config.getValue("rate", 8000))

    # on définit notre fenetre
    form=MainWindows(widgetFFT)
    form.show()

    #on définit la fenetre de paramètre
    formParam=ParamWindows(form)

    # on initialise la lecture audio
    lectureAudio = Audio.LectureAudio(form.setProgressBar)

    # on initialise l'Enregistrement audio
    enregistrementAudio = Audio.EnregistrementAudio(config.getValue("chunk", 1024), config.getValue("rate", 8000), config.getValue("channel", 1), widgetFFT.read_collected)

    # on définit le fichier audio
    audioFile = None;
    form.textBrowser.setText("Bienvenue sur Karaoke !\nAucun fichier audio a ete selectionne !")

    # on exécute l'application
    app.exec_()

    # fermeture de l'application
    print("Fermeture de Karaoke")

    # on libère la lecture audio
    lectureAudio.close()

    # on libère l'enregistrement audio
    enregistrementAudio.close()

    # on libère la configuration
    config.close()
