from PyQt4 import QtCore, QtGui
import time

class WorkerThread(QtCore.QThread):
    '''Handles processing and functionality'''
    def __init__(self, parent):
        super(WorkerThread, self).__init__(parent)

        self.running = True
        self.stopFlag = False

    def run(self):
        '''Starts the thread doing work when inbuilt start() is called'''
        try:
            if not self.stopFlag:
                #Gaussian
                self.emit(QtCore.SIGNAL('updateGaussianLabel'))
                sigma = float(self.parent().gblurSigma.currentText())
                radius = int(self.parent().gblurRadius.currentText())
                self.parent().I.gaussian_(sigma, radius)
                self.emit(QtCore.SIGNAL('finishGaussian'))

            if not self.stopFlag:
                #Sobel
                self.emit(QtCore.SIGNAL('updateSobelLabel'))
                self.parent().I.sobel_()
                self.emit(QtCore.SIGNAL('finishSobel'))

            if not self.stopFlag:
                #NMS
                self.emit(QtCore.SIGNAL('updateNmsLabel'))
                self.parent().I.nms_()
                self.emit(QtCore.SIGNAL('finishNms'))

            if not self.stopFlag:
                #Threshold
                self.emit(QtCore.SIGNAL('updateThresholdLabel'))
                self.parent().I.threshold_(self.parent().lowThresh, self.parent().highThresh)
                self.emit(QtCore.SIGNAL('finishThreshold'))

            if not self.stopFlag:
                #Hysteresis
                self.emit(QtCore.SIGNAL('updateHysteresisLabel'))
                self.parent().I.hysteresis_()
                self.emit(QtCore.SIGNAL('finishHysteresis'))

            #Stop thread
            self.running = False

        #If there is an exception, display and then stop the thread
        except Exception as e:
            print(e)
            self.running = False

    def __del__(self):
        print('this got called')
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
        from .guiApp import App
        #Update GUI every 0.1 seconds to prevent GUI lock
        while self.worker.running:
            App.processEvents()
            time.sleep(0.1)
