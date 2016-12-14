from PyQt4 import QtGui, QtCore

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
        #Ask Liam: is it better to pass the data, rather than accessing it through the parent? encapsulation 'n' stuff? also the whole module interface thing...

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
