from PyQt4 import QtCore, QtGui

class SaveAllDialog(QtGui.QDialog):
    """
        Class to act as a dialog for the user selecting which images to save
        as well as extensions and save locations
    """
    def __init__(self, parent):
        # Initialise superclass
        super(SaveAllDialog, self).__init__(parent)

        # Set default file extension
        self.fileExt = '.bmp'

        # Set default filenames
        self.filenames={'gblur':'gblur', 'smag':'sobel_mag', \
                'sdir':'sobel_dir', 'shoriz':'sobel_horiz', \
                'svert':'sobel_vert', 'nms':'nms', 'thresh':'threshold', \
                'hyst':'hysteresis'}

        # Initialise empty variable for filepath
        self.filepath = None

        self.createWidgets()

        self.layout()

    def createWidgets(self):
        """
            Function to create widgets for the window and connect them to
            other functions
        """
        # Create button to open a file
        self.openDirButton = QtGui.QPushButton('Select Directory')

        # Create tick boxes and input boxes (line edits) with default names
        self.gblurOption = QtGui.QCheckBox('Gaussian Blur')
        self.gblurName = QtGui.QLineEdit(self.filnames['gblur'])

        self.sobelMagOption = QtGui.QCheckBox('Sobel Gradient Magnitude')
        self.sobelMagName = QtGui.QLineEdit(self.filenames['smag'])

        self.sobelDirOption = QtGui.QCheckBox('Sobel Gradient Direction')
        self.sobelDirName = QtGui.QLineEdit(self.filenames['sdir'])

        self.sobelHorizOption = QtGui.QCheckBox('Sobel Horizontal Gradient')
        self.sobelHorizName = QtGui.QLineEdit(self.filenames['shoriz'])

        self.sobelVertOption = QtGui.QCheckBox('Sobel Vertical Gradient')
        self.sobelVertName = QtGui.QLineEdit(self.filenames['svert'])

        self.nmsOption = QtGui.QCheckBox('Non Maximum Suppression')
        self.nmsName = QtGui.QLineEdit(self.filenames['nms'])

        self.thresholdOption = QtGui.QCheckBox('Threshold')
        self.thresholdName = QtGui.QLineEdit(self.filenames['thresh'])

        self.hysteresisOption = QtGui.QCheckBox('Hysteresis')
        self.hysteresisName = QtGui.QLineEdit(self.filenames['hyst'])

        # Set all boxes as ticked
        self.gblurOption.setChecked(True)
        self.sobelMagOption.setChecked(True)
        self.sobelDirOption.setChecked(True)
        self.sobelHorizOption.setChecked(True)
        self.sobelVertOption.setChecked(True)
        self.nmsOption.setChecked(True)
        self.thresholdOption.setChecked(True)
        self.hysteresisOption.setChecked(True)

        # Add a dropdown menu to select a format to save in (defafult is .bmp)
        self.dropDown = QtGui.QComboBox(self)
        self.dropDown.addItem('.bmp')
        self.dropDown.addItem('.jpg')
        self.dropDown.addItem('.png')
        self.dropDown.addItem('.gif')
        self.dropDown.setCurrentIndex(0)

        # Create buttons to save everything and close the dialog
        self.saveButton = QtGui.QPushButton('Save')
        self.saveButton.setMaximumWidth(80)
        self.closeButton = QtGui.QPushButton('Close')
        self.closeButton.setMaximumWidth(80)

        # Connect buttons to their relevant functions
        self.closeButton.clicked.connect(self.exit)
        self.dropDown.activated[str].connect(self.setFileExt)
        self.openDirButton.clicked.connect(self.openFileFunc)

        # Connect line edits to a function that will change the required
        # variable
        self.gblurName.textChanged.connect(lambda: self.updateFilename(\
                'gblur', self.gblurName.text()))
        self.sobelMagName.textChanged.connect(lambda: self.updateFilename(\
                'smag', self.sobelMagName.text()))
        self.sobelDirName.textChanged.connect(lambda: self.updateFilename(\
                'sdir', self.sobelDirName.text()))
        self.sobelHorizName.textChanged.connect(lambda: self.updateFilename(\
                'shoriz', self.sobelHorizName.text()))
        self.sobelVertName.textChanged.connect(lambda: self.updateFilename(\
                'svert', self.sobelVertName.text()))
        self.nmsName.textChanged.connect(lambda: self.updateFilename(\
                'nms', self.nmsName.text()))
        self.thresholdName.textChanged.connect(lambda: self.updateFilename(\
                'thresh', self.thresholdName.text()))
        self.hysteresisName.textChanged.connect(lambda: self.updateFilename(\
                'hyst', self.hysteresisName.text()))

    def layout(self):
        """
            Function to create and format the layout for the window
        """
        # Create layout
        formLayout = QtGui.QFormLayout()

        # Add a new layout so that the button is horizontally centred
        openDirLayout = QtGui.QGridLayout()
        openDirLayout.addWidget(self.openDirButton,0,0,QtCore.Qt.AlignCenter)
        formLayout.addRow(openDirLayout)

        # Add a new layout so that the label is horizontally centred
        filenameLabel = QtGui.QGridLayout()
        filenameLabel.addWidget(QtGui.QLabel('Filename'))
        formLayout.addRow('Select images to save', filenameLabel)

        # Add checkboxes and line edits to layout in rows
        formLayout.addRow(self.gblurOption, self.gblurName)
        formLayout.addRow(self.sobelMagOption, self.sobelMagName)
        formLayout.addRow(self.sobelDirOption, self.sobelDirName)
        formLayout.addRow(self.sobelHorizOption, self.sobelHorizName)
        formLayout.addRow(self.sobelVertOption, self.sobelVertName)
        formLayout.addRow(self.nmsOption, self.nmsName)
        formLayout.addRow(self.thresholdOption, self.thresholdName)
        formLayout.addRow(self.hysteresisOption, self.hysteresisName)
        formLayout.addRow('File Extension', self.dropDown)

        # Add a new layout so that the save and close buttons are centred
        buttonsLayout = QtGui.QGridLayout()
        buttonsLayout.addWidget(self.saveButton,0,0,QtCore.Qt.AlignCenter)
        buttonsLayout.addWidget(self.closeButton,1,0,QtCore.Qt.AlignCenter)
        formLayout.addRow(buttonsLayout)

        # Set layout to window
        self.setLayout(formLayout)

    def setFileExt(self, text):
        """
            Function that sets the file extension, called when the line edit
            is edited
        """
        self.fileExt = text

    def updateFilename(self, key, text):
        """
            Function that updates the given filename (key) with the given
            contents of the line edit (text)
        """
        self.filenames[key] = text

    def openFileFunc(self):
        """
            Function to open a file dialog and set the filepath
        """
        # Create the file dialog
        fileDialog = QtGui.QFileDialog(self)

        # Set the dialog to only be able to select directories
        fileDialog.setFileMode(QtGui.QFileDialog.Directory)

        # Show only directories
        fileDialog.setOption(QtGui.QFileDialog.ShowDirsOnly, True)

        # If the filedialog exits the event loop correctly, set the filepath
        if fileDialog.exec_():
            self.filepath = fileDialog.selectedFiles()[0]

    def saveFiles(self):
        """
            Function that will save the chosen files with chosen names & ext

            NB: it's not necessary to check whether each image array exists,
            since the save all button will only appear if processing is
            complete and thus all image arrays must be present
        """
        # Check that the filepath has been selected
        if self.filepath is None:
            # If the filepath isn't present, raise an error
            self.parent().errorMessage('No directory selected')

        # If the filepath does exist
        else:
            # For each possible file to save, check if it's been selected
            if self.gblurOption.isChecked():
                # Get the image array
                data = self.parent().parent().parent().I.gblur

                # Save the image with the chosen filepath, filename and ext
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+\
                        self.filenames['gblur']+self.fileExt)

            # The above process is repeated for all following loops
            if self.sobelMagOption.isChecked():
                data = self.parent().parent().parent().I.smagnitude
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+\
                        self.filenames['smag']+self.fileExt)

            if self.sobelDirOption.isChecked():
                data = self.parent().parent().parent().I.sdirection
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+\
                        self.filenames['sdir']+self.fileExt)

            if self.sobelHorizOption.isChecked():
                data = self.parent().parent().parent().I.shgradient
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+\
                        self.filenames['shoriz']+self.fileExt)

            if self.sobelVertOption.isChecked():
                data = self.parent().parent().parent().I.svgradient
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+\
                        self.filenames['svert']+self.fileExt)

            if self.nmsOption.isChecked():
                data = self.parent().parent().parent().I.suppressed
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+\
                        self.filenames['nms']+self.fileExt)

            if self.thresholdOption.isChecked():
                data = self.parent().parent().parent().I.thresholded
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+\
                        self.filenames['thresh']+self.fileExt)

            if self.hysteresisOption.isChecked():
                data = self.parent().parent().parent().I.final
                im.fromarray(data).convert('RGB').save(self.filepath+'/'+\
                        self.filenames['hyst']+self.fileExt)

    def exit(self):
        """
            Function that kills the dialog
        """
        self.close()
