"""import sys, time
sys.path.insert(0,'/home/cwp/NEA/')

from PyQt4 import QtCore, QtGui
from PIL import Image as im
import numpy as np

#Force matplotlib to use qt4 backends
#from matplotlib import use
#use('Qt4Agg')

from matplotlib import pyplot as plt
#Matplotlib backends for qt4 to show images
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure

#Import Image class
from main import Image
import sys
sys.path.insert(0,'/home/cwp/')
import NEA
import NEA.canny
import NEA.gui"""

class MainWindow(QtGui.QMainWindow):
    """Main window for application."""
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        #Set title
        self.setWindowTitle('Canny Edge Detection')

        self.setFixedSize(750,600)

        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self, self.close)

        #Initialise central widget
        self.cannyWidget = CannyWindow(self)
        self.setCentralWidget(self.cannyWidget)

class App(QtGui.QApplication):
    def __init__(self,*args):
        #Initialise
        app = QtGui.QApplication.__init__(self,*args)
        #Initialise main window
        self.main = MainWindow()
        self.main.resize(500,500)
        self.main.show()

        #Connect exit buttons and safe closing
        self.main.cannyWidget.quitButton.clicked.connect(self.exit)
        self.lastWindowClosed.connect(self.exit)

"""if __name__ == '__main__':
    #Create QApplication
    app = App(sys.argv)

    #Enter main loop
    app.exec_()
    sys.exit()"""
