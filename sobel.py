from __future__ import division
import numpy as np
import math
from matplotlib import pyplot as plt

from convolution import convolution

def sobel(image):
    #Sobel horiz/vert kernels
    horizontal_kernel = np.array([[ 1, 2, 1],
                                  [ 0, 0, 0],
                                  [-1,-2,-1]])

    vertical_kernel  = np.array([[ 1, 0,-1],
                                 [ 2, 0,-2],
                                 [ 1, 0,-1]])
    #Perform convolution using kernels
    horizontal = convolution(image, vertical_kernel)
    vertical = convolution(image, horizontal_kernel)

    #Create arrays of zeros
    gradient = np.zeros(image.shape)
    direction = np.zeros(image.shape).astype(np.str)

    #Iterate over image
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            #Calculate gradient magnitude
            gradient[y][x] =math.sqrt(horizontal[y][x]**2 + vertical[y][x]**2)

            #If horizontal component isn't 0, calculate gradient direction
            if horizontal[y][x] != 0:
                direction[y][x] = math.atan2(vertical[y][x],horizontal[y][x])
            #If horizontal component is 0, then direction is either +pi or -pi
            else:
                if vertical[y][x] >= 0:
                    direction[y][x] = math.pi/2
                else:
                    direction[y][x] = -math.pi/2

    #normalise gradient so that the image isn't darkened
    normalised_gradient = 255.*np.absolute(gradient)/np.max(gradient)

    return normalised_gradient, direction, horizontal, vertical

