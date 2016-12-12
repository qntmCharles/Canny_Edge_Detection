import sys, time
from PyQt4 import QtCore, QtGui
from PIL import Image as im
import numpy as np

#Force matplotlib to use qt4 backends
from matplotlib import use
use('Qt4Agg')

from matplotlib import pyplot as plt
#Matplotlib backends for qt4 to show images
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure

#Import Image class
from main import Image

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

class CannyWindow(QtGui.QWidget):
    def __init__(self, parent):
        super(CannyWindow, self).__init__(parent)
        #Create widgets
        self.createWidgets()

        #Set layout
        self.layout()

        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+C"), self, self.terminateThread)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+O"), self, self.openFileFunc)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self, self.startFunctionCheck)

        self.setFixedSize(750,600)
        self.worker = None
        self.I = None
        self.sigma = 1.0
        self.radius = 5
        self.lowThresh = 0.275 #OF highThresh - effective low threshold is low * high
        self.highThresh = 0.25
        self.minutes = 0
        self.seconds = 0

    def createWidgets(self):
        self.widgets = [[],[]]
        #Define widgets
        fileStatusFont = QtGui.QFont()
        fileStatusFont.setPointSize(15)
        self.fileStatusLabel = QtGui.QLabel('')
        self.fileStatusLabel.setText('File: not loaded')
        self.fileStatusLabel.setFont(fileStatusFont)

        self.openFileButton = QtGui.QPushButton('Open file')
        self.quitButton = QtGui.QPushButton('Quit')
        self.startButton = QtGui.QPushButton('Start')
        self.cancelButton = QtGui.QPushButton('Cancel')
        self.cancelButton.hide()
        self.threadLabel = QtGui.QLabel('')
        self.guiTimer = QtCore.QTimer()

        self.timerLabel = QtGui.QLabel('00:00')
        timerLabelFont = QtGui.QFont()
        timerLabelFont.setPointSize(18)
        self.timerLabel.setFont(timerLabelFont)
        self.timerLabel.setMaximumWidth(88)
        self.timerLabel.setStyleSheet("border: 2px solid")

        self.showFileButton = QtGui.QPushButton('Show file')
        self.saveAllButton = QtGui.QPushButton('Save all')

        self.resetButton = QtGui.QPushButton('Reset')
        self.resetButton.setMaximumWidth(80)
        self.resetButton.hide()

        self.gblurSigmaLabel = QtGui.QLabel('Sigma')
        self.gblurRadiusLabel = QtGui.QLabel('Radius')

        labelFont = QtGui.QFont()
        labelFont.setPointSize(11)
        self.gblurLabel = QtGui.QLabel('Gaussian Blur: not started')
        self.gblurLabel.setFont(labelFont)
        self.sobelLabel = QtGui.QLabel('Sobel Filter: not started')
        self.sobelLabel.setFont(labelFont)
        self.nmsLabel = QtGui.QLabel('Non Maximum Suppression: not started')
        self.nmsLabel.setFont(labelFont)
        self.threshLowLabel = QtGui.QLabel('Low')
        self.threshHighLabel = QtGui.QLabel('High')
        self.thresholdLabel = QtGui.QLabel('Thresholding: not started')
        self.thresholdLabel.setFont(labelFont)
        self.hysteresisLabel = QtGui.QLabel('Hysteresis: not started')
        self.hysteresisLabel.setFont(labelFont)

        self.gblurLabel.activated = False
        self.sobelLabel.activated = False
        self.nmsLabel.activated = False
        self.thresholdLabel.activated = False
        self.hysteresisLabel.activated = False
        self.threadLabel.activated = False

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

        self.gblurSigma = QtGui.QComboBox()
        self.gblurSigma.addItems(['0.5','0.6','0.7','0.8','0.9','1.0','1.1','1.2','1.3','1.4','1.5','2.0','2.5','3.0'])
        self.gblurSigma.setCurrentIndex(5)
        #Force widget to be width 70
        self.gblurSigma.setMaximumWidth(70)
        self.gblurSigma.setMinimumWidth(70)

        self.gblurRadius = QtGui.QComboBox()
        self.gblurRadius.addItems(['3','5','7','9','11'])
        self.gblurRadius.setCurrentIndex(1)
        #Force widget to be width 70
        self.gblurRadius.setMaximumWidth(70)
        self.gblurRadius.setMinimumWidth(70)

        self.threshLow = QtGui.QLineEdit('0.275')
        self.threshLow.setMaximumWidth(70)
        self.threshHigh = QtGui.QLineEdit('0.25')
        self.threshHigh.setMaximumWidth(70)

        self.openFileButton.clicked.connect(self.openFileFunc)
        self.startButton.clicked.connect(self.startFunctionCheck)
        self.showFileButton.clicked.connect(lambda: self.showFunc(self.I.original, 'gray'))
        self.threshLow.textChanged.connect(lambda: self.updateThresholds('low', self.threshLow.text()))
        self.threshHigh.textChanged.connect(lambda: self.updateThresholds('high', self.threshHigh.text()))
        self.gblurSave.clicked.connect(lambda: self.saveFunc(self.I.gblur))
        self.gblurShow.clicked.connect(lambda: self.showFunc(self.I.gblur, 'gray'))
        self.sobelSave.clicked.connect(lambda: self.sobelOptionsFunc('Save'))
        self.sobelShow.clicked.connect(lambda: self.sobelOptionsFunc('Show'))
        self.nmsSave.clicked.connect(lambda: self.saveFunc(self.I.suppressed))
        self.nmsShow.clicked.connect(lambda: self.showFunc(self.I.suppressed, 'gray'))
        self.thresholdSave.clicked.connect(lambda: self.saveFunc(self.I.thresholded))
        self.thresholdShow.clicked.connect(lambda: self.showFunc(self.I.thresholded, 'gray'))
        self.hysteresisShow.clicked.connect(lambda: self.showFunc(self.I.final, 'gray'))
        self.saveAllButton.clicked.connect(self.saveAllFunc)
        self.cancelButton.clicked.connect(self.terminateThread)
        self.resetButton.clicked.connect(self.resetFunc)

    def layout(self):
        #Create layout
        gridLayout = QtGui.QGridLayout()

        #Add widgets
        gridLayout.addWidget(self.fileStatusLabel,0,0,QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.showFileButton,0,3,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.openFileButton,0,4,QtCore.Qt.AlignCenter)

        gridLayout.addWidget(self.timerLabel,1,0)

        hline = QtGui.QFrame()
        hline.setFrameShape(QtGui.QFrame.HLine)
        hline.setFrameShadow(QtGui.QFrame.Plain)
        gridLayout.addWidget(hline,2,0,2,-1,QtCore.Qt.AlignTop)

        self.startCancelLayout = QtGui.QHBoxLayout()
        self.startCancelLayout.addWidget(self.startButton)
        self.startCancelLayout.addWidget(self.cancelButton)
        gridLayout.addLayout(self.startCancelLayout,2,0,2,-1,QtCore.Qt.AlignCenter)

        gridLayout.addWidget(self.threadLabel,3,0)
        #gridLayout.addWidget(self.gblurSigmaLabel,3,1,QtCore.Qt.AlignBottom)
        #gridLayout.addWidget(self.gblurRadiusLabel,3,2,QtCore.Qt.AlignBottom)

        gridLayout.addWidget(self.gblurLabel,4,0)
        self.gblurLayout = QtGui.QFormLayout()
        self.gblurLayout.addRow(QtGui.QLabel('Gaussian Parameters'))
        self.gblurLayout.addRow(self.gblurSigmaLabel,self.gblurRadiusLabel)
        self.gblurLayout.addRow(self.gblurSigma, self.gblurRadius)
        gridLayout.addLayout(self.gblurLayout, 4,1,1,2)
        #gridLayout.addWidget(self.gblurSigma,4,1,QtCore.Qt.AlignVCenter)
        #igridLayout.addWidget(self.gblurRadius,4,2,QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(self.sobelLabel,5,0)
        gridLayout.addWidget(self.nmsLabel,6,0)

        #gridLayout.addWidget(self.threshLowLabel,6,1,QtCore.Qt.AlignBottom)
        #gridLayout.addWidget(self.threshHighLabel,6,2,QtCore.Qt.AlignBottom)

        #To prevent label from moving show & save widgets
        self.nmsLabel.setMinimumWidth(350)

        self.threshLayout = QtGui.QFormLayout()
        self.threshLayout.addRow(QtGui.QLabel('Thresholds'))
        self.threshLayout.addRow(self.threshLowLabel, self.threshHighLabel)
        self.threshLayout.addRow(self.threshLow, self.threshHigh)

        gridLayout.addWidget(self.thresholdLabel,7,0)
        gridLayout.addLayout(self.threshLayout,7,1,1,2)
        #gridLayout.addWidget(QtGui.QLabel('Thresholds'),6,1)
        #gridLayout.addWidget(self.threshLow,7,1,QtCore.Qt.AlignVCenter)
        #gridLayout.addWidget(self.threshHigh,7,2,QtCore.Qt.AlignVCenter)
        gridLayout.addWidget(self.hysteresisLabel,8,0)

        gridLayout.addWidget(self.saveAllButton,9,4,QtCore.Qt.AlignCenter)

        gridLayout.addWidget(self.resetButton,10,0,QtCore.Qt.AlignBottom)
        gridLayout.addWidget(self.quitButton,10,4,QtCore.Qt.AlignBottom)

        for i in range(0,2):
            for j in range(0,5):
                gridLayout.addWidget(self.widgets[i][j],j+4,i+3,QtCore.Qt.AlignCenter)

        #Hide show and save buttons
        for i in range(0,2):
            for j in range(0,5):
                self.widgets[i][j].hide()

        self.saveAllButton.hide()
        self.showFileButton.hide()

        #Set layout
        self.setLayout(gridLayout)

    def updateThresholds(self, threshold, text):
        flag = True
        try:
            text = float(text)
        except:
            self.errorMessage('Thresholds Must Be Numerical')
            flag = False

        if flag:
            if (text>1) or (text<0):
                self.errorMessage('Thresholds Must Be Between 0 and 1')

            if threshold == 'low':
                self.lowThresh = text
            else:
                self.highThresh = text


    def resetFunc(self):
        self.saveAllButton.hide()

        for i in range(0,2):
            for j in range(0,5):
                self.widgets[i][j].hide()

        self.I.__init__(self.I.original)
        self.timerLabel.setText('00:00')
        self.resetButton.hide()

    def terminateThread(self):
        if self.worker:
            #Tell worker to stop running
            self.worker.stopFlag = True

            #Disconnect all connections with worker
            self.worker.finished.disconnect(self.finishedThreadFunc)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL('updateGaussianLabel'), self.gblurUpdateConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL('finishGaussian'), self.gblurFinishConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL('updateSobelLabel'), self.sobelUpdateConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL('finishSobel'), self.sobelFinishConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL('updateNmsLabel'), self.nmsUpdateConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL('finishNms'), self.nmsFinishConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL('updateThresholdLabel'), self.threshUpdateConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL('finishThreshold'), self.threshFinishConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL('updateHysteresisLabel'), self.hystUpdateConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL('finishHysteresis'), self.hystFinishConnection)

            #Remove reference to current worker
            self.worker = None

            self.gblurLabel.activated = False
            self.sobelLabel.activated = False
            self.nmsLabel.activated = False
            self.thresholdLabel.activated = False
            self.hysteresisLabel.activated = False

            self.gblurLabel.setText('Gaussian Blur: not started')
            self.sobelLabel.setText('Sobel Filter: not started')
            self.nmsLabel.setText('Non Maximum Suppression: not started')
            self.thresholdLabel.setText('Thresholding: not started')
            self.hysteresisLabel.setText('Hysteresis: not started')

            self.guiTimer.stop()
            self.timerLabel.setText('00:00')
            self.finishedThreadFunc()
        else:
            self.errorMessage('Thread Does Not Exist')

    def finishedThreadFunc(self):
        self.guiTimer.stop()
        self.guiTimer.timeout.disconnect(self.updateStrings)
        self.guiTimer.timeout.disconnect(self.updateTimer)

        self.threadLabel.activated=False
        self.threadLabel.setText('')

        self.startButton.show()
        self.cancelButton.hide()
        self.resetButton.show()
        self.cancelButton.setEnabled(True)
        self.cancelButton.setWindowOpacity(1)

    def saveAllFunc(self):
        saveDialog = SaveAllDialog(self)
        saveDialog.exec_()

    def dotDotDot(self):
        strList = ['.','..','...']
        return strList[self.seconds % 3]

    #Change this to a lambda in connect
    def showOriginalFunc(self):
        #Ask liam about this - technically it's exception handling but I /know/ it won't be needed - do I keep it?
        if self.parent().parent().I is None:
            self.errorMessage('No Image Loaded')
        else:
            self.showFunc(self.parent().parent().I.original,'gray')

    def showFunc(self, image, colourmap):
        try:
            self.showImage = mplWindow(image, colourmap)
            self.showImage.exec_()
        except Exception as e:
            print(e)
            self.errorMessage('Exception Occured')

    def saveFunc(self, image):
        filepath = QtGui.QFileDialog.getSaveFileName(self, 'Save file', '~', 'Image files (*.jpg *.gif *.bmp *.png)')
        if filepath:
            try:
                im.fromarray(image.astype(np.uint8)).save(filepath)
            except Exception as e:
                print(e)
                self.errorMessage('Exception Occured')

    def sobelOptionsFunc(self, dialogType):
        dialog = SobelOptionsDialog(self, dialogType)
        dialog.exec_()

    def updateTimer(self):
        self.seconds += 1
        if self.seconds == 60:
            self.seconds=0
            self.minutes += 1

        minutesString = "{0:02d}".format(self.minutes)
        secondsString = "{0:02d}".format(self.seconds)
        self.timerLabel.setText(minutesString+':'+secondsString)

    def errorMessage(self, message):
        #Set up and display error message
        errorMsg = QtGui.QMessageBox()
        errorMsg.setIcon(QtGui.QMessageBox.Warning)
        errorMsg.setText(message)
        errorMsg.setStandardButtons(QtGui.QMessageBox.Ok)
        errorMsg.setDefaultButton(QtGui.QMessageBox.Ok)
        errorMsg.setEscapeButton(QtGui.QMessageBox.Ok)
        errorMsg.exec_()

    def updateFromThreadFunc(self, label, labelText):
        if not self.worker.stopFlag:
            label.setText(labelText)
            label.activated = True

    def finishFromThreadFunc(self, label, labelText, saveButton, showButton, flag=False):
        if not self.worker.stopFlag:
            label.activated = False
            label.setText(labelText)
            saveButton.show()
            showButton.show()
            if flag:
                #Show saveAllButton here - saves trouble when using finishThread function elsewhere
                self.saveAllButton.show()

    def openFileFunc(self):
        #Open file dialog and get selected filepath
        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~', 'Image files (*.jpg *.gif *.bmp *.png)')
        if filepath:
            #Store loaded image in Image object
            self.I = Image(np.asarray(im.open(filepath).convert('L'),dtype=np.float))
            #Set file status
            self.fileStatusLabel.setText('File: '+str(filepath.split('/')[-1]))

            #Show 'show file' button
            self.showFileButton.show()

    def startFunctionCheck(self):
        #Check if no image has been loaded
        if self.I is None:
            #Show error message
            self.errorMessage('No Image Loaded')
        else:
            #Continue
            self.startFunction()

    def updateStrings(self):
        if self.gblurLabel.activated:
            self.gblurLabel.setText('Gaussian Blur: processing'+self.dotDotDot())
        if self.sobelLabel.activated:
            self.sobelLabel.setText('Sobel Filter: processing'+self.dotDotDot())
        if self.nmsLabel.activated:
            self.nmsLabel.setText('Non Maximum Suppression: processing'+self.dotDotDot())
        if self.thresholdLabel.activated:
            self.thresholdLabel.setText('Thresholding: processing'+self.dotDotDot())
        if self.hysteresisLabel.activated:
            self.hysteresisLabel.setText('Hysteresis: processing'+self.dotDotDot())
        if self.threadLabel.activated:
            self.threadLabel.setText('Waiting for thread termination'+self.dotDotDot())

    def startFunction(self):
        #Ensure no data from previous processes
        self.resetFunc()

        #Timer
        self.seconds = 0
        self.minutes = 0
        self.timerLabel.setText('00:00')
        self.guiTimer.timeout.connect(self.updateTimer)
        self.guiTimer.timeout.connect(self.updateStrings)
        self.guiTimer.start(1000)

        #Define threads
        self.worker = WorkerThread(self)
        self.update = BackgroundThread(self.worker, self)

        #Show/hide necessary buttons
        self.cancelButton.show()
        self.startButton.hide()

        #Define custom signals
        updateGaussianLabel = QtCore.pyqtSignal()
        finishGaussian = QtCore.pyqtSignal()
        updateSobelLabel = QtCore.pyqtSignal()
        finishSobel = QtCore.pyqtSignal()
        updateNmsLabel = QtCore.pyqtSignal()
        finishNms = QtCore.pyqtSignal()
        updateThresholdLabel = QtCore.pyqtSignal()
        finishThreshold = QtCore.pyqtSignal()
        updateHysteresisLabel = QtCore.pyqtSignal()
        finishHysteresis = QtCore.pyqtSignal()

        #Connect signals
        self.gblurUpdateConnection = lambda: self.updateFromThreadFunc(self.gblurLabel, 'Gaussian Blur: processing.')
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('updateGaussianLabel'), self.gblurUpdateConnection)
        self.gblurFinishConnection = lambda: self.finishFromThreadFunc(self.gblurLabel, 'Gaussian Blur: complete', self.gblurSave, self.gblurShow)
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishGaussian'), self.gblurFinishConnection)

        self.sobelUpdateConnection = lambda: self.updateFromThreadFunc(self.sobelLabel, 'Sobel Filter: processing.')
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('updateSobelLabel'), self.sobelUpdateConnection)
        self.sobelFinishConnection = lambda: self.finishFromThreadFunc(self.sobelLabel, 'Sobel Filter: complete', self.sobelSave, self.sobelShow)
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishSobel'), self.sobelFinishConnection)

        self.nmsUpdateConnection = lambda: self.updateFromThreadFunc(self.nmsLabel, 'Non Maximum Suppression: processing.')
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('updateNmsLabel'), self.nmsUpdateConnection)
        self.nmsFinishConnection = lambda: self.finishFromThreadFunc(self.nmsLabel, 'Non Maximum Suppression: complete', self.nmsSave, self.nmsShow)
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishNms'), self.nmsFinishConnection)

        self.threshUpdateConnection = lambda: self.updateFromThreadFunc(self.thresholdLabel, 'Thresholding: processing.')
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('updateThresholdLabel'), self.threshUpdateConnection)
        self.threshFinishConnection = lambda: self.finishFromThreadFunc(self.thresholdLabel, 'Thresholding: complete', self.thresholdSave, self.thresholdShow)
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishThreshold'), self.threshFinishConnection)

        self.hystUpdateConnection = lambda: self.updateFromThreadFunc(self.hysteresisLabel, 'Hysteresis: processing.')
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('updateHysteresisLabel'), self.hystUpdateConnection)
        self.hystFinishConnection = lambda: self.finishFromThreadFunc(self.hysteresisLabel, 'Hysteresis: complete', self.hysteresisSave, self.hysteresisShow, True)
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishHysteresis'), self.hystFinishConnection)

        self.worker.finished.connect(self.finishedThreadFunc)

        #Start threads
        self.worker.start()
        self.update.start()

