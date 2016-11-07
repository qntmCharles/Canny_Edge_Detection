"""
Created on Sun Jul 31 12:57:42 2016

@author: qntmCharles
"""
from __future__ import division
from PIL import Image as im
import numpy as np
import math
import matplotlib.pyplot as plt

from gaussian import gaussian
from sobel import sobel
from nms import nonMaximumSuppression
from hysteresis import hysteresis
from threshold import threshold,generateHistogram

class Image():
    def __init__(self,originalImage):
        self.original = originalImage
        self.gblur = np.array([])
        self.smagnitude = np.array([])
        self.sdirection = np.array([])
        self.shgradient = np.array([])
        self.svgradient = np.array([])
        self.suppressed = np.array([])
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

def main():
    I = Image(np.asarray(im.open('test.png').convert('L'),dtype=np.float32))
    print('Performing Gaussian blur...')
    gaussian_result = gaussian(0.5,5,I)
    print('Gaussian blur complete!')
    #Image.fromarray(gaussian_result.astype(np.uint8)).show()
    print('Performing Sobel convolution...')
    sobelGradient,sobelDirection = sobel(gaussian_result)
    sobelDirection = sobelDirection.astype('float')
    sobelGradient = sobelGradient.astype('float')
    print('Sobel convolution complete!')
    print('Performing non maximum suppression...')
    suppressed_image = nonMaximumSuppression(sobelGradient,sobelDirection)
    print('Non maximum suppression complete!')
    h = generateHistogram(suppressed_image)
    plt.bar(h.keys(),h.values(),1)
    plt.show()
    print('Thresholding image...')
    thresholded_image = threshold(I,suppressed_image)
    print('Thresholding complete!')
    #Image.fromarray(thresholded_image).show()
    print('Performing threshold hysteresis...')
    final_image = hysteresis(thresholded_image)
    print('Threshold hysteresis complete!')
    im.fromarray(final_image).show()


if __name__ == '__main__':
    main()


#########
"""sobel (works - just doesn't look as it will at the end)
I = np.asarray(Image.open('test.png').convert('L'),dtype=np.float32)
print(I.shape)
g = np.array(gaussiankernel(3,5))
a = convolution(I,g,'extend')
g = np.array([[1,0,-1],
          [2,0,-2],
          [1,0,-1]])
r = convolution(a,g,'extend')
r = 255.0*np.absolute(r)/np.max(r)
final = Image.fromarray(r.round().astype(np.uint8))
final.show()"""


############
"""gaussian (definitely works)
I = np.asarray(Image.open('pigeon.jpg'),dtype=np.float32)

Image.fromarray(r.round().astype(np.uint8)).show()"""
