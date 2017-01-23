import numpy as np
import time
from .gaussian import gaussianInterface
from .sobel import sobel
from .nms import nonMaximumSuppression
from .threshold import thresholdInterface
from .hysteresis import hysteresis
from .hysteresis import Queue

class Image():
    """
        A class that holds all data relating to a single image that is loaded
        into the program

        NB: this class acts as a data structure, as well as holding all
        methods that can be applied to the data

        NB: python does not support private, public and protected attributes.
        In the interests of encapsulation, the data should be private, however
        enforcing this without built in support is unnecessarily obfuscated,
        so the data is treated as public and can be accessed from outside the
        object
    """
    def __init__(self, originalImage):
        # Initialised all attributes with empty arrays (or empty Queue)
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
        toCheck = [self.original, self.gblur, self.smagnitude, \
                self.suppressed, self.thresholded, self.final]
        # Strings associated with said attributes (in same order)
        associatedStrs = ['Original', 'Gaussian blur', 'Sobel', \
                'Suppression', 'Thresholding', 'Final']

        # Iterate through toCheck
        for i in range(len(toCheck)):
            if toCheck[i] != nil:
                # If array isn't empty, it has been processed
                finalStr += associatedStrs[i]+': complete\n'
            else:
                # Otherwise it has not yet been started
                finalStr += associatedStrs[i]+': not started\n'

        return finalStr

    def fullCanny(self, stdev, width, autoBool, lowThreshold=None, highThreshold=None):
        newTime = time.time()
        self.gaussian_(stdev, width)
        print('Gaussian blur complete! '+str(time.time()-newTime)+' secs')
        newTime = time.time()
        self.sobel_()
        print('Sobel filter complete! '+str(time.time()-newTime)+' secs')
        newTime = time.time()
        self.nms_()
        print('Non maximum suppression complete! '+str(time.time()-newTime)\
                +' secs')
        newTime = time.time()
        self.threshold_(autoBool, lowThreshold, highThreshold)
        print('Thresholding complete! '+str(time.time()-newTime)+' secs')
        newTime = time.time()
        self.hysteresis_()
        print('Full canny complete! '+str(time.time()-newTime)+' secs')

    def gaussian_(self,stdev,width):
        """
            Gaussian blur takes standard deviation, kernel width and original
            image

            Returns blurred image
        """
        self.gblur = gaussianInterface(stdev,width,self.original)

    def sobel_(self):
        """
            Sobel filter takes the blurred image

            Returns gradient magnitude and direction, as well as horizontal
            and vertical gradient components (all represented as arrays)
        """
        self.smagnitude,self.sdirection,self.shgradient,self.svgradient = \
                sobel(self.gblur)

        ##########IS this needed?
        # Ensure gradient magnitude & direction arrays contain floats
        #self.smagnitude = self.smagnitude.astype('float')
        #self.sdirection = self.sdirection.astype('float')

    def nms_(self):
        """
            NMS algorithm takes all sobel filter result arrays

            Returns array of 0s and gradient magnitudes where not suppressed
        """
        self.suppressed = nonMaximumSuppression(self.smagnitude, \
                self.shgradient, self.svgradient,self.sdirection)

    def threshold_(self, autoBool, lowThresholdRatio=None, \
            highThresholdRatio=None):
        """
            Automatic thresholding takes original image, gradient magnitude,
            and suppressed image

            User defined thresholding takes original image, gradient
            magnitude, suppressed image and low & high threshold ratios

            Returns thresholded image containing 0s (no edge), 128s
            (edge candidate), 255s (strong/definite edges) and queue of
            strong edges
        """
        # Automatic thresholding
        if autoBool:
            self.thresholded, self.strongEdgesQueue = thresholdInterface(\
                    self.original, self.smagnitude, self.suppressed, True)

        # User defined thresholds
        else:
            self.thresholded, self.strongEdgesQueue  = thresholdInterface(\
                    self.original, self.smagnitude,self.suppressed, False, \
                    lowThresholdRatio, highThresholdRatio)

    def hysteresis_(self):
        """
            Hysteresis algorithm takes thresholded image and strong
            edges queue

            Returns final image containing only strong edges
        """
        self.final = hysteresis(self.thresholded, self.strongEdgesQueue)