class SaveAllDialog(QtGui.QDialog):
    def __init__(self, parent):
        super(SaveAllDialog, self).__init__(parent)

        self.fileExt = '.bmp'
        self.filenames={'gblur':'gblur', 'smag':'sobel_mag', 'sdir':'sobel_dir', 'shoriz':'sobel_horiz', 'svert':'sobel_vert', 'nms':'nms', 'thresh':'threshold', 'hyst':'hysteresis'}
        self.filepath = None

        self.createWidgets()

        self.layout()

    def createWidgets(self):
        self.openDirButton = QtGui.QPushButton('Select Directory')
        self.gblurOption = QtGui.QCheckBox('Gaussian Blur')
        self.gblurName = QtGui.QLineEdit('gblur')
        self.sobelMagOption = QtGui.QCheckBox('Sobel Gradient Magnitude')
        self.sobelMagName = QtGui.QLineEdit('sobel_mag')
        self.sobelDirOption = QtGui.QCheckBox('Sobel Gradient Direction')
        self.sobelDirName = QtGui.QLineEdit('sobel_dir')
        self.sobelHorizOption = QtGui.QCheckBox('Sobel Horizontal Gradient')
        self.sobelHorizName = QtGui.QLineEdit('sobel_horiz')
        self.sobelVertOption = QtGui.QCheckBox('Sobel Vertical Gradient')
        self.sobelVertName = QtGui.QLineEdit('sobel_vert')
        self.nmsOption = QtGui.QCheckBox('Non Maximum Suppression')
        self.nmsName = QtGui.QLineEdit('nms')
        self.thresholdOption = QtGui.QCheckBox('Threshold')
        self.thresholdName = QtGui.QLineEdit('threshold')
        self.hysteresisOption = QtGui.QCheckBox('Hysteresis')
        self.hysteresisName = QtGui.QLineEdit('hysteresis')

        self.gblurOption.setChecked(True)
        self.sobelMagOption.setChecked(True)
        self.sobelDirOption.setChecked(True)
        self.sobelHorizOption.setChecked(True)
        self.sobelVertOption.setChecked(True)
        self.nmsOption.setChecked(True)
        self.thresholdOption.setChecked(True)
        self.hysteresisOption.setChecked(True)

        self.dropDown = QtGui.QComboBox(self)
        self.dropDown.addItem('.bmp')
        self.dropDown.addItem('.jpg')
        self.dropDown.addItem('.png')
        self.dropDown.addItem('.gif')
        self.dropDown.setCurrentIndex(0)

        self.saveButton = QtGui.QPushButton('Save')
        self.saveButton.setMaximumWidth(80)
        self.closeButton = QtGui.QPushButton('Close')
        self.closeButton.setMaximumWidth(80)

        self.closeButton.clicked.connect(self.exit)
        self.dropDown.activated[str].connect(self.setFileExt)
        self.openDirButton.clicked.connect(self.openFileFunc)

        self.gblurName.textChanged.connect(lambda: self.updateFilename('gblur', self.gblurName.text()))
        self.sobelMagName.textChanged.connect(lambda: self.updateFilename('smag', self.sobelMagName.text()))
        self.sobelDirName.textChanged.connect(lambda: self.updateFilename('sdir', self.sobelDirName.text()))
        self.sobelHorizName.textChanged.connect(lambda: self.updateFilename('shoriz', self.sobelHorizName.text()))
        self.sobelVertName.textChanged.connect(lambda: self.updateFilename('svert', self.sobelVertName.text()))
        self.nmsName.textChanged.connect(lambda: self.updateFilename('nms', self.nmsName.text()))
        self.thresholdName.textChanged.connect(lambda: self.updateFilename('thresh', self.thresholdName.text()))
        self.hysteresisName.textChanged.connect(lambda: self.updateFilename('hyst', self.hysteresisName.text()))

    def layout(self):
        formLayout = QtGui.QFormLayout()

        openDirLayout = QtGui.QGridLayout()
        openDirLayout.addWidget(self.openDirButton,0,0,QtCore.Qt.AlignCenter)
        formLayout.addRow(openDirLayout)

        filenameLabel = QtGui.QGridLayout()
        filenameLabel.addWidget(QtGui.QLabel('Filename'))
        formLayout.addRow('Select images to save', filenameLabel)

        formLayout.addRow(self.gblurOption, self.gblurName)
        formLayout.addRow(self.sobelMagOption, self.sobelMagName)
        formLayout.addRow(self.sobelDirOption, self.sobelDirName)
        formLayout.addRow(self.sobelHorizOption, self.sobelHorizName)
        formLayout.addRow(self.sobelVertOption, self.sobelVertName)
        formLayout.addRow(self.nmsOption, self.nmsName)
        formLayout.addRow(self.thresholdOption, self.thresholdName)
        formLayout.addRow(self.hysteresisOption, self.hysteresisName)
        formLayout.addRow('File Extension', self.dropDown)

        buttonsLayout = QtGui.QGridLayout()
        buttonsLayout.addWidget(self.saveButton,0,0,QtCore.Qt.AlignCenter)
        buttonsLayout.addWidget(self.closeButton,1,0,QtCore.Qt.AlignCenter)
        formLayout.addRow(buttonsLayout)

        self.setLayout(formLayout)

    def openFileFunc(self):
        fileDialog = QtGui.QFileDialog(self)
        fileDialog.setFileMode(QtGui.QFileDialog.Directory)
        fileDialog.setOption(QtGui.QFileDialog.ShowDirsOnly, True)

        if fileDialog.exec_():
            self.filepath = fileDialog.selectedFiles()[0]

    def saveFiles(self):
        if self.filepath is None:
            self.parent().errorMessage('No Directory Selected')
        else:
            if self.gblurOption.isChecked():
                data = self.parent().parent().parent().I.gblur
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+self.filenames['gblur']+self.fileExt)
            if self.sobelMagOption.isChecked():
                data = self.parent().parent().parent().I.smagnitude
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+self.filenames['smag']+self.fileExt)
            if self.sobelDirOption.isChecked():
                data = self.parent().parent().parent().I.sdirection
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+self.filenames['sdir']+self.fileExt)
            if self.sobelHorizOption.isChecked():
                data = self.parent().parent().parent().I.shgradient
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+self.filenames['shoriz']+self.fileExt)
            if self.sobelVertOption.isChecked():
                data = self.parent().parent().parent().I.svgradient
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+self.filenames['svert']+self.fileExt)
            if self.nmsOption.isChecked():
                data = self.parent().parent().parent().I.suppressed
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+self.filenames['nms']+self.fileExt)
            if self.thresholdOption.isChecked():
                data = self.parent().parent().parent().I.thresholded
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+self.filenames['thresh']+self.fileExt)
            if self.hysteresisOption.isChecked():
                data = self.parent().parent().parent().I.final
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+self.filenames['hyst']+self.fileExt)

    def exit(self):
        self.close()

    def updateFilename(self, key, text):
        self.filenames[key] = text
        print(text)

    def setFileExt(self, text):
        self.fileExt = text

