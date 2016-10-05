import math
import numpy as np

def non_maximum_suppresion(gradient_magnitude, gradient_direction):
    for y in range(gradient_magnitude.shape[0]):
        for x in range(gradient_magnitude.shape[1]):
            output = np.zeros(gradient_magnitude.shape)
            if gradient_direction[y][x] == 'h':
                if (gradient_magnitude[y][x] > gradient_magnitude[y][x-1]) and (gradient_magnitude[y][x] > gradient_magnitude[y][x+1]):
                    output[y][x] = 1
                else:
                    output[y][x] = 0
            if gradient_direction[y][x] == 'v':
                if (gradient_magnitude[y][x] > gradient_magnitude[y-1][x]) and (gradient_magnitude[y][x] > gradient_magnitude[y+1][x]):
                    output[y][x] = 1
                else:
                    output[y][x] = 0
    #Need some kind of edge handling. What should happen when the
    #check goes over the edge? Simply ignore the other side?
    return output


