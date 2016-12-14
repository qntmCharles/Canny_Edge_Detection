"""from PyQt4 import QtCore, QtGui

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure"""

from .guiMain import MainWindow, App
from .guiCanny import CannyWindow
from .guiSaveDialog import SaveAllDialog
from .guiMpl import mplCanvas, navigationToolbar, mplWindow
from .guiSobelDialog import SobelOptionsDialog
from .guiThreads import WorkerThread, BackgroundThread

print('GUI initialised')