class SobelOptionsDialog(QtGui.QDialog):
    def __init__(self, parent, dialogType):
        super(SobelOptionsDialog, self).__init__(parent)

        self.setWindowTitle('Show Images')

        self.createWidgets(dialogType)

        self.layout()

    def createWidgets(self, dialogType):
        self.magnitudeLabel = QtGui.QLabel('Gradient Magnitude')
        self.directionLabel = QtGui.QLabel('Gradient Direction')
        self.horizontalLabel = QtGui.QLabel('Horizontal Gradient')
        self.verticalLabel = QtGui.QLabel('Vertical Gradient')

        #Connect these to the saving function
        self.magnitudeOption = QtGui.QPushButton(dialogType)
        self.directionOption = QtGui.QPushButton(dialogType)
        self.horizontalOption = QtGui.QPushButton(dialogType)
        self.verticalOption = QtGui.QPushButton(dialogType)
        self.closeButton = QtGui.QPushButton('Close')

        self.closeButton.clicked.connect(self.exit)

        if dialogType == 'Show':
            func = self.parent().showFunc
            self.magnitudeOption.clicked.connect(lambda: func(self.parent().I.smagnitude, 'gray'))
            self.directionOption.clicked.connect(lambda: func(self.parent().I.sdirection, 'gist_rainbow'))
            self.horizontalOption.clicked.connect(lambda: func(self.parent().I.shgradient, 'gray'))
            self.verticalOption.clicked.connect(lambda: func(self.parent().I.svgradient,  'gray'))
        else:
            func = self.parent().saveFunc
            self.magnitudeOption.clicked.connect(lambda: func(self.parent().I.smagnitude))
            self.directionOption.clicked.connect(lambda: func(self.parent().I.sdirection))
            self.horizontalOption.clicked.connect(lambda: func(self.parent().I.shgradient))
            self.verticalOption.clicked.connect(lambda: func(self.parent().I.svgradient))
        #Ask Liam: is it better to pass the data, rather than accessing it through the parent? encapsulation 'n' stuff? also interfaces

    def layout(self):
        #Create layout
        boxLayout = QtGui.QGridLayout()

        boxLayout.addWidget(self.magnitudeLabel,0,0)
        boxLayout.addWidget(self.magnitudeOption,0,1)
        boxLayout.addWidget(self.directionLabel,1,0)
        boxLayout.addWidget(self.directionOption,1,1)
        boxLayout.addWidget(self.horizontalLabel,2,0)
        boxLayout.addWidget(self.horizontalOption,2,1)
        boxLayout.addWidget(self.verticalLabel,3,0)
        boxLayout.addWidget(self.verticalOption,3,1)
        boxLayout.addWidget(self.closeButton,4,1)

        self.setLayout(boxLayout)

    def exit(self):
        self.close()

