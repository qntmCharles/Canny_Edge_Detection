"""
Created on Sun Jul 31 12:57:42 2016

@author: qntmCharles
"""
from __future__ import division
from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt

from convolution import convolution
from gaussian import G,gaussiankernel
from sobel import sobel
from nms import non_maximum_suppression
from hysteresis import hysteresis
from threshold import calculateThresholds, threshold_image

def main():
    I = np.asarray(Image.open('sample.png').convert('L'),dtype=np.float32)
    #np.savetxt('image.txt',np.around(I,3),fmt='%.2f',delimiter='|')
    g = gaussiankernel(0.5,5)
    print('Performing Gaussian blur...')
    gaussian_result = convolution(I,g,'extend')
    print('Gaussian blur complete!')
    #Image.fromarray(gaussian_result.astype(np.uint8)).show()
    print('Performing Sobel convolution...')
    sobel_result_gradient,sobel_result_direction = sobel(gaussian_result)
    sobel_result_direction = sobel_result_direction.astype('float')
    sobel_result_gradient = sobel_result_gradient.astype('float')
    print('Sobel convolution complete!')
    print('Performing non maximum suppression...')
    suppressed_image = non_maximum_suppression(sobel_result_gradient,sobel_result_direction)
    print('Non maximum suppression complete!')
    print('Thresholding image...')
    threshold = calculateThresholds(I)
    thresholded_image = threshold_image(suppressed_image,0.05*threshold,0.3*threshold)
    print('Thresholding complete!')
    #Image.fromarray(thresholded_image).show()
    print('Performing threshold hysteresis...')
    final_image = hysteresis(thresholded_image)
    print('Threshold hysteresis complete!')
    Image.fromarray(final_image).show()


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
