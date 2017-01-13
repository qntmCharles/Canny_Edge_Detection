from PyQt4 import QtCore, QtGui
import time

class WorkerThread(QtCore.QThread):
    """
        Class that handles processing and functionality of the program as a
        thread so that a separate thread can keep the app responsive

        Inherits functionality from QtCore.QThread

        NB: 'stopFlag' is a flag that tells the thread to stop, whilst
        'running' is a flag that tells the parent of the thread that the
        thread has finished
    """
    def __init__(self, parent):
        # Initialise superclass
        super(WorkerThread, self).__init__(parent)

        # Set running flag to True
        self.running = True
        self.stopFlag = False

    def run(self):
        """
            Function that starts the thread working when inbuilt start() is
            called

            NB: try except loop surrounds the entire run function since
            several functions have been called, and theoretically any could
            return an error (though unlikely due to other exception handling)
            This is done so that the GUI remains responsive and can still be
            used if an error occurs here
        """
        try:
            # If the worker hasn't yet been told to stop (this comment applies
            # to all following loops)
            if not self.stopFlag:
                # Gaussian
                # Emit signal to tell the GUI to update the required label
                # Signal also starts the '...' animation
                # (This comment applies to all following loops)
                self.emit(QtCore.SIGNAL('updateGaussianLabel'))

                # Get the standard deviation (sigma) from the GUI input
                sigma = float(self.parent().gblurSigma.currentText())

                # Get the kernel width from the
                width = int(self.parent().gblurWidth.currentText())

                # Start gaussian blur function
                self.parent().I.gaussian_(sigma, width)

                # Emit signal to signify function completion
                self.emit(QtCore.SIGNAL('finishGaussian'))

            if not self.stopFlag:
                # Sobel
                self.emit(QtCore.SIGNAL('updateSobelLabel'))

                # Start sobel filter function
                self.parent().I.sobel_()

                self.emit(QtCore.SIGNAL('finishSobel'))

            if not self.stopFlag:
                # NMS
                self.emit(QtCore.SIGNAL('updateNmsLabel'))

                # Start NMS function
                self.parent().I.nms_()

                self.emit(QtCore.SIGNAL('finishNms'))

            if not self.stopFlag:
                # Threshold
                self.emit(QtCore.SIGNAL('updateThresholdLabel'))

                # If automatic thresholding selected
                if self.parent().thresholdAuto:
                    self.parent().I.threshold_(True)

                # If manual thresholds entered
                else:
                    self.parent().I.threshold_(False, \
                            self.parent().lowThreshRatio, self.parent().\
                            highThreshRatio)

                self.emit(QtCore.SIGNAL('finishThreshold'))

            if not self.stopFlag:
                # Hysteresis
                self.emit(QtCore.SIGNAL('updateHysteresisLabel'))

                # Start hysteresis function
                self.parent().I.hysteresis_()

                self.emit(QtCore.SIGNAL('finishHysteresis'))

            # Stop thread if all functions have been completed successfully
            self.running = False

        # If there is an exception, display error message, then stop thread
        except Exception as error:
            self.running = False
            exceptionMessage = type(error).__name__+': '+str(error)
            # Must call a signal rather than the errorMessage function itself,
            # since it must occur in the main GUI thread
            self.emit(QtCore.SIGNAL('errorException'), exceptionMessage)

class BackgroundThread(QtCore.QThread):
    """
        Class that keeps the GUI responsive whislt a separate thread
        does the processing

        Inherits functionality from QtCore.QThread
    """
    def __init__(self, worker, parent):
        # Initialise super class
        super(BackgroundThread, self).__init__(parent)

        # Assign worker to this thread
        self.worker = worker

    def run(self):
        """
            Function that starts the thread doing work when inbuilt start()
            is called
        """
        #  Update GUI every 0.1 seconds to prevent GUI becoming unresponsive
        while self.worker.running:
            # Forces GUI to respond
            QtGui.QApplication.processEvents()

            # Zzzzz...
            time.sleep(0.1)