class mplCanvas(FigCanvas):
    """Figure canvas to show matplotlib imshow plot"""
    def __init__(self, parent, data, colourmap):
        fig = Figure(figsize=(5,4))
        self.axes = fig.add_subplot(111)
        FigCanvas.__init__(self,fig)
        self.setParent(parent)
        image = self.axes.imshow(data, cmap=colourmap)
        fig.colorbar(image)
        FigCanvas.updateGeometry(self)

class navigationToolbar(NavBar):
    "A modified version of matplotlib Navigation Toolbar, to remove unneeded buttons."""
    toolitems = [item for item in NavBar.toolitems if item[0] in ('Home', 'Pan', 'Zoom')]
    def __init__(self, *args, **kwargs):
        super(navigationToolbar, self).__init__(*args, **kwargs)
        toolbarActions = self.findChildren(QtGui.QAction)
        for action in toolbarActions:
            if action.text() == 'Customize':
                self.removeAction(action)
                break

class mplWindow(QtGui.QDialog):
    """Dialog to contain matplotlib figure canvas"""
    def __init__(self, figureData, colourmap):
        super(mplWindow, self).__init__()

        self.display = mplCanvas(self, figureData, colourmap)
        self.toolbar = navigationToolbar(self.display, self)
        self.closeButton = QtGui.QPushButton('Close')

        self.closeButton.clicked.connect(self.exit)

        boxLayout = QtGui.QVBoxLayout()
        boxLayout.addWidget(self.toolbar)
        boxLayout.addWidget(self.display)
        boxLayout.addWidget(self.closeButton)
        self.setLayout(boxLayout)

    def exit(self):
        self.close()

