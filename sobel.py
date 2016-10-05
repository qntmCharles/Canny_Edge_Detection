from __future__ import division
import numpy as np
import math

from convolution import convolution

def sobel(image):

    horizontal_kernel = np.array([[ 1, 2, 1],
                                  [ 0, 0, 0],
                                  [-1,-2,-1]])

    vertical_kernel  = np.array([[ 1, 0,-1],
                                 [ 2, 0,-2],
                                 [ 1, 0,-1]])

    horizontal_convolution = convolution(image, vertical_kernel, 'extend')
    vertical_convolution = convolution(image, horizontal_kernel, 'extend')

    edge_gradient = np.zeros(image.shape)
    gradient_direction = np.zeros(image.shape).astype(np.str)

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            edge_gradient[y][x] = math.sqrt(horizontal_convolution[y][x]**2 + vertical_convolution[y][x]**2)
            temp_direction = math.atan2(vertical_convolution[y][x], horizontal_convolution[y][x])
            if (temp_direction>=-(math.pi/4)) and (temp_direction<(math.pi/4)):
                gradient_direction[y][x] = 'h'
            if (temp_direction>=(math.pi/4)) and (temp_direction<(3*math.pi/4)):
                gradient_direction[y][x] = 'v'
            if (temp_direction>=(3*math.pi/4)) or (temp_direction<-(3*math.pi/4)):
                gradient_direction[y][x] = 'h'
                if (temp_direction>=-(3*math.pi/4)) and (temp_direction<-(math.pi/4)):
                    gradient_direction[y][x] = 'v'

    normalized_edge_gradient = 255.*np.absolute(edge_gradient)/np.max(edge_gradient)

    return normalized_edge_gradient, gradient_direction
