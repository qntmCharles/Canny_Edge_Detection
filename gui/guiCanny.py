from PyQt4 import QtCore, QtGui
from PIL import Image as im
import numpy as np
from canny.imageClass import Image
from .guiMpl import mplWindow
from .guiSobelDialog import SobelOptionsDialog
from .guiThreads import BackgroundThread, WorkerThread
from .guiSaveDialog import SaveAllDialog

class CannyWindow(QtGui.QWidget):
    """
        Class that acts as the main window for the program

        Inherits core widget functionality from QtGui.QWidget
    """
    def __init__(self):
        # Initialise superclass
        super(CannyWindow, self).__init__()

        # Set window title
        self.setWindowTitle("Canny Edge Detection")

        # Create widgets
        self.createWidgets()

        # Set layout
        self.layout()

        # Add common key shortcuts
        # Stop processing
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+C"), self, self.terminateThread)
        # Open file
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+O"), self, self.openFileFunc)
        # Start processing
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self, self.startFunctionCheck)
        # Quit program
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self, self.close)

        # Set size of GUI
        self.setFixedSize(750,600)

        # Initialise variables
        self.worker = None
        self.I = None
        self.sigma = 1.0
        self.width = 5
        self.lowThreshRatio = 0.275
        self.highThreshRatio = 0.25
        self.minutes = 0
        self.seconds = 0

    def createWidgets(self):
        """
            Function to create the widgets for the GUI

            NB: widgets, in PyQt, are 'things' that do 'stuff'
            NB: some widgets or associated variables are not defined using
            'self.' since they will not need to be referenced elsewhere in
            the program
        """
        # Initialise an empty list of lists to hold similar widgets for easy
        # modification
        self.widgets = [[],[]]

        # Define widgets
        # File status label
        fileStatusFont = QtGui.QFont()
        fileStatusFont.setPointSize(15)
        self.fileStatusLabel = QtGui.QLabel('')
        self.fileStatusLabel.setText('File: not loaded')
        self.fileStatusLabel.setFont(fileStatusFont)

        # Create buttons for opening the file dialog, quitting, starting the
        # processing, cancelling the proessing, showing the loaded file, and
        # saving all images
        self.openFileButton = QtGui.QPushButton('Open file')
        self.quitButton = QtGui.QPushButton('Quit')
        self.startButton = QtGui.QPushButton('Start')
        self.cancelButton = QtGui.QPushButton('Cancel')
        self.cancelButton.hide()
        self.showFileButton = QtGui.QPushButton('Show file')
        self.saveAllButton = QtGui.QPushButton('Save all')

        # Create a label for thread warnings
        self.threadLabel = QtGui.QLabel('')

        # Create a timer and label to display it
        self.guiTimer = QtCore.QTimer()
        self.timerLabel = QtGui.QLabel('00:00')
        timerLabelFont = QtGui.QFont()
        timerLabelFont.setPointSize(18)
        self.timerLabel.setFont(timerLabelFont)
        self.timerLabel.setMaximumWidth(88)
        self.timerLabel.setStyleSheet("border: 2px solid")

        # Create a button for resetting the gui
        self.resetButton = QtGui.QPushButton('Reset')
        self.resetButton.setMaximumWidth(80)
        self.resetButton.hide()

        # Create headings for standard deviation (sigma) and width
        self.gblurSigmaLabel = QtGui.QLabel('Sigma')
        self.gblurWidthLabel = QtGui.QLabel('Width')

        # Create labels for each process
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

        # Set flags for if the process is activated to false
        # (this flag tells the program to animate the label)
        self.gblurLabel.activated = False
        self.sobelLabel.activated = False
        self.nmsLabel.activated = False
        self.thresholdLabel.activated = False
        self.hysteresisLabel.activated = False
        self.threadLabel.activated = False

        # Create show image buttons for each stage and add to widgets list
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

        # Create save image buttons for each stage and add to widgets list
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

        # Create dropdown box for selecting standard deviation for gaussian
        # blur stage
        self.gblurSigma = QtGui.QComboBox()
        self.gblurSigma.addItems(['0.5','0.6','0.7','0.8','0.9','1.0','1.1',\
                '1.2','1.3','1.4','1.5','2.0','2.5','3.0'])
        self.gblurSigma.setCurrentIndex(5)
        # Force widget to be width 70 to neaten appearence
        self.gblurSigma.setMaximumWidth(70)
        self.gblurSigma.setMinimumWidth(70)

        # Create dropdown box for selecting kernel width for gaussian blur
        self.gblurWidth = QtGui.QComboBox()
        self.gblurWidth.addItems(['3','5','7','9','11'])
        self.gblurWidth.setCurrentIndex(1)
        # Force widget to be width 70 to neaten appearence
        self.gblurWidth.setMaximumWidth(70)
        self.gblurWidth.setMinimumWidth(70)

        # Create input boxes for entering low and high threshold ratios, and
        # selecting manual or automatic thresholding
        self.threshLow = QtGui.QLineEdit('0.275')
        self.threshLow.setMaximumWidth(70)
        self.threshHigh = QtGui.QLineEdit('0.25')
        self.threshHigh.setMaximumWidth(70)
        self.thresholdOption = QtGui.QButtonGroup()
        self.thresholdAuto = True
        self.automaticOption = QtGui.QRadioButton('Automatic Threshold')
        self.automaticOption.setChecked(True)
        self.thresholdOption.addButton(self.automaticOption)
        self.manualOption = QtGui.QRadioButton('Manual Threshold')
        self.thresholdOption.addButton(self.manualOption)

        # Connect all (required) buttons to their associated functions
        # Lambda allows connection to a function using arguments
        self.openFileButton.clicked.connect(self.openFileFunc)
        self.startButton.clicked.connect(self.startFunctionCheck)
        self.showFileButton.clicked.connect(lambda: self.showFunc(\
                self.I.original, 'gray'))
        self.threshLow.textChanged.connect(lambda: self.updateThresholds(\
                'low', self.threshLow.text()))
        self.threshHigh.textChanged.connect(lambda: self.updateThresholds(\
                'high', self.threshHigh.text()))
        self.gblurSave.clicked.connect(lambda: self.saveFunc(self.I.gblur))
        self.gblurShow.clicked.connect(lambda: self.showFunc(self.I.gblur,\
                'gray'))
        self.sobelSave.clicked.connect(lambda: self.sobelOptionsFunc('Save'))
        self.sobelShow.clicked.connect(lambda: self.sobelOptionsFunc('Show'))
        self.nmsSave.clicked.connect(lambda: self.saveFunc(self.I.suppressed))
        self.nmsShow.clicked.connect(lambda: self.showFunc(self.I.suppressed,\
                'gray'))
        self.manualOption.toggled.connect(lambda: \
                self.handleThresholdOptions('manual',True))
        self.automaticOption.toggled.connect(lambda: \
                self.handleThresholdOptions('auto'))
        self.thresholdSave.clicked.connect(lambda: self.saveFunc(\
                self.I.thresholded))
        self.thresholdShow.clicked.connect(lambda: self.showFunc(\
                self.I.thresholded, 'gray'))
        self.hysteresisShow.clicked.connect(lambda: self.showFunc(\
                self.I.final, 'gray'))
        self.saveAllButton.clicked.connect(self.saveAllFunc)
        self.cancelButton.clicked.connect(self.terminateThread)
        self.resetButton.clicked.connect(self.resetFunc)

    def layout(self):
        """
            Function for setting the layout of the window

            NB: appears in slightly strange order since the order in which
            widgets are added determines the order when using arrow keys
            to navigate GUI
        """
        # Create layout
        gridLayout = QtGui.QGridLayout()

        # Add widgets to the layout
        gridLayout.addWidget(self.fileStatusLabel,0,0,QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.showFileButton,0,3,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.openFileButton,0,4,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.timerLabel,1,0)

        # Add a line to split up the GUI
        hline = QtGui.QFrame()
        hline.setFrameShape(QtGui.QFrame.HLine)
        hline.setFrameShadow(QtGui.QFrame.Plain)
        gridLayout.addWidget(hline,2,0,2,-1,QtCore.Qt.AlignTop)

        # Add a layout for cancelling - rqeuires it's own layout to be
        # horizontally centred
        self.startCancelLayout = QtGui.QHBoxLayout()
        self.startCancelLayout.addWidget(self.startButton)
        self.startCancelLayout.addWidget(self.cancelButton)
        gridLayout.addLayout(self.startCancelLayout,2,0,2,-1,\
                QtCore.Qt.AlignCenter)

        gridLayout.addWidget(self.threadLabel,3,0)

        # Add a layout for gaussian blur parameters
        gridLayout.addWidget(self.gblurLabel,4,0)
        self.gblurLayout = QtGui.QFormLayout()
        self.gblurLayout.addRow(QtGui.QLabel('Gaussian Parameters'))
        self.gblurLayout.addRow(self.gblurSigmaLabel,self.gblurWidthLabel)
        self.gblurLayout.addRow(self.gblurSigma, self.gblurWidth)
        gridLayout.addLayout(self.gblurLayout, 4,1,1,2)

        gridLayout.addWidget(self.sobelLabel,5,0)
        gridLayout.addWidget(self.nmsLabel,6,0)

        # To prevent label from moving show & save widgets when the dots move
        self.nmsLabel.setMinimumWidth(350)

        # Add a layout for threshold parameters
        self.threshLayout = QtGui.QFormLayout()
        self.threshLayout.addRow(self.automaticOption)
        self.threshLayout.addRow(self.manualOption)
        self.threshLayout.addRow(self.threshLowLabel, self.threshHighLabel)
        self.threshLayout.addRow(self.threshLow, self.threshHigh)

        gridLayout.addWidget(self.thresholdLabel,7,0)
        gridLayout.addLayout(self.threshLayout,7,1,1,2)
        gridLayout.addWidget(self.hysteresisLabel,8,0)
        gridLayout.addWidget(self.saveAllButton,9,4,QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.resetButton,10,0,QtCore.Qt.AlignBottom)
        gridLayout.addWidget(self.quitButton,10,4,QtCore.Qt.AlignBottom)

        # Iterate through the show & save buttons list and add to layout
        for i in range(0,2):
            for j in range(0,5):
                gridLayout.addWidget(self.widgets[i][j],j+4,i+3,\
                        QtCore.Qt.AlignCenter)

        # Hide show and save buttons
        for i in range(0,2):
            for j in range(0,5):
                self.widgets[i][j].hide()

        # Hide necessary widgets
        self.saveAllButton.hide()
        self.showFileButton.hide()
        self.threshLowLabel.hide()
        self.threshLow.hide()
        self.threshHighLabel.hide()
        self.threshHigh.hide()

        # Set layout to window
        self.setLayout(gridLayout)

    def startFunction(self):
        """
            Function that starts the processing
        """
        # Ensure no data from previous processes
        self.resetFunc()

        # Start timer and connect to required functions
        self.seconds = 0
        self.minutes = 0
        self.timerLabel.setText('00:00')
        self.guiTimer.timeout.connect(self.updateTimer)
        self.guiTimer.timeout.connect(self.updateStrings)
        self.guiTimer.start(1000)

        # Create the threads for actual processing & for background updating
        self.worker = WorkerThread(self)
        self.update = BackgroundThread(self.worker, self)

        # Show/hide necessary buttons
        self.cancelButton.show()
        self.startButton.hide()

        # Define custom signals for communicating with the working thread
        errorException = QtCore.pyqtSignal()
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

        # Connect signals
        # Connect signal for an error message from the thread
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('errorException'), \
                self.errorMessage)

        # Create a lambda function that updates the relevant labels once
        # the processing is started
        self.gblurUpdateConnection = lambda: self.updateFromThreadFunc(\
                self.gblurLabel, 'Gaussian Blur: processing.')

        # Connect to said function
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL(\
                'updateGaussianLabel'), self.gblurUpdateConnection)

        # Create a lambda for updating the relevant labels once finished
        self.gblurFinishConnection = lambda: self.finishFromThreadFunc(\
                self.gblurLabel, 'Gaussian Blur: complete', self.gblurSave,\
                self.gblurShow)

        # Connect to said function
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishGaussian'), \
                self.gblurFinishConnection)

        #NB: this is repeated for the following 4 blocks of code

        self.sobelUpdateConnection = lambda: self.updateFromThreadFunc(\
                self.sobelLabel, 'Sobel Filter: processing.')
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL(\
                'updateSobelLabel'), self.sobelUpdateConnection)
        self.sobelFinishConnection = lambda: self.finishFromThreadFunc(\
                self.sobelLabel, 'Sobel Filter: complete', self.sobelSave, \
                self.sobelShow)
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishSobel'), \
                self.sobelFinishConnection)

        self.nmsUpdateConnection = lambda: self.updateFromThreadFunc(\
                self.nmsLabel, 'Non Maximum Suppression: processing.')
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('updateNmsLabel'), \
                self.nmsUpdateConnection)
        self.nmsFinishConnection = lambda: self.finishFromThreadFunc(\
                self.nmsLabel, 'Non Maximum Suppression: complete', \
                self.nmsSave, self.nmsShow)
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishNms'), \
                self.nmsFinishConnection)

        self.threshUpdateConnection = lambda: self.updateFromThreadFunc(\
                self.thresholdLabel, 'Thresholding: processing.')
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL(\
                'updateThresholdLabel'), self.threshUpdateConnection)
        self.threshFinishConnection = lambda: self.finishFromThreadFunc(\
                self.thresholdLabel, 'Thresholding: complete', \
                self.thresholdSave, self.thresholdShow)
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL('finishThreshold'),\
                self.threshFinishConnection)

        self.hystUpdateConnection = lambda: self.updateFromThreadFunc(\
                self.hysteresisLabel, 'Hysteresis: processing.')
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL(\
                'updateHysteresisLabel'), self.hystUpdateConnection)
        self.hystFinishConnection = lambda: self.finishFromThreadFunc(\
                self.hysteresisLabel, 'Hysteresis: complete', \
                self.hysteresisSave, self.hysteresisShow, True)
        QtCore.QObject.connect(self.worker, QtCore.SIGNAL(\
                'finishHysteresis'), self.hystFinishConnection)

        # Connect function for finishing the thread
        self.worker.finished.connect(self.finishedThreadFunc)

        # Start threads
        self.worker.start()
        self.update.start()

    def startFunctionCheck(self):
        """
            Function to ensure that there is an image loaded into the program
            before starting the processing
        """
        # Check if no image has been loaded
        if self.I is None:
            # Show error message
            self.errorMessage('No Image Loaded')

        else:
            # Start function if there is an image
            self.startFunction()

    def updateFromThreadFunc(self, label, labelText):
        """
            Function to update a given label with given text
        """
        # Provided the worker hasn't stopped, change the label
        if not self.worker.stopFlag:
            # Set text of label
            label.setText(labelText)

            # Activate the label animation
            label.activated = True

    def finishFromThreadFunc(self, label, labelText, saveButton, \
            showButton, flag=False):
        """
            Function to handle the end of a stage:
            stop animating a label, set it's text, then show the show and
            save buttons
        """
        # If the worker thread is still running
        if not self.worker.stopFlag:
            # Change label activation flag and text
            label.activated = False
            label.setText(labelText)

            # Show show and save buttons
            saveButton.show()
            showButton.show()

            # If a flag is given, then show the save all button. This is done
            # here so that an extra function purely for this button is not
            # needed
            if flag:
                self.saveAllButton.show()

    def updateStrings(self):
        """
            Function to animate any labels with an activation flag
        """
        # If the flag is activated, then update the dots
        if self.gblurLabel.activated:
            self.gblurLabel.setText('Gaussian Blur: processing'+\
                    self.dotDotDot())

        if self.sobelLabel.activated:
            self.sobelLabel.setText('Sobel Filter: processing'+\
                    self.dotDotDot())

        if self.nmsLabel.activated:
            self.nmsLabel.setText('Non Maximum Suppression: processing'+\
                    self.dotDotDot())

        if self.thresholdLabel.activated:
            self.thresholdLabel.setText('Thresholding: processing'+\
                    self.dotDotDot())

        if self.hysteresisLabel.activated:
            self.hysteresisLabel.setText('Hysteresis: processing'+\
                    self.dotDotDot())

        if self.threadLabel.activated:
            self.threadLabel.setText('Waiting for thread termination'+\
                    self.dotDotDot())

    def dotDotDot(self):
        """
            Function to animate the '...' on labels
        """
        # Create list of dots
        strList = ['.','..','...']

        # Return a different dot based on the number of seconds
        return strList[self.seconds % 3]

    def updateTimer(self):
        """
            Function to update the timer
        """
        # Increment the number of seconds
        self.seconds += 1

        # If the number of seconds is 60, reset to 0 and increment minutes
        if self.seconds == 60:
            self.seconds=0
            self.minutes += 1

        # Format the strings
        minutesString = "{0:02d}".format(self.minutes)
        secondsString = "{0:02d}".format(self.seconds)

        # Set timer label text
        self.timerLabel.setText(minutesString+':'+secondsString)

    def openFileFunc(self):
        """
            Function to open a file and load it into the program

            NB: excepting handling is not needed here - the only images that
            the user can load can be handled by the program, it is not
            possible to load anything other than (*.jpg *.gif *.bmp *.png)
        """
        # Open file dialog and get selected filepath
        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~', \
                'Image files (*.jpg *.gif *.bmp *.png)')

        # If the dialog returns an filepath (it may not if it is cancelled)
        if filepath:
            # Store loaded image in Image object
            self.I = Image(np.asarray(im.open(filepath).convert('L'),\
                dtype=np.float))

            # Set file status
            self.fileStatusLabel.setText('File: '+str(filepath.split('/')\
                    [-1]))

            # Show 'show file' button
            self.showFileButton.show()

    def showFunc(self, image, colourmap):
        """
            Function to show a given image using a given colourmap
        """
        try:
            # Call the matplotlib window
            showImage = mplWindow(image, colourmap)
            # Set focus to the mpl window
            showImage.setFocus()
            # Start event loop for the mpl window
            showImage.exec_()

        except Exception as error:
            # If an exception occurs during the display of the image,
            # stop the program from crashing and display error
            exceptionMessage = type(error).__name__+': '+str(error)
            self.errorMessage(exceptionMessage)

    def saveFunc(self, image):
        """
            Function to save a given image
        """
        # Get the filepath to save the image to
        filepath = QtGui.QFileDialog.getSaveFileName(self, 'Save file', '~', \
                'Image files (*.jpg *.gif *.bmp *.png)')

        # If the file dialog returned a filepath
        if filepath:
            try:
                # Try to save the image
                im.fromarray(image.astype(np.uint8)).save(filepath)

            except Exception as error:
                # If an error occurs, display the error
                exceptionMessage = type(error).__name__+': '+str(error)
                self.errorMessage(exceptionMessage)

    def sobelOptionsFunc(self, dialogType):
        """
            Function to call the dialog to handle the various options for
            saving/showing images from the sobel filter algorithm
        """
        # Call the dialog
        dialog = SobelOptionsDialog(self, dialogType)

        # Set focus to the sobel dialog
        dialog.setFocus()

        # Start event loop of the sobel dialog
        dialog.exec_()

    def handleThresholdOptions(self, option, Flag=None):
        """
            Function for handling the threshold parameters visibility - when
            manual is selected, the input boxes must be shown, when no longer
            selected, must be hidden
        """
        # Check that option is either 'manual' or 'auto'
        assert option in ['manual', 'auto'], 'Function handleThresholdOptions\
                : option entered was not a known value'

        if option == 'manual':
            self.threshHighLabel.show()
            self.threshHigh.show()
            self.threshLowLabel.show()
            self.threshLow.show()
        else:
            self.thresholdAuto = not self.thresholdAuto
            self.threshHighLabel.hide()
            self.threshHigh.hide()
            self.threshLowLabel.hide()
            self.threshLow.hide()

    def updateThresholds(self, threshold, text):
        """
            Function to update value of high and low threshold ratios when
            text is entered into the associated input boxes
        """
        # Check if the text holds a float
        errorFlag = False
        try:
            # Check if it contains a float by trying to convert to float
            text = float(text)

        except ValueError:
            # If it fails, set errorFlag to False
            errorFlag = True

        # If there is no error
        if not errorFlag:
            # Check that the ratios are between 0 and 1
            if (text >= 1) or (text <= 0):
                self.errorMessage('Threshold ratios must be a number \
                        between 0 and 1')

            # Set the relevant threshold ratio
            if threshold == 'low':
                self.lowThreshRatio = text
            else:
                self.highThreshRatio = text
        else:
            # If it fails, raise an error message
            self.errorMessage('Threshold ratios must be a number between \
                    0 and 1')

    def errorMessage(self, message):
        """
            Function to display an error dialog with a given message
        """
        # Create a dialog, set text and buttons
        errorMsg = QtGui.QMessageBox()
        errorMsg.setIcon(QtGui.QMessageBox.Warning)
        errorMsg.setText(message)
        errorMsg.setStandardButtons(QtGui.QMessageBox.Ok)
        errorMsg.setDefaultButton(QtGui.QMessageBox.Ok)
        errorMsg.setEscapeButton(QtGui.QMessageBox.Ok)

        # Set focus to the dialog
        errorMsg.setFocus()

        # Start event loop of dialog
        errorMsg.exec_()


    def saveAllFunc(self):
        """
            Function to call the dialog for saving all images
        """
        # Call the dialog
        saveDialog = SaveAllDialog(self)

        # Set window focus to the save all dialog
        saveDialog.setFocus()

        # Start the event loop of the dialog
        saveDialog.exec_()

    def terminateThread(self):
        """
            Function to terminate the working thread when the cancel button
            is pressed

            NB: terminating a thread cannot be done forcefully - the thread
            must finish what it is doing. Hence the aim here is to disconnect
            any reference to the thread, tell it to stop and not move to the
            next stage of the algorithm, and wait for it to finish on it's own
        """
        # If the worker thread exists
        if self.worker:
            # Tell worker to stop running
            self.worker.stopFlag = True

            # Disconnect all connections with worker so that functions do not
            # communicate with it
            self.worker.finished.disconnect(self.finishedThreadFunc)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL(\
                    'updateGaussianLabel'), self.gblurUpdateConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL(\
                    'finishGaussian'), self.gblurFinishConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL(\
                    'updateSobelLabel'), self.sobelUpdateConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL(\
                    'finishSobel'), self.sobelFinishConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL(\
                    'updateNmsLabel'), self.nmsUpdateConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL(\
                    'finishNms'), self.nmsFinishConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL(\
                    'updateThresholdLabel'), self.threshUpdateConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL(\
                    'finishThreshold'), self.threshFinishConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL(\
                    'updateHysteresisLabel'), self.hystUpdateConnection)
            QtCore.QObject.disconnect(self.worker, QtCore.SIGNAL(\
                    'finishHysteresis'), self.hystFinishConnection)

            # Remove reference to current worker
            self.worker = None

            # Set activation flags to false
            self.gblurLabel.activated = False
            self.sobelLabel.activated = False
            self.nmsLabel.activated = False
            self.thresholdLabel.activated = False
            self.hysteresisLabel.activated = False

            # Reset stage flags
            self.gblurLabel.setText('Gaussian Blur: not started')
            self.sobelLabel.setText('Sobel Filter: not started')
            self.nmsLabel.setText('Non Maximum Suppression: not started')
            self.thresholdLabel.setText('Thresholding: not started')
            self.hysteresisLabel.setText('Hysteresis: not started')

            # Stop the timer and reset
            self.guiTimer.stop()
            self.timerLabel.setText('00:00')

            # Call the function that handles the GUI when the thread has
            # finished
            self.finishedThreadFunc()

        # If the worker thread doesn't exist, raise an error message
        else:
            self.errorMessage('Thread does not exist')

    def finishedThreadFunc(self):
        """
            Function that handles the GUI when the working thread has
            finished e.g. resetting the timer, dealing with button visibility

            NB: there is no need to tell the background thread to stop since
            it will automatically stop when the worker is no longer running
        """
        # Stop timer and remove connections
        self.guiTimer.stop()
        self.guiTimer.timeout.disconnect(self.updateStrings)
        self.guiTimer.timeout.disconnect(self.updateTimer)

        # Reset the thread label
        self.threadLabel.activated=False
        self.threadLabel.setText('')

        # Hide and show the relevant buttons
        self.startButton.show()
        self.cancelButton.hide()
        self.resetButton.show()
        self.cancelButton.setEnabled(True)
        self.cancelButton.setWindowOpacity(1)

    def resetFunc(self):
        """
            Function to reset the program if processing has been cancelled
        """
        # Hide the save all button
        self.saveAllButton.hide()

        # Hide show & save buttons
        for i in range(0,2):
            for j in range(0,5):
                self.widgets[i][j].hide()

        # Reinitialise the image object with the original
        self.I.__init__(self.I.original)

        # Reset timer
        self.timerLabel.setText('00:00')

        # Hide reset button
        self.resetButton.hide()
