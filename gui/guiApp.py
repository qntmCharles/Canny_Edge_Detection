from PyQt4 import QtCore, QtGui
from .guiCanny import CannyWindow

class App(QtGui.QApplication):
    """
        Class that is the main application, and initialise the main
        windows and is the last 'window' to be closed when quitting

        Inherits functionality from QtGui.QApplication
    """
    def __init__(self, *args):
        #Initialise application using system args
        app = QtGui.QApplication.__init__(self,*args)

        #Initialise main window
        self.main = CannyWindow()

        #Display main window
        self.main.show()

        #Connect exit buttons and ensure safe closing
        self.main.quitButton.clicked.connect(self.exit)
        self.lastWindowClosed.connect(self.exit)
