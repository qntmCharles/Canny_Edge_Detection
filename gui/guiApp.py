from PyQt4 import QtCore, QtGui
from .guiMain import MainWindow

class App(QtGui.QApplication):
    def __init__(self,*args):
        #Initialise
        app = QtGui.QApplication.__init__(self,*args)
        #Initialise main window
        self.main = MainWindow()
        self.main.resize(500,500)
        self.main.show()

        #Connect exit buttons and ensure safe closing
        self.main.cannyWidget.quitButton.clicked.connect(self.exit)
        self.lastWindowClosed.connect(self.exit)
