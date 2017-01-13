from PyQt4 import QtCore, QtGui

import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure

class mplCanvas(FigCanvas):
    """
        Class that acts as a figure canvas to show matplotlib imshow plot
        rather than a simple plot (hence the extension)

        Inherits from FigCanvas for Qt (this is simply an extension, all methods &
        most functionality is in FigCanvas)
    """
    def __init__(self, parent, data, colourmap):
        # Initialise figure with set size
        fig = Figure(figsize=(8,6))

        # Initialise super class
        FigCanvas.__init__(self,fig)

        # Initialise subplot
        self.axes = fig.add_subplot(111)

        # Set parent of class
        self.setParent(parent)

        # Create image
        image = self.axes.imshow(data, cmap=colourmap, interpolation="none")

        # Add colourbar
        fig.colorbar(image)

        # Update geometry so that everything is displayed properly
        FigCanvas.updateGeometry(self)

class navigationToolbar(NavBar):
    """
        A modified version of matplotlib Navigation Toolbar, to remove
        unneeded buttons in the figure

        Inherits from original navigation toolbar for Qt
    """
    # Get a list of all toolbar items from the superclass
    # Needs to be static since it acts on the class rather than an object
    toolitems = [item for item in NavBar.toolitems if item[0] in ('Home', \
            'Pan', 'Zoom')]

    def __init__(self, *args, **kwargs):
        # Initialise superclass using system args
        super(navigationToolbar, self).__init__(*args, **kwargs)

        # Remove plot customization button
        # Find all possible actions
        toolbarActions = self.findChildren(QtGui.QAction)

        # For each action...
        for action in toolbarActions:
            #Find the customization action and remove
            if action.text() == 'Customize':
                self.removeAction(action)

                #No longer need to loop so break
                break

class mplWindow(QtGui.QDialog):
    """
        Dialog to contain matplotlib figure canvas and navigation toolbar
    """
    def __init__(self, figureData, colourmap):
        # Initialise superclass
        super(mplWindow, self).__init__()

        # Initialise matplotlib canvas
        self.display = mplCanvas(self, figureData, colourmap)

        # Initialise matplotlib toolbar
        self.toolbar = navigationToolbar(self.display, self)

        # Add a button to close the figure
        self.closeButton = QtGui.QPushButton('Close')
        self.closeButton.setMaximumWidth(100)

        # Connect button
        self.closeButton.clicked.connect(self.exit)

        # Create a vertical box layout and add toolbar, display and button
        self.boxLayout = QtGui.QVBoxLayout()
        self.boxLayout.addWidget(self.toolbar)
        self.boxLayout.addWidget(self.display)

        # Add a horizontal layout simply to horizontally centre the button
        self.closeButtonLayout = QtGui.QHBoxLayout()
        self.closeButtonLayout.addWidget(self.closeButton)
        self.boxLayout.addLayout(self.closeButtonLayout)

        # Set dialaog layout to boxLayout
        self.setLayout(self.boxLayout)

    def exit(self):
        # When the exit function is called, close the figure
        self.close()
