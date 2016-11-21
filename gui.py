import sys
from PyQt4 import QtCore, QtGui
from PIL import Image as im
from main import Image
import numpy as np


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        #Initialise main window
        super(MainWindow, self).__init__(parent)

        #Set title
        self.setWindowTitle('Canny Edge Detection')

        #Initialise central widget
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.startWidget = StartWindow(self)
        self.startWidget.fileStatusString = 'File: not loaded'
        self.optionsWidget = OptionsWindow(self)
        self.central_widget.addWidget(self.optionsWidget)
        self.central_widget.addWidget(self.startWidget)
        self.central_widget.setCurrentWidget(self.startWidget)


    def otherOptionsShowFunction(self):
        self.central_widget.setCurrentWidget(self.optionsWidget)

    def otherOptionsHideFunction(self):
        self.startWidget.fileStatusLabel.setText(self.startWidget.fileStatusString)
        self.central_widget.setCurrentWidget(self.startWidget)

class StartWindow(QtGui.QWidget):
    def __init__(self,parent):
        super(StartWindow,self).__init__(parent)

        #Create widgets
        self.createWidgets()

        #Set layout
        self.layout()

    def createWidgets(self):
        #Define widgets
        self.openFileButton = QtGui.QPushButton('Open File')
        self.quitButton = QtGui.QPushButton('Quit')
        self.fileStatusLabel = QtGui.QLabel('File: not loaded')
        self.fullCannyButton = QtGui.QPushButton('Full Canny Edge Detection')
        self.otherOptionsButton = QtGui.QPushButton('Select Individual Options')

        #Connect widgets
        QtCore.QObject.connect(self.openFileButton, QtCore.SIGNAL('clicked()'), self.openFileFunction)
        QtCore.QObject.connect(self.fullCannyButton, QtCore.SIGNAL('clicked()'), self.fullCannyFunction)
        QtCore.QObject.connect(self.otherOptionsButton, QtCore.SIGNAL('clicked()'), self.parent().otherOptionsShowFunction)

    def layout(self):
        #Set layout
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(self.openFileButton,0,2,QtCore.Qt.AlignTop)
        gridLayout.addWidget(self.fileStatusLabel,0,0,QtCore.Qt.AlignTop)
        gridLayout.addWidget(self.quitButton,6,1,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.fullCannyButton,3,1,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.otherOptionsButton,4,1,QtCore.Qt.AlignCenter)
        self.setLayout(gridLayout)

    def openFileFunction(self):
        #Open file dialog and get selected filepath
        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~', 'Image files (*.jpg *.gif *.bmp *.png)')
        #Store loaded image in Image object
        I = Image(np.asarray(im.open(filepath).convert('L'),dtype=np.float))
        #Set file status
        self.fileStatusString = 'File: '+str(filepath.split('/')[-1])
        self.fileStatusLabel.setText(self.fileStatusString)

    def fullCannyFunction(self):
        print('Full Canny Edge Detection')


class OptionsWindow(QtGui.QWidget):
    def __init__(self,parent):
        super(OptionsWindow, self).__init__(parent)

        #Create widgets
        self.createWidgets()

        #Set layout
        self.layout()


    def createWidgets(self):
        #Define widgets
        self.backButton = QtGui.QPushButton('Back')
        self.fileStatusLabel = QtGui.QLabel('')
        self.fileStatusLabel.setText(self.parent().startWidget.fileStatusString)
        self.quitButton = QtGui.QPushButton('Quit')

        #Connect widgets
        QtCore.QObject.connect(self.backButton, QtCore.SIGNAL('clicked()'), self.parent().otherOptionsHideFunction)

    def layout(self):
        #Set layout
        gridLayout = QtGui.QGridLayout()

        gridLayout.addWidget(self.backButton,6,0,QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.fileStatusLabel,0,0,QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.quitButton,6,2,QtCore.Qt.AlignRight)

        self.setLayout(gridLayout)



class App(QtGui.QApplication):
    def __init__(self,*args):
        #Initialise app
        QtGui.QApplication.__init__(self,*args)

        #Initialise main window
        self.main = MainWindow()
        self.main.resize(500,500)
        self.main.show()

        #Connect exit button and safe closing
        QtCore.QObject.connect(self.main.startWidget.quitButton, QtCore.SIGNAL('clicked()'),self.Exit)
        QtCore.QObject.connect(self, QtCore.SIGNAL('lastWindowClosed()'),self.Exit)

    def Exit(self):
        self.exit(0)

if __name__ == '__main__':
    #Create QApplication
    app = App(sys.argv)

    #Enter main loop
    app.exec_()
