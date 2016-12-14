import numpy as np
from .gaussian import gaussian
from .sobel import sobel
from .nms import nonMaximumSuppression
from .threshold import threshold
from .hysteresis import hysteresis
from .hysteresis import Queue

class Image():
    def __init__(self,originalImage):
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
        str=''
        if self.original != np.array([]):
            str += 'Original: assigned\n'
        else:
            str += 'Original: unassigned\n'
        if self.gblur != np.array([]):
            str += 'Gaussian blur: assigned\n'
        else:
            str += 'Gaussian blur: unassigned\n'
        if self.smagnitude != np.array([]):
            str += 'Sobel: assigned\n'
        else:
            str += 'Sobel: unassigned\n'
        if self.suppressed != np.array([]):
            str += 'Suppression: assigned\n'
        else:
            str += 'Suppression: unassigned\n'
        if self.thresholded != np.array([]):
            str += 'Thresholding: assigned\n'
        else:
            str += 'Thresholding: unassigned\n'
        if self.final != np.array([]):
            str += 'Final: assigned'
        else:
            str += 'Final: unassigned'
        return str

    def gaussian_(self,sigma,width):
        self.gblur = gaussian(sigma,width,self.original)

    def sobel_(self):
        self.smagnitude,self.sdirection,self.shgradient,self.svgradient = sobel(self.gblur)
        self.smagnitude = self.smagnitude.astype('float')
        self.sdirection = self.sdirection.astype('float')

    def nms_(self):
        self.suppressed = nonMaximumSuppression(self.smagnitude,self.shgradient,self.svgradient,self.sdirection)
        #self.suppressed = nonMaximumSuppression(self.smagnitude, self.sdirection)

    def threshold_(self, lowThreshold, highThreshold):
        self.thresholded, self.strongEdgesQueue  = threshold(self.original,self.smagnitude,self.suppressed, lowThreshold, highThreshold)

    def hysteresis_(self):
        self.final = hysteresis(self.thresholded, self.strongEdgesQueue)

