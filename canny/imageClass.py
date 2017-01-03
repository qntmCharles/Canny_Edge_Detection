import numpy as np
from .gaussian import gaussian
from .sobel import sobel
from .nms import nonMaximumSuppression
from .threshold import threshold
from .hysteresis import hysteresis
from .hysteresis import Queue

class Image():
    def __init__(self,originalImage):
        #Initialised all attributes with empty arrays (or empty Queue)
        self.original = originalImage
        self.gblur = np.array([])
        self.smagnitude = np.array([])
        self.sdirection = np.array([])
        self.shgradient = np.array([])
        self.svgradient = np.array([])
        self.suppressed = np.array([])
        self.strongEdgesQueue = Queue()
        self.thresholded = np.array([])
        self.final = np.array([])

    def __str__(self):
        """
            This method returns a string representation of this Image class
            Primarily used for testing
        """
        finalStr=''
        nil = np.array([])
        # List of attributes to be checked
        toCheck = [self.original, self.gblur, self.smagnitude, self.suppressed, \
                self.thresholded, self.final]
        # Strings associated with said attributes (in same order)
        associatedStrs = ['Original', 'Gaussian blur', 'Sobel', 'Suppression', \
                'Thresholding', 'Final']

        # Iterate through toCheck
        for i in range(len(toCheck)):
            if toCheck[i] != nul:
                # If array isn't empty, it has been processed
                finalStr += associatedStrs[i]+': complete\n'
            else:
                # Otherwise it has not yet been started
                finalStr += associatedStrs[i]+': not started\n'

        return finalStr

    def gaussian_(self,stdev,width):
        """
            Gaussian blur takes standard deviation, kernel width and original image
            Returns blurred image
        """
        self.gblur = gaussian(stdev,width,self.original)

    def sobel_(self):
        """
            Sobel filter takes the blurred image

            Returns gradient magnitude and direction, as well as horizontal and
            vertical gradient components
        """
        self.smagnitude,self.sdirection,self.shgradient,self.svgradient = sobel(self.gblur)

        # Ensure data type of gradient magnitude & direction arrays contain floats
        self.smagnitude = self.smagnitude.astype('float')
        self.sdirection = self.sdirection.astype('float')

    def nms_(self):
        """
            NMS algorithm takes all sobel filter result arrays

            Returns array of 0s and gradient magnitudes where not suppressed
        """
        self.suppressed = nonMaximumSuppression(self.smagnitude,self.shgradient, \
                self.svgradient,self.sdirection)

    def threshold_(self, autoBool, lowThreshold=None, highThreshold=None):
        """
            Automatic thresholding takes original image, gradient magnitude,
            and suppressed image

            User defined thresholding takes original image, gradient magnitude,
            suppressed image and low & high threshold ratios

            Returns thresholded image containing 0s (no edge), 128s (edge candidate),
            255s (strong/definite edges) and queue of strong edges
        """
        # Automatic thresholding
        if autoBool:
            self.thresholded, self.strongEdgesQueue = threshold(self.original, \
                    self.smagnitude, self.suppressed, True)

        # User defined thresholds
        else:
            self.thresholded, self.strongEdgesQueue  = threshold(self.original, \
                    self.smagnitude,self.suppressed, False, lowThreshold, highThreshold)

    def hysteresis_(self):
        """
            Hysteresis algorithm takes thresholded image and strong edges queue

            Returns final image containing only strong edges
        """
        self.final = hysteresis(self.thresholded, self.strongEdgesQueue)

