from PyQt4 import QtGui, QtCore

class SobelOptionsDialog(QtGui.QDialog):
    """
        Class that acts as a dialog for the user to select which results of
        the sobel filter to show or save

        NB: this class acts as both the show and save dialog, dependent on
        the 'dialogType' passed to the class when instantiated
    """
    def __init__(self, parent, dialogType):
        # Initialise superclass
        super(SobelOptionsDialog, self).__init__(parent)

        # Set window title
        self.setWindowTitle('Show Images')

        self.createWidgets(dialogType)

        self.layout()

    def createWidgets(self, dialogType):
        """
            Function that creates the widgets for the window and connects
            them to the required functions
        """
        # Create labels to identify the image being considered
        self.magnitudeLabel = QtGui.QLabel('Gradient Magnitude')
        self.directionLabel = QtGui.QLabel('Gradient Direction')
        self.horizontalLabel = QtGui.QLabel('Horizontal Gradient')
        self.verticalLabel = QtGui.QLabel('Vertical Gradient')

        # Create the buttons to show or save each image
        self.magnitudeOption = QtGui.QPushButton(dialogType)
        self.directionOption = QtGui.QPushButton(dialogType)
        self.horizontalOption = QtGui.QPushButton(dialogType)
        self.verticalOption = QtGui.QPushButton(dialogType)

        # Create a close button
        self.closeButton = QtGui.QPushButton('Close')

        # Connect the closing button to the exit function
        self.closeButton.clicked.connect(self.exit)

        # Connect each image option to the necessary function based on the
        # dialog type
        if dialogType == 'Show':
            # Func is used to shorten and neaten the code
            func = self.parent().showFunc

            # Connect each image with it's colourmap
            self.magnitudeOption.clicked.connect(lambda: func(\
                    self.parent().I.smagnitude, 'gray'))
            self.directionOption.clicked.connect(lambda: func(\
                    self.parent().I.sdirection, 'gist_rainbow'))
            self.horizontalOption.clicked.connect(lambda: func(\
                    self.parent().I.shgradient, 'gray'))
            self.verticalOption.clicked.connect(lambda: func(\
                    self.parent().I.svgradient,  'gray'))
        else:
            func = self.parent().saveFunc

            self.magnitudeOption.clicked.connect(lambda: func(\
                    self.parent().I.smagnitude))
            self.directionOption.clicked.connect(lambda: func(\
                    self.parent().I.sdirection))
            self.horizontalOption.clicked.connect(lambda: func(\
                    self.parent().I.shgradient))
            self.verticalOption.clicked.connect(lambda: func(\
                    self.parent().I.svgradient))

    def layout(self):
        """
            Function that sets the layout of the window
        """
        # Create the layout
        boxLayout = QtGui.QGridLayout()

        # Add widgets to layout
        boxLayout.addWidget(self.magnitudeLabel,0,0)
        boxLayout.addWidget(self.magnitudeOption,0,1)
        boxLayout.addWidget(self.directionLabel,1,0)
        boxLayout.addWidget(self.directionOption,1,1)
        boxLayout.addWidget(self.horizontalLabel,2,0)
        boxLayout.addWidget(self.horizontalOption,2,1)
        boxLayout.addWidget(self.verticalLabel,3,0)
        boxLayout.addWidget(self.verticalOption,3,1)
        boxLayout.addWidget(self.closeButton,4,1)

        # Set layout to window
        self.setLayout(boxLayout)

    def exit(self):
        """
            Function that kills the dialog
        """
        self.close()
