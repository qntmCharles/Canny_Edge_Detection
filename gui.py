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
        self.fileStatusString = 'File: not loaded'
        self.optionsWidget = OptionsWindow(self)
        self.cannyWidget = CannyWindow(self)
        self.central_widget.addWidget(self.cannyWidget)
        self.central_widget.addWidget(self.optionsWidget)
        self.central_widget.addWidget(self.startWidget)
        self.central_widget.setCurrentWidget(self.startWidget)

    def fullCannyShowFunction(self):
        self.central_widget.setCurrentWidget(self.cannyWidget)

    def fullCannyHideFunction(self):
        self.central_widget.setCurrentWidget(self.startWidget)

    def otherOptionsShowFunction(self):
        self.central_widget.setCurrentWidget(self.optionsWidget)

    def otherOptionsHideFunction(self):
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
        self.quitButton = QtGui.QPushButton('Quit')
        self.fullCannyButton = QtGui.QPushButton('Full Canny Edge Detection')
        self.otherOptionsButton = QtGui.QPushButton('Select Individual Options')
        self.titleLabel = QtGui.QLabel('Canny Edge Detection')

        #Connect widgets
        QtCore.QObject.connect(self.fullCannyButton, QtCore.SIGNAL('clicked()'), self.parent().fullCannyShowFunction)
        QtCore.QObject.connect(self.otherOptionsButton, QtCore.SIGNAL('clicked()'), self.parent().otherOptionsShowFunction)

    def layout(self):
        #Set layout
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(self.quitButton,6,1,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.fullCannyButton,3,1,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.otherOptionsButton,4,1,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.titleLabel,0,1,QtCore.Qt.AlignCenter)
        self.setLayout(gridLayout)

