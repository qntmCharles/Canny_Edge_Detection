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
    gradient_direction_plot = np.zeros(image.shape)

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            edge_gradient[y][x] = math.sqrt(horizontal_convolution[y][x]**2 + vertical_convolution[y][x]**2)
            if horizontal_convolution[y][x] != 0:
                temp_direction = math.atan(vertical_convolution[y][x]/horizontal_convolution[y][x])
            else:
                temp_direction = 90
            gradient_direction_plot[y][x] = temp_direction
            if temp_direction >= math.atan(3*math.pi/8) or (temp_direction < math.atan(-3*math.pi/8)):
                gradient_direction[y][x] = 90
            if (temp_direction < math.atan(3*math.pi/8)) and (temp_direction >= math.atan(math.pi/8)):
                gradient_direction[y][x] = 45
            if (temp_direction < math.atan(math.pi/8)) and (temp_direction >= math.atan(-math.pi/8)):
                gradient_direction[y][x] = 0
            if (temp_direction < math.atan(-math.pi/8)) and (temp_direction >= math.atan(-3*math.pi/8)):
                    gradient_direction[y][x] = 135


    normalized_edge_gradient = 255.*np.absolute(edge_gradient)/np.max(edge_gradient)

    return normalized_edge_gradient, gradient_direction, gradient_direction_plot

