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

        self.setFixedSize(600,600)

        #Initialise central widget
        self.I=None
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
    """Initial window."""
    def __init__(self,parent):
        super(StartWindow,self).__init__(parent)

        self.setFixedSize(600,600)

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
        #Create layout
        gridLayout = QtGui.QGridLayout()

        #Add widgets
        gridLayout.addWidget(self.quitButton,6,1,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.fullCannyButton,3,1,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.otherOptionsButton,4,1,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.titleLabel,0,1,QtCore.Qt.AlignCenter)

        #Set layout to window
        self.setLayout(gridLayout)

class OptionsWindow(QtGui.QWidget):
    def __init__(self,parent):
        super(OptionsWindow, self).__init__(parent)
        #Create widgets
        self.createWidgets()

        #Set layout
        self.layout()

        self.setFixedSize(600,600)


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

        self.setFixedSize(600,600)
        self.minutes=0
        self.seconds=0

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
        self.cancelButton = QtGui.QPushButton('Cancel')
        self.cancelButton.hide()
        self.threadLabel = QtGui.QLabel('')
        self.guiTimer = QtCore.QTimer()
        self.timerLabel = QtGui.QLabel('00:00')
        self.showButton = QtGui.QPushButton('Show file')
        self.saveAllButton = QtGui.QPushButton('Save all')

        self.gblurLabel = QtGui.QLabel('Gaussian Blur: not started')
        self.sobelLabel = QtGui.QLabel('Sobel Filter: not started')
        self.nmsLabel = QtGui.QLabel('Non Maximum Suppression: not started')
        self.thresholdLabel = QtGui.QLabel('Thresholding: not started')
        self.hysteresisLabel = QtGui.QLabel('Hysteresis: not started')

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
        self.gblurRadius = QtGui.QComboBox()
        self.gblurRadius.addItems(['3','5','7','9','11'])

        QtCore.QObject.connect(self.backButton, QtCore.SIGNAL('clicked()'), self.parent().fullCannyHideFunction)
        QtCore.QObject.connect(self.openFileButton, QtCore.SIGNAL('clicked()'), self.openFileFunction)
        QtCore.QObject.connect(self.startButton, QtCore.SIGNAL('clicked()'), self.startFunctionCheck)
        QtCore.QObject.connect(self.showButton, QtCore.SIGNAL('clicked()'), self.showOriginalFunc)
        QtCore.QObject.connect(self.gblurSave, QtCore.SIGNAL('clicked()'), lambda: self.saveFunc(self.parent().parent().I.gblur))
        QtCore.QObject.connect(self.gblurShow, QtCore.SIGNAL('clicked()'), lambda: self.showFunc(self.parent().parent().I.gblur, 'gray'))
        QtCore.QObject.connect(self.sobelSave, QtCore.SIGNAL('clicked()'), lambda: self.sobelOptionsFunc(self, 'Save'))
        QtCore.QObject.connect(self.sobelShow, QtCore.SIGNAL('clicked()'), lambda: self.sobelOptionsFunc(self, 'Show'))
        QtCore.QObject.connect(self.nmsSave, QtCore.SIGNAL('clicked()'), lambda: self.saveFunc(self.parent().parent().I.suppressed))
        QtCore.QObject.connect(self.nmsShow, QtCore.SIGNAL('clicked()'), lambda: self.showFunc(self.parent().parent().I.suppressed, 'gray'))
        QtCore.QObject.connect(self.thresholdSave, QtCore.SIGNAL('clicked()'), lambda: self.saveFunc(self.parent().parent().I.thresholded))
        QtCore.QObject.connect(self.thresholdShow, QtCore.SIGNAL('clicked()'), lambda: self.showFunc(self.parent().parent().I.thresholded, 'gray'))
        QtCore.QObject.connect(self.hysteresisSave, QtCore.SIGNAL('clicked()'), lambda: self.saveFunc(self.parent().parent().I.final))
        QtCore.QObject.connect(self.hysteresisShow, QtCore.SIGNAL('clicked()'), lambda: self.showFunc(self.parent().parent().I.final, 'gray'))
        QtCore.QObject.connect(self.saveAllButton, QtCore.SIGNAL('clicked()'), self.saveAllFunc)

    def layout(self):
        #Create layout
        gridLayout = QtGui.QGridLayout()

        #Add widgets
        gridLayout.addWidget(self.fileStatusLabel,0,0,QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.showButton,0,3,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.openFileButton,0,4,QtCore.Qt.AlignCenter)

        gridLayout.addWidget(self.timerLabel,1,0)

        gridLayout.addWidget(QtGui.QLabel('Sigma'),3,1,QtCore.Qt.AlignBottom)
        gridLayout.addWidget(QtGui.QLabel('Radius'),3,2,QtCore.Qt.AlignBottom)
        gridLayout.addWidget(self.startButton,2,0,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.cancelButton,2,0,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.threadLabel,3,0)

        gridLayout.addWidget(self.gblurLabel,4,0)
        gridLayout.addWidget(self.gblurSigma,4,1,QtCore.Qt.AlignVCenter)
        gridLayout.addWidget(self.gblurRadius,4,2,QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(self.sobelLabel,5,0)
        gridLayout.addWidget(self.nmsLabel,6,0)
        #To prevent label from moving show & save widgets
        self.nmsLabel.setMinimumWidth(270)
        gridLayout.addWidget(self.thresholdLabel,7,0)
        gridLayout.addWidget(self.hysteresisLabel,8,0)
        gridLayout.addWidget(self.saveAllButton,9,4,QtCore.Qt.AlignCenter)

        gridLayout.addWidget(self.backButton,10,0,QtCore.Qt.AlignBottom)
        gridLayout.addWidget(self.quitButton,10,4,QtCore.Qt.AlignBottom)


        for i in range(0,2):
            for j in range(0,5):
                gridLayout.addWidget(self.widgets[i][j],j+3,i+3,QtCore.Qt.AlignCenter)

        #Hide show and save buttons
        for i in range(0,2):
            for j in range(0,5):
                self.widgets[i][j].hide()

        self.saveAllButton.hide()

        #Set layout
        self.setLayout(gridLayout)

    def saveAllFunc(self):
        saveDialog = SaveAllDialog(self)
        saveDialog.exec_()

    def dotDotDot(self):
        strList = ['.','..','...']
        return strList[self.seconds % 3]

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

    def showOriginalFunc(self):
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

    def startFunctionCheck(self):
        #Check if no image has been loaded
        if self.parent().parent().I is None:
            #Show error message
            self.errorMessage('No Image Loaded')
        else:
            #Continue
            self.startFunction()

    def startFunction(self):
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

        #Show cancel button
        self.cancelButton.show()
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL('clicked()'), self.terminateThread)

        #Disable start button
        self.startButton.setDisabled(True)
        self.startButton.setWindowOpacity(0.5)

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
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('updateGaussianLabel'),
                lambda: self.updateFromThreadFunc(self.gblurLabel, 'Gaussian Blur: processing.'))
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishGaussian'),
                lambda: self.finishFromThreadFunc(self.gblurLabel, 'Gaussian Blur: complete', self.gblurSave, self.gblurShow))
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('updateSobelLabel'),
                lambda: self.updateFromThreadFunc(self.sobelLabel, 'Sobel Filter: processing.'))
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishSobel'),
                lambda: self.finishFromThreadFunc(self.sobelLabel, 'Sobel Filter: complete', self.sobelSave, self.sobelShow))
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('updateNmsLabel'),
                lambda: self.updateFromThreadFunc(self.nmsLabel, 'Non Maximum Suppression: processing.'))
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishNms'),
                lambda: self.finishFromThreadFunc(self.nmsLabel, 'Non Maximum Suppression: complete', self.nmsSave, self.nmsShow))
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('updateThresholdLabel'),
                lambda: self.updateFromThreadFunc(self.thresholdLabel, 'Thresholding: processing.'))
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishThreshold'),
                lambda: self.finishFromThreadFunc(self.thresholdLabel, 'Thresholding: complete', self.thresholdSave, self.thresholdShow))
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('updateHysteresisLabel'),
                lambda: self.updateFromThreadFunc(self.hysteresisLabel, 'Hysteresis: processing.'))
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishHysteresis'),
                lambda: self.finishFromThreadFunc(self.hysteresisLabel, 'Hysteresis: complete', self.hysteresisSave, self.hysteresisShow, True))
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finished()'), self.finishedThreadFunc)

        #Start threads
        self.worker.start()
        self.update.start()

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
                self.saveAllButton.show()

    def terminateThread(self):
        self.threadLabel.setText('Waiting for thread termination...')
        self.threadLabel.activated = True
        self.worker.stopFlag = True

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


    def finishedThreadFunc(self):
        self.guiTimer.stop()

        self.startButton.setEnabled(True)
        self.startButton.setWindowOpacity(1)

        self.threadLabel.setText('')

        self.cancelButton.hide()

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
                self.saveAllButton.show()

    def openFileFunction(self):
        #Open file dialog and get selected filepath
        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~', 'Image files (*.jpg *.gif *.bmp *.png)')
        if filepath:
            #Store loaded image in Image object
            self.parent().parent().I = Image(np.asarray(im.open(filepath).convert('L'),dtype=np.float))
            #Set file status
            self.parent().parent().fileStatusString = 'File: '+str(filepath.split('/')[-1])
            self.fileStatusLabel.setText(self.parent().parent().fileStatusString)
            self.parent().parent().optionsWidget.fileStatusLabel.setText(self.parent().parent().fileStatusString)

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

        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL('clicked()'), self.exit)
        self.dropDown.activated[str].connect(self.setFileExt)
        QtCore.QObject.connect(self.openDirButton, QtCore.SIGNAL('clicked()'), self.openFileFunc)
        self.gblurName.textChanged.connect(self.updateGblur)
        self.sobelMagName.textChanged.connect(self.updateSmag)
        self.sobelDirName.textChanged.connect(self.updateSdir)
        self.sobelHorizName.textChanged.connect(self.updateShoriz)
        self.sobelVertName.textChanged.connect(self.updateSvert)
        self.nmsName.textChanged.connect(self.updateNms)
        self.thresholdName.textChanged.connect(self.updateThreshold)
        self.hysteresisName.textChanged.connect(self.updateHysteresis)

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

    def updateGblur(self, text):
        self.filenames['gblur'] = text

    def updateSmag(self, text):
        self.filenames['smag'] = text

    def updateSdir(self, text):
        self.filenames['sdir'] = text

    def updateShoriz(self, text):
        self.filenames['shoriz'] = text

    def updateSvert(self, text):
        self.filenames['svert'] = text

    def updateNms(self, text):
        self.filenames['nms'] = text

    def updateThreshold(self, text):
        self.filenames['thresh'] = text

    def updateHysteresis(self, text):
        self.filenames['hyst'] = text

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

        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL('clicked()'), self.exit)

        if dialogType == 'Show':
            QtCore.QObject.connect(self.magnitudeOption, QtCore.SIGNAL('clicked()'), lambda: self.parent().showFunc(self.parent().parent().parent().I.smagnitude, 'gray'))
            QtCore.QObject.connect(self.directionOption, QtCore.SIGNAL('clicked()'), lambda: self.parent().showFunc(self.parent().parent().parent().I.sdirection, 'gist_rainbow'))
            QtCore.QObject.connect(self.horizontalOption, QtCore.SIGNAL('clicked()'), lambda: self.parent().showFunc(self.parent().parent().parent().I.shgradient, 'gray'))
            QtCore.QObject.connect(self.verticalOption, QtCore.SIGNAL('clicked()'), lambda: self.parent().showFunc(self.parent().parent().parent().I.svgradient, 'gray'))
        if dialogType == 'Save':
            QtCore.QObject.connect(self.magnitudeOption, QtCore.SIGNAL('clicked()'), lambda: self.parent().saveFunc(self.parent().parent().parent().I.smagnitude))

            QtCore.QObject.connect(self.directionOption, QtCore.SIGNAL('clicked()'), lambda: self.parent().saveFunc(self.parent().parent().parent().I.sdirection))
            QtCore.QObject.connect(self.horizontalOption, QtCore.SIGNAL('clicked()'), lambda: self.parent().saveFunc(self.parent().parent().parent().I.shgradient))
            QtCore.QObject.connect(self.verticalOption, QtCore.SIGNAL('clicked()'), lambda: self.parent().saveFunc(self.parent().parent().parent().I.svgradient))

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

        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL('clicked()'), self.exit)

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
        #Do stuff here
        try: #Add more if not self.StopFlag around the updating things
            if not self.stopFlag:
                #Gaussian
                self.emit(QtCore.SIGNAL('updateGaussianLabel'))
                self.parent().parent().parent().I.gaussian_(1,5)
                self.emit(QtCore.SIGNAL('finishGaussian'))

            if not self.stopFlag:
                #Sobel
                self.emit(QtCore.SIGNAL('updateSobelLabel'))
                self.parent().parent().parent().I.sobel_()
                self.emit(QtCore.SIGNAL('finishSobel'))

            if not self.stopFlag:
                #NMS
                self.emit(QtCore.SIGNAL('updateNmsLabel'))
                self.parent().parent().parent().I.nms_()
                self.emit(QtCore.SIGNAL('finishNms'))

            if not self.stopFlag:
                #Threshold
                self.emit(QtCore.SIGNAL('updateThresholdLabel'))
                self.parent().parent().parent().I.threshold_()
                self.emit(QtCore.SIGNAL('finishThreshold'))

            if not self.stopFlag:
                #Hysteresis
                self.emit(QtCore.SIGNAL('updateHysteresisLabel'))
                self.parent().parent().parent().I.hysteresis_()
                self.emit(QtCore.SIGNAL('finishHysteresis'))

            #Stop thread
            self.running = False

        #If there is an exception, display and then stop the thread
        except Exception as e:
            print(e)
            self.running = False

    def __del__(self):
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
    sys.exit()