class WorkerThread(QtCore.QThread):
    '''Handles processing and functionality'''
    def __init__(self, parent):
        super(WorkerThread, self).__init__(parent)

        self.running = True
        self.stopFlag = False

    def run(self):
        '''Starts the thread doing work when inbuilt start() is called'''
        try:
            if not self.stopFlag:
                #Gaussian
                self.emit(QtCore.SIGNAL('updateGaussianLabel'))
                sigma = float(self.parent().gblurSigma.currentText())
                radius = int(self.parent().gblurRadius.currentText())
                self.parent().I.gaussian_(sigma, radius)
                self.emit(QtCore.SIGNAL('finishGaussian'))

            if not self.stopFlag:
                #Sobel
                self.emit(QtCore.SIGNAL('updateSobelLabel'))
                self.parent().I.sobel_()
                self.emit(QtCore.SIGNAL('finishSobel'))

            if not self.stopFlag:
                #NMS
                self.emit(QtCore.SIGNAL('updateNmsLabel'))
                self.parent().I.nms_()
                self.emit(QtCore.SIGNAL('finishNms'))

            if not self.stopFlag:
                #Threshold
                self.emit(QtCore.SIGNAL('updateThresholdLabel'))
                self.parent().I.threshold_(self.parent().lowThresh, self.parent().highThresh)
                self.emit(QtCore.SIGNAL('finishThreshold'))

            if not self.stopFlag:
                #Hysteresis
                self.emit(QtCore.SIGNAL('updateHysteresisLabel'))
                self.parent().I.hysteresis_()
                self.emit(QtCore.SIGNAL('finishHysteresis'))

            #Stop thread
            self.running = False

        #If there is an exception, display and then stop the thread
        except Exception as e:
            print(e)
            self.running = False

    def __del__(self):
        print('this got called')
        #Set stopping flag
        self.stopFlag = True
        #Wait for thread to finish processing before terminating
        self.wait()

class BackgroundThread(QtCore.QThread):
    '''Keeps the GUI responsive by updating the main loop'''
    def __init__(self, worker, parent):
        super(BackgroundThread, self).__init__(parent)

        #Assign worker to this thread
        self.worker = worker

    def run(self):
        '''Starts the thread doing work when inbuilt start() is called'''
        #Update GUI every 0.1 seconds to prevent GUI lock
        while self.worker.running:
            App.processEvents()
            time.sleep(0.1)

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

if __name__ == '__main__':
    #Create QApplication
    app = App(sys.argv)

    #Enter main loop
    app.exec_()
    sys.exit()
