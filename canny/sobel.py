import numpy as np
import math
from .convolution import convolution

def sobel(image):
    # Sobel horizontal & vertical kernels
    verticalKernel = np.array([[ 1, 2, 1],
                                [ 0, 0, 0],
                                [-1,-2,-1]])

    horizontalKernel  = np.array([[-1, 0, 1],
                                   [-2, 0, 2],
                                   [-1, 0, 1]])

    # Perform convolution using kernels
    horizontal = convolution(image, horizontalKernel)
    vertical = convolution(image, verticalKernel)

    # Initialise arrays of zeros
    gradient = np.zeros(image.shape)
    direction = np.zeros(image.shape)

    # Iterate over image
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            # Calculate gradient magnitude
            gradient[y][x]=math.sqrt(horizontal[y][x]**2 + vertical[y][x]**2)

            # If horizontal component isn't 0, calculate gradient direction
            if horizontal[y][x] != 0:
                direction[y][x] = math.atan2(vertical[y][x],horizontal[y][x])

            # If horizontal component is 0, then direction is either
            # +pi/2 or -pi/2, dependent on +/-
            else:
                if vertical[y][x] >= 0:
                    direction[y][x] = math.pi/2
                else:
                    direction[y][x] = -math.pi/2

    # Normalise gradient so that the image isn't darkened
    normalisedGradient = 255.0*np.absolute(gradient)/np.max(gradient)

    return normalisedGradient, direction, horizontal, vertical

