import sys
from PyQt4 import QtCore, QtGui
from PIL import Image as im
from main import Image
import numpy as np

class Main(QtGui.QMainWindow):
    def __init__(self, win_parent = None):
        #Initialise main window
        QtGui.QMainWindow.__init__(self,win_parent)

        #Set title
        self.setWindowTitle('Canny Edge Detection')

        #Create widgets
        self.create_widgets()

    def create_widgets(self):
        #Widgets
        self.open_file = QtGui.QPushButton('Open File')
        self.quit = QtGui.QPushButton('Quit') #NB: conncted in App
        self.file = QtGui.QLabel('File: not loaded')

        #Connect widgets
        QtCore.QObject.connect(self.open_file, QtCore.SIGNAL('clicked()'),self.getFile)

        #Set layout
        grid = QtGui.QGridLayout()
        grid.addWidget(self.open_file,1,1)
        grid.addWidget(self.quit,2,2)
        grid.addWidget(self.file,2,0)

        #Initialise central widget
        central_widget = QtGui.QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

    def getFile(self):
        filepath = QtGui.QFileDialog.getOpenFileName(self,'Open file','~','Image files (*.jpg *.gif *.bmp *.png)')
        self.ImageObj = Image(np.asarray(im.open(filepath).convert('L'),dtype=np.float))



class App(QtGui.QApplication):
    def __init__(self,*args):
        #Initialise app
        QtGui.QApplication.__init__(self,*args)
        self.main = Main()

        #Connect widgets
        self.connect(self, QtCore.SIGNAL('lastWindowClosed()'), self.Exit)
        self.connect(self.main.quit, QtCore.SIGNAL('clicked()'), self.Exit)

        #Show main window
        self.main.show()

    def Exit(self):
        self.exit(0)


if __name__ == "__main__":
    #Create QApplication
    app = App(sys.argv)

    #Enter main loop
    app.exec_()
