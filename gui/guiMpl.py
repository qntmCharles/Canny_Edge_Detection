from PyQt4 import QtCore, QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure

class mplCanvas(FigCanvas):
    """Figure canvas to show matplotlib imshow plot."""
    def __init__(self, parent, data, colourmap):
        fig = Figure(figsize=(8,6))
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
        self.closeButton.setMaximumWidth(100)

        self.closeButton.clicked.connect(self.exit)

        boxLayout = QtGui.QVBoxLayout()
        boxLayout.addWidget(self.toolbar)
        boxLayout.addWidget(self.display)
        self.closeButtonLayout = QtGui.QHBoxLayout()
        self.closeButtonLayout.addWidget(self.closeButton)
        boxLayout.addLayout(self.closeButtonLayout)
        self.setLayout(boxLayout)

    def exit(self):
        self.close()
