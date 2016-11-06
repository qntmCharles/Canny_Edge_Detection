import sys
from PyQt4 import QtCore, QtGui

class Main(QtGui.QMainWindow):
    def __init__(self, win_parent = None):
        QtGui.QMainWindow.__init__(self,win_parent)
        self.setWindowTitle('Canny Edge Detection')
        self.create_widgets()

    def create_widgets(self):
        #Widgets
        self.open_file = QtGui.QPushButton('Open File')

        #Connect widgets
        QtCore.QObject.connect(self.open_file, QtCore.SIGNAL('clicked()'),self.getFile)
        """
        #Widgets
        self.label = QtGui.QLabel('Say hello: ')
        self.hello_edit = QtGui.QLineEdit()
        self.hello_button = QtGui.QPushButton('Push me!')"""

        #Set layout
        grid = QtGui.QGridLayout()
        grid.addWidget(self.open_file,1,2,QtCore.Qt.AlignCenter)
        """
        h_box.addWidget(self.label)
        h_box.addWidget(self.hello_edit)
        h_box.addWidget(self.hello_button)

        #Connect button
        QtCore.QObject.connect(self.hello_button, QtCore.SIGNAL('clicked()'),self.on_hello_clicked)
"""
        #Initialise central widget
        central_widget = QtGui.QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

    def getFile(self):
        print('FUCK')



if __name__ == "__main__":
    #Create QApplication
    app = QtGui.QApplication(sys.argv)

    #Main Window
    main_window = Main()
    main_window.show()

    #Enter main loop
    app.exec_()