class OptionsWindow(QtGui.QWidget):
    def __init__(self,parent):
        super(OptionsWindow, self).__init__(parent)
        #Create widgets
        self.createWidgets()

        #Set layout
        self.layout()


    def createWidgets(self):
        self.widgets=[[],[],[],[]]

        #Define widgets
        self.backButton = QtGui.QPushButton('Back')
        self.backButton.setMaximumWidth(100)
        self.fileStatusLabel = QtGui.QLabel('')
        self.fileStatusLabel.setText(self.parent().fileStatusString)
        self.quitButton = QtGui.QPushButton('Quit')
        self.quitButton.setMaximumWidth(100)
        self.openFileButton = QtGui.QPushButton('Open file')

        self.gblurButton = QtGui.QPushButton('Gaussian Blur')
        self.widgets[0].append(self.gblurButton)
        self.sobelButton = QtGui.QPushButton('Sobel Filter')
        self.widgets[0].append(self.sobelButton)
        self.nmsButton = QtGui.QPushButton('Non Maximum Suppression')
        self.widgets[0].append(self.nmsButton)
        self.thresholdButton = QtGui.QPushButton('Thresholding')
        self.widgets[0].append(self.thresholdButton)
        self.hysteresisButton = QtGui.QPushButton('Hysteresis')
        self.widgets[0].append(self.hysteresisButton)

        self.gblurLabel = QtGui.QLabel('Not started')
        self.widgets[1].append(self.gblurLabel)
        self.sobelLabel = QtGui.QLabel('Not started')
        self.widgets[1].append(self.sobelLabel)
        self.nmsLabel = QtGui.QLabel('Not started')
        self.widgets[1].append(self.nmsLabel)
        self.thresholdLabel = QtGui.QLabel('Not started')
        self.widgets[1].append(self.thresholdLabel)
        self.hysteresisLabel = QtGui.QLabel('Not started')
        self.widgets[1].append(self.hysteresisLabel)

        self.gblurShow = QtGui.QPushButton('Show')
        self.widgets[2].append(self.gblurShow)
        self.sobelShow = QtGui.QPushButton('Show')
        self.widgets[2].append(self.sobelShow)
        self.nmsShow = QtGui.QPushButton('Show')
        self.widgets[2].append(self.nmsShow)
        self.thresholdShow = QtGui.QPushButton('Show')
        self.widgets[2].append(self.thresholdShow)
        self.hysteresisShow = QtGui.QPushButton('Show')
        self.widgets[2].append(self.hysteresisShow)

        self.gblurSave = QtGui.QPushButton('Save')
        self.widgets[3].append(self.gblurSave)
        self.sobelSave = QtGui.QPushButton('Save')
        self.widgets[3].append(self.sobelSave)
        self.nmsSave = QtGui.QPushButton('Save')
        self.widgets[3].append(self.nmsSave)
        self.thresholdSave = QtGui.QPushButton('Save')
        self.widgets[3].append(self.thresholdSave)
        self.hysteresisSave = QtGui.QPushButton('Save')
        self.widgets[3].append(self.hysteresisSave)

        #Connect widgets
        QtCore.QObject.connect(self.backButton, QtCore.SIGNAL('clicked()'), self.parent().otherOptionsHideFunction)
        QtCore.QObject.connect(self.openFileButton, QtCore.SIGNAL('clicked()'), self.openFileFunction)

    def layout(self):
        #Create layout
        gridLayout = QtGui.QGridLayout()

        #Add widgets
        gridLayout.addWidget(self.backButton,6,0,QtCore.Qt.AlignBottom)
        gridLayout.addWidget(self.fileStatusLabel,0,0,QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.quitButton,6,3,QtCore.Qt.AlignBottom)
        gridLayout.addWidget(self.openFileButton,0,3,QtCore.Qt.AlignRight)

        for i in range(0,4):
            for j in range(0,5):
                if i == 0:
                    self.widgets[i][j].setMinimumWidth(200)
                gridLayout.addWidget(self.widgets[i][j],j+1,i,QtCore.Qt.AlignCenter)

        #Set layout
        self.setLayout(gridLayout)

    def openFileFunction(self):
        #Open file dialog and get selected filepath
        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~', 'Image files (*.jpg *.gif *.bmp *.png)')
        if len(filepath) != 0:
            #Store loaded image in Image object
            self.parent().parent().I = Image(np.asarray(im.open(filepath).convert('L'),dtype=np.float))
            #Set file status
            self.parent().parent().fileStatusString = 'File: '+str(filepath.split('/')[-1])
            self.fileStatusLabel.setText(self.parent().parent().fileStatusString)
            self.parent().parent().cannyWidget.fileStatusLabel.setText(self.parent().parent().fileStatusString)

