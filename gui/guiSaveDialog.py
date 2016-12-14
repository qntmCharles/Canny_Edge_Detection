from PyQt4 import QtCore, QtGui

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