class CannyWindow(QtGui.QWidget):
    def __init__(self, parent):
        super(CannyWindow, self).__init__(parent)
        #Create widgets
        self.createWidgets()

        #Set layout
        self.layout()

    def createWidgets(self):
        self.widgets = [[],[]]
        #Define widgets
        self.backButton = QtGui.QPushButton('Back')
        self.backButton.setMaximumWidth(100)
        self.fileStatusLabel = QtGui.QLabel('')
        self.fileStatusLabel.setText(self.parent().fileStatusString)
        self.openFileButton = QtGui.QPushButton('Open file')
        self.quitButton = QtGui.QPushButton('Quit')
        self.quitButton.setMaximumWidth(100)
        self.startButton = QtGui.QPushButton('Start')

        self.gblurLabel = QtGui.QLabel('Gaussian Blur: not started')
        self.sobelLabel = QtGui.QLabel('Sobel Filter: not started')
        self.nmsLabel = QtGui.QLabel('Non Maximum Suppression: not started')
        self.thresholdLabel = QtGui.QLabel('Thresholding: not started')
        self.hysteresisLabel = QtGui.QLabel('Hysteresis: not started')

        self.gblurShow = QtGui.QPushButton('Show')
        self.widgets[0].append(self.gblurShow)
        self.sobelShow = QtGui.QPushButton('Show')
        self.widgets[0].append(self.sobelShow)
        self.nmsShow = QtGui.QPushButton('Show')
        self.widgets[0].append(self.nmsShow)
        self.thresholdShow = QtGui.QPushButton('Show')
        self.widgets[0].append(self.thresholdShow)
        self.hysteresisShow = QtGui.QPushButton('Show')
        self.widgets[0].append(self.hysteresisShow)

        self.gblurSave = QtGui.QPushButton('Save')
        self.widgets[1].append(self.gblurSave)
        self.sobelSave = QtGui.QPushButton('Save')
        self.widgets[1].append(self.sobelSave)
        self.nmsSave = QtGui.QPushButton('Save')
        self.widgets[1].append(self.nmsSave)
        self.thresholdSave = QtGui.QPushButton('Save')
        self.widgets[1].append(self.thresholdSave)
        self.hysteresisSave = QtGui.QPushButton('Save')
        self.widgets[1].append(self.hysteresisSave)

        QtCore.QObject.connect(self.backButton, QtCore.SIGNAL('clicked()'), self.parent().fullCannyHideFunction)
        QtCore.QObject.connect(self.openFileButton, QtCore.SIGNAL('clicked()'), self.openFileFunction)

    def layout(self):
        gridLayout = QtGui.QGridLayout()

        gridLayout.addWidget(self.backButton,7,0,QtCore.Qt.AlignBottom)
        gridLayout.addWidget(self.openFileButton,0,2,QtCore.Qt.AlignRight)
        gridLayout.addWidget(self.quitButton,7,2,QtCore.Qt.AlignBottom)
        gridLayout.addWidget(self.startButton,1,1,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.gblurLabel,2,0)
        gridLayout.addWidget(self.sobelLabel,3,0)
        gridLayout.addWidget(self.nmsLabel,4,0)
        gridLayout.addWidget(self.thresholdLabel,5,0)
        gridLayout.addWidget(self.hysteresisLabel,6,0)
        gridLayout.addWidget(self.fileStatusLabel,0,0,QtCore.Qt.AlignLeft)

        for i in range(0,2):
            for j in range(0,5):
                gridLayout.addWidget(self.widgets[i][j],j+2,i+1,QtCore.Qt.AlignCenter)
        for i in range(0,2):
            for j in range(0,5):
                self.widgets[i][j].hide()

        self.setLayout(gridLayout)

    def openFileFunction(self):
        #Open file dialog and get selected filepath
        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~', 'Image files (*.jpg *.gif *.bmp *.png)')
        if len(filepath) != 0:
            #Store loaded image in Image object
            self.parent().parent().I = Image(np.asarray(im.open(filepath).convert('L'),dtype=np.float))
            #Set file status
            self.parent().parent().fileStatusString = 'File: '+str(filepath.split('/')[-1])
            self.fileStatusLabel.setText(self.parent().parent().fileStatusString)
            self.parent().parent().optionsWidget.fileStatusLabel.setText(self.parent().parent().fileStatusString)

class App(QtGui.QApplication):
    def __init__(self,*args):
        #Initialise
        app = QtGui.QApplication.__init__(self,*args)
        #Initialise main window
        self.main = MainWindow()
        self.main.resize(500,500)
        self.main.show()

        #Connect exit buttons and safe closing
        QtCore.QObject.connect(self.main.startWidget.quitButton, QtCore.SIGNAL('clicked()'),self.Exit)
        QtCore.QObject.connect(self.main.optionsWidget.quitButton, QtCore.SIGNAL('clicked()'), self.Exit)
        QtCore.QObject.connect(self.main.cannyWidget.quitButton, QtCore.SIGNAL('clicked()'), self.Exit)
        QtCore.QObject.connect(self, QtCore.SIGNAL('lastWindowClosed()'),self.Exit)

    def Exit(self):

        self.exit(0)

if __name__ == '__main__':
    #Create QApplication
    app = App(sys.argv)

    #Enter main loop
    app.exec_()
